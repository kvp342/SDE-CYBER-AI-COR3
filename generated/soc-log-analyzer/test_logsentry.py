"""Tests for logsentry. Run from this folder: python3 -m unittest -v test_logsentry"""
import json, os, subprocess, sys, tempfile, unittest
from datetime import datetime, timedelta
from logsentry.parse import parse_auth, parse_web
from logsentry.detect import run_all, ssh_bruteforce, login_after_failures, web_attacks, web_scanning
HERE = os.path.dirname(os.path.abspath(__file__))
def auth_line(t, ok, user, ip): return f"{t.strftime('%b %d %H:%M:%S')} h sshd[1]: {'Accepted' if ok else 'Failed'} password for {user} from {ip} port 1 ssh2"
def web_line(ip, path, status=200, ua="Mozilla/5.0", t=datetime(2026, 11, 17, 9, 0, 0)): return f'{ip} - - [{t.strftime("%d/%b/%Y:%H:%M:%S")} +0000] "GET {path} HTTP/1.1" {status} 1 "-" "{ua}"'
T0 = datetime(2026, 11, 17, 9, 0, 0)
class Samples(unittest.TestCase):
    def setUp(self):
        self.auth = list(parse_auth(open(f"{HERE}/samples/auth.log"), 2026)); self.web = list(parse_web(open(f"{HERE}/samples/access.log")))
    def test_parses_every_relevant_line(self):
        self.assertEqual((len(self.auth), len(self.web)), (23, 45))        # the CRON line is ignored
    def test_exact_alerts_on_samples(self):
        got = sorted((a["rule"], a["ip"]) for a in run_all(self.auth, self.web))
        self.assertEqual(got, sorted([("ssh-bruteforce", "203.0.113.50"), ("ssh-success-after-failures", "192.0.2.99"), ("web-scanning", "203.0.113.77"),
            ("scanner-user-agent", "203.0.113.77"), ("scanner-user-agent", "192.0.2.150"), ("sql-injection", "192.0.2.150"), ("xss", "198.51.100.33"), ("path-traversal", "198.51.100.34")]))
    def test_no_alerts_for_normal_activity(self):
        ips = {a["ip"] for a in run_all(self.auth, self.web)}
        self.assertTrue({"198.51.100.7", "198.51.100.8", "198.51.100.20"}.isdisjoint(ips))
    def test_alerts_carry_attack_ids_and_evidence(self):
        for a in run_all(self.auth, self.web):
            self.assertRegex(a["technique"], r"^T\d{4}"); self.assertTrue(a["evidence"])
class Rules(unittest.TestCase):
    def test_bruteforce_threshold_edge(self):
        four = list(parse_auth([auth_line(T0 + timedelta(seconds=i), False, "root", "192.0.2.1") for i in range(4)], 2026))
        five = list(parse_auth([auth_line(T0 + timedelta(seconds=i), False, "root", "192.0.2.1") for i in range(5)], 2026))
        self.assertEqual(ssh_bruteforce(four), []); self.assertEqual(len(ssh_bruteforce(five)), 1)
    def test_slow_failures_are_not_a_burst(self):
        slow = list(parse_auth([auth_line(T0 + timedelta(minutes=i), False, "root", "192.0.2.1") for i in range(10)], 2026))
        self.assertEqual(ssh_bruteforce(slow), [])
    def test_success_after_failures_resets(self):
        ev = [auth_line(T0 + timedelta(seconds=i), False, "a", "192.0.2.2") for i in range(5)] + [auth_line(T0 + timedelta(seconds=9), True, "a", "192.0.2.2"), auth_line(T0 + timedelta(seconds=20), True, "a", "192.0.2.2")]
        self.assertEqual(len(login_after_failures(list(parse_auth(ev, 2026)))), 1)
    def test_double_encoded_attack_is_caught(self):
        w = list(parse_web([web_line("192.0.2.3", "/f?file=%252e%252e%252fetc%252fpasswd")]))
        self.assertEqual([a["rule"] for a in web_attacks(w)], ["path-traversal"])
    def test_harmless_queries_pass(self):
        w = list(parse_web([web_line("192.0.2.4", p) for p in ("/search?q=union+station", "/search?q=O%27Brien", "/blog/selected-works", "/a?x=1&y=2")]))
        self.assertEqual(web_attacks(w), [])
    def test_scanning_needs_errors(self):
        ok = list(parse_web([web_line("192.0.2.5", f"/p{i}", 200, t=T0 + timedelta(seconds=i)) for i in range(30)]))
        self.assertEqual(web_scanning(ok), [])
class Cli(unittest.TestCase):
    def test_json_output_and_exit_code(self):
        out = os.path.join(tempfile.mkdtemp(), "alerts.json")
        r = subprocess.run([sys.executable, "-m", "logsentry", "--auth", "samples/auth.log", "--web", "samples/access.log", "--out", out], cwd=HERE, capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)                                  # 2 = a critical alert was raised
        self.assertEqual(len(json.load(open(out))), 8)
if __name__ == "__main__":
    unittest.main()
