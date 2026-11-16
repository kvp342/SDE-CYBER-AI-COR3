"""Codeforces practice ladder, 800 to 1600 by topic, with weekly targets for the 1400 gate on 31 Mar 2027.
Links use the official problemset filter (tag + rating range); no problem ids are invented. Run from the repo root: python3 generated/src/cp_ladder.py"""
import datetime as dt, html, io, pathlib, subprocess, urllib.parse
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
E = lambda s: html.escape(str(s), quote=True); KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
CF_TAGS = {"implementation", "math", "greedy", "brute force", "sortings", "binary search", "two pointers", "constructive algorithms", "number theory",
           "strings", "dp", "graphs", "dfs and similar", "bitmasks", "data structures"}     # tag names exactly as Codeforces uses them
BANDS = [(800, 800), (900, 1000), (1100, 1200), (1300, 1400), (1500, 1600)]
TOPICS = [
 ("implementation", "Implementation", "Simulate exactly what the statement says; careful indexing.", "two-pointers"),
 ("math", "Math", "Parity, divisibility, sums, simple formulas; prove before coding.", "complexity"),
 ("greedy", "Greedy", "Sort, then take the locally best; look for an exchange argument.", "greedy"),
 ("sortings", "Sorting", "Sorting first turns many problems into a scan.", "binary-search"),
 ("binary search", "Binary search", "On the answer: is there a monotone yes/no check?", "binary-search"),
 ("two pointers", "Two pointers and windows", "Prefix sums and windows also live here and under implementation.", "sliding-window"),
 ("constructive algorithms", "Constructive", "Build an answer that satisfies the rules; try small cases by hand.", "greedy"),
 ("number theory", "Number theory", "GCD, primes, modular arithmetic, sieves.", "complexity"),
 ("dp", "Dynamic programming", "State, transition, base case; start from brute force recursion.", "dp"),
 ("graphs", "Graphs", "BFS, DFS, components, shortest paths; trees count as graphs.", "bfs"),
]
assert all(t in CF_TAGS for t, *_ in TOPICS)
def link(tag, lo, hi):
    return "https://codeforces.com/problemset?tags=" + urllib.parse.quote(f"{tag},{lo}-{hi}", safe=",-")
# Weekly plan: the CP habit from 8 Feb (Tue and Thu, 2 problems each) plus one weekend round; exams pause it from 22 Mar.
START = dt.date(2027, 2, 8); EXAMS = dt.date(2027, 3, 22); GATE = dt.date(2027, 3, 31)
WEEKS = [("Implementation, math", "800–1000", "Reach a stable 800–1000 solve speed: under 15 minutes each."),
         ("Greedy, sorting", "900–1100", "First rated or virtual Div 3/Div 4 round; upsolve one problem you missed."),
         ("Binary search, two pointers", "1000–1200", "Solve the first two problems of a Div 3 in under 30 minutes."),
         ("Constructive, number theory", "1100–1300", "Third problem of a Div 3 attempted in every round."),
         ("DP, graphs", "1200–1400", "Upsolve every problem up to 1400 from your round."),
         ("Mixed, weakest two topics", "1300–1500", "Two rounds this week if possible; review every wrong answer.")]
weeks = []
for i, (topics, band, goal) in enumerate(WEEKS):
    mon = START + dt.timedelta(weeks=i)
    weeks.append((i + 1, mon, mon + dt.timedelta(days=6), topics, band, goal))
