"""Rebuild Part 00's route chart and route table for the 16 Nov 2026 → 30 May 2027 window, and fix leftover old-pace texts."""
import json, re, datetime, sys
dt = datetime.date; TD = datetime.timedelta
OLD, CUR = sys.argv[1], sys.argv[2]
ho = open(OLD).read(); h = open(CUR).read()
getD = lambda x: json.loads(x[x.index("\nvar D=") + 7: x.index("};", x.index("\nvar D=")) + 1])
DO, N = getD(ho), getD(h)
A, B = dt(2026, 11, 16), dt(2027, 5, 30); SPAN = (B - A).days + 1
P = lambda d: round((d - A).days / SPAN * 100, 2)
def seg(a, b, c, t, dim=False):  # a..b inclusive
    return f'<i class="sg{" dim" if dim else ""}" style="left:{P(a):.2f}%;width:{P(b + TD(days=1)) - P(a):.2f}%;--c:{c}" title="{t}"><em>{t}</em></i>'
def ranges(pred):  # contiguous date ranges where pred(date) gives a key
    out, cur = [], None
    d = A
    while d <= B:
        k = pred(d)
        if cur and k == cur[0] and (d - cur[2]).days <= 1: cur[2] = d
        else:
            if cur and cur[0] is not None: out.append(tuple(cur))
            cur = [k, d, d]
        d += TD(days=1)
    if cur and cur[0] is not None: out.append(tuple(cur))
    return out
# old colours by segment title
a0 = ho.find('<div class="route">'); seg_old = ho[a0: ho.find('<div class="tw">', a0)]
COL = {t: c for c, t in re.findall(r'--c:(#\w+)" title="([^"]*)"', seg_old)}
d_ = lambda k: dt.fromisoformat(k)

# DSA: C++ days, each step (Sundays inside a step don't split it), buffer, hard pass, exams
stepdays = {}
for k, v in N.items():
    if v.get("steps"):
        for p in v["due"]: stepdays.setdefault(p[0], []).append(d_(k))
names = {s[0]: s[1] for v in N.values() for s in v.get("steps", [])}
short = {t.split(" ", 1)[1].lower(): t for t in COL if re.match(r"\d+ ", t)}
dsa = [seg(A, A + TD(days=1), COL.get("C++", "#A8A8A8"), "C++")]
for st in sorted(stepdays):
    ds = sorted(stepdays[st]); t = next((v for k_, v in COL.items() if re.match(rf"{st} ", k_)), f"{st} {names[st]}")
    dsa.append(seg(ds[0], ds[-1], COL.get(t, "#BDBDBD"), t))
EX0, EX1 = dt(2027, 3, 22), dt(2027, 4, 7)
hard = sorted(d_(k) for k, v in N.items() if v.get("due") and not v.get("steps"))
dsa += [seg(dt(2027, 1, 31), dt(2027, 2, 7), "#8F8F8F", "Redo H/F", True),
        seg(hard[0], EX0 - TD(days=1), "#8F8F8F", "Hard pass"), seg(EX0, EX1, "#6E6E6E", "Exams", True),
        seg(EX1 + TD(days=1), hard[-1], "#8F8F8F", "Hard pass 2"), seg(hard[-1] + TD(days=1), B, "#6E6E6E", "Buffer", True)]
lcd = sorted(d_(k) for k, v in N.items() if "lc" in v)
lc = [seg(lcd[0], lcd[-1], COL.get("30-day grind", "#CFCFCF"), "30-day grind"), seg(lcd[-1] + TD(days=1), B, "#CFCFCF", "1 a day + Sunday contest", True)]
SH = {"Object-oriented programming (C++)": "OOP", "Operating systems": "OS", "DBMS and SQL": "DBMS", "Computer networks": "CN", "System design basics": "Design", "Core CS revision": "Revision"}
cs = [seg(a, b, next((v["cs"][1] for v in N.values() if v.get("cs") and v["cs"][0] == k), "#BDBDBD"), SH.get(k, k), k == "Core CS revision")
      for k, a, b in ranges(lambda d: (N.get(d.isoformat(), {}).get("cs") or [None])[0])]
