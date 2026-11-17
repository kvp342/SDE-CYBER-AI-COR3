"""Check the computable facts in the cyber-security interview bank. Usage: python3 generated/src/test_secbank.py"""
import hashlib, ipaddress, os, socket, stat, sys
sys.path.insert(0, os.path.dirname(__file__)); from secbank_data import SECTIONS
A = {q: a for s in SECTIONS for q, a in s["qs"]}
qs = [q for s in SECTIONS for q, a in s["qs"]]; assert len(qs) == len(set(qs)), "duplicate question"
assert 90 <= len(qs) <= 110, len(qs)
# ports: compare with the system services database where it has the entry
ports = {"ssh": 22, "domain": 53, "http": 80, "https": 443, "microsoft-ds": 445, "mysql": 3306, "ms-wbt-server": 3389}
for name, p in ports.items():
    try: assert socket.getservbyname(name, "tcp") == p, name
    except OSError: pass                                   # not in this machine's /etc/services; checked against IANA by hand
ans = A["Default ports: SSH, DNS, HTTP, HTTPS, RDP, SMB, MySQL?"]
for frag in ["SSH 22", "DNS 53", "HTTP 80", "HTTPS 443", "RDP 3389", "SMB 445", "MySQL 3306"]: assert frag in ans, frag
# hash sizes
bits = {n: hashlib.new(n).digest_size * 8 for n in ("md5", "sha1", "sha256")}; assert bits == {"md5": 128, "sha1": 160, "sha256": 256}
assert "128, 160 and 256 bits (32, 40 and 64 hex" in A["Output sizes of MD5, SHA-1 and SHA-256?"]
# subnet sizes
n = ipaddress.ip_network("10.0.0.0/26"); assert n.num_addresses == 64 and len(list(n.hosts())) == 62 and 64 - 5 == 59
assert "64 addresses" in A["What does a /26 give you?"] and "62 are usable" in A["What does a /26 give you?"] and "leaving 59" in A["What does a /26 give you?"]
# permission bits
assert stat.filemode(0o100750) == "-rwxr-x---"; assert "Owner rwx (7), group r-x (5), others nothing (0)" in A["What does chmod 750 mean?"]
assert stat.S_ISUID == 0o4000 and "-perm -4000" in A["What is the SUID bit and why is it risky?"]
print(f"{len(qs)} questions in {len(SECTIONS)} sections; ports, hash sizes, subnet maths and permission bits checked")