assert weeks[-1][2] < EXAMS and all(w[1].weekday() == 0 for w in weeks) and GATE.weekday() == 2
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{a}">{t}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for t, a in [("The ladder: 10 topics × 5 rating bands", "ladder"), ("Six-week plan to the 31 March gate", "weeks"), ("How to practise and how rating moves", "how")])
    out = [f'''<section class="cover"><p class="eb">COMPETITIVE PROGRAMMING · LADDER</p><h1>Codeforces<br><span>800 → 1600</span></h1>
<p class="lead">Your plan's HFT gate on 31 March 2027 is a Codeforces rating of 1400 or more (or LeetCode contest 1800+). This ladder gives each core topic five rating bands, each a link to Codeforces' own problem set filtered by that topic and rating, plus a six-week plan that fits the plan's CP habit: two problems on Tuesday and Thursday, and one round at the weekend.</p>
<p class="how"><b>Be realistic.</b> Rating moves only through rated contests, and each round shifts it by tens of points, not hundreds. If you want a real chance at 1400 by 31 March, start taking a Div 3 or Div 4 round every two weeks from January so your rating exists before February. Missing the gate is fine: you stay on Path A.</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    head = "".join(f"<th>{lo}{'' if lo == hi else '–' + str(hi)}</th>" for lo, hi in BANDS)
    body_rows = "".join(f'<tr><td class=k><a href="{KB}{kb}">{E(name)}</a><div class=d>{E(tip)}</div></td>' + "".join(f'<td class=c><a href="{link(tag, lo, hi)}">☐ open</a></td>' for lo, hi in BANDS) + "</tr>" for tag, name, tip, kb in TOPICS)
    out.append(f'<section class="sec" id="ladder"><h2>The ladder<a class="back" href="#top">↑ Index</a></h2><p class="meta">Each cell opens the Codeforces problem set filtered to that topic and rating range. Sort by "solved" (the column with the person icon) so the most-solved, most classic problems come first. Tick a cell after 5 solved problems in it. Topic names link to the Knowledge Base page for the pattern.</p><div class="sc"><table class="lad"><thead><tr><th>Topic</th>{head}</tr></thead><tbody>{body_rows}</tbody></table></div><p class="meta">Prefix sums are not a Codeforces tag; they appear under implementation, two pointers and data structures. Link format: <code>{E(link("greedy", 900, 1000))}</code>.</p></section>')
    wr = "".join(f"<tr><td class=n>{n}</td><td class=dt>{a.strftime('%d %b')} – {b.strftime('%d %b')}</td><td><b>{E(t)}</b><div class=d>Tue and Thu: 2 problems each in {E(band)} · weekend: one round</div></td><td class=g>☐ {E(goal)}</td></tr>" for n, a, b, t, band, goal in weeks)
    out.append(f'<section class="sec" id="weeks"><h2>Six weeks to the gate<a class="back" href="#top">↑ Index</a></h2><table class="t"><thead><tr><th>Week</th><th>Dates</th><th>Focus</th><th>Goal</th></tr></thead><tbody>{wr}</tbody></table><p class="meta">Exams run 22 March to 7 April: the CP habit pauses (minimum day only). The gate is checked on Wednesday 31 March from your current rating. If Codeforces rounds clash with exams, skip them; one missed round does not change the decision much.</p></section>')
    out.append(f'''<section class="sec" id="how"><h2>How to practise<a class="back" href="#top">↑ Index</a></h2><ul>
<li><b>Time-box:</b> 30 minutes on a problem below your level, 45 at your level. Then read the editorial, close it, and write the solution yourself.</li>
<li><b>Upsolve:</b> after every round, solve the next problem you could not finish. This is where most improvement comes from.</li>
<li><b>Log:</b> add each problem you needed help on to your revision tracker; redo it after 3, 7 and 21 days like the DSA problems.</li>
<li><b>Speed:</b> Div 3 problems A and B should take under 15 minutes together by week 4. Typing a clean template (fast I/O, long long) saves minutes: see the STL card and the 30 C++ bugs.</li>
<li><b>Rounds:</b> Div 4 and Div 3 rounds suit 800–1400. Educational rounds and Div 2 are harder; try them after 1300. Virtual contests count for practice but not for rating.</li>
<li><b>Hacks and penalties:</b> wrong submissions cost penalty time; test on edge cases (n = 1, all equal, maximum values) before submitting.</li></ul>
<h3>Rating, in short</h3><p>Your rating changes after each rated round based on your rank against the ratings of other participants: beating the expectation raises it. New accounts start low and climb fastest in the first few rounds, so start rounds early rather than practising only offline.</p>
<p class="meta">Sources: Codeforces problem set and contest pages (codeforces.com; not reachable from the build machine, so links use the site's standard filter format). See also the <a href="{KB}cp">competitive programming</a> Knowledge Base page.</p></section>''')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9pt/1.45 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } code { font: 400 7.4pt "JetBrains Mono"; }
h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; } .lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; }
table { border-collapse: collapse; width: 100%; } .ix td { padding: 2.2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10.5pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2.5mm; display: flex; align-items: baseline; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; } .lad td, .t td { border-bottom: 1px solid #e2e8f0; padding: 1.6mm 2mm; vertical-align: top; }
.k { width: 62mm; } .k a { color: #0f172a; font-weight: 700; } .d { color: #64748b; font-size: 7.8pt; } .c { text-align: center; font: 600 8pt "JetBrains Mono"; } .n { font: 700 9pt "JetBrains Mono"; color: #c2410c; width: 10mm; } .dt { font: 600 8pt "JetBrains Mono"; width: 30mm; } .g { width: 62mm; font-size: 8.3pt; }
.meta { color: #475569; font-size: 8.4pt; margin: 2mm 0; } h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 4mm 0 1mm; } ul { padding-left: 5mm; } li { margin-bottom: 1.5mm; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "cp.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/cp.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in ("ladder", "weeks", "how"))
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for t, k in [("Ladder", "ladder"), ("Six weeks", "weeks"), ("How to practise", "how")]: w.add_outline_item(t, d2[k] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Codeforces ladder"}); w.write(str(OUT / "codeforces-ladder.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "cp.html"): (SRC / f).unlink()
print(NP, "pages", d2, "sample link:", link("binary search", 1100, 1200))
