PROJECT · SECURITY OPERATIONS

# logsentry detect attacks in logs

A portfolio project for SOC and security-engineering roles: a Python tool that finds SSH brute force, a likely compromised account, web scanning and injection attempts in real log formats, maps each alert to MITRE ATT&CK, and is tested against both attacks and normal activity.

| Section                                          |
|--------------------------------------------------|
| [1. What it is and why it helps](#01-what-it-is-and-why-it-helps)        |
| [2. The six rules](#02-the-six-rules)                      |
| [3. How it is tested](#03-how-it-is-tested)                   |
| [4. Limits, and how to talk about them](#04-limits-and-how-to-talk-about-them) |
| [5. On your resume and GitHub](#05-on-your-resume-and-github)          |
| [Sources (4)](#-sources)                           |

Code: `generated/soc-log-analyzer/`. 11 tests pass; on the sample logs the tool raises exactly the 8 expected alerts and none for normal activity.

## 01. What it is and why it helps

- **logsentry** reads SSH auth logs and web access logs, applies six detection rules and writes JSON alerts, each with a severity, an ATT&CK technique and the evidence lines. About 120 lines of standard-library Python in [generated/soc-log-analyzer/](https://github.com/kvp342/intrusion-detection-and-prevention/tree/ccr-ca7232a7-t7lq94/generated/soc-log-analyzer).
- **Why:** SOC and security-engineering interviews ask how you would detect brute force, scanning or injection attempts. This project lets you answer with a rule you wrote, tested and can explain, including its limits.
- **Pairs with:** the security labs workbook (Lab 6 is a simpler version of the first rule) and the TenantWall alerting work on AWS.

### Run

``` bash
cd generated/soc-log-analyzer
python3 -m logsentry --auth samples/auth.log --web samples/access.log --out alerts.json
python3 -m unittest -v test_logsentry      # 11 tests
```

### Output on the sample logs

``` text
parsed 23 auth events and 45 web requests; 8 alerts
[CRITICAL] ssh-success-after-failures from 192.0.2.99 (T1078 Valid Accounts)
[HIGH] ssh-bruteforce from 203.0.113.50 (T1110.001 Password Guessing)
[HIGH] sql-injection from 192.0.2.150 (T1190 Exploit Public-Facing Application)
[HIGH] path-traversal from 198.51.100.34 (T1190)
[MEDIUM] scanner-user-agent from 203.0.113.77 (gobuster) and 192.0.2.150 (sqlmap)
[MEDIUM] web-scanning from 203.0.113.77 (T1595 Active Scanning)
[MEDIUM] xss from 198.51.100.33 (T1190)
```

## 02. The six rules

| Rule                               | Logic                                                                                                      | ATT&CK                                                     |
|------------------------------------|------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| ssh-bruteforce                     | Sliding 60 s window per IP over failed logins; fire once at 5                                              | T1110.001 Password Guessing^([\[1\]](#-sources))             |
| ssh-success-after-failures         | A success from an IP that had 5+ failures in the previous 10 minutes (critical: the guess may have worked) | T1078 Valid Accounts^([\[2\]](#-sources))                    |
| web-scanning                       | Sliding 60 s window per IP over 403/404 responses; fire at 20                                              | T1595 Active Scanning^([\[3\]](#-sources))                   |
| scanner-user-agent                 | User agent contains a known tool name                                                                      | T1595                                                      |
| sql-injection, xss, path-traversal | Decode the URL twice (attackers double-encode), then match patterns                                        | T1190 Exploit Public-Facing Application^([\[4\]](#-sources)) |

### The sliding-window core

``` python
def burst(events, key, threshold, window):
    q, fired = defaultdict(deque), set()
    for e in sorted(events, key=lambda e: e["ts"]):
        k = key(e); d = q[k]; d.append(e)
        while (e["ts"] - d[0]["ts"]).total_seconds() > window: d.popleft()
        if len(d) >= threshold and k not in fired: fired.add(k); yield k, list(d)
```

## 03. How it is tested

- The sample logs mix attacks with normal activity on purpose: a normal login, a user mistyping a password 3 times, ordinary browsing, a harmless query string. The test asserts exactly the 8 expected alerts and none for the normal IPs.
- Edges: 4 failures do not alert and 5 do; 10 failures spread over 10 minutes are not a burst; a second success after the alert does not alert again.
- Evasion and false positives: a double-encoded `%252e%252e%252f` traversal is caught; `O'Brien`, `union station` and normal query strings are not.
- The command line writes valid JSON and exits with 2 when a critical alert is raised, so it can fail a cron job or CI step.
- IPs come from the documentation ranges (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24), so the samples never point at real hosts.

## 04. Limits, and how to talk about them

| Limit                                                  | Better approach                                                                        |
|--------------------------------------------------------|----------------------------------------------------------------------------------------|
| Per-IP thresholds miss password spraying from many IPs | Add a per-account rule; combine with MFA                                               |
| Shared NAT or office IPs cause false positives         | Allow-lists, and alerting on success-after-failure rather than failures alone          |
| Regex payload matching is easy to evade and noisy      | Log rejected input in the app; use a WAF; treat these alerts as low-confidence signals |
| No state between runs; files only                      | Ship logs to a SIEM and run the rules continuously                                     |
| Syslog has no year or time zone                        | Use structured JSON logs with ISO timestamps                                           |

Interviewers value honest limits more than big claims. "It catches a burst from one IP; spraying across IPs needs a per-account rule" is a strong answer.

## 05. On your resume and GitHub

- Resume line: "Built logsentry, a Python log-analysis tool that detects SSH brute force, account compromise, web scanning and injection attempts, mapped to MITRE ATT&CK, with 11 tests including false-positive cases."
- Push it as its own repository with the README, the samples and a screenshot of the output. Add a GitHub Actions workflow that runs the tests (see [the Docker and CI guide](docker-ci-guide.md)).
- Next steps: per-account and impossible-travel rules, a Sigma rule export, and an Elastic or Splunk import of the JSON alerts.
- Related: [security labs workbook](security-labs-workbook.md), [cyber-security interview bank](cyber-security-interview-bank.md).

## ··. Sources

Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.

1.  [MITRE ATT&CK T1110.001 Password Guessing](https://attack.mitre.org/techniques/T1110/001/)  
    https://attack.mitre.org/techniques/T1110/001/
2.  [MITRE ATT&CK T1078 Valid Accounts](https://attack.mitre.org/techniques/T1078/)  
    https://attack.mitre.org/techniques/T1078/
3.  [MITRE ATT&CK T1595 Active Scanning](https://attack.mitre.org/techniques/T1595/)  
    https://attack.mitre.org/techniques/T1595/
4.  [MITRE ATT&CK T1190 Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/)  
    https://attack.mitre.org/techniques/T1190/
