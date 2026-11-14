"""Re-date the Playbook to the intensive track (same schedule as the Roadmap) and fix account storage.
Ticks are keyed by problem, so nothing already ticked is lost."""
import json, re, datetime, html as H, sys
dt = datetime.date; TD = datetime.timedelta
SRC, OUT = sys.argv[1], sys.argv[2]
h = open(SRC, encoding="utf-8").read()
s = h.index("\nvar D=") + 7; DEND = h.index("};", s) + 1; D = json.loads(h[s:DEND])

def rep(old, new, count=1):
    global h
    n = h.count(old)
    if n != count: raise SystemExit(f"anchor count {n} != {count}: {old[:100]!r}")
    h = h.replace(old, new)

# ---------- the same schedule as roadmap/rebuild.py ----------
core, hard, seen = [], [], set()
for k in sorted(D):
    for x in D[k].get("due", []):
        if (x[0], x[1]) in seen: continue
        seen.add((x[0], x[1])); (hard if x[2] == "H" else core).append(x)
core.sort(key=lambda x: x[0]); hard.sort(key=lambda x: x[0])
assert len(core) == 359 and len(hard) == 84
names = {}
for k in sorted(D):
    for st in D[k].get("steps", []): names[st[0]] = st[1]
EX0, EX1 = dt(2027, 3, 22), dt(2027, 4, 7)
striver = {}; q = list(core); d = dt(2026, 11, 18)
while q:
    if d.weekday() != 6:
        n = 6 if q[0][0] <= 12 else 5
        striver[d] = q[:n]; q = q[n:]
    d += TD(days=1)
hardday = {}; q = list(hard); d = dt(2027, 2, 8)
while q:
    if not (EX0 <= d <= EX1): hardday[d] = q.pop(0)
    d += TD(days=1)
assert max(striver) == dt(2027, 1, 30) and max(hardday) == dt(2027, 5, 19), (max(striver), max(hardday))

# weekly tracks, mapped exactly as in the Roadmap
W0 = dt(2026, 11, 16); START, END = dt(2026, 11, 16), dt(2027, 5, 30)
csb, csfull, cyfull, aifull = [], {}, {}, {}
for k in sorted(D):
    c = D[k].get("cs")
    if c and c[2]:
        key = (c[0], c[2][0])
        if key not in csfull: csfull[key] = c; csb.append(key)
    c = D[k].get("cy")
    if c and c[0] not in cyfull: cyfull[c[0]] = c
    c = D[k].get("ai")
    if c and c[0] not in aifull: aifull[c[0]] = c
CS_REV = ["Core CS revision", "#BDBDBD", None, "cs-how"]
CYMAP = [1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 7, 8] + [9, 10, 11, 12, 13, 14] + [None, None] + [15, 16, 17, 18, 19, 20]
AIMAP = {12 + i: i + 1 for i in range(6)}; AIMAP.update({20 + i: i + 7 for i in range(6)})

# LeetCode month: keep its order, contests on Sundays, problem days follow the Striver step
lc_days = [k for k in sorted(D) if "lc" in D[k]]
contests = [D[k]["lc"] for k in lc_days if D[k]["lc"]["contest"]]
probs = [(max(st[0] for st in D[k].get("steps", [[99]])), D[k]["lc"]) for k in lc_days if not D[k]["lc"]["contest"]]

N = {}
x = START
while x <= END:
    w = (x - W0).days // 7; k = x.isoformat(); old = D.get(k, {}); e = {}
    exam = EX0 <= x <= EX1
    if k in ("2026-11-16", "2026-11-17"): e["cpp"] = D[k]["cpp"]
    if x in striver:
        e["steps"] = [[n_, names[n_]] for n_ in sorted({p[0] for p in striver[x]})]
        e["due"] = striver[x]
    elif x in hardday: e["due"] = [hardday[x]]
    else: e["due"] = []
    if exam: e["exam"] = 1
    if "tw" in old: e["tw"] = old["tw"]
    if not exam and "cpp" not in e:
        e["cs"] = csfull[csb[w]] if w < len(csb) else CS_REV
        c = CYMAP[w] if w < len(CYMAP) else None
        if c: e["cy"] = cyfull[c]
        if w in AIMAP: e["ai"] = aifull[AIMAP[w]]
        if x >= dt(2026, 11, 18):
            if x.weekday() == 6 and contests: e["lc"] = contests.pop(0)
            elif x in striver and probs and probs[0][0] <= max(p[0] for p in striver[x]): e["lc"] = probs.pop(0)[1]
    N[k] = e
    x += TD(days=1)
print("LeetCode month entries left unplaced:", len(contests), len(probs))
newdue = {}
for k, v in N.items():
    for p in v.get("due", []): newdue[(p[0], p[1])] = k
assert len(newdue) == 443

h = h[:s] + json.dumps(N, ensure_ascii=False, separators=(",", ":")) + h[DEND:]

# ---------- range, texts ----------
rep('var MIN="2026-11-05",MAX="2027-03-28";', 'var MIN="2026-11-16",MAX="2027-05-30";')
rep('min="2026-11-05" max="2027-03-28"', 'min="2026-11-16" max="2027-05-30"')
days = (END - START).days + 1
for a_, b_ in [("144 days · 443 problems", f"{days} days · 443 problems"), ("5 NOV 2026 → 28 MAR 2027", "16 NOV 2026 → 30 MAY 2027")]:
    h = h.replace(a_, b_)
# need(): LeetCode from 18 Nov; exam days are DSA-minimum only; AWS only in AWS weeks
rep('function need(day){var e=D[day]||{},n=["dsa"];',
    'function need(day){var e=D[day]||{},n=["dsa"];if(e.exam)return n;')
