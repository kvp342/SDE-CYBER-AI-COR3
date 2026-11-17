# logsentry: detect attacks in SSH and web logs

A small detection tool written like a SOC analyst's first project. It reads OpenSSH lines from a syslog auth log and Apache/Nginx "combined" access logs, applies six detection rules, and writes alerts as JSON, each tagged with a MITRE ATT&CK technique and the log lines that triggered it. Python standard library only.

| Rule | Fires when | Severity | ATT&CK |
|---|---|---|---|
| ssh-bruteforce | 5+ failed SSH logins from one IP within 60 s | high | T1110.001 Password Guessing |
| ssh-success-after-failures | a successful login from an IP with 5+ failures in the previous 10 min | critical | T1078 Valid Accounts |
| web-scanning | 20+ 403/404 responses to one IP within 60 s | medium | T1595 Active Scanning |
| scanner-user-agent | user agent names a tool (sqlmap, nikto, nmap, gobuster, …) | medium | T1595 Active Scanning |
| sql-injection / xss / path-traversal | URL (decoded twice) matches attack patterns | high / medium / high | T1190 Exploit Public-Facing Application |

## Run

```bash
python3 make_samples.py                     # regenerate samples/ (fictional IPs from documentation ranges)
python3 -m logsentry --auth samples/auth.log --web samples/access.log --out alerts.json
python3 -m unittest -v test_logsentry       # 11 tests
```

Exit code 2 means a critical alert was raised, so it can fail a scheduled job or CI step.

## Results on the samples

8 alerts, and none for the planted normal activity (a normal login, a user mistyping a password 3 times, ordinary browsing and a harmless query string). The tests also check threshold edges (4 failures: no alert; 5: alert), slow guessing that is not a burst, double-encoded traversal, and harmless queries such as `O'Brien` and `union station`.

## Limits (say these in an interview)

- Per-IP thresholds miss password spraying from many IPs and flag shared NAT addresses; a per-account rule helps.
- Regex payload matching has false positives and is easy to evade; a WAF or the app's own logging of rejected input is better evidence.
- Syslog lines have no year; pass `--year`. Real deployments ship logs to a SIEM (for example Elastic or Splunk) and run rules there.
