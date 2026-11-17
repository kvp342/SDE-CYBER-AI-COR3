"""Verify MCQ bank II: structure, no repeats from bank I, every C++ output, and every computable OS, DBMS, CN and OOP answer.
Usage: python3 generated/src/test_mcq2.py"""
import ipaddress, itertools, os, sqlite3, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__)); from mcq2_data import SECTIONS; import mcq_data
S = {s["key"]: s for s in SECTIONS}; A = lambda k, i: S[k]["qs"][i][1]; bad = []
def ok(cond, what): print(("ok   " if cond else "FAIL ") + what); cond or bad.append(what)
ok(len(SECTIONS) == 5 and all(len(s["qs"]) == 30 for s in SECTIONS), "5 sections x 30 questions")
ok(all(len(set(q[1:5])) == 4 for s in SECTIONS for q in s["qs"]), "4 distinct options everywhere")
old = {q[0] for s in mcq_data.SECTIONS for q in s["qs"] if len(q) < 7} | {q[6] for s in mcq_data.SECTIONS for q in s["qs"] if len(q) > 6}
new = [q[6] if len(q) > 6 else q[0] for s in SECTIONS for q in s["qs"]]
ok(not old & set(new) and len(new) == len(set(new)), "no repeats within bank II or from bank I")
d = tempfile.mkdtemp()
def run_cpp(code, name):
    src = f"{d}/{name}.cpp"; open(src, "w").write(code)
    c = subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-fsanitize=address,undefined", "-fno-sanitize-recover=all", src, "-o", src[:-4]], capture_output=True, text=True)
    if c.returncode or "warning" in c.stderr: return "COMPILE: " + c.stderr[:400]
    return subprocess.run([src[:-4]], capture_output=True, text=True, env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0"}).stdout
for i, q in enumerate(S["cpp"]["qs"]):
    out = run_cpp(q[6], f"q{i}"); ok(out == q[1], f"cpp {i + 1}: printed {out!r}, key {q[1]!r}")
    ok(all(out != w for w in q[2:5]), f"cpp {i + 1}: no wrong option equals the real output")
# ---------- OS
def avg_wait(jobs, preemptive):                      # jobs: (name, arrival, burst); SRTF if preemptive else SJF
    t, rem, done = 0, {n: b for n, a, b in jobs}, {}
    while rem:
        ready = [(rem[n], a, n) for n, a, b in jobs if n in rem and a <= t]
        if not ready: t += 1; continue
        _, _, n = min(ready); step = 1 if preemptive else rem[n]
        rem[n] -= step; t += step
        if rem[n] == 0: del rem[n]; done[n] = t
    return sum(done[n] - a - b for n, a, b in jobs) / len(jobs)
ok(f"{avg_wait([('P1', 0, 8), ('P2', 1, 4), ('P3', 2, 9), ('P4', 3, 5)], True):g}" == A("os", 0), "SRTF average waiting 6.5")
def rr(bursts, q):
    from collections import deque
    rem, t, done, dq = list(bursts), 0, {}, deque(range(len(bursts)))
    while dq:
        i = dq.popleft(); s = min(q, rem[i]); t += s; rem[i] -= s
        if rem[i]: dq.append(i)
        else: done[i] = t
    return sum(done[i] - bursts[i] for i in done) / len(bursts)
ok(f"{rr([5, 3, 1], 2):.2f}" == A("os", 1), f"RR average waiting {rr([5, 3, 1], 2):.2f}")
REF = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
def faults(ref, n, kind):
    fr, f = [], 0
    for i, p in enumerate(ref):
        if p in fr:
            if kind == "lru": fr.remove(p); fr.append(p)
            continue
        f += 1
        if len(fr) == n:
            if kind == "opt": fr.remove(max(fr, key=lambda x: ref.index(x, i + 1) if x in ref[i + 1:] else 10**9))
            else: fr.pop(0)
        fr.append(p)
    return f
ok(str(faults(REF, 3, "opt")) == A("os", 2) and faults(REF, 3, "lru") == 12 and faults(REF, 3, "fifo") == 15, "optimal 9, LRU 12, FIFO 15")
ok(f"{0.8 * (20 + 100) + 0.2 * (20 + 200):g} ns" == A("os", 3), "EAT 140 ns")
ok(2**30 // 2**12 == 262144 and A("os", 4).startswith("262144"), "2^18 frames")
ok((32 - 10, 10) == (22, 10), "22 + 10 bits")
Q, H = [98, 183, 37, 122, 14, 124, 65, 67], 53
fcfs = sum(abs(b - a) for a, b in zip([H] + Q, Q))
def sstf(h, q):
    q, tot = list(q), 0
    while q: n = min(q, key=lambda x: abs(x - h)); tot += abs(n - h); h = n; q.remove(n)
    return tot
ok(str(fcfs) == A("os", 6) and str(sstf(H, Q)) == A("os", 7), f"disk FCFS {fcfs}, SSTF {sstf(H, Q)}")
jobs = [(6, 'a'), (8, 'b'), (7, 'c'), (3, 'd')]                       # SJF optimal: no order beats shortest-first
best = min(sum(sum(b for b, _ in p[:k]) for k in range(len(p))) for p in itertools.permutations(jobs))
ok(best == sum(sum(b for b, _ in sorted(jobs)[:k]) for k in range(len(jobs))), "SJF order is optimal for total waiting")
# ---------- DBMS
def closure(attrs, fds):
    c = set(attrs); changed = True
    while changed:
        changed = False
        for l, r in fds:
            if set(l) <= c and not set(r) <= c: c |= set(r); changed = True
    return c
FD = [("A", "B"), ("B", "C")]; ALL = set("ABCD")
keys = [''.join(k) for n in range(1, 5) for k in itertools.combinations("ABCD", n) if closure(k, FD) == ALL]
cand = [k for k in keys if not any(set(o) < set(k) for o in keys)]
ok(cand == [A("dbms", 0)], f"candidate keys {cand}")
supers = [k for n in range(1, 4) for k in itertools.combinations("ABC", n) if "A" in k]
ok(str(len(supers)) == A("dbms", 1), "4 super keys")
db = sqlite3.connect(":memory:"); x = db.execute
x("create table t(x)"); [x("insert into t values (?)", (v,)) for v in (1, 1, 2, None)]
ok(str(x("select count(distinct x) from t").fetchone()[0]) == A("dbms", 13), "COUNT(DISTINCT) = 2")
x("create table n(x)"); [x("insert into n values (NULL)") for _ in range(3)]
ok(x("select sum(x) from n").fetchone()[0] is None, "SUM of only NULLs is NULL")
x("create table v(x)"); [x("insert into v values (?)", (a,)) for a in (2, 4, None)]
ok(f"{x('select avg(x) from v').fetchone()[0]:g}" == A("dbms", 15), "AVG skips NULL")
x("create table o(id)"); [x("insert into o values (?)", (i,)) for i in (1, 2, 3)]
ok(x("select count(*) from o where id not in (select x from v)").fetchone()[0] == 0, "NOT IN with a NULL returns nothing")
x("create table ja(k)"); x("create table jb(k)"); [x("insert into ja values (1)") for _ in range(3)]; [x("insert into jb values (1)") for _ in range(3)]
ok(x("select count(*) from ja join jb on ja.k = jb.k").fetchone()[0] == 9, "3 x 3 duplicate keys give 9 rows")
# ---------- CN
ok(len(list(ipaddress.ip_network("10.0.0.0/16").subnets(new_prefix=24))) == int(A("cn", 0)), "256 /24s in a /16")
ok(len(list(ipaddress.ip_network("10.0.0.0/29").hosts())) == int(A("cn", 1)), "/29 has 6 hosts")
n23 = ipaddress.ip_network("10.0.0.0/23"); ok(ipaddress.ip_address("10.0.0.255") in list(n23.hosts()), "10.0.0.255 is a host in the /23")
agg = list(ipaddress.collapse_addresses([ipaddress.ip_network("192.168.0.0/24"), ipaddress.ip_network("192.168.1.0/24")]))
ok([str(a) for a in agg] == [A("cn", 3)], f"aggregate {agg}")
ok(2e6 / 2e8 * 1000 == 10, "propagation 10 ms")
ok(10e6 * 0.02 / 8 == 25000, "BDP 25,000 bytes")
ok(1 / (1 + 2 * 2) == 0.2, "stop-and-wait 20%")
ok(ipaddress.ip_address("127.0.0.1").is_loopback and ipaddress.ip_address("::1").is_loopback, "loopback")
ok(min(sum(a != b for a, b in zip(u, v)) for u, v in itertools.combinations(["0000000", "1101001", "0101010", "1000011", "1001100", "0100101", "0011001", "1110000"], 2)) == 3, "Hamming(7,4) code words have minimum distance 3")
# ---------- OOP behaviours that compile
ok(run_cpp(INC := "#include <bits/stdc++.h>\nusing namespace std;\n" + "struct A { A() { cout << 'A'; } virtual ~A() { cout << 'a'; } }; struct B : A { B() { cout << 'B'; } ~B() { cout << 'b'; } }; struct C : B { C() { cout << 'C'; } ~C() { cout << 'c'; } }; int main() { C c; }", "order") == "ABCcba", "construction A, B, C and reverse destruction")
ok(run_cpp("#include <bits/stdc++.h>\nusing namespace std;\nstruct B { B() { f(); } virtual void f() { cout << 'B'; } virtual ~B() {} }; struct D : B { void f() override { cout << 'D'; } }; int main() { D d; }", "ctor") == "B", "virtual call in a constructor uses the base version")
ok(run_cpp("#include <bits/stdc++.h>\nusing namespace std;\nstruct B { virtual void f(int x = 1) { cout << x; } virtual ~B() {} }; struct D : B { void f(int x = 2) override { cout << x * 10; } }; int main() { B* p = new D; p->f(); delete p; }", "defarg") == "10", "virtual call with base default argument")
print(f"\n{len(bad)} failures"); sys.exit(1 if bad else 0)
