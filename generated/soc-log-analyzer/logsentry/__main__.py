"""Command line: python -m logsentry --auth auth.log --web access.log [--year 2026] [--out alerts.json]"""
import argparse, json, sys
from collections import Counter
from .parse import parse_auth, parse_web
from .detect import run_all
def main(argv=None):
    ap = argparse.ArgumentParser(prog="logsentry", description="Detect brute force, scanning and web attacks in auth and access logs.")
    ap.add_argument("--auth"); ap.add_argument("--web"); ap.add_argument("--year", type=int, default=2026, help="syslog lines have no year")
    ap.add_argument("--out", help="write alerts as JSON here (default: print a summary only)")
    a = ap.parse_args(argv)
    auth = list(parse_auth(open(a.auth), a.year)) if a.auth else []
    web = list(parse_web(open(a.web))) if a.web else []
    alerts = run_all(auth, web)
    if a.out:
        with open(a.out, "w") as f: json.dump(alerts, f, indent=2)
    print(f"parsed {len(auth)} auth events and {len(web)} web requests; {len(alerts)} alerts")
    for (sev, rule), n in sorted(Counter((x["severity"], x["rule"]) for x in alerts).items()): print(f"  {sev:8} {rule:28} {n}")
    for x in alerts: print(f"[{x['severity'].upper()}] {x['rule']} from {x['ip']} ({x['technique']}): {x['why']}")
    return 0 if not any(x["severity"] == "critical" for x in alerts) else 2
if __name__ == "__main__":
    sys.exit(main())