# cyber: old groups by lab number
oldgrp = re.findall(r'style="left:([\d.]+)%;width:([\d.]+)%;--c:(#\w+)" title="([^"]*)"', seg_old[seg_old.find("<b>Cyber</b>"): seg_old.find("<b>AI</b>")])
OA = dt(2026, 11, 5); OSPAN = 144
labgrp = {}
for l_, w_, c, t in oldgrp:
    a_ = OA + TD(days=round(float(l_) / 100 * OSPAN)); b_ = OA + TD(days=round((float(l_) + float(w_)) / 100 * OSPAN) - 1)
    for k, v in DO.items():
        if "cy" in v and a_ <= d_(k) <= b_: labgrp.setdefault(v["cy"][0], (t, c))
cy = [seg(a, b, labgrp[k][1], labgrp[k][0]) for k, a, b in ranges(lambda d: labgrp.get((N.get(d.isoformat(), {}).get("cy") or [None])[0], (None,))[0] and (N.get(d.isoformat(), {}).get("cy") or [None])[0] and labgrp[(N[d.isoformat()]["cy"])[0]][0] if d.isoformat() in N and N[d.isoformat()].get("cy") else None)
      for _ in [0]] if False else []
for t, a, b in ranges(lambda d: labgrp[N[d.isoformat()]["cy"][0]][0] if N.get(d.isoformat(), {}).get("cy") else None):
    cy.append(seg(a, b, next(c for (tt, c) in labgrp.values() if tt == t), t))
ai = [seg(dt(2027, 5, 3), dt(2027, 5, 30), COL["Build with AI"], "AI-security")]
cpl = [seg(dt(2027, 2, 8), dt(2027, 3, 21), COL.get("30-day grind", "#CFCFCF"), "CP habit"), seg(dt(2027, 4, 8), B, COL.get("30-day grind", "#CFCFCF"), "CP habit")]
elite = [seg(dt(2027, 4, 8), B, "#8C8C8C", "Elite (gated)", True)]
W = lambda w: A + TD(days=7 * w)
aws = [seg(W(0), W(9) - TD(days=1), COL["Course modules"], "Course modules"), seg(W(9), W(13) - TD(days=1), COL["Labs and profile"], "Labs and profile"),
       seg(W(13), EX0 - TD(days=1), COL["SAA exam prep"], "SAA exam prep"), seg(W(20), W(22) - TD(days=1), COL["SAA exam prep"], "Review"),
       seg(W(22), W(23) - TD(days=1), "#FFFFFF", "Exam")]
months = "".join(f'<span style="left:{P(dt(y, m, 1) if (y, m) != (2026, 11) else A):.2f}%">{n}</span>' for y, m, n in [(2026, 11, "Nov"), (2026, 12, "Dec"), (2027, 1, "Jan"), (2027, 2, "Feb"), (2027, 3, "Mar"), (2027, 4, "Apr"), (2027, 5, "May")])
lane = lambda n, xs: f'<div class="lane"><b>{n}</b><div class="track">{"".join(xs)}</div></div>'
ROUTE = f'<div class="route"><div class="months">{months}</div>' + lane("DSA", dsa) + lane("LeetCode", lc) + lane("Core CS", cs) + lane("Cyber", cy) + lane("AI", ai) + lane("AWS", aws) + lane("CP", cpl) + lane("Elite", elite) + '</div>'
a1 = h.find('<div class="route">'); b1 = h.find('<div class="tw">', a1)
old_route = h[a1:b1]; assert old_route.count('<div class="lane">') >= 6
h = h[:a1] + ROUTE + h[b1:]

fm = lambda d: f"{d.day} {d.strftime('%b')}"
def span_of(key):
    ds = sorted(d_(k) for k, v in N.items() if v.get(key)); return ds
