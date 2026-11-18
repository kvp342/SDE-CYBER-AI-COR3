"""TenantWall paper outline PDF: section-by-section guidance, figures and tables, a writing timeline to 21 Mar 2027, a submission
checklist and the reference list. Pairs with the LaTeX skeleton in generated/tenantwall/paper/ (compiled with pdflatex + bibtex).
Run from the repo root: python3 generated/src/paper_outline.py"""
import datetime as dt, html, io, pathlib, re, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; PAPER = OUT / "tenantwall" / "paper"
E = lambda s: html.escape(str(s), quote=True)
SECTIONS = [
 ("Abstract", "150–200 words, written last", ["Problem: tenants sharing S3 and EC2 must not reach each other's data.", "Approach: ABAC with tag-matched policies and explicit denies; CloudTrail → CloudWatch → SNS alerting.", "Evaluation and result in one sentence, with numbers.", "Why it matters."]),
 ("I. Introduction", "about 0.75 page", ["Shared resources are cheap but one bad policy exposes a tenant.", "Role-per-tenant RBAC grows with every tenant; ABAC keeps one policy.", "Prevention is not enough: denied attempts must be detected and reported.", "Three contributions as a list, then a one-line roadmap."]),
 ("II. Background", "about 0.75 page", ["Multi-tenancy and resource pooling (NIST SP 800-145); isolation risks in shared clouds.", "RBAC and ABAC models; NIST SP 800-162.", "IAM evaluation order (explicit deny > allow > implicit deny), ABAC with tags, CloudTrail management vs data events."]),
 ("III. Threat model", "about 0.5 page", ["Assets, attacker (a tenant or a stolen tenant credential), trust boundary, out of scope.", "STRIDE table (already in the skeleton; from the security lab notebook)."]),
 ("IV. Design", "about 1 page", ["Architecture figure.", "Identity policy (prefix and tag matching), explicit-deny policy, TLS-only bucket policy.", "Why denies are separate from allows; one short policy excerpt."]),
 ("V. Implementation", "about 0.5 page", ["Region and services; how tenants and roles are created and tagged.", "Trail with S3 data events, metric filter pattern, alarm settings (from the TenantWall helpers).", "Method flowchart; cost controls."]),
 ("VI. Evaluation", "about 1 page", ["Research questions: RQ1 isolation holds? RQ2 how fast are denials reported? RQ3 cost and overhead?", "Run the isolation test plan several times; fill the results table.", "Detection delay as median and range; false alerts; monthly cost."]),
 ("VII. Discussion and limitations", "about 0.5 page", ["Tags as the trust anchor and who may set them.", "DescribeInstances has no resource-level control.", "CloudTrail delivery delay; scaling to many tenants; production changes."]),
 ("VIII. Related work", "about 0.5 page", ["Cloud isolation research, access-control models, cloud audit and monitoring.", "How TenantWall differs: a concrete, tested design on one provider with alerting."]),
 ("IX. Conclusion", "1 paragraph", ["What was built, measured results, one line of future work."]),
]
FIGS = [("Fig. 1", "Architecture with official AWS icons (generated/tenantwall/diagrams/tenantwall-architecture.png, from the .drawio file)"), ("Fig. 2", "Method flowchart (generated/tenantwall/diagrams/tenantwall-flowchart.png)"),
        ("Table I", "STRIDE threats and mitigations"), ("Table II", "Isolation test results: expected, observed, alert delay"), ("Optional", "Detection delay over trials (a small bar or box plot)")]
WEEKS = [("Week 1", "Related work and background: read the cited sources, write Sections II and VIII"), ("Week 2", "Design: Section IV with the policy excerpt and Fig. 1"),
         ("Week 3", "Implementation: Section V; run every isolation test once and save the evidence"), ("Week 4", "Evaluation runs: repeat tests, measure alert delays and cost; fill Table II"),
         ("Week 5", "Results and discussion: Sections VI and VII"), ("Week 6", "Introduction, abstract, conclusion; check every reference; send the draft to the professor"),
         ("Week 7", "Revise from the professor's comments; final read-through and submit by 21 March")]
START = dt.date(2027, 2, 1); DEADLINE = dt.date(2027, 3, 21)
weeks = [(n, START + dt.timedelta(weeks=i), min(START + dt.timedelta(weeks=i, days=6), DEADLINE), t) for i, (n, t) in enumerate(WEEKS)]
assert weeks[-1][2] == DEADLINE and START.weekday() == 0
CHECK = ["Page limit and template of the target venue checked (this skeleton uses IEEE conference format)", "Every number in the paper comes from your own measured runs", "Every reference verified on Google Scholar or the publisher's page (titles, authors, years, pages)",
         "No account ids, keys, bucket names or emails in figures, listings or screenshots", "Figures readable when printed in grey; captions say what to look at", "Professor has read and approved the final version",
         "Acknowledgement and author order agreed", "Policies and test scripts published on GitHub (no secrets) if the venue allows a link"]
