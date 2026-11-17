"""Tests for the security labs: every exploit works on the vulnerable app and fails on the fixed one; the lockout and the
detector catch a brute force; the cracking lab cracks weak test passwords and misses the strong one.
Run from this folder: python -m pytest -q test_labs.py"""
import os, sys, importlib, pathlib, tempfile
HERE = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
os.chdir(tempfile.mkdtemp())                                   # auth.log goes to a throw-away folder
vuln = importlib.import_module("app_vulnerable").app.test_client()
fixed = importlib.import_module("app_fixed").app.test_client()
import detect_bruteforce, crack_lab
SQLI = "x' UNION SELECT name, password FROM users --"

def test_search_normal_works_on_both():
    for c in (vuln, fixed): assert c.get("/search", query_string={"q": "lap"}).get_json() == {"results": [["laptop", 60000]]}

def test_sql_injection_leaks_passwords_only_on_vulnerable():
    leaked = vuln.get("/search", query_string={"q": SQLI}).get_json()["results"]
    assert ["alice", "wonderland"] in leaked and ["bob", "builder"] in leaked
    assert fixed.get("/search", query_string={"q": SQLI}).get_json() == {"results": []}

def test_login_bypass_only_on_vulnerable():
    assert vuln.post("/login", data={"user": "alice' --", "password": "anything"}).status_code == 200
    assert fixed.post("/login", data={"user": "alice' --", "password": "anything"}).status_code == 401
    assert fixed.post("/login", data={"user": "alice", "password": "wonderland"}).status_code == 200

def test_reflected_xss_only_on_vulnerable():
    payload = "<script>alert(1)</script>"
    assert payload in vuln.get("/greet", query_string={"name": payload}).get_data(as_text=True)
    r = fixed.get("/greet", query_string={"name": payload}); body = r.get_data(as_text=True)
    assert payload not in body and "&lt;script&gt;" in body and r.headers["Content-Security-Policy"] == "default-src 'self'"

def test_lockout_and_detection():
    codes = [vuln.post("/login", data={"user": "bob", "password": w}).status_code for w in crack_lab.WORDLIST[:8]]
    assert codes == [401] * 8                                   # vulnerable app never slows the attacker down
    import app_fixed; app_fixed.FAILS.clear()
    codes = [fixed.post("/login", data={"user": "bob", "password": w}).status_code for w in crack_lab.WORDLIST[:8]]
    assert codes == [401] * 5 + [429] * 3                       # fixed app locks the IP after 5 failures
    alerts = detect_bruteforce.detect(open("auth.log"))
    assert alerts and alerts[0][0] == "127.0.0.1"

def test_detector_ignores_slow_failures():
    lines = [f"2026-11-17 10:{m:02d}:00,000 login fail user=bob ip=10.0.0.9" for m in range(0, 10, 2)]   # 5 failures over 8 minutes
    assert detect_bruteforce.detect(lines) == []
    fast = [f"2026-11-17 10:00:{s:02d},000 login fail user=bob ip=10.0.0.9" for s in range(0, 50, 10)]  # 5 in 40 seconds
    assert detect_bruteforce.detect(fast) == [("10.0.0.9", "2026-11-17 10:00:40", "bob")]

def test_cracking_lab():
    rows = crack_lab.main()
    found = {(pw, kind): f for pw, kind, f, _, _ in rows}
    assert found[("sunshine", "MD5, no salt")] == "sunshine" and found[("india123", "scrypt + salt")] == "india123"
    assert all(found[("correct-horse-battery-staple", k)] is None for k in ("MD5, no salt", "SHA-256 + salt", "scrypt + salt"))
    t = {(pw, kind): s for pw, kind, _, _, s in rows}
    assert t[("correct-horse-battery-staple", "scrypt + salt")] > 20 * t[("correct-horse-battery-staple", "MD5, no salt")]
