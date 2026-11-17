"""Run every SQL pack II query in SQLite and compare its full output with an answer computed independently in Python.
Usage: python3 generated/src/test_sql2.py"""
import datetime as dt, itertools, os, sqlite3, statistics, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__)); from sql2_data import T, SCHEMA, Q
R = {t: rows for t, (_, rows) in T.items()}
D = lambda s: dt.date.fromisoformat(s)
TS = lambda s: dt.datetime.strptime(s, "%Y-%m-%d %H:%M")
users, logins, events, txns = R["users"], R["logins"], R["events"], R["txns"]
txs = sorted(txns, key=lambda r: (r[2], r[0]))                      # by day, id

def streaks():
    out = []
    for u in sorted({l[0] for l in logins}):
        days = sorted({D(d) for uu, d in logins if uu == u}); best = run = 1
        for a, b in zip(days, days[1:]): run = run + 1 if (b - a).days == 1 else 1; best = max(best, run)
        out.append((u, best))
    return out
def sessions():
    out = []
    for u in sorted({e[0] for e in events}):
        ts = sorted(TS(e[1]) for e in events if e[0] == u)
        out.append((u, 1 + sum((b - a).total_seconds() / 60 > 30 for a, b in zip(ts, ts[1:]))))
    return out
def balance(u):
    b, out = 0, []
    for r in txs:
        if r[1] == u: b += r[3]; out.append((r[0], r[2], r[3], b))
    return out
def first_negative():
    out = []
    for u in sorted({r[1] for r in txns}):
        neg = [d for _, d, _, b in balance(u) if b < 0]
        if neg: out.append((u, min(neg)))
    return out
SC = R["scores"]
def top3():
    out = []
    for s in sorted({x[1] for x in SC}):
        top = sorted({x[2] for x in SC if x[1] == s}, reverse=True)[:3]
        out += sorted(((s, x[0], x[2]) for x in SC if x[1] == s and x[2] in top), key=lambda r: (-r[2], r[1]))
    return out
def medians(): return [(s, float(statistics.median([x[2] for x in SC if x[1] == s]))) for s in sorted({x[1] for x in SC})]
def ntile():
    rows = sorted(((x[0], x[2]) for x in SC if x[1] == "DSA"), key=lambda r: (-r[1], r[0])); n = len(rows); first = (n + 1) // 2
    return [(st, sc, 1 if i < first else 2) for i, (st, sc) in enumerate(rows)]
def top_bottom():
    out = []
    for s in sorted({x[1] for x in SC}):
        rows = sorted((x for x in SC if x[1] == s), key=lambda x: (-x[2], x[0])); out.append((s, rows[0][0], rows[-1][0]))
    return out
def next_event():
    ev = sorted((e for e in events if e[0] == 1), key=lambda e: e[1])
    return [(e[1], e[2], round((TS(n[1]) - TS(e[1])).total_seconds() / 60) if n else None) for e, n in zip(ev, ev[1:] + [None])]
def behind():
    mx = {s: max(x[2] for x in SC if x[1] == s) for s in {x[1] for x in SC}}
    return sorted(((x[1], x[0], x[2], mx[x[1]] - x[2]) for x in SC), key=lambda r: (r[0], r[3], r[1]))
def new_users():
    first = Counter(min(d for uu, d in logins if uu == u) for u in {l[0] for l in logins}); out, tot = [], 0
    for d in sorted(first): tot += first[d]; out.append((d, first[d], tot))
    return out
def retention():
    lg = set(logins); out = []
    for m in sorted({u[2][:7] for u in users}):
        us = [u for u in users if u[2][:7] == m]
        kept = sum((u[0], str(D(u[2]) + dt.timedelta(days=1))) in lg for u in us)
        out.append((m, len(us), round(100.0 * kept / len(us), 1)))
    return out
def funnel():
    v = c = p = 0
    for u in {e[0] for e in events}:
        ev = sorted((e for e in events if e[0] == u), key=lambda e: e[1])
        vt = next((e[1] for e in ev if e[2] == "view"), None)
        if vt is None: continue
        v += 1; ct = next((e[1] for e in ev if e[2] == "cart" and e[1] > vt), None)
        if ct is None: continue
        c += 1; p += any(e[2] == "purchase" and e[1] > ct for e in ev)
    return [(v, c, p)]
def rising():
    out = []
    for u in sorted({r[1] for r in txns}):
        m = defaultdict(int)
        for r in txns:
            if r[1] == u and r[3] < 0: m[r[2][:7]] -= r[3]
        sp = [m[k] for k in sorted(m)]
        if len(sp) >= 2 and all(b > a for a, b in zip(sp, sp[1:])): out.append(next(x[1] for x in users if x[0] == u))
    return [(n,) for n in sorted(out)]
