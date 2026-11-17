"""Parsers for OpenSSH lines in syslog-style auth logs and for Apache/Nginx 'combined' access logs."""
import re
from datetime import datetime
SSH = re.compile(r"^(?P<ts>\w{3}\s+\d{1,2} \d{2}:\d{2}:\d{2}) (?P<host>\S+) sshd\[\d+\]: "
                 r"(?P<result>Failed|Accepted) (?P<method>password|publickey) for (?:invalid user )?(?P<user>\S+) from (?P<ip>[\d.:a-fA-F]+) port \d+")
WEB = re.compile(r'^(?P<ip>\S+) \S+ \S+ \[(?P<ts>[^\]]+)\] "(?P<method>[A-Z]+) (?P<path>\S+) [^"]*" (?P<status>\d{3}) (?P<size>\S+) "[^"]*" "(?P<ua>[^"]*)"')
def parse_auth(lines, year):
    for line in lines:
        m = SSH.match(line)
        if m:
            yield dict(ts=datetime.strptime(f"{year} {m['ts']}", "%Y %b %d %H:%M:%S"), ip=m["ip"], user=m["user"], ok=m["result"] == "Accepted", raw=line.rstrip("\n"))
def parse_web(lines):
    for line in lines:
        m = WEB.match(line)
        if m:
            yield dict(ts=datetime.strptime(m["ts"], "%d/%b/%Y:%H:%M:%S %z").replace(tzinfo=None), ip=m["ip"], method=m["method"], path=m["path"],
                       status=int(m["status"]), ua=m["ua"], raw=line.rstrip("\n"))
