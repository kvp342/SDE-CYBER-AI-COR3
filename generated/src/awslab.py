"""AWS hands-on lab workbook PDF. Run from the repo root: <python with botocore> generated/src/test_awslab.py && python3 generated/src/awslab.py"""
import html, io, pathlib, subprocess, sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
sys.path.insert(0, str(SRC)); from awslab_data import LABS
E = html.escape
SEC = [(l["id"], l["title"], l) for l in LABS]
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
.qa { break-inside: avoid; margin: 0 0 2.4mm; padding: 1.6mm 2.5mm; border-left: 3px solid #1d4ed8; background: #f8fafc; } .q { font-weight: 600; color: #0f172a; } .q .n { font: 600 7.5pt "JetBrains Mono"; color: #c2410c; margin-right: 1.5mm; } .a { margin-top: .6mm; } .refs { font-size: 8pt; color: #475569; margin-top: 3mm; }
pre { font: 400 7.6pt/1.45 "JetBrains Mono"; background: #0f172a; color: #e2e8f0; padding: 2.5mm 3mm; white-space: pre-wrap; overflow-wrap: anywhere; margin: 1mm 0 2mm; font-variant-ligatures: none; } pre .c { display: block; padding-left: 4mm; text-indent: -4mm; margin-bottom: 1.2mm; } code.cmd { font: 400 7.6pt "JetBrains Mono"; font-variant-ligatures: none; overflow-wrap: anywhere; } .meta { font: 600 8pt "JetBrains Mono"; color: #475569; margin: -1mm 0 2mm; } .cost { background: #ecfdf5; border-left: 3px solid #059669; padding: 1.8mm 3mm; font-size: 8.6pt; margin: 0 0 2mm; } ol { padding-left: 5mm; margin: 1mm 0; }"""
def body(pages):
    pg = lambda k: str(pages.get(k, "00")) if pages else "00"
    ix = "".join(f'<tr><td><a href="#{i}">Lab {n + 1}. {E(t)}</a></td><td>{E(l["domain"])}</td><td class="pg">{l["minutes"]} min</td><td class="pg"><a href="#{i}">{pg(i)}</a></td></tr>' for n, (i, t, l) in enumerate(SEC))
    NC = sum(len(l["cli"]) + sum(c.startswith("aws ") for c in l["cleanup"]) for l in LABS)
    out = [f'''<section><p class="eb">AWS SAA-C03 · HANDS-ON</p><h1>{len(LABS) - 1} AWS labs<br><span>plus a teardown checklist</span></h1>
<p class="lead">Build what the exam asks about: IAM roles, S3, a VPC, EC2, a load balancer with Auto Scaling, RDS, Lambda, CloudTrail alarms and KMS. Each lab has the goal, console steps, the same thing in the AWS CLI, how to check it worked, cleanup, and what the exam expects you to know. All {NC} CLI commands were checked against the AWS service models and passed the AWS CLI's own argument parser.</p>
<table class="ix"><thead><tr><th>Lab</th><th>Exam domain</th><th class="pg">Time</th><th class="pg">Page</th></tr></thead><tbody>{ix}</tbody></table>
<p class="note"><b>Before you start.</b> Do Lab 1 first: a budget alert and MFA on the root user. Accounts created on or after 15 July 2025 are on AWS's credit-based Free plan (up to 200 USD of credits for 6 months), not the old 12-month free tier, so every lab says what it may cost and how to delete it (<a href="https://aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan">AWS announcement</a>). Region: ap-south-1 (Mumbai). Words like $VPC_ID are placeholders: copy the ID from the previous command's output. Never paste access keys into code or chat; use roles and <code>aws configure sso</code> or a named profile.</p></section>''']
    for n, (i, t, l) in enumerate(SEC):
        ol = "".join(f"<li>{E(x)}</li>" for x in l["console"])
        cl = "".join(f'<li><code class="cmd">{E(x)}</code></li>' if x.startswith("aws ") else f"<li>{E(x)}</li>" for x in l["cleanup"])
        ex = "".join(f"<li>{E(x)}</li>" for x in l["exam"])
        out.append(f'''<section class="sec" id="{i}"><h2><span class="num">{n + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2>
<p class="meta">{E(l["domain"])} · about {l["minutes"]} minutes</p><p class="cost"><b>Cost:</b> {E(l["cost"])}</p>
<p><b>Goal.</b> {E(l["goal"])}</p><h3>Console</h3><ol>{ol}</ol><h3>CLI</h3><pre>{"".join(f'<span class="c">{E(c)}</span>' for c in l["cli"])}</pre>
<h3>Check it worked</h3><p>{E(l["check"])}</p><h3>Clean up</h3><ul>{cl}</ul><h3>For the exam</h3><ul>{ex}</ul>
<p class="refs"><b>Official guide:</b> <a href="{l["doc"][1]}">{E(l["doc"][0])}</a></p></section>''')
    return "".join(out)
js = SRC / "ra.js"
def render(pages, name):
    (SRC / "awslab.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/awslab.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "a1.pdf"); d2, n2 = render(d1, "a2.pdf"); assert n1 == n2 and all(d1[i] == d2[i] for i, _, _ in SEC)
w = PdfWriter(clone_from=PdfReader(str(SRC / "a2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for n, (i, t, _) in enumerate(SEC): w.add_outline_item(f"Lab {n + 1}. {t}", d2[i] - 1, fit=Fit.fit())
NP = len(w.pages)
for k, pg in enumerate(w.pages):
    if k == 0: continue
    buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
    cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{k + 1} / {NP}"); cv.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "AWS hands-on lab workbook"}); w.write(str(OUT / "aws-lab-workbook.pdf"))
for f in ("a1.pdf", "a2.pdf", "ra.js", "awslab.html"): (SRC / f).unlink()
print(NP, "pages;", d2)