csd, cyd, aid = span_of("cs"), span_of("cy"), span_of("ai")
def runs(ds):
    out = [];
    for d in ds:
        if out and (d - out[-1][1]).days <= 8: out[-1][1] = d
        else: out.append([d, d])
    return ", ".join(f"{fm(a)} to {fm(b)}" for a, b in out)
TABLE = ('<tr><td>C++ days</td><td>16 to 17 Nov</td><td>9 h (both days)</td><td>Gate test passed: 4 of 5</td></tr>'
 f'<tr><td>Striver A2Z core</td><td>18 Nov to 30 Jan</td><td>6 problems a day to step 12, then 5 (Mon to Sat)</td><td>359 problems and 18 builds</td></tr>'
 f'<tr><td>LeetCode month</td><td>{fm(lcd[0])} to {fm(lcd[-1])}</td><td>2 h</td><td>75 problems, 5 contests</td></tr>'
 f'<tr><td>Core CS</td><td>{runs(csd)}</td><td>45 min</td><td>5 subjects, 60 answers practised</td></tr>'
 f'<tr><td>Cyber</td><td>{runs(cyd)}</td><td>1 h (2 h Sundays)</td><td>20 weekly proofs of work</td></tr>'
 f'<tr><td>AI-security project</td><td>{runs(aid)}</td><td>1 h</td><td>A RAG assistant, attacked and defended, with a demo (<a href="#p10">Part 10</a>)</td></tr>'
 '<tr><td>AWS</td><td>16 Nov to 21 Mar, then 5 Apr to 25 Apr</td><td>30 min</td><td>Course, labs and prep done; SAA-C03 sat in the week of 19 Apr</td></tr>'
 '<tr><td>CP habit</td><td>8 Feb to 21 Mar, 8 Apr to 30 May</td><td>Tue and Thu, plus a weekend round</td><td>Ratings 800 to 1200 (<a href="#cp31">Part 03</a>)</td></tr>'
 "<tr><td>TenantWall</td><td>Saturdays, 21 Nov to 12 Dec</td><td>3 h</td><td>Professor's changes done; paper submitted by 21 Mar</td></tr>"
 f'<tr><td>Hard pass</td><td>{fm(hard[0])} to {fm(hard[-1])}, not in exams</td><td>1 problem a day</td><td>84 Hard problems attempted</td></tr>'
 '<tr><td>Semester exams</td><td>22 Mar to 7 Apr</td><td>Minimum day</td><td>Revision and 2 problems a day only</td></tr>'
 '<tr><td>Checkpoints</td><td>30 Jan and 31 Mar</td><td>—</td><td>Checkpoint 1: Striver on time. Checkpoint 2, the HFT gate: Codeforces 1400+ or LeetCode contest 1800+</td></tr>'
 '<tr><td>Elite: HFT track</td><td>8 Apr to 25 Jul, only if you pass the gate</td><td>1 to 1.5 h</td><td>16 weeks of probability, puzzles and low-latency C++ (<a href="#p11">Part 11</a>)</td></tr>')
t0 = h.find('<tr><td>C++ sprint</td>'); t1 = h.find('</tbody>', t0)
h = h[:t0] + TABLE + h[t1:]
for a_, b_ in [("Each line is a track from 5 Nov 2026 to 28 Mar 2027.", "Each line is a track from 16 Nov 2026 to 30 May 2027."),
               ("The daily shape from 7 Nov", "The daily shape from 18 Nov"), ("800 to 1400 done by 28 Mar.", "800 to 1400 done by 21 Mar."),
               ("No cyber on the C++ days. Starts Sat 7 Nov.", "No cyber on the C++ days. Starts Wed 18 Nov.")]:
    h = h.replace(a_, b_)
open(CUR, "w").write(h); print("route rebuilt:", len(dsa), "DSA segments;", len(cs), "Core CS;", len(cy), "cyber;", len(ai), "AI")
