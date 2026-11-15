"""AWS SAA-C03 study pack PDF. Run from the repo root: python3 generated/src/aws_pack.py"""
import html, subprocess, pathlib, io, sys, random
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
sys.path.insert(0, str(SRC)); from aws_data import EXAM, DOMAINS, NEED, QS, PLAN
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
EXAM_PAGE = "https://aws.amazon.com/certification/certified-solutions-architect-associate/"
GUIDE = "https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf"
WA = "https://aws.amazon.com/architecture/well-architected/"; SB = "https://skillbuilder.aws/"; FAQ = "https://aws.amazon.com/faqs/"
rng = random.Random(419); L = "ABCD"; n = 0; ITEMS = {}
assert [len(QS[k]) for k, *_ in DOMAINS] == [18, 16, 14, 12]
for k, *_ in DOMAINS:
    ITEMS[k] = []
    for q in QS[k]:
        n += 1; o = list(q[1:5]); assert len(set(o)) == 4; rng.shuffle(o)
        ITEMS[k].append(dict(n=n, q=q[0], o=o, a=L[o.index(q[1])], why=q[5]))
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    ix = [("Exam facts and how to use this pack", "facts")] + [(f"Notes: {t} ({w})", f"n-{k}") for k, t, w, *_ in DOMAINS] + [("Which service for which need", "need")] + \
         [(f"Questions: {t} (Q{ITEMS[k][0]['n']}–Q{ITEMS[k][-1]['n']})", f"q-{k}") for k, t, *_ in DOMAINS] + [("Answer keys", "keys"), ("Final revision plan, 5–18 Apr 2027", "plan")]
    rows = "".join(f'<tr><td><a href="#{a}">{E(t)}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for t, a in ix)
    out = [f'''<section class="cover"><p class="eb">AWS · SOLUTIONS ARCHITECT ASSOCIATE · SAA-C03</p><h1>SAA-C03<br><span>study pack</span></h1>
<p class="lead">Notes for the four exam domains, a service-for-need table, 60 original practice questions in the exam's scenario style with explained answers, and a two-week final revision plan for 5–18 April 2027, before your exam in the week of 19 April.</p>
<h2>Index</h2><table class="ix"><tbody>{rows}</tbody></table>
<p class="src">Sources: the official <a href="{EXAM_PAGE}">exam page</a> and <a href="{GUIDE}">exam guide</a> (domains, weights, format), the <a href="{WA}">Well-Architected Framework</a> and the <a href="{FAQ}">AWS service FAQs</a>. Notes and questions are original summaries, not copied exam content. AWS changes services and prices often: check the exam guide for the current version before you book.</p></section>
<section class="sec" id="facts"><h2>Exam facts and how to use this pack<a class="back" href="#top">↑ Index</a></h2>
<table class="kv"><tbody>{"".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in EXAM)}</tbody></table>
<p class="note">From the official exam guide. Unscored questions are not marked; you cannot tell which they are, so answer everything. There is no penalty for guessing.</p>
<h3>How to use</h3><ol><li>Learn the services hands-on first (your plan's AWS track and the <a href="{KB}aws-core">Knowledge Base AWS pages</a>). This pack is for the final revision.</li><li>Read one domain's notes, then do that domain's questions without looking at the key. Aim for 80%.</li><li>For every miss, write one line: what clue in the question should have pointed to the right service.</li><li>Follow the revision plan on the last page. Take full practice exams from <a href="{SB}">AWS Skill Builder</a> (it has a free official practice question set) and the sample questions on the exam page.</li></ol>
<h3>Reading scenario questions</h3><ul><li>Find the constraint words: <b>most cost-effective</b>, <b>least operational overhead</b>, <b>highly available</b>, <b>lowest latency</b>, <b>without code changes</b>. They decide between two answers that both work.</li><li>Managed and serverless usually wins "least operational overhead". Multi-AZ wins "highly available". Caching and edge services win "lowest latency".</li><li>Eliminate options that are insecure (keys in code, public buckets, root user) or do not exist (security groups on S3, deny rules in security groups).</li></ul></section>''']
    for k, t, w, kb, notes in DOMAINS:
        out.append(f'<section class="sec" id="n-{k}"><h2>{E(t)} <span class="w">{w} of the exam</span><a class="pat" href="{KB}{kb}">Knowledge Base ↗</a><a class="back" href="#top">↑ Index</a></h2><ul class="notes">{"".join(f"<li>{E(x)}</li>" for x in notes)}</ul><p class="go"><a href="#q-{k}">Practice questions for this domain →</a></p></section>')
    out.append(f'<section class="sec" id="need"><h2>Which service for which need<a class="back" href="#top">↑ Index</a></h2><table class="need"><thead><tr><th>Need</th><th>Service</th></tr></thead><tbody>{"".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in NEED)}</tbody></table><p class="note">Cover the right column and test yourself.</p></section>')
    for k, t, *_ in DOMAINS:
        qs = "".join(f'<div class="q" id="q{it["n"]}"><p class="qq"><b>Q{it["n"]}.</b> {E(it["q"])}</p><ol class="o">{"".join(f"<li><b>{L[j]}</b> {E(x)}</li>" for j, x in enumerate(it["o"]))}</ol></div>' for it in ITEMS[k])
        out.append(f'<section class="sec" id="q-{k}"><h2>Questions: {E(t)}<a class="pat" href="#k-{k}">Answer key</a><a class="back" href="#n-{k}">↑ Notes</a><a class="back" href="#top">↑ Index</a></h2><div class="cols">{qs}</div></section>')
    first = True
    for k, t, *_ in DOMAINS:
        rows = "".join(f'<tr><td><a href="#q{it["n"]}">Q{it["n"]}</a></td><td class="a">{it["a"]}</td><td>{E(it["o"][L.index(it["a"])])}</td><td class="wy">{E(it["why"])}</td></tr>' for it in ITEMS[k])
        out.append(f'<section class="sec" id="k-{k}">{"<span id=keys></span>" if first else ""}<h2>Answer key: {E(t)}<a class="back" href="#q-{k}">↑ Questions</a><a class="back" href="#top">↑ Index</a></h2><table class="key"><thead><tr><th>Q</th><th>Ans</th><th>Answer</th><th>Why</th></tr></thead><tbody>{rows}</tbody></table><p class="note">Score: ______ / {len(ITEMS[k])}</p></section>')
        first = False
    out.append(f'<section class="sec" id="plan"><h2>Final revision plan, 5–18 Apr 2027<a class="back" href="#top">↑ Index</a></h2><p class="note">Your semester exams run until 7 April, so the first three days are light. Exam in the week of 19 April.</p><table class="plan"><thead><tr><th></th><th>Day</th><th>Focus</th><th>Do</th></tr></thead><tbody>{"".join(f"<tr><td class=box>☐</td><td class=d>{E(a)}</td><td class=f>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in PLAN)}</tbody></table>'
               f'<h3>Free resources</h3><ul><li><a href="{EXAM_PAGE}">Official exam page</a>: exam guide and sample questions.</li><li><a href="{SB}">AWS Skill Builder</a>: free exam-prep course and official practice question set.</li><li><a href="{WA}">Well-Architected Framework</a>: the six pillars.</li><li><a href="{FAQ}">AWS FAQs</a> for IAM, VPC, S3, EC2, RDS, DynamoDB: many exam details come from these.</li><li>Free tier: build a VPC, an ALB with an Auto Scaling group, and an S3 static site; delete everything after and set an AWS Budgets alert first.</li></ul></section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.8pt/1.45 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; }
.lead { font-size: 10pt; color: #475569; } table { border-collapse: collapse; width: 100%; } th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.2mm 2mm; text-align: left; }
.ix td { padding: 2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 9.5pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.src { font-size: 7.8pt; color: #64748b; margin-top: 4mm; } .sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 3mm; display: flex; align-items: baseline; gap: 2.5mm; }
h2 .w { font: 600 8pt "JetBrains Mono"; color: #c2410c; } .pat { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; } .back { font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; white-space: nowrap; } h2 > .back:first-of-type { margin-left: auto; } h2 .pat + .back { margin-left: 0; }
h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 4mm 0 1.5mm; } ul, ol { padding-left: 5mm; margin: 0; } li { margin-bottom: 1.2mm; }
.kv td { border-bottom: 1px solid #e2e8f0; padding: 1.8mm 2mm; font-size: 9.5pt; } .kv td:first-child { font-weight: 600; width: 38mm; } .note { color: #64748b; font-size: 8pt; margin: 2mm 0; }
.notes li { font-size: 9.6pt; margin-bottom: 2.4mm; } .go { margin-top: 4mm; font-weight: 600; }
.need td { border-bottom: 1px solid #eef2f7; padding: .85mm 2mm; } .need td:last-child { font-weight: 600; color: #0f172a; }
.cols { column-count: 2; column-gap: 7mm; } .q { break-inside: avoid; margin-bottom: 3mm; } .qq { margin: 0 0 1mm; } .qq b { color: #c2410c; } .o { list-style: none; padding-left: 2mm; } .o li { margin-bottom: .5mm; } .o b { display: inline-block; width: 4mm; color: #1d4ed8; font: 600 7.5pt "JetBrains Mono"; }
.key td { padding: 1.1mm 2mm; border-bottom: 1px solid #eef2f7; vertical-align: top; font-size: 8pt; } .key td:first-child a { font: 600 8pt "JetBrains Mono"; } .key .a { font: 700 9pt "JetBrains Mono"; color: #166534; text-align: center; } .key .wy { color: #475569; width: 45%; }
.plan td { border-bottom: 1px solid #e2e8f0; padding: 1.8mm 2mm; vertical-align: top; } .plan .box { color: #94a3b8; width: 5mm; } .plan .d { font: 600 8pt "JetBrains Mono"; white-space: nowrap; } .plan .f { font-weight: 600; width: 34mm; }"""
def render(pages, name):
    (SRC / "aws.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js = SRC / "r.js"; js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/aws.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = ["facts", "need", "keys", "plan"] + [f"{p}-{k}" for k, *_ in DOMAINS for p in ("n", "q", "k")]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit()); w.add_outline_item("Exam facts", d2["facts"] - 1, fit=Fit.fit())
nt = w.add_outline_item("Domain notes", d2["n-secure"] - 1, fit=Fit.fit())
for k, t, *_ in DOMAINS: w.add_outline_item(t, d2[f"n-{k}"] - 1, parent=nt, fit=Fit.fit())
w.add_outline_item("Which service for which need", d2["need"] - 1, fit=Fit.fit())
qt = w.add_outline_item("Practice questions", d2["q-secure"] - 1, fit=Fit.fit())
for k, t, *_ in DOMAINS: w.add_outline_item(t, d2[f"q-{k}"] - 1, parent=qt, fit=Fit.fit())
kt = w.add_outline_item("Answer keys", d2["keys"] - 1, fit=Fit.fit())
for k, t, *_ in DOMAINS: w.add_outline_item(t, d2[f"k-{k}"] - 1, parent=kt, fit=Fit.fit())
w.add_outline_item("Revision plan 5–18 Apr", d2["plan"] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "AWS SAA-C03 study pack"}); w.write(str(OUT / "aws-saa-c03-study-pack.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "aws.html"): (SRC / f).unlink()
print(NP, "pages", {k: d2[k] for k in KEYS}, "answer letters", {c: sum(1 for k in ITEMS for it in ITEMS[k] if it["a"] == c) for c in L})
