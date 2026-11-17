"""Generate the sample logs (fictional IPs from documentation ranges 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24)."""
import pathlib
from datetime import datetime, timedelta
D = pathlib.Path(__file__).parent / "samples"; D.mkdir(exist_ok=True)
t0 = datetime(2026, 11, 17, 9, 0, 0); auth = []
def ssh(t, ok, user, ip, invalid=False):
    return f"{t.strftime('%b %d %H:%M:%S').replace(' 0', '  ', 1) if t.day < 10 else t.strftime('%b %d %H:%M:%S')} web01 sshd[{1000 + len(auth)}]: {'Accepted' if ok else 'Failed'} password for {'invalid user ' if invalid else ''}{user} from {ip} port {40000 + len(auth)} ssh2"
auth.append(ssh(t0, True, "deploy", "198.51.100.7"))                                   # normal login
for i in range(12): auth.append(ssh(t0 + timedelta(seconds=5 + 3 * i), False, ["root", "admin", "test", "oracle"][i % 4], "203.0.113.50", invalid=i % 4 != 0))   # brute force
for i in range(6): auth.append(ssh(t0 + timedelta(minutes=10, seconds=20 * i), False, "alice", "192.0.2.99"))   # slow guessing...
auth.append(ssh(t0 + timedelta(minutes=12, seconds=30), True, "alice", "192.0.2.99"))   # ...then success
for i in range(3): auth.append(ssh(t0 + timedelta(minutes=20 + 5 * i), False, "bob", "198.51.100.8"))   # a user mistyping, no alert
(D / "auth.log").write_text("\n".join(auth) + "\nNov 17 09:30:00 web01 CRON[2001]: pam_unix(cron:session): session opened for user root\n")
web = []
def req(t, ip, path, status, ua="Mozilla/5.0"):
    web.append(f'{ip} - - [{t.strftime("%d/%b/%Y:%H:%M:%S")} +0530] "GET {path} HTTP/1.1" {status} 512 "-" "{ua}"')
for i in range(10): req(t0 + timedelta(seconds=30 * i), "198.51.100.20", ["/", "/products", "/cart"][i % 3], 200)            # normal browsing
for i in range(30): req(t0 + timedelta(minutes=5, seconds=i), "203.0.113.77", f"/{['admin', 'wp-login.php', '.env', 'backup.zip', 'phpmyadmin', '.git/config'][i % 6]}{i}", 404, "gobuster/3.6")
req(t0 + timedelta(minutes=8), "192.0.2.150", "/search?q=x%27%20UNION%20SELECT%20name,password%20FROM%20users--", 200, "sqlmap/1.8")
req(t0 + timedelta(minutes=8, seconds=2), "192.0.2.150", "/search?q=1%27%20AND%20SLEEP(5)--", 200, "sqlmap/1.8")
req(t0 + timedelta(minutes=9), "198.51.100.33", "/greet?name=%3Cscript%3Ealert(1)%3C%2Fscript%3E", 200)
req(t0 + timedelta(minutes=9, seconds=30), "198.51.100.34", "/download?file=..%2F..%2F..%2Fetc%2Fpasswd", 400)
req(t0 + timedelta(minutes=10), "198.51.100.20", "/products?sort=price&order=asc", 200)                                     # harmless query
(D / "access.log").write_text("\n".join(web) + "\n")
print(len(auth), "auth lines,", len(web), "web lines")
