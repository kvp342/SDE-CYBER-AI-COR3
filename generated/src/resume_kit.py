"""Resume kit: an ATS-safe one-page template (placeholders only), bullet formulas with project examples, and a review checklist.
Writes generated/resume/resume-template.html and .md, and generated/resume-kit.pdf. Checks the template page is one page and that its
extracted text reads top to bottom in the right order (what an ATS parser sees). Run from the repo root: python3 generated/src/resume_kit.py"""
import html, io, pathlib, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; RES = OUT / "resume"
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
R = dict(
 name="YOUR NAME", contact="City, India · your.email@example.com · +91 XXXXX XXXXX · linkedin.com/in/your-handle · github.com/your-handle",
 sections=[
  ("Education", [("B.Tech, Computer Science and Engineering (Cyber Security)", "Your College, City", "2024 – 2028", ["CGPA: X.XX / 10 (only if 7.5 or above; otherwise leave it out)", "Relevant courses: Data Structures, Operating Systems, DBMS, Computer Networks, Cryptography"])]),
  ("Projects", [
   ("TenantWall: tenant isolation on AWS with ABAC", "Research project with Prof. [Name] · github.com/your-handle/tenantwall", "Dec 2026 – Mar 2027",
    ["Designed attribute-based access control for a shared S3 bucket and EC2 fleet so each tenant reaches only its own resources, using tag-matched IAM policies and explicit denies; validated with IAM Access Analyzer (0 findings)",
     "Verified isolation with 14 scenarios on real AWS (10 refusals, each classified as explicit or implicit deny) and built CloudTrail → CloudWatch → SNS alerting that emailed on refused calls within 3 minutes",
     "Paper [submitted to / accepted at] [venue], [month year]"]),
   ("Secure RAG assistant with prompt-injection defences", "Python, Claude API · github.com/your-handle/secrag", "May 2027",
    ["Built a retrieval-augmented assistant over security notes with four defence layers (input scanning, document sanitising, prompt separation, output checks)",
     "Cut attack success rate from [A]% to [B]% on [N] held-out prompt-injection attacks while blocking [C]% of [M] normal questions, measured with an evaluation harness"]),
   ("Study tracker REST API", "Python, FastAPI, SQLite, JWT · github.com/your-handle/study-tracker", "Jan 2027",
    ["Built a REST API with JWT login, scrypt password hashing, per-user authorisation on every query and login rate limiting",
     "Wrote [N] tests covering forged and expired tokens, cross-user access and SQL injection; ran them in GitHub Actions on every push"])]),
  ("Skills", [("Languages: C++ (STL), Python, SQL, Bash", "", "", []), ("Cloud and security: AWS (IAM, S3, EC2, CloudTrail, CloudWatch), OWASP Top 10, Burp Suite, Linux", "", "", []), ("Tools: Git, Docker, FastAPI, Linux", "", "", [])]),
  ("Achievements", [("", "", "", ["AWS Certified Solutions Architect – Associate (SAA-C03), [month year]", "Solved [N]+ DSA problems (LeetCode: [handle]); Codeforces rating [R] ([handle])", "[CTF or hackathon result, with rank and number of teams]"])]),
 ])
def resume_html():
    parts = [f'<header><h1>{E(R["name"])}</h1><p>{E(R["contact"])}</p></header>']
    for title, items in R["sections"]:
        parts.append(f"<h2>{E(title)}</h2>")
        for head, sub, date, bullets in items:
            if head and not sub and not date and not bullets: parts.append(f'<p class="line">{E(head)}</p>'); continue
            if head: parts.append(f'<div class="row"><b>{E(head)}</b><span>{E(date)}</span></div>' + (f'<div class="sub">{E(sub)}</div>' if sub else ""))
            if bullets: parts.append("<ul>" + "".join(f"<li>{E(b)}</li>" for b in bullets) + "</ul>")
    return "".join(parts)
