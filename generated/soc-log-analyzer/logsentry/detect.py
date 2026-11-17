"""Detection rules. Each alert: rule, severity, ip, first and last time, count, MITRE ATT&CK technique, evidence lines."""
import re
from collections import defaultdict, deque
from urllib.parse import unquote_plus
def _alert(rule, sev, ip, events, technique, why):
    return dict(rule=rule, severity=sev, ip=ip, first=events[0]["ts"].isoformat(), last=events[-1]["ts"].isoformat(), count=len(events),
                technique=technique, why=why, evidence=[e["raw"] for e in events[:3]])
def burst(events, key, threshold, window):
    """Yield (key, events-in-window) the first time `threshold` events with the same key fall inside `window` seconds."""
    q, fired = defaultdict(deque), set()
    for e in sorted(events, key=lambda e: e["ts"]):
        k = key(e); d = q[k]; d.append(e)
        while (e["ts"] - d[0]["ts"]).total_seconds() > window: d.popleft()
        if len(d) >= threshold and k not in fired: fired.add(k); yield k, list(d)
def ssh_bruteforce(auth, threshold=5, window=60):
    fails = [e for e in auth if not e["ok"]]
    return [_alert("ssh-bruteforce", "high", ip, ev, "T1110.001 Password Guessing", f"{len(ev)} failed SSH logins within {window}s")
            for ip, ev in burst(fails, lambda e: e["ip"], threshold, window)]
def login_after_failures(auth, threshold=5, window=600):
    out, recent = [], defaultdict(list)
    for e in sorted(auth, key=lambda e: e["ts"]):
        r = [x for x in recent[e["ip"]] if (e["ts"] - x["ts"]).total_seconds() <= window]
        if e["ok"] and len(r) >= threshold:
            out.append(_alert("ssh-success-after-failures", "critical", e["ip"], r + [e], "T1078 Valid Accounts", f"login as {e['user']} after {len(r)} failures in {window}s: possible compromised account"))
            r = []
        recent[e["ip"]] = r if e["ok"] else r + [e]
    return out
def web_scanning(web, threshold=20, window=60):
    errs = [e for e in web if e["status"] in (403, 404)]
    return [_alert("web-scanning", "medium", ip, ev, "T1595 Active Scanning", f"{len(ev)} 403/404 responses within {window}s")
            for ip, ev in burst(errs, lambda e: e["ip"], threshold, window)]
TOOLS = re.compile(r"sqlmap|nikto|nmap|masscan|zgrab|gobuster|dirbuster|wpscan|nuclei", re.I)
def scanner_user_agents(web):
    by = defaultdict(list)
    for e in web:
        m = TOOLS.search(e["ua"])
        if m: by[(e["ip"], m.group(0).lower())].append(e)
    return [_alert("scanner-user-agent", "medium", ip, ev, "T1595 Active Scanning", f"user agent names a scanning tool: {tool}") for (ip, tool), ev in by.items()]
ATTACKS = [("sql-injection", re.compile(r"('|%27)\s*(or|and|union)\b|union\s+select|sleep\(\d|--\s*$", re.I)),
           ("xss", re.compile(r"<script|javascript:|onerror\s*=|onload\s*=", re.I)),
           ("path-traversal", re.compile(r"\.\./|\.\.\\|/etc/passwd|win\.ini", re.I))]
def web_attacks(web):
    by = defaultdict(list)
    for e in web:
        path = unquote_plus(unquote_plus(e["path"]))           # attackers often double-encode
        for name, rx in ATTACKS:
            if rx.search(path): by[(e["ip"], name)].append(e)
    sev = {"sql-injection": "high", "xss": "medium", "path-traversal": "high"}
    return [_alert(name, sev[name], ip, ev, "T1190 Exploit Public-Facing Application", f"{len(ev)} request(s) matching {name} patterns")
            for (ip, name), ev in by.items()]
def run_all(auth, web):
    alerts = ssh_bruteforce(auth) + login_after_failures(auth) + web_scanning(web) + scanner_user_agents(web) + web_attacks(web)
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(alerts, key=lambda a: (order[a["severity"]], a["first"], a["rule"]))
