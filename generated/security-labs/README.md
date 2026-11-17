# Security labs (code for the security labs workbook)

Run these **only on your own machine** (everything listens on 127.0.0.1). The workbook is `generated/security-labs-workbook.pdf` (readable copy: `generated/read/security-labs-workbook.md`).

| File | Lab | What it is |
|---|---|---|
| `cli_labs.sh` | 1–3 | Permissions and SUID, port scanning localhost with nmap, capturing HTTP vs HTTPS with tcpdump and tshark. `./cli_labs.sh lab1` (or lab2, lab3) |
| `crack_lab.py` | 4 | Makes hashes of three **test** passwords (MD5, salted SHA-256, salted scrypt) and runs a 20-word dictionary attack on them |
| `app_vulnerable.py` | 5–6 | A deliberately vulnerable Flask app: SQL injection in `/search` and `/login`, reflected XSS in `/greet`, no rate limit. Port 5000 |
| `app_fixed.py` | 5–6 | The same app fixed: parameterised SQL, escaped output, a Content-Security-Policy, lockout after 5 failures a minute. Port 5001 |
| `detect_bruteforce.py` | 6 | Reads `auth.log` and alerts on 5 or more failed logins from one IP within 60 seconds |
| `test_labs.py` | all | `pip install flask pytest && python -m pytest -q test_labs.py` (7 tests): every exploit works on the vulnerable app and fails on the fixed one, the lockout and detector work, and the cracking lab behaves as described |

Tested on 17 Nov 2026 on Linux: all 7 tests pass, and every command in the workbook was run as printed (nmap 7.x, tcpdump, tshark, OpenSSL, Flask, Python 3.13).
