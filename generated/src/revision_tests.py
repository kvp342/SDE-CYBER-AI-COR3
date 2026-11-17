"""Weekly revision tests: one 30-minute self-test every Sunday from 22 Nov 2026 to 25 Jul 2027 (none in the exam break),
matched to what the plan covers that week, drawn only from checked kit material, answers on the following page.
Run from the repo root: python3 generated/src/revision_tests.py"""
import datetime, html, io, pathlib, random, subprocess, sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
sys.path[:0] = [str(SRC), str(ROOT / "sources" / "kb")]
import mcq_data, aws_data, secbank_data, t_probs, t_probs2, t_probs3
E = html.escape

# ---- the plan's DSA order (Striver A2Z classic, 18 Nov - 30 Jan), then the hard pass: mixed revision of everything so far
FOCUS = [  # (first Sunday it applies from, label, patterns introduced that week)
 ("2026-11-22", "Arrays and hashing (A2Z steps 1–3)", ["Hashing", "Two pointers", "Prefix sum", "Kadane", "Matrix"]),
 ("2026-12-06", "Binary search (step 4)", ["Binary search", "Binary search on the answer"]),
 ("2026-12-13", "Strings and linked lists (steps 5–6)", ["Linked list"]),
 ("2026-12-27", "Recursion and backtracking (step 7)", ["Backtracking"]),
 ("2027-01-03", "Bits, stacks and queues (steps 8–9)", ["Stack", "Monotonic stack", "Bit manipulation", "Monotonic deque"]),
 ("2027-01-10", "Sliding window and heaps (steps 10–11)", ["Sliding window", "Heap"]),
 ("2027-01-17", "Greedy and binary trees (steps 12–13)", ["Greedy", "Intervals", "Trees"]),
 ("2027-01-24", "BST and graph traversal (steps 14–15)", ["BST", "BFS", "DFS"]),
 ("2027-01-31", "Graph algorithms (step 15)", ["Topological sort", "Shortest paths", "Dijkstra", "DSU", "Union-Find", "MST"]),
 ("2027-02-07", "Dynamic programming (step 16)", ["DP", "Knapsack"]),
 ("2027-02-14", "String DP and tries (steps 16–18)", ["String DP", "Trie"]),
 ("2027-02-21", "Hard pass: mixed revision", []),
 ("2027-05-30", "Placement sprint: mixed revision", []),
]
EXAMS = (datetime.date(2027, 3, 22), datetime.date(2027, 4, 7))
AWS_WEEKS = (datetime.date(2027, 4, 11), datetime.date(2027, 4, 18))           # the two Sundays before the AWS exam week
CORE = ["os", "dbms", "cn", "oop", "cpp"]

pat = lambda p: p["why"].split(".")[0].replace("Pattern: ", "")
PROBS = t_probs.P + t_probs2.P + t_probs3.P
def cx(p): return next((str(x).replace("Complexity: ", "") for x in p["points"] if str(x).startswith("Complexity")), "")
def src_of(p): return "Knowledge Base" if p in t_probs.P else "Worked Solutions II" if p in t_probs2.P else "Worked Solutions III"

d, sundays = datetime.date(2026, 11, 22), []
while d <= datetime.date(2027, 7, 31):
    if not (EXAMS[0] <= d <= EXAMS[1]): sundays.append(d)
    d += datetime.timedelta(days=7)

rng = random.Random(2028)
used_p, used_m, used_a, used_s = set(), {k: 0 for k in CORE}, 0, 0
MCQ = {s["key"]: s for s in mcq_data.SECTIONS}
AWSQ = [q for k in aws_data.QS for q in aws_data.QS[k]]; rng.shuffle(AWSQ)
SECQ = [(s["title"], q, a) for s in secbank_data.SECTIONS for q, a in s["qs"]]; rng.shuffle(SECQ)
covered, WEEKS = [], []
def mcq(q):
    opts = list(q[1:5]); rng.shuffle(opts)
    code = q[6].replace("#include <bits/stdc++.h>\nusing namespace std;\n", "") if len(q) > 6 else None   # same two lines on every snippet
    return dict(q=q[0], code=code, opts=opts, ans="ABCD"[opts.index(q[1])], why=q[5])