RCSS = """body { font: 400 10pt/1.32 Arial, Helvetica, sans-serif; color: #000; } header { text-align: center; } h1 { font-size: 17pt; margin: 0 0 1mm; letter-spacing: .02em; }
header p { margin: 0 0 2mm; font-size: 9.2pt; } h2 { font-size: 10.5pt; text-transform: uppercase; letter-spacing: .06em; border-bottom: 1px solid #000; margin: 3.2mm 0 1.2mm; padding-bottom: .5mm; }
.row { display: flex; justify-content: space-between; margin-top: 1.2mm; } .sub { font-style: italic; font-size: 9.4pt; } ul { margin: .5mm 0 0; padding-left: 5mm; } li { margin-bottom: .6mm; } .line { margin: .6mm 0; }"""
def resume_md():
    out = [f"# {R['name']}", R["contact"], ""]
    for title, items in R["sections"]:
        out.append(f"## {title}")
        for head, sub, date, bullets in items:
            if head: out.append(f"**{head}**" + (f" | {sub}" if sub else "") + (f" | {date}" if date else ""))
            out += [f"- {b}" for b in bullets]
        out.append("")
    return "\n".join(out)
FORMULA = [("Action verb", "Built, designed, reduced, automated, tested, led"), ("What you did", "the technical work, in plain words"), ("How", "the tools or method that matter for the job"), ("Result", "a measured number, or a concrete outcome if you cannot measure")]
WEAK_STRONG = [
 ("Worked on AWS security for a project.", "Designed attribute-based access control for a shared S3 bucket so each tenant reaches only its own data, using tag-matched IAM policies and explicit denies."),
 ("Made a chatbot using AI.", "Built a retrieval-augmented assistant with four prompt-injection defences and cut attack success rate from [A]% to [B]% on [N] held-out attacks."),
 ("Created a backend app with login.", "Built a FastAPI service with JWT login, per-user authorisation and rate limiting, covered by [N] security tests run in CI on every push."),
 ("Good at DSA.", "Solved [N]+ problems on LeetCode and Codeforces; rated [R] on Codeforces."),
]
NUMBERS = [("TenantWall", "number of isolation tests and how many were denied (the test plan in the TenantWall helpers); alert delay measured over several trials"),
           ("AI-security project", "attack success rate before and after defences, false-block rate and answer quality, from the starter's run_attacks.py and run_eval.py with a real model"),
           ("Backend project", "number of tests; requests per second and p95 latency if you load-test it (one of the README's extension ideas)"),
           ("DSA and contests", "problems solved and contest rating, from your profiles on the day you apply")]
CHECK = ["One page. Single column, no tables, text boxes, icons, photos or skill bars: resume filters (ATS) read text top to bottom.",
         "File: PDF exported from Google Docs, Word or LaTeX, named Firstname-Lastname-Resume.pdf. Check that you can select and copy all the text.",
         "Standard headings: Education, Experience (if any), Projects, Skills, Achievements.",
         "Every bullet starts with an action verb and has a result; no 'responsible for' or 'worked on'.",
         "Every number is real and you can explain how you measured it. Leave a bullet without a number rather than invent one.",
         "Every skill listed appears in a project or you can answer three questions on it.",
         "GitHub links work, repositories have a README with results, and no keys or secrets are committed.",
         "Match the job post: reorder skills and projects so the most relevant come first; use the post's exact words where true.",
         "Consistent dates, tense (past for finished work) and punctuation; no spelling mistakes (read it aloud once).",
         "No personal details beyond city, email, phone and links (no photo, date of birth or address).",
         "Ask a senior or a mentor to read it for 30 seconds and tell you what they remember; that is what a recruiter sees.",
         "Keep a master version with everything, and a tailored copy per company."]
