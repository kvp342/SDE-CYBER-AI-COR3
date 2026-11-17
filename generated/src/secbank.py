"""Cyber-security interview bank PDF. Run from the repo root: python3 generated/src/test_secbank.py && python3 generated/src/secbank.py"""
import html, io, pathlib, subprocess, sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
sys.path.insert(0, str(SRC)); from secbank_data import SECTIONS
E = html.escape
SEC = [(s["id"], s["title"], s) for s in SECTIONS]
NQ = sum(len(s["qs"]) for s in SECTIONS)
CSS = """@page { size: A4; margin: 13mm 14mm 15mm; } * { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 9.2pt/1.5 Inter, sans-serif; color: #1e293b; } a { color: #1d4ed8; text-decoration: none; } a.kit { font: 600 7.8pt "JetBrains Mono"; color: #0f766e; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; } h1 { font: 700 30pt/1.05 "Space Grotesk"; margin: 0 0 3mm; color: #0f172a; } h1 span { color: #c2410c; }
h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; margin: 0 0 3mm; padding-bottom: 1.5mm; border-bottom: 2px solid #c2410c; display: flex; align-items: baseline; }
h2 .num { color: #c2410c; margin-right: 3mm; } h2 .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; color: #64748b; } h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1.5mm; }
section.sec { break-before: page; } table { border-collapse: collapse; width: 100%; margin: 1mm 0 2mm; break-inside: auto; } tr { break-inside: avoid; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; letter-spacing: .05em; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
td { border-bottom: 1px solid #e2e8f0; padding: 1.4mm 2mm; vertical-align: top; } table.km td:first-child { width: 45%; } ul { padding-left: 5mm; margin: 1mm 0; } li { margin-bottom: 1.6mm; }
.note { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; margin: 3mm 0; font-size: 8.6pt; } .lead { font-size: 10.5pt; } sup a { font: 600 6.5pt "JetBrains Mono"; color: #c2410c; }
table.ix td { padding: 1.6mm 2mm; } td.pg { text-align: right; font-family: "JetBrains Mono"; width: 14mm; } ol.src { font-size: 7.8pt; padding-left: 6mm; } ol.src li { margin-bottom: 1mm; word-break: break-all; }
.qa { break-inside: avoid; margin: 0 0 2.4mm; padding: 1.6mm 2.5mm; border-left: 3px solid #1d4ed8; background: #f8fafc; } .q { font-weight: 600; color: #0f172a; } .q .n { font: 600 7.5pt "JetBrains Mono"; color: #c2410c; margin-right: 1.5mm; } .a { margin-top: .6mm; } .refs { font-size: 8pt; color: #475569; margin-top: 3mm; }"""
def body(pages):
    pg = lambda k: str(pages.get(k, "00")) if pages else "00"
    ix = "".join(f'<tr><td><a href="#{i}">{n + 1}. {E(t)}</a></td><td class="pg">{len(s["qs"])} Q</td><td class="pg"><a href="#{i}">{pg(i)}</a></td></tr>' for n, (i, t, s) in enumerate(SEC))
    out = [f'''<section><p class="eb">SECURITY ROLES · INTERVIEW BANK</p><h1>{NQ} security questions<br><span>with model answers</span></h1>
<p class="lead">For security-aware SDE, SOC, cloud-security and application-security interviews. It goes past the Knowledge Base's security pages: networks, web, cryptography, identity and cloud, incident response, Linux and Windows, and scenario questions. Facts that can be computed (ports, hash sizes, subnet maths, permission bits) were checked by script; the rest follow the official documents listed under each section.</p>
<table class="ix"><thead><tr><th>Section</th><th class="pg">Size</th><th class="pg">Page</th></tr></thead><tbody>{ix}</tbody></table>
<p class="note"><b>How to use.</b> Cover the answer, say yours aloud in under a minute, then compare. Mark the ones you missed and redo them in 1, 3, 7 and 21 days. Before a security interview, read the scenario section twice: interviewers judge the order of your steps as much as the facts.</p></section>''']
    k = 0
    for n, (i, t, s) in enumerate(SEC):
        qa = ""
        for q, a in s["qs"]:
            k += 1; qa += f'<div class="qa"><div class="q"><span class="n">Q{k}</span>{E(q)}</div><div class="a">{E(a)}</div></div>'
        refs = " · ".join(f'<a href="{u}">{E(l)}</a>' for l, u in s["src"])
        out.append(f'<section class="sec" id="{i}"><h2><span class="num">{n + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2><p class="note">{E(s["intro"])}</p>{qa}<p class="refs"><b>Read more:</b> {refs}</p></section>')
    return "".join(out)
js = SRC / "rs.js"
def render(pages, name):
    (SRC / "secbank.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/secbank.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "s1.pdf"); d2, n2 = render(d1, "s2.pdf"); assert n1 == n2 and all(d1[i] == d2[i] for i, _, _ in SEC)
w = PdfWriter(clone_from=PdfReader(str(SRC / "s2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for n, (i, t, _) in enumerate(SEC): w.add_outline_item(f"{n + 1}. {t}", d2[i] - 1, fit=Fit.fit())
NP = len(w.pages)
for k, pg in enumerate(w.pages):
    if k == 0: continue
    buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
    cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{k + 1} / {NP}"); cv.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Cyber-security interview bank"}); w.write(str(OUT / "cyber-security-interview-bank.pdf"))
for f in ("s1.pdf", "s2.pdf", "rs.js", "secbank.html"): (SRC / f).unlink()
print(NP, "pages;", NQ, "questions;", d2)