for n, day in enumerate(sundays):
    f = [x for x in FOCUS if datetime.date.fromisoformat(x[0]) <= day][-1]
    if f[2] and f[2][0] not in covered: covered += [p for p in f[2] if p not in covered]
    new = f[2] or covered
    pool = lambda pats: [p for p in PROBS if pat(p) in pats and p["id"] not in used_p]
    pick = (pool(new) or pool(covered))[:2] if f[2] else []
    rest = [p for p in pool(covered) if p not in pick]
    rng.shuffle(rest); pick += rest[: 3 - len(pick)]
    if len(pick) < 3: pick += [p for p in PROBS if p["id"] not in used_p and p not in pick][: 3 - len(pick)]
    for p in pick: used_p.add(p["id"])
    key = CORE[n % 5]; ms = [mcq(q) for q in MCQ[key]["qs"][used_m[key]: used_m[key] + 4]]; used_m[key] += 4
    aws_n = 2 if day in AWS_WEEKS else 1
    aw = [mcq(q) for q in AWSQ[used_a: used_a + aws_n]]; used_a += aws_n
    sq = [] if aws_n == 2 else [SECQ[used_s]]; used_s += len(sq)
    WEEKS.append(dict(n=n + 1, day=day, focus=f[1], probs=pick, core=MCQ[key]["title"], mcq=ms, aws=aw, sec=sq))

# ---- checks: every week is a Sunday outside the exam break, nothing repeats, every answer letter points at the right option
assert all(w["day"].weekday() == 6 and not (EXAMS[0] <= w["day"] <= EXAMS[1]) for w in WEEKS)
assert WEEKS[0]["day"] == datetime.date(2026, 11, 22) and WEEKS[-1]["day"] == datetime.date(2027, 7, 25)
ids = [p["id"] for w in WEEKS for p in w["probs"]]; assert len(ids) == len(set(ids)) == 3 * len(WEEKS)
for w in WEEKS:
    assert len(w["mcq"]) == 4 and len(w["aws"]) + len(w["sec"]) == 2
    for m in w["mcq"] + w["aws"]: assert m["opts"]["ABCD".index(m["ans"])] in [q[1] for q in sum((s["qs"] for s in mcq_data.SECTIONS), []) + AWSQ]
assert all(used_m[k] <= 30 for k in CORE) and used_a <= len(AWSQ) and used_s <= len(SECQ)
for w in WEEKS:                                                             # the week's problems use only patterns studied by then
    seen = sum((x[2] for x in FOCUS if datetime.date.fromisoformat(x[0]) <= w["day"]), [])
    assert all(pat(p) in seen for p in w["probs"]), (w["day"], [pat(p) for p in w["probs"]])

