"""Worked Solutions IV PDF. Run from the repo root: python3 generated/src/test_probs4.py && python3 generated/src/worked4.py"""
import html, subprocess, pathlib, io, sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
sys.path.insert(0, str(SRC)); from t_probs4 import P
E = lambda s: html.escape(s, quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
LV = {1: "L1", 2: "L2", 3: "L3"}
ORDER = ["String DP", "String algorithms", "Sliding window", "Backtracking", "Simulation", "Stack", "Geometry and hashing", "Heap", "Greedy", "Trie + backtracking", "BFS", "Bitmask BFS", "Union-Find", "Divide and conquer", "Binary search on the answer", "Grid DP", "Stock DP", "DP", "LIS", "Interval DP", "Digit DP"]
pat = lambda p: p["why"].split(".")[0].replace("Pattern: ", "")
PS = sorted(P, key=lambda p: (ORDER.index(pat(p)), p["lvl"]))
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td class="n">{i + 1}</td><td><a href="#{p["id"]}">{E(p["title"])}</a></td><td>{E(pat(p))}</td><td class="c"><span class="l{p["lvl"]}">{LV[p["lvl"]]}</span></td><td class="pg"><a href="#{p["id"]}">{pg(p["id"])}</a></td></tr>' for i, p in enumerate(PS))
    cnt = {l: sum(1 for p in P if p["lvl"] == l) for l in (1, 2, 3)}
    out = [f'''<section class="cover"><p class="eb">WORKED SOLUTIONS · PART IV · HARD</p><h1>25 hard problems<br><span>tested solutions</span></h1>
<p class="lead">Twenty-five hard (L3) LeetCode problems of the kind product companies use in final rounds, none of them in Parts I to III or the 72 OA practice problems (195 problems checked by script). Each page gives the pattern, the key idea, the steps, a C++17 solution, the test it passed, the complexity, the traps and the follow-up questions interviewers ask. Levels: L1 {cnt[1]}, L2 {cnt[2]}, L3 {cnt[3]}.</p>
<p class="how"><b>How to use.</b> Read the title, try the problem on LeetCode for 40 minutes, then open the page. If you needed the solution, log it in your revision tracker and redo it in 3, 7 and 21 days. Every solution here was compiled with <code>g++ -std=c++17 -Wall -Wextra -fsanitize=address,undefined</code> and passed the test shown.</p>
<h2>Index (grouped by pattern)</h2><table class="ix"><thead><tr><th>#</th><th>Problem</th><th>Pattern</th><th>Level</th><th>Page</th></tr></thead><tbody>{rows}</tbody></table>
<p class="src">Problem statements are on LeetCode (each page links to it). Pattern pages link to the online Knowledge Base. Explanations and code are original.</p></section>''']
    for i, p in enumerate(PS):
        lc = p["prac"][0][1]; rel = p["rel"][0]
        out.append(f'''<section class="sec" id="{p["id"]}"><h2><span class="num">{i + 1:02d}</span>{E(p["title"])}<a class="back" href="#top">↑ Index</a></h2>
<p class="meta"><span class="l{p["lvl"]}">{LV[p["lvl"]]}</span> <a href="{KB}{rel}">{E(pat(p))}</a> · <a href="{lc}">LeetCode ↗</a> · {E(p["why"].split(". ", 1)[1])}</p>
<h3>Key idea</h3>{"".join(f"<p>{E(x)}</p>" for x in p["core"])}
<h3>Steps</h3><ol>{"".join(f"<li>{E(x)}</li>" for x in p["points"][:-1])}</ol>
<h3>C++17 solution</h3><pre>{E(p["code"])}</pre>
<h3>Test it passed</h3><pre class="t">{E(p["test"])}</pre>
<div class="grid"><div><h3>Complexity</h3><p>{E(p["points"][-1].replace("Complexity: ", ""))}</p></div><div><h3>Traps</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in p["pit"])}</ul></div><div><h3>Follow-ups</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in p["ask"])}</ul></div></div></section>''')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9pt/1.45 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 10mm 14mm 6mm; break-after: page; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } h1 { font: 700 26pt/1 "Space Grotesk"; margin: 0 0 3mm; color: #0f172a; } h1 span { color: #c2410c; }
.lead { font-size: 9pt; color: #475569; margin-bottom: 2mm; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; font-size: 8.5pt; } code { font: 600 7.8pt "JetBrains Mono"; }
h2 { font: 700 13pt "Space Grotesk"; color: #0f172a; margin: 4mm 0 2mm; }
table { width: 100%; border-collapse: collapse; } .ix th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1mm 2mm; text-align: left; }
.ix td { padding: .2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 7.8pt; line-height: 1.3; } .ix td a { color: #0f172a; font-weight: 600; } .ix .n { color: #94a3b8; font-family: "JetBrains Mono"; width: 8mm; } .ix .c { text-align: center; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.l1, .l2, .l3 { font: 600 7pt "JetBrains Mono"; border-radius: 4px; padding: 0 5px; } .l1 { background: #dcfce7; color: #166534; } .l2 { background: #fef3c7; color: #92400e; } .l3 { background: #fde2e1; color: #b42318; }
.src { font-size: 7.6pt; color: #64748b; margin-top: 3mm; } .sec { break-before: page; }
.sec h2 { font-size: 16pt; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin-top: 0; display: flex; align-items: baseline; gap: 3mm; }
.num { font: 600 10pt "JetBrains Mono"; color: #c2410c; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; white-space: nowrap; }
.meta { color: #475569; font-size: 8.5pt; } h3 { font: 700 9.5pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1mm; } p { margin: 0 0 1.5mm; } ol, ul { margin: 0; padding-left: 5mm; }
pre { font: 400 7.6pt/1.4 "JetBrains Mono"; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #1d4ed8; padding: 2mm 3mm; white-space: pre-wrap; margin: 0; break-inside: avoid; }
pre.t { border-left-color: #16a34a; font-size: 7pt; } .grid { display: grid; grid-template-columns: 1fr 1.2fr 1.4fr; gap: 4mm; break-inside: avoid; } .grid ul { font-size: 8.3pt; }
pre { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }"""
def render(pages, name):
    (SRC / "w4.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js = SRC / "r.js"; js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/w4.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[p["id"]] == d2[p["id"]] for p in P)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for i, p in enumerate(PS): w.add_outline_item(f"{i + 1}. {p['title']}", d2[p["id"]] - 1, fit=Fit.fit())
N = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {N}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Worked Solutions IV: 25 hard problems, tested C++"}); w.write(str(OUT / "worked-solutions-4.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "w4.html"): (SRC / f).unlink()
print(N, "pages")