def kit_body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{a}">{t}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for t, a in [("One-page template (placeholders)", "tpl"), ("Writing bullets", "bul"), ("Review checklist", "chk")])
    out = [f'''<section class="cover"><p class="eb">PLACEMENTS · RESUME KIT</p><h1>Resume kit<br><span>one page, ATS-safe, honest numbers</span></h1>
<p class="lead">A one-page template with placeholders (fill it in Google Docs or Word from <code>generated/resume/resume-template.md</code> or <code>.html</code>), a formula for strong bullets with examples for TenantWall, the AI-security project and the backend project, and a checklist to run before every application.</p>
<p class="how"><b>The rule.</b> Every number on your resume must be real and you must be able to explain how you measured it. The examples use [brackets] where your measured value goes.</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    out.append(f'<section class="sec tpl" id="tpl"><div class="resume">{resume_html()}</div></section>')
    out.append(f'''<section class="sec" id="bul"><h2>Writing bullets<a class="back" href="#top">↑ Index</a></h2>
<h3>Formula</h3><table class="t"><tbody>{"".join(f"<tr><td class=k>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in FORMULA)}</tbody></table>
<h3>Weak → strong</h3><table class="t"><thead><tr><th>Weak</th><th>Strong</th></tr></thead><tbody>{"".join(f"<tr><td class=w>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in WEAK_STRONG)}</tbody></table>
<h3>Where your numbers come from</h3><table class="t"><tbody>{"".join(f"<tr><td class=k>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in NUMBERS)}</tbody></table>
<p class="meta">Order projects by relevance to the role: for SDE roles put the backend project or TenantWall first; for security roles, TenantWall and the AI-security project. See the <a href="{KB}resume">resume</a> Knowledge Base page.</p></section>''')
    out.append(f'<section class="sec" id="chk"><h2>Review checklist<a class="back" href="#top">↑ Index</a></h2><table class="t"><tbody>{"".join(f"<tr><td class=box>☐</td><td>{E(x)}</td></tr>" for x in CHECK)}</tbody></table></section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 13mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9.2pt/1.5 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } code { font: 600 8pt "JetBrains Mono"; }
h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 18pt; } .lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; }
table { border-collapse: collapse; width: 100%; } .ix td { padding: 2.2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10.5pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } .cover h1, .sec > h2 { font-family: "Space Grotesk"; } .sec > h2 { font-size: 15pt; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2.5mm; display: flex; align-items: baseline; }
.back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; } h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 4mm 0 1.2mm; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.2mm 2mm; text-align: left; } .t td { border-bottom: 1px solid #e2e8f0; padding: 1.8mm 2mm; vertical-align: top; } .k { font-weight: 700; width: 34mm; } .w { color: #b42318; width: 40%; } .box { width: 6mm; color: #94a3b8; }
.meta { color: #475569; font-size: 8.6pt; margin-top: 3mm; } .tpl { padding: 0; } .resume { """ + RCSS.replace("body {", "").split("}", 1)[0] + "} .resume " + " .resume ".join(r + "}" for r in RCSS.split("}", 1)[1].split("}") if r.strip())
js = SRC / "r.js"
def render(pages, name):
    (SRC / "rk.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{kit_body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/rk.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
RES.mkdir(exist_ok=True)
(RES / "resume-template.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><title>Resume template</title><style>@page {{ size: A4; margin: 12mm 13mm; }} {RCSS}</style></head><body>{resume_html()}</body></html>')
(RES / "resume-template.md").write_text(resume_md())
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in ("tpl", "bul", "chk"))
assert d2["bul"] - d2["tpl"] == 1, "the resume template must fit on exactly one page"
text = subprocess.run(["pdftotext", "-f", str(d2["tpl"]), "-l", str(d2["tpl"]), str(SRC / "p2.pdf"), "-"], capture_output=True, text=True).stdout
order = [text.find(h) for h in ("YOUR NAME", "EDUCATION", "PROJECTS", "TenantWall", "Secure RAG", "Study tracker", "SKILLS", "ACHIEVEMENTS")]
assert all(i >= 0 for i in order) and order == sorted(order), f"text order wrong for a parser: {order}"
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for t, k in [("Template", "tpl"), ("Bullets", "bul"), ("Checklist", "chk")]: w.add_outline_item(t, d2[k] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0 or i + 1 == d2["tpl"]: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Resume kit"}); w.write(str(OUT / "resume-kit.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "rk.html"): (SRC / f).unlink()
print(NP, "pages", d2, "template text order ok")