CSS = """@page { size: A4; margin: 13mm 14mm 15mm; } * { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 9.3pt/1.5 Inter, sans-serif; color: #1e293b; } a { color: #1d4ed8; text-decoration: none; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; } h1 { font: 700 28pt/1.05 "Space Grotesk"; margin: 0 0 3mm; color: #0f172a; } h1 span { color: #c2410c; }
h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; margin: 0 0 1mm; padding-bottom: 1.5mm; border-bottom: 2px solid #c2410c; display: flex; align-items: baseline; }
h2 .num { color: #c2410c; margin-right: 3mm; } h2 .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; color: #64748b; margin-left: 3mm; } h2 .back:first-of-type { margin-left: auto; }
h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1.5mm; } .meta { font: 600 8pt "JetBrains Mono"; color: #475569; margin: 1mm 0 2mm; }
section.sec { break-before: page; } table { border-collapse: collapse; width: 100%; } th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.2mm 2mm; text-align: left; }
td { border-bottom: 1px solid #e2e8f0; padding: 1.1mm 2mm; vertical-align: top; } td.pg { text-align: right; font-family: "JetBrains Mono"; width: 12mm; } .ix td { font-size: 8.4pt; }
.q { margin: 0 0 2.2mm; } .q b.n { font: 600 8pt "JetBrains Mono"; color: #c2410c; margin-right: 1.5mm; } .opts { margin: .6mm 0 0 6mm; } .opts span { display: inline-block; min-width: 46%; margin-right: 2%; }
pre { font: 400 7.6pt/1.35 "JetBrains Mono"; background: #f1f5f9; padding: 1.2mm 2.5mm; margin: .8mm 0; white-space: pre-wrap; font-variant-ligatures: none; }
.line { border-bottom: 1px dotted #94a3b8; height: 6mm; } .note { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; margin: 3mm 0; font-size: 8.6pt; }
.ans { margin: 0 0 2.4mm; padding: 1.4mm 2.5mm; border-left: 3px solid #059669; background: #f0fdf4; } .score { font: 600 8.5pt "JetBrains Mono"; color: #0f172a; margin-top: 3mm; }"""
def body(pages):
    pg = lambda k: str(pages.get(k, "00")) if pages else "00"
    ix = "".join(f'<tr><td>{w["n"]}</td><td>{w["day"].strftime("%a %d %b %Y")}</td><td><a href="#w{w["n"]}">{E(w["focus"])}</a></td><td>{E(w["core"])}</td><td class="pg"><a href="#w{w["n"]}">{pg(f"w{w["n"]}")}</a></td><td class="pg"><a href="#a{w["n"]}">{pg(f"a{w["n"]}")}</a></td></tr>' for w in WEEKS)
    out = [f'''<section><p class="eb">REVISION · EVERY SUNDAY</p><h1>{len(WEEKS)} weekly tests<br><span>30 minutes each</span></h1>
<p>One short test every Sunday from 22 November 2026 to 25 July 2027, as part of the weekly review. Each test checks what the plan covered that week (the Striver A2Z order until 30 January, then mixed revision of everything studied so far), plus Core CS on a five-week rotation and one AWS and one security question. No test falls in the exam break (22 March – 7 April); the two Sundays before the AWS exam have two AWS questions instead of a security one.</p>
<p class="note"><b>How to take it.</b> Timer on, no notes. Part A 10 minutes, Part B 10 minutes, Part C 10 minutes. Then turn to the answer page and score: 1 point per question (Part A: half for the right pattern, half for a correct key idea and complexity). Every wrong answer becomes an Anki card and a redo in your tracker. Every question comes from material already checked elsewhere in the kit: the {len(PROBS)} worked solutions, the Core CS MCQ bank, the AWS pack and the security interview bank.</p>
<table class="ix"><thead><tr><th>#</th><th>Sunday</th><th>Focus</th><th>Core CS</th><th class="pg">Test</th><th class="pg">Ans</th></tr></thead><tbody>{ix}</tbody></table></section>''']
    for w in WEEKS:
        qn = 0; A = []; lines = '<div class="line"></div>' * (1 if any(m["code"] for m in w["mcq"]) else 2)   # C++ weeks need room for code
        for p in w["probs"]:
            qn += 1; A.append(f'<div class="q"><b class="n">{qn}</b><a href="{p["prac"][0][1]}">{E(p["title"])}</a>: name the pattern, the key idea in two lines, and the time complexity.{lines}</div>')
        def mc(m, k):
            code = f'<pre>{E(m["code"])}</pre>' if m["code"] else ""
            return f'<div class="q"><b class="n">{k}</b>{E(m["q"])}{code}<div class="opts">{"".join(f"<span>{L}. {E(o)}</span>" for L, o in zip("ABCD", m["opts"]))}</div></div>'
        B = []
        for m in w["mcq"]: qn += 1; B.append(mc(m, qn))
        C = []
        for m in w["aws"]: qn += 1; C.append(mc(m, qn))
        for t, q, a in w["sec"]: qn += 1; C.append(f'<div class="q"><b class="n">{qn}</b>{E(q)} <i>(security: {E(t)})</i><div class="line"></div><div class="line"></div></div>')
        out.append(f'''<section class="sec" id="w{w["n"]}"><h2><span class="num">WEEK {w["n"]}</span>{w["day"].strftime("%a %d %b %Y")}<a class="back" href="#a{w["n"]}">Answers →</a><a class="back" href="#top">↑ Index</a></h2>
<p class="meta">{E(w["focus"])} · Core CS: {E(w["core"])} · 30 minutes · {qn} points</p>
<h3>Part A: patterns (10 min)</h3>{"".join(A)}<h3>Part B: {E(w["core"])} (10 min)</h3>{'<p class="meta">Every snippet starts with #include &lt;bits/stdc++.h&gt; and using namespace std;</p>' if any(m["code"] for m in w["mcq"]) else ""}{"".join(B)}<h3>Part C: cloud and security (10 min)</h3>{"".join(C)}
<p class="score">Score: ____ / {qn}</p></section>''')
        k = 0; R = []
        for p in w["probs"]:
            k += 1; R.append(f'<div class="ans"><b>{k}. {E(p["title"])}</b>: <b>{E(pat(p))}</b>. {E(" ".join(p["core"]))} <i>Complexity: {E(cx(p))}.</i> Full solution: {E(src_of(p))}.</div>')
        for m in w["mcq"] + w["aws"]:
            k += 1; R.append(f'<div class="ans"><b>{k}. {m["ans"]}</b> ({E(m["opts"]["ABCD".index(m["ans"])])}). {E(m["why"])}</div>')
        for t, q, a in w["sec"]:
            k += 1; R.append(f'<div class="ans"><b>{k}.</b> {E(a)}</div>')
        out.append(f'''<section class="sec" id="a{w["n"]}"><h2><span class="num">WEEK {w["n"]}</span>Answers<a class="back" href="#w{w["n"]}">← Test</a><a class="back" href="#top">↑ Index</a></h2>
<p class="meta">Score 1 point each. Under 60%: redo the week's problems this week and add every miss to Anki.</p>{"".join(R)}</section>''')
    return "".join(out)