rep('if(day>="2026-11-07"&&!e.tw)n.push("lc");', 'if(day>="2026-11-18"&&!e.tw)n.push("lc");')
rep('if(day>="2026-11-16")n.push("aws");if(day>="2026-12-14")n.push("cp");',
    'if(awsOn(day))n.push("aws");if(day>="2026-12-14"&&day<"2027-03-22")n.push("cp");')
rep('function need(day){', 'function awsOn(day){if(day<"2026-11-16")return false;var w=Math.floor(Math.round((Date.UTC(+day.slice(0,4),+day.slice(5,7)-1,+day.slice(8,10))-Date.UTC(2026,10,16))/864e5)/7);return w<24&&w!==18&&w!==19}\nfunction need(day){')
# AWS weeks: the Roadmap's mapping, with the exam weeks off and the exam in the week of 19 Apr
m = re.search(r'AWS_WEEKS=(\[.*?\]);', h); AW = json.loads(m.group(1)); assert len(AW) == 19
AW2 = AW[:18] + [None, None, AW[18].replace(" and book the exam for April", " and book the exam for the week of 19 Apr"),
                 "Light review of notes and wrong answers; one more practice exam if the last was under 80%.",
                 "Sit SAA-C03 this week. June is the latest.", "Certified: add it to the resume and LinkedIn. If not yet sat, sit it now."]
h = h[:m.start(1)] + json.dumps(AW2, ensure_ascii=False) + h[m.end(1):]
rep('return i<AWS_WEEKS.length?{n:i+1,t:AWS_WEEKS[i]}:null}', 'return i<AWS_WEEKS.length&&AWS_WEEKS[i]?{n:i+1,t:AWS_WEEKS[i]}:null}')
# DSA card: exam days
rep("  else if(e.steps){h='<div class=\"big\">'",
    "  else if(e.exam){h='<div class=\"big\">Semester exams</div><p>Minimum day: 30 minutes of revision, 2 problems from your redo list, 1 LeetCode problem. Exams come first.</p>';}\n  else if(e.steps){h='<div class=\"big\">'")
rep("Moved here from 5 and 6 Nov. Only C++ and AWS count today; LeetCode, Core CS and cyber restart tomorrow, and this day\\'s Striver problems wait in Overdue.",
    "Only C++ and AWS count today. Striver, LeetCode, Core CS and cyber start on Wed 18 Nov.")
rep("else if(day<\"2026-11-07\"){h='<p>Starts Sat 7 Nov, after the C++ sprint.</p>';}", "else if(day<\"2026-11-18\"){h='<p>Starts Wed 18 Nov, after the C++ days.</p>';}")
rep("else h='<p>Starts Sat 7 Nov with OOP.</p>';", "else h=e.exam?'<p>Exam week: exam subjects come first.</p>':'<p>Starts Wed 18 Nov with OOP.</p>';")

rep("if(day>=\"2026-12-14\"){h='<div class=\"big\">'+cpBand(day)", "if(day>=\"2026-12-14\"&&day<\"2027-03-22\"){h='<div class=\"big\">'+cpBand(day)")
# ---------- per-problem due dates in the 18 step tables ----------
def fmt(k): d_ = datetime.date.fromisoformat(k); return d_.strftime("%a %d %b")
bystep = {}
for (st, nm), k in newdue.items(): bystep.setdefault(nm, []).append(k)
cnt = 0; miss = 0
def fix(m_):
    global cnt, miss
    nm = H.unescape(re.sub(r"<[^>]+>", "", m_.group(1))).strip()
    ks = bystep.get(nm)
    if not ks: miss += 1; return m_.group(0)
    cnt += 1; return m_.group(0)[: m_.start(3) - m_.start(0)] + fmt(sorted(ks)[0]) + m_.group(0)[m_.end(3) - m_.start(0):]
h = re.sub(r'<tr><td>((?:(?!</tr>).)*?)</td><td>(<span class="lv [EMH]">\w+</span>)</td><td class="mono">([A-Z][a-z]{2} \d{2} [A-Z][a-z]{2})(?: \(hard pass\))?</td></tr>', fix, h)
cnt_core = cnt; cnt = 0; miss = 0
h = re.sub(r'<tr><td>((?:(?!</tr>).)*?)</td><td>(<span class="lv H">\w+</span>)</td><td class="mono hard">([A-Z][a-z]{2} \d{2} [A-Z][a-z]{2})(?: \(hard pass\))?</td></tr>', fix, h)
print("core rows:", cnt_core, "hard rows:", cnt, "unmatched:", miss)

# ---------- account storage: a valid per-person document path, with this browser's saved progress carried over ----------
rep('db.doc("data/users/"+uid+"/trackers/apps").get()', 'db.doc("data/users/"+uid+"/pb-apps").get()')
rep('if(probe)STORE={get:function(k){return db.doc("data/users/"+uid+"/trackers/"+k).get().then(function(sn){return sn.exists?sn.data():null})},\n          set:function(k,v){return db.doc("data/users/"+uid+"/trackers/"+k).set(v)},name:"your claude.ai account"};',
    'if(probe){var P=function(k){return db.doc("data/users/"+uid+"/pb-"+k)};\n          STORE={get:function(k){return P(k).get().then(function(sn){if(sn.exists)return sn.data();return LOCAL.get(k).then(function(v){if(v&&typeof v==="object")P(k).set(v).catch(function(){});return v})})},\n          set:function(k,v){LOCAL.set(k,v).catch(function(){});return P(k).set(v)},name:"your claude.ai account"};}')
open(OUT, "w", encoding="utf-8").write(h)
print("written", OUT, len(h))
