"""OA simulation packs III PDF (sets 17-24). Run from the repo root: python3 generated/src/test_oa3.py && python3 generated/src/oa_packs3.py"""
import html, subprocess, pathlib, io, sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
sys.path.insert(0, str(SRC)); from oa_data3 import SETS
E = lambda s: html.escape(s, quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
LC = lambda s: f"https://leetcode.com/problems/{s}/"
PTS = {"Easy": 100, "Medium": 200, "Hard": 300}
DC = {"Easy": "l1", "Medium": "l2", "Hard": "l3"}
assert all(sum(p["mins"] for p in s["probs"]) == 90 for s in SETS)
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td class="n">{i + 17}</td><td><a href="#set{i + 1}">{E(s["title"].split(": ")[1])}</a><div class="f">{E(s["focus"])}</div></td><td>{E(s["date"])}</td><td>{" · ".join(f"<span class={DC[p["diff"]]}>{p["diff"][0]}</span>" for p in s["probs"])}</td><td>{sum(PTS[p["diff"]] for p in s["probs"])}</td><td class="pg"><a href="#set{i + 1}">{pg(f"set{i + 1}")}</a></td><td class="pg"><a href="#sol{i + 1}">{pg(f"sol{i + 1}")}</a></td></tr>' for i, s in enumerate(SETS))
    out = [f'''<section class="cover"><p class="eb">ONLINE ASSESSMENT · SIMULATION PACKS III</p><h1>8 more timed OAs<br><span>sets 17–24 · 90 minutes each</span></h1>
<p class="lead">Eight more practice online assessments for the placement season itself: three problems, one timer, no help. Each set has a company-style theme (strings, graphs, DP, heaps, hashing, trees, matrices, mixed). 24 new LeetCode problems, none repeated from OA packs I and II or Worked Solutions I to III (171 problems, checked by script). Each set has a question page (open it when the timer starts) and a solution page (open it only after you have scored yourself).</p>
<h2>Index</h2><table class="ix"><thead><tr><th>#</th><th>Set</th><th>Suggested date</th><th>Mix</th><th>Max</th><th>Questions</th><th>Solutions</th></tr></thead><tbody>{rows}
<tr><td class="n">·</td><td colspan="5"><a href="#rules">How to run a set, and the scoring guide</a></td><td class="pg"><a href="#rules">{pg("rules")}</a></td></tr></tbody></table>
<p class="src">Dates run every Saturday from 17 July to 4 September 2027, as placement OAs start. If a real OA falls on a Saturday, take the set on Sunday instead. Problem statements are on LeetCode; the one-line summaries, sketches and code here are original. Every reference solution was compiled with <code>g++ -std=c++17 -Wall -Wextra -fsanitize=address,undefined</code> and passed its tests.</p></section>
<section class="sec" id="rules"><h2>How to run a set<a class="back" href="#top">↑ Index</a></h2>
<h3>Before</h3><ul><li>Pick a 90-minute slot with no interruptions. Phone on silent, notes closed, no AI tools, no searching. Use C++ in the LeetCode editor (or a plain editor without autocomplete, closer to HackerRank and similar platforms).</li><li>Read the <a href="{KB}oa-tactics">OA tactics page</a> once beforehand.</li></ul>
<h3>During</h3><ul><li>Start the timer, then open the question page. Spend the first 5 minutes reading all three problems and decide the order: usually easiest first.</li><li>The minutes next to each problem are a budget. When a budget runs out, submit what you have and move on; come back at the end if time is left.</li><li>If you cannot find the optimal idea, write a correct brute force: in real OAs it often passes part of the hidden tests.</li><li>Test on the given examples and one edge case you write yourself before every submit.</li></ul>
<h3>Scoring guide</h3><table class="sc"><thead><tr><th>Problem</th><th>Full marks</th><th>Partial marks</th></tr></thead><tbody>
<tr><td><span class="l1">Easy</span></td><td>100</td><td rowspan="3">If a submission fails, LeetCode shows how many test cases passed. Score = full marks × passed / total, rounded down. No submission scores 0.</td></tr><tr><td><span class="l2">Medium</span></td><td>200</td></tr><tr><td><span class="l3">Hard</span></td><td>300</td></tr></tbody></table>
<p>Maximum points per set: {", ".join(f"set {i + 17}: {sum(PTS[p['diff']] for p in st['probs'])}" for i, st in enumerate(SETS))}. Because the maximum differs, score yourself as a percentage of the set's maximum:</p>
<table class="sc"><tbody><tr><td class="b">80% or more</td><td>Strong. Keep the next set on its date.</td></tr><tr><td class="b">50–79%</td><td>On track. Redo every problem you did not fully solve within 3 days, without looking.</td></tr><tr><td class="b">Below 50%</td><td>Repeat the set in 2 weeks after revising the patterns on its solution page (each links to the Knowledge Base).</td></tr></tbody></table>
<p class="note">These bands are a personal benchmark for tracking progress, not a company's cut-off. Real cut-offs vary by company and by batch.</p>
<h3>After</h3><ul><li>Write the score, the time each problem took and the number of wrong submissions in your revision tracker. Add every problem you did not fully solve to its Log so it comes back for revision.</li><li>Then read the solution page: compare your idea with the sketch, not just the code.</li></ul>
<h3>Record</h3><table class="rec"><thead><tr><th>Set</th><th>Date done</th><th>P1</th><th>P2</th><th>P3</th><th>Total</th><th>%</th><th>Redo by</th></tr></thead><tbody>{"".join(f"<tr><td>{i + 1}</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>" for i in range(8))}</tbody></table></section>''']
    for i, s in enumerate(SETS):
        mx = sum(PTS[p["diff"]] for p in s["probs"])
        q = "".join(f'''<div class="q"><div class="qh"><span class="qn">Problem {j + 1}</span><a class="qt" href="{LC(p["slug"])}">{E(p["title"])} ↗</a><span class="{DC[p["diff"]]}">{p["diff"]}</span><span class="m">{p["mins"]} min · {PTS[p["diff"]]} pts</span></div><p>{E(p["gist"])}</p><p class="url">{LC(p["slug"])}</p><div class="box">Your score: ______ / {PTS[p["diff"]]} &nbsp;&nbsp; Time used: ______ min &nbsp;&nbsp; Wrong submissions: ______</div></div>''' for j, p in enumerate(s["probs"]))
        out.append(f'''<section class="sec" id="set{i + 1}"><h2><span class="num">SET {i + 17}</span>{E(s["title"].split(": ")[1])}<a class="back" href="#top">↑ Index</a></h2>
<p class="meta">90 minutes · maximum {mx} points · suggested date {E(s["date"])}. Topics are hidden on purpose: working out the pattern is part of the test.</p>{q}
<div class="tot">Total: ______ / {mx} = ______ % &nbsp;&nbsp; <a href="#sol{i + 1}">Solutions for this set →</a></div></section>''')
        sol = "".join(f'''<div class="s"><h3>{j + 1}. <a href="{LC(p["slug"])}">{E(p["title"])}</a> <span class="{DC[p["diff"]]}">{p["diff"]}</span> <a class="pat" href="{KB}{p["kb"]}">{E(p["pattern"])}</a></h3>
<ol>{"".join(f"<li>{E(x)}</li>" for x in p["sketch"])}</ol><p class="cx"><b>Complexity:</b> {E(p["cx"])} &nbsp; <b>Edge cases:</b> {E("; ".join(p["edges"]))}</p><pre>{E(p["code"])}</pre></div>''' for j, p in enumerate(s["probs"]))
        out.append(f'''<section class="sec" id="sol{i + 1}"><h2><span class="num">SET {i + 17}</span>Solutions<a class="back" href="#set{i + 1}">↑ Set {i + 17}</a><a class="back" href="#top">↑ Index</a></h2>
<p class="meta">Focus: {E(s["focus"])}. Read the sketch first, then rewrite the code yourself from memory.</p>{sol}</section>''')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9pt/1.45 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 14mm 15mm; break-after: page; } code { font: 600 7.8pt "JetBrains Mono"; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } h1 { font: 700 30pt/1.05 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 20pt; }
.lead { font-size: 10pt; color: #475569; } h2 { font: 700 13pt "Space Grotesk"; color: #0f172a; margin: 5mm 0 2mm; }
table { width: 100%; border-collapse: collapse; } th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
.ix td { padding: 1.4mm 2mm; border-bottom: 1px solid #e2e8f0; } .ix td a { color: #0f172a; font-weight: 600; } .ix .f { font-size: 7.8pt; color: #64748b; } .ix .n { color: #94a3b8; font-family: "JetBrains Mono"; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.l1, .l2, .l3 { font: 600 7pt "JetBrains Mono"; border-radius: 4px; padding: 0 5px; } .l1 { background: #dcfce7; color: #166534; } .l2 { background: #fef3c7; color: #92400e; } .l3 { background: #fde2e1; color: #b42318; }
.src { font-size: 7.8pt; color: #64748b; margin-top: 4mm; } .sec { break-before: page; }
.sec h2 { font-size: 16pt; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin-top: 0; display: flex; align-items: baseline; gap: 3mm; }
.num { font: 600 9pt "JetBrains Mono"; color: #c2410c; } .back { font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; white-space: nowrap; } h2 .back:first-of-type { margin-left: auto; }
.meta { color: #475569; } h3 { font: 700 10pt "Space Grotesk"; color: #1d4ed8; margin: 4mm 0 1mm; } ul, ol { margin: 0; padding-left: 5mm; } li { margin-bottom: .8mm; } p { margin: 0 0 1.5mm; }
.sc td, .rec td { border: 1px solid #e2e8f0; padding: 1.5mm 2mm; } .sc .b { font-weight: 600; width: 32mm; } .rec td { height: 7mm; } .note { font-size: 8pt; color: #64748b; margin-top: 1.5mm; }
.q { border: 1px solid #e2e8f0; border-left: 4px solid #1d4ed8; padding: 3mm 4mm; margin: 4mm 0; } .qh { display: flex; align-items: baseline; gap: 3mm; margin-bottom: 2mm; } .qn { font: 600 7.5pt "JetBrains Mono"; color: #64748b; text-transform: uppercase; }
.qt { font: 700 12pt "Space Grotesk"; color: #0f172a; } .m { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; color: #475569; } .q p { font-size: 10pt; } .url { font: 400 7.5pt "JetBrains Mono"; color: #64748b; }
.box { margin-top: 3mm; border-top: 1px dashed #cbd5e1; padding-top: 2.5mm; font-size: 8.5pt; color: #475569; } .tot { margin-top: 5mm; font: 600 10pt "Space Grotesk"; }
.s { break-inside: avoid; margin-bottom: 2mm; } .s h3 { display: flex; align-items: baseline; gap: 2mm; font-size: 10.5pt; } .s h3 a:first-child { color: #0f172a; } .pat { font: 600 7.5pt "JetBrains Mono"; margin-left: auto; }
.cx { font-size: 8.3pt; color: #475569; margin-top: 1mm; } pre { font: 400 7.2pt/1.35 "JetBrains Mono"; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #1d4ed8; padding: 1.8mm 2.5mm; white-space: pre-wrap; margin: 0; }
pre { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }"""
def render(pages, name):
    (SRC / "oa3.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js = SRC / "r.js"; js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/oa3.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = ["rules"] + [f"set{i + 1}" for i in range(8)] + [f"sol{i + 1}" for i in range(8)]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit()); w.add_outline_item("How to run and scoring", d2["rules"] - 1, fit=Fit.fit())
for i, s in enumerate(SETS):
    par = w.add_outline_item(s["title"], d2[f"set{i + 1}"] - 1, fit=Fit.fit()); w.add_outline_item("Solutions", d2[f"sol{i + 1}"] - 1, parent=par, fit=Fit.fit())
N = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {N}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "OA simulation packs III: sets 17-24"}); w.write(str(OUT / "oa-simulation-packs-3.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "oa3.html"): (SRC / f).unlink()
print(N, "pages", {k: d2[k] for k in KEYS})
