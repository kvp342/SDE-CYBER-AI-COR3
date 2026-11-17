"""Lab 6: read auth.log and flag any IP with 5 or more failed logins inside 60 seconds (a simple SOC detection rule)."""
import re, sys
from collections import defaultdict, deque
from datetime import datetime
LINE = re.compile(r"^(\S+ \S+),\d+ login (ok|fail) user=(\S*) ip=(\S+)")
def detect(lines, threshold=5, window=60):
    recent, alerts = defaultdict(deque), []
    for line in lines:
        m = LINE.match(line)
        if not m or m.group(2) != "fail": continue
        t = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S"); ip = m.group(4); q = recent[ip]
        q.append(t)
        while (t - q[0]).total_seconds() > window: q.popleft()
        if len(q) == threshold: alerts.append((ip, m.group(1), m.group(3)))
    return alerts
if __name__ == "__main__":
    for ip, when, user in detect(open(sys.argv[1] if len(sys.argv) > 1 else "auth.log")):
        print(f"ALERT brute force from {ip} at {when} (last user tried: {user})")