js = SRC / "rv.js"
def render(pages, name):
    (SRC / "rv.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/rv.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "v1.pdf"); d2, n2 = render(d1, "v2.pdf"); assert n1 == n2 and d1 == d2
_long = [(x["n"], d2[f"a{x['n']}"] - d2[f"w{x['n']}"], (d2.get(f"w{x['n'] + 1}", n2 + 1) - d2[f"a{x['n']}"])) for x in WEEKS if d2[f"a{x['n']}"] != d2[f"w{x['n']}"] + 1 or d2.get(f"w{x['n'] + 1}", d2[f"a{x['n']}"] + 1) != d2[f"a{x['n']}"] + 1]
assert not _long, f"(week, test pages, answer pages) not 1+1: {_long}"
w = PdfWriter(clone_from=PdfReader(str(SRC / "v2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for x in WEEKS: w.add_outline_item(f"Week {x['n']}: {x['day'].strftime('%d %b %Y')}", d2[f"w{x['n']}"] - 1, fit=Fit.fit())
NP = len(w.pages)
for k, pg in enumerate(w.pages):
    if k == 0: continue
    buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
    cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{k + 1} / {NP}"); cv.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Weekly revision tests"}); w.write(str(OUT / "weekly-revision-tests.pdf"))
for f in ("v1.pdf", "v2.pdf", "rv.js", "rv.html"): (SRC / f).unlink()
print(NP, "pages;", len(WEEKS), "weeks;", len(ids), "problems,", sum(used_m.values()), "Core CS MCQs,", used_a, "AWS,", used_s, "security questions")
