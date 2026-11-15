"""Core CS MCQ bank PDF. Run from the repo root: python3 generated/src/test_mcq.py && python3 generated/src/mcq.py"""
import html, subprocess, pathlib, io, sys, random
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
sys.path.insert(0, str(SRC)); from mcq_data import SECTIONS
E = lambda s: html.escape(s, quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
rng = random.Random(2027); N = 0; L = "ABCD"
for s in SECTIONS:
    s["items"] = []
    for q in s["qs"]:
        N += 1; opts = list(q[1:5]); rng.shuffle(opts)
        s["items"].append(dict(n=N, q=q[0], opts=opts, ans=L[opts.index(q[1])], why=q[5], code=q[6] if len(q) > 6 else None))
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{s["key"]}">{E(s["title"])}</a></td><td class="c">Q{s["items"][0]["n"]}–Q{s["items"][-1]["n"]}</td><td class="pg"><a href="#{s["key"]}">{pg(s["key"])}</a></td><td class="pg"><a href="#key-{s["key"]}">{pg("key-" + s["key"])}</a></td></tr>' for s in SECTIONS)
    dist = {c: sum(1 for s in SECTIONS for it in s["items"] if it["ans"] == c) for c in L}
    out = [f'''<section class="cover"><p class="eb">CORE CS · OA MULTIPLE CHOICE</p><h1>150 MCQs<br><span>with answers and reasons</span></h1>
<p class="lead">Online assessments often add a short MCQ round on Operating Systems, DBMS, Computer Networks, OOP and C++ output. This bank has 30 questions on each. Answers are on separate pages at the end, so you can test yourself first. Each answer has a one-line reason.</p>
<p class="how"><b>How to use.</b> Do one section in 20 minutes (40 seconds a question), mark your answers, then check the key. Score 24 or more out of 30 before you move on; below that, read the linked Knowledge Base page and retry the section a week later. Put every wrong question into your revision tracker.</p>
<h2>Index</h2><table class="ix"><thead><tr><th>Section</th><th>Questions</th><th>Page</th><th>Answer key</th></tr></thead><tbody>{rows}</tbody></table>
<h2>How the answers were checked</h2><ul class="chk"><li>All 30 C++ questions were compiled with <code>g++ -std=c++17 -Wall -fsanitize=address,undefined</code> and run; the printed output is the keyed answer. None depends on undefined behaviour.</li><li>Page-fault counts were simulated, the fork count was run, subnet answers were computed with Python's ipaddress module, and the SQL answers (joins, COUNT, NULL comparison, second-highest salary, RANK and DENSE_RANK) were run in SQLite.</li><li>Answer positions are shuffled: A {dist["A"]}, B {dist["B"]}, C {dist["C"]}, D {dist["D"]}.</li></ul>
<p class="src">Questions and explanations are original. For deeper reading use the Knowledge Base pages linked in each section heading and the Core CS Q&A pages.</p></section>''']
    for s in SECTIONS:
        qs = "".join(f'''<div class="q" id="q{it["n"]}"><p class="qq"><b>Q{it["n"]}.</b> {E(it["q"])}</p>{f'<pre>{E(it["code"].split(chr(10), 2)[2])}</pre>' if it["code"] else ""}<ol class="o">{"".join(f"<li><b>{L[k]}</b> {E(o)}</li>" for k, o in enumerate(it["opts"]))}</ol></div>''' for it in s["items"])
        note = '<p class="meta">Every program below includes &lt;bits/stdc++.h&gt; and uses namespace std (left out to save space). Compiled as C++17.</p>' if s["key"] == "cpp" else ""
        out.append(f'<section class="sec" id="{s["key"]}"><h2>{E(s["title"])}<a class="pat" href="{KB}{s["kb"]}">Knowledge Base ↗</a><a class="back" href="#key-{s["key"]}">Answer key</a><a class="back" href="#top">↑ Index</a></h2>{note}<div class="cols">{qs}</div></section>')
    for s in SECTIONS:
        rows = "".join(f'<tr><td><a href="#q{it["n"]}">Q{it["n"]}</a></td><td class="a">{it["ans"]}</td><td>{E(it["opts"][L.index(it["ans"])])}</td><td class="w">{E(it["why"])}</td></tr>' for it in s["items"])
        out.append(f'<section class="sec" id="key-{s["key"]}"><h2>Answer key: {E(s["title"])}<a class="back" href="#{s["key"]}">↑ Questions</a><a class="back" href="#top">↑ Index</a></h2><table class="key"><thead><tr><th>Q</th><th>Ans</th><th>Option</th><th>Why</th></tr></thead><tbody>{rows}</tbody></table><p class="meta">Score: ______ / 30. Target 24 or more.</p></section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.6pt/1.4 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 15mm 15mm; break-after: page; } code { font: 600 7.8pt "JetBrains Mono"; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } h1 { font: 700 32pt/1.05 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 20pt; }
.lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; font-size: 9pt; } h2 { font: 700 13pt "Space Grotesk"; color: #0f172a; margin: 5mm 0 2mm; }
table { width: 100%; border-collapse: collapse; } th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
.ix td { padding: 1.8mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 9.5pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .c { font-family: "JetBrains Mono"; color: #64748b; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.chk { font-size: 9pt; padding-left: 5mm; } .src { font-size: 7.8pt; color: #64748b; margin-top: 4mm; } .sec { break-before: page; }
.sec h2 { font-size: 15pt; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin-top: 0; display: flex; align-items: baseline; gap: 2.5mm; }
.pat { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; } .back { font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; white-space: nowrap; }
.meta { color: #64748b; font-size: 8pt; } .cols { column-count: 2; column-gap: 7mm; } .q { break-inside: avoid; margin-bottom: 3mm; } .qq { margin: 0 0 1mm; } .qq b { color: #c2410c; }
.o { list-style: none; margin: 0; padding-left: 3mm; } .o li { margin-bottom: .4mm; } .o b { display: inline-block; width: 4mm; color: #1d4ed8; font-family: "JetBrains Mono"; font-size: 7.5pt; }
pre { font: 400 6.9pt/1.35 "JetBrains Mono"; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #1d4ed8; padding: 1.5mm 2mm; white-space: pre-wrap; margin: 0 0 1mm; }
pre { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
.key td { padding: 1.1mm 2mm; border-bottom: 1px solid #eef2f7; vertical-align: top; font-size: 8pt; } .key td:first-child a { font-family: "JetBrains Mono"; font-weight: 600; } .key .a { font: 700 9pt "JetBrains Mono"; color: #166534; text-align: center; } .key .w { color: #475569; width: 48%; }"""
def render(pages, name):
    (SRC / "mcq.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js = SRC / "r.js"; js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/mcq.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = [s["key"] for s in SECTIONS] + ["key-" + s["key"] for s in SECTIONS]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for s in SECTIONS: w.add_outline_item(s["title"], d2[s["key"]] - 1, fit=Fit.fit())
ak = w.add_outline_item("Answer keys", d2["key-" + SECTIONS[0]["key"]] - 1, fit=Fit.fit())
for s in SECTIONS: w.add_outline_item(s["title"], d2["key-" + s["key"]] - 1, parent=ak, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Core CS MCQ bank: 150 questions"}); w.write(str(OUT / "core-cs-mcq-bank.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "mcq.html"): (SRC / f).unlink()
print(NP, "pages", {k: d2[k] for k in KEYS})