bib = (PAPER / "refs.bib").read_text()
REFS = re.findall(r"@\w+\{(\w+),.*?title = \{(.+?)\},", bib, re.S)
assert len(REFS) == 9
tex = (PAPER / "main.tex").read_text()
assert all(f"\\cite{{{k}" in tex or f",{k}" in tex or f"{k}," in tex for k, _ in REFS), "every reference should be cited in the skeleton"
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{a}">{t}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for t, a in [("Section by section", "secs"), ("Figures, tables and writing plan", "plan"), ("Submission checklist and references", "check")])
    out = [f'''<section class="cover"><p class="eb">TENANTWALL · PAPER</p><h1>Paper<br><span>outline</span></h1>
<p class="lead">What goes in each section of the TenantWall paper, how long it should be, the figures and tables, a seven-week writing plan ending on the 21 March deadline, and a checklist before submission. The matching LaTeX skeleton (IEEE conference format) is in <code>generated/tenantwall/paper/</code>: <code>main.tex</code> with a writing prompt in every section, <code>refs.bib</code>, and a compiled preview <code>main.pdf</code>.</p>
<p class="how"><b>Before you write.</b> Ask your professor which venue and template to use and what "explicit deny" should mean in the paper. Write in Overleaf (free) by uploading the three files and the two images.</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    secs = "".join(f'<div class="s"><h3>{E(t)} <span>{E(l)}</span></h3><ul>{"".join(f"<li>{E(x)}</li>" for x in pts)}</ul></div>' for t, l, pts in SECTIONS)
    out.append(f'<section class="sec" id="secs"><h2>Section by section<a class="back" href="#top">↑ Index</a></h2><p class="meta">Lengths assume a 6-page two-column paper; scale to your venue.</p><div class="cols">{secs}</div></section>')
    fr = "".join(f"<tr><td class=k>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in FIGS)
    wr = "".join(f"<tr><td class=box>☐</td><td class=k>{E(n)}</td><td class=d>{a.strftime('%d %b')} – {b.strftime('%d %b')}</td><td>{E(t)}</td></tr>" for n, a, b, t in weeks)
    out.append(f'<section class="sec" id="plan"><h2>Figures, tables and writing plan<a class="back" href="#top">↑ Index</a></h2><h3>Figures and tables</h3><table class="t"><tbody>{fr}</tbody></table><h3>Seven weeks to 21 March</h3><table class="t"><tbody>{wr}</tbody></table><p class="meta">This overlaps the Hard pass in your plan: about 45 minutes a day on the paper, more at weekends. Build and test TenantWall in December and January first, as planned; the plan above is for writing.</p></section>')
    cr = "".join(f"<tr><td class=box>☐</td><td>{E(x)}</td></tr>" for x in CHECK)
    rr = "".join(f"<li>[{i + 1}] {E(t.replace('{', '').replace('}', ''))}</li>" for i, (k, t) in enumerate(REFS))
    out.append(f'<section class="sec" id="check"><h2>Submission checklist and references<a class="back" href="#top">↑ Index</a></h2><table class="t"><tbody>{cr}</tbody></table><h3>References in the skeleton</h3><ol class="refs">{rr}</ol><p class="meta">Full entries are in <code>refs.bib</code>. They are well-known sources, but verify every detail before submission and add the papers your professor recommends.</p></section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 13mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9pt/1.45 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } code { font: 600 7.8pt "JetBrains Mono"; }
h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; } .lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; }
table { border-collapse: collapse; width: 100%; } .ix td { padding: 2.2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10.5pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2.5mm; display: flex; align-items: baseline; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
h3 { font: 700 10pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1mm; } h3 span { font: 500 8pt "JetBrains Mono"; color: #64748b; } .cols { column-count: 2; column-gap: 7mm; } .s { break-inside: avoid; margin-bottom: 2mm; }
ul, ol { padding-left: 5mm; margin: 0; } li { margin-bottom: .8mm; } .t td { border-bottom: 1px solid #e2e8f0; padding: 1.6mm 2mm; vertical-align: top; } .k { font-weight: 700; width: 22mm; } .d { font: 600 8pt "JetBrains Mono"; width: 32mm; } .box { width: 6mm; color: #94a3b8; }
.meta { color: #475569; font-size: 8.4pt; margin: 2mm 0; } .refs li { font-size: 8.4pt; list-style: none; margin-left: -5mm; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "po.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/po.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = ["secs", "plan", "check"]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for t, k in [("Sections", "secs"), ("Figures and plan", "plan"), ("Checklist and references", "check")]: w.add_outline_item(t, d2[k] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "TenantWall paper outline"}); w.write(str(OUT / "tenantwall-paper-outline.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "po.html"): (SRC / f).unlink()
print(NP, "pages", d2)