CAT = R["categories"]
def paths():
    by = {c[0]: c for c in CAT}
    def path(c): return (path(by[c[2]])[0] + " > " + c[1], path(by[c[2]])[1] + 1) if c[2] else (c[1], 0)
    return sorted(path(c) for c in CAT)
def descendants():
    root = next(c[0] for c in CAT if c[1] == "Electronics"); s = {root}; changed = True
    while changed:
        changed = False
        for c in CAT:
            if c[2] in s and c[0] not in s: s.add(c[0]); changed = True
    return [(n,) for n in sorted(c[1] for c in CAT if c[0] in s and c[0] != root)]
def fill_days():
    return [(str(D("2024-01-01") + dt.timedelta(days=i)), len({u for u, d in logins if d == str(D("2024-01-01") + dt.timedelta(days=i))})) for i in range(7)]
def missing_ids():
    ids = {r[0] for r in txns}; return [(i,) for i in range(min(ids), max(ids) + 1) if i not in ids]
def pivot():
    out = []
    for u in sorted({r[1] for r in txns}):
        out.append((u,) + tuple(-sum(r[3] for r in txns if r[1] == u and r[3] < 0 and r[2][5:7] == m) for m in ("01", "02", "03")))
    return out
def histogram():
    c = Counter("1: under 1000" if -r[3] < 1000 else "2: 1000-2999" if -r[3] < 3000 else "3: 3000+" for r in txns if r[3] < 0)
    return sorted(c.items())
F = R["follows"]
def mutual(): return sorted((a, b) for a, b in F if (b, a) in F and a < b)
def suggest():
    mine = {b for a, b in F if a == 1}; c = Counter(b2 for a, b in F if a == 1 for a2, b2 in F if a2 == b and b2 != 1 and b2 not in mine)
    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))
def together():
    orders = defaultdict(set)
    for o, p in R["basket"]: orders[o].add(p)
    c = Counter(pair for ps in orders.values() for pair in itertools.combinations(sorted(ps), 2))
    return sorted(((a, b, n) for (a, b), n in c.items() if n >= 2), key=lambda r: (-r[2], r[0], r[1]))
def overlaps():
    B = R["bookings"]
    return [(a[0], b[0], a[1]) for a, b in itertools.combinations(sorted(B), 2) if a[1] == b[1] and a[2] < b[3] and b[2] < a[3]]
def latest():
    best = {}
    for u, t, e in R["profile_updates"]:
        if u not in best or t > best[u][0]: best[u] = (t, e)
    return [(u, best[u][1]) for u in sorted(best)]
def swap():
    S = sorted(R["seats"]); n = len(S); out = []
    for i, s in S: out.append((i if i % 2 == 1 and i == n else i + 1 if i % 2 == 1 else i - 1, s))
    return sorted(out)
def except_():
    return [(u,) for u in sorted({a for a, _ in F} - {b for _, b in F})]
def every_month():
    months = {r[2][:7] for r in txns}
    return [(u,) for u in sorted({r[1] for r in txns}) if {r[2][:7] for r in txns if r[1] == u} == months]
def same_cat():
    out = []
    for u in sorted({r[1] for r in txns}):
        rows = [r for r in txs if r[1] == u]
        out += [(b[0], u, b[4]) for a, b in zip(rows, rows[1:]) if a[4] == b[4]]
    return sorted(out)
def keyset():
    rows = sorted(((x[2], x[0], x[1]) for x in SC), key=lambda r: (-r[0], r[1], r[2]))
    i = rows.index((85, "Ravi", "OS")); return rows[i + 1: i + 4]

EXPECT = [streaks(), sessions(), balance(1), first_negative(), top3(), medians(), ntile(), top_bottom(), next_event(), behind(),
          new_users(), retention(), funnel(), rising(), paths(), descendants(), fill_days(), missing_ids(), pivot(), histogram(),
          mutual(), suggest(), together(), overlaps(), latest(), swap(), except_(), every_month(), same_cat(), keyset()]

def run_all():
    db = sqlite3.connect(":memory:"); db.executescript(SCHEMA); res = []
    for i, (q, exp) in enumerate(zip(Q, EXPECT), 1):
        cur = db.execute(q[4]); rows = [tuple(r) for r in cur.fetchall()]; cols = [c[0] for c in cur.description]
        norm = lambda rs: [tuple(round(v, 6) if isinstance(v, float) else v for v in r) for r in rs]
        assert norm(rows) == norm([tuple(r) for r in exp]), f"Q{i} {q[0]}:\n  SQL    {rows}\n  Python {exp}"
        assert rows, f"Q{i} {q[0]} returned no rows"
        res.append((cols, rows))
    return db, res
if __name__ == "__main__":
    assert len(Q) == 30 and len(EXPECT) == 30 and len({q[0] for q in Q}) == 30
    run_all(); print(f"30/30 queries match their independent Python answers (SQLite {sqlite3.sqlite_version})")
