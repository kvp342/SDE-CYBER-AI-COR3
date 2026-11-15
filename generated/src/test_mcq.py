"""Verify the MCQ bank: run every C++ output question, and recompute the numeric OS, DBMS and CN answers. Usage: python3 generated/src/test_mcq.py"""
import os, subprocess, sys, tempfile, sqlite3, ipaddress, re, glob
sys.path.insert(0, os.path.dirname(__file__)); from mcq_data import SECTIONS
S = {s["key"]: s for s in SECTIONS}; bad = []
def ok(cond, what): print(("ok   " if cond else "FAIL ") + what); cond or bad.append(what)
ok(len(SECTIONS) == 5 and all(len(s["qs"]) == 30 for s in SECTIONS), "5 sections x 30 questions")
for s in SECTIONS:
    for i, q in enumerate(s["qs"]):
        if len(set(q[1:5])) != 4: ok(False, f"{s['key']} {i + 1} options not distinct")
ids = set()
for f in glob.glob(os.path.join(os.path.dirname(__file__), "../../sources/kb/t_*.py")): ids |= set(re.findall(r'id="([\w-]+)"', open(f).read())) | set(re.findall(r'\("([\w-]+)",', open(f).read()))
ok(all(s["kb"] in ids for s in SECTIONS), "Knowledge Base ids exist " + str([s["kb"] for s in SECTIONS if s["kb"] not in ids]))
# C++ output questions
d = tempfile.mkdtemp()
for i, q in enumerate(S["cpp"]["qs"]):
    src = f"{d}/q{i}.cpp"; open(src, "w").write(q[6])
    c = subprocess.run(["g++", "-std=c++17", "-Wall", "-fsanitize=address,undefined", "-fno-sanitize-recover=all", src, "-o", src[:-4]], capture_output=True, text=True)
    out = subprocess.run([src[:-4]], capture_output=True, text=True).stdout if not c.returncode else "COMPILE: " + c.stderr[:300]
    ok(out == q[1] and "warning" not in c.stderr, f"cpp {i + 1}: printed {out!r}, key {q[1]!r}")
# OS
def faults(ref, n, lru):
    fr, f = [], 0
    for p in ref:
        if p in fr:
            if lru: fr.remove(p); fr.append(p)
            continue
        f += 1
        if len(fr) == n: fr.pop(0)
        fr.append(p)
    return f
R = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
ok(str(faults(R, 3, False)) == S["os"]["qs"][5][1] and faults(R, 4, False) == 10, "FIFO faults 9 (and 10 with 4 frames)")
ok(str(faults(R, 3, True)) == S["os"]["qs"][6][1], f"LRU faults {faults(R, 3, True)}")
src = f"{d}/fork.c"; open(src, "w").write('#include <stdio.h>\n#include <unistd.h>\n#include <sys/wait.h>\nint main(){fork();fork();fork();printf("x\\n");fflush(stdout);while(wait(NULL)>0);}')
subprocess.run(["gcc", src, "-o", f"{d}/fork"], check=True); ok(subprocess.run([f"{d}/fork"], capture_output=True, text=True).stdout.count("x") == 8, "fork x3 gives 8 processes")
ok(str((0 + 24 + 27) // 3) == S["os"]["qs"][18][1], "FCFS average waiting 17")
# DBMS via SQLite
db = sqlite3.connect(":memory:"); x = db.execute
x("create table a(id)"); x("create table b(id)"); [x("insert into a values(?)", (i,)) for i in range(1, 6)]; [x("insert into b values(?)", (i,)) for i in range(10, 13)]
x("create table c(id)"); [x("insert into c values(?)", (i,)) for i in range(4)]
ok(x("select count(*) from c cross join (select * from a)").fetchone()[0] == 20, "cross join 4 x 5 = 20")
ok(x("select count(*) from a left join b on a.id = b.id").fetchone()[0] == 5, "left join keeps 5")
x("create table n(v)"); [x("insert into n values(?)", (v,)) for v in (1, None, 3, None)]
ok(x("select count(v), count(*) from n").fetchone() == (2, 4), "COUNT(col) skips NULL")
ok(x("select null = null").fetchone()[0] is None, "NULL = NULL is NULL")
x("create table e(salary)"); [x("insert into e values(?)", (v,)) for v in (300, 500, 500, 400)]
ok(x(S["dbms"]["qs"][25][1]).fetchone()[0] == 400, "second-highest salary query")
ok([r[0] for r in x("select dense_rank() over (order by v desc) from (select 5 v union all select 5 union all select 3)")] == [1, 1, 2], "DENSE_RANK no gaps")
ok([r[0] for r in x("select rank() over (order by v desc) from (select 5 v union all select 5 union all select 3)")] == [1, 1, 3], "RANK leaves gaps")
# CN
ok(ipaddress.ip_network("10.0.0.0/26").num_addresses - 2 == 62, "/26 has 62 hosts")
ok(str(ipaddress.ip_network("0.0.0.0/20").netmask) == "255.255.240.0", "/20 mask")
ok(ipaddress.ip_address("192.168.1.10").is_private and not ipaddress.ip_address("172.32.0.1").is_private and not ipaddress.ip_address("11.0.0.1").is_private, "private address")
ok(str(ipaddress.ip_network("192.168.10.0/24").broadcast_address) == "192.168.10.255", "broadcast")
ok(str(ipaddress.ip_interface("10.1.5.77/22").network.network_address) == "10.1.4.0", "network address /22")
ok(1000 * 8 / 1e6 * 1000 == 8, "transmission time 8 ms")
print(f"\n{len(bad)} failures"); sys.exit(1 if bad else 0)
