"""Profile kit: LinkedIn headline and About templates (length-checked against LinkedIn's limits), a GitHub profile README template,
project pinning and description guide, and a 4-week posting plan. Placeholders only. Run from the repo root: python3 generated/src/profile_kit.py"""
import html, io, pathlib, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; PRO = OUT / "profile"
E = lambda s: html.escape(str(s), quote=True)
HEADLINE_MAX, ABOUT_MAX = 220, 2600          # LinkedIn's limits for the headline and About section
HEADLINES = [
 "CSE (Cyber Security) student, class of 2028 | C++, DSA, AWS | Building secure cloud and backend systems | TenantWall: tenant isolation on AWS",
 "Aspiring SDE | Cloud security research (AWS IAM, ABAC) | C++ · Python · FastAPI | Open to SDE and security internships",
 "B.Tech CSE (Cyber Security) '28 | Prompt-injection defences for RAG | Backend APIs | AWS Solutions Architect – Associate [after you pass]",
]
ABOUT = """I'm a third-year B.Tech student in Computer Science (Cyber Security) who likes building systems that are correct and hard to break.

What I'm working on:
• TenantWall: research on tenant isolation in AWS using attribute-based access control, with CloudTrail and CloudWatch alerting on denied access. [one result, e.g. N cross-tenant tests, all denied]
• A RAG assistant with layered prompt-injection defences, measured on held-out attacks. [attack success rate before → after]
• A study-tracker REST API (FastAPI, JWT, tests in CI). [link]

Skills: C++ (STL), Python, SQL, AWS (IAM, S3, EC2, CloudTrail), FastAPI, Linux, Git, OWASP Top 10.

I practise DSA daily ([N]+ problems; Codeforces [rating]) and write up CTF and PortSwigger labs on GitHub.

Looking for: software engineering and security internships and new-grad roles from [month year]. Happy to talk about cloud security, backend systems or competitive programming.

GitHub: github.com/your-handle · Email: your.email@example.com"""
GH_README = """# Hi, I'm [Your Name]

B.Tech CSE (Cyber Security), class of 2028. I build secure backend and cloud systems and practise DSA in C++.

### Projects
| Project | What it is | Stack |
|---|---|---|
| [TenantWall](https://github.com/your-handle/tenantwall) | Tenant isolation on AWS with ABAC, plus alerting on denied access | AWS IAM, S3, EC2, CloudTrail, CloudWatch |
| [secrag](https://github.com/your-handle/secrag) | RAG assistant with layered prompt-injection defences and an attack suite | Python, Claude API |
| [study-tracker](https://github.com/your-handle/study-tracker) | REST API with JWT, per-user authorisation and security tests in CI | FastAPI, SQLite, GitHub Actions |

### Now
- Solving [N]+ DSA problems; Codeforces: [handle]
- Preparing for AWS Solutions Architect – Associate
- Writing up PortSwigger and CTF labs in [security-notes](https://github.com/your-handle/security-notes)

### Contact
[LinkedIn](https://linkedin.com/in/your-handle) · your.email@example.com
"""
PIN = [("Pin 4 to 6 repositories", "GitHub lets you pin up to six. Pin your best three projects first, then write-ups and a DSA solutions repo."),
       ("Profile README", "Create a public repository with exactly your username as its name; its README.md appears at the top of your profile."),
       ("Each project README", "First screen: one sentence on what it does, a screenshot or diagram, how to run it in three commands, results with numbers, and what you would do next."),
       ("Repository description", "One line under 100 characters with the main technology: 'Tenant isolation on AWS using ABAC IAM policies and CloudTrail alerting'."),
       ("Topics", "Add 3 to 5 topics (aws, iam, security, fastapi, cpp) so recruiters' searches find the repository."),
       ("Hygiene", "No keys or .env files committed (add a .gitignore first); delete empty or tutorial repositories or make them private; commit regularly in small steps.")]
LINKEDIN_TIPS = ["Photo: clear face, plain background. Banner: optional; a simple one with your focus area is enough.",
                 "Headline: what you are, what you build, one proof point. Stay under 220 characters.",
                 "About: first two lines are shown before 'see more', so put your focus and best project there.",
                 "Featured: add the TenantWall diagram, the paper (when public) and the project repositories.",
                 "Experience and projects: the same bullets as your resume, with links.",
                 "Skills: 10 to 15 real ones; put the five most relevant at the top.",
                 "Open to work: set it to recruiters only if you prefer; list the roles and cities you want."]
PLAN = [
 ("Week 1", "Set up", ["Update photo, headline, About, skills and links (templates on the next pages)", "Create the GitHub profile README and pin repositories", "Connect with classmates, seniors and alumni at your target companies (with a one-line note)"]),
 ("Week 2", "Show work", ["Post 1: what TenantWall is and why tenant isolation matters, with the architecture diagram", "Comment thoughtfully on 3 posts from engineers in your area", "Push one PortSwigger or CTF write-up to GitHub"]),
 ("Week 3", "Teach something", ["Post 2: one thing you learned (for example how IAM evaluates an explicit deny) in 5 short lines", "Ask two seniors for 15-minute calls about their teams' hiring", "Add a README with results to your backend project"]),
 ("Week 4", "Result and ask", ["Post 3: a result (an attack success rate, a contest rating, a passed certification) and what you will do next", "Message alumni at three target companies for referral advice, with your resume link", "Review: which posts got responses? Keep the format that worked, one post every two weeks after this"]),
]
POST_RULES = ["Short: 5 to 10 lines, one idea, one image or diagram.", "Specific: numbers and what you learned, not 'excited to share'.", "Honest: no inflated claims; tag people only if they were involved.", "No confidential details from internships or the professor's unpublished work."]
assert all(len(h) <= HEADLINE_MAX for h in HEADLINES), [len(h) for h in HEADLINES]
assert len(ABOUT) <= ABOUT_MAX, len(ABOUT)
PRO.mkdir(exist_ok=True)
(PRO / "github-profile-README.md").write_text(GH_README)
(PRO / "linkedin.md").write_text("# LinkedIn templates\n\n## Headlines (pick one, under 220 characters)\n" + "".join(f"- {h} ({len(h)} characters)\n" for h in HEADLINES) + f"\n## About ({len(ABOUT)} of 2600 characters)\n\n{ABOUT}\n")
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    ix = [("LinkedIn", "li"), ("GitHub profile and projects", "gh"), ("4-week posting plan", "plan")]
    rows = "".join(f'<tr><td><a href="#{a}">{t}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for t, a in ix)
    out = [f'''<section class="cover"><p class="eb">PLACEMENTS · PROFILE KIT</p><h1>Profile kit<br><span>LinkedIn, GitHub, a 4-week plan</span></h1>
<p class="lead">Recruiters and interviewers look at your LinkedIn and GitHub before they talk to you. This kit gives you templates (placeholders only), what to pin and how to describe projects, and a four-week plan to make the profiles active. Copy the text from <code>generated/profile/linkedin.md</code> and <code>generated/profile/github-profile-README.md</code>.</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    out.append(f'''<section class="sec" id="li"><h2>LinkedIn<a class="back" href="#top">↑ Index</a></h2><h3>Checklist</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in LINKEDIN_TIPS)}</ul>
<h3>Headline options</h3><table class="t"><tbody>{"".join(f"<tr><td>{E(h)}</td><td class=c>{len(h)} / 220</td></tr>" for h in HEADLINES)}</tbody></table>
<h3>About template ({len(ABOUT)} of 2,600 characters)</h3><pre>{E(ABOUT)}</pre></section>''')
    out.append(f'''<section class="sec" id="gh"><h2>GitHub profile and projects<a class="back" href="#top">↑ Index</a></h2><table class="t"><tbody>{"".join(f"<tr><td class=k>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in PIN)}</tbody></table>
<h3>Profile README template</h3><pre>{E(GH_README)}</pre></section>''')
    plan = "".join(f'<div class="wk"><h3>{E(w)}: {E(t)}</h3><ul>{"".join(f"<li>☐ {E(x)}</li>" for x in items)}</ul></div>' for w, t, items in PLAN)
    out.append(f'<section class="sec" id="plan"><h2>4-week posting plan<a class="back" href="#top">↑ Index</a></h2><p class="meta">Start any time; a good moment is after the first TenantWall results (January) or the AWS exam (April). About 30 minutes a week.</p>{plan}<h3>Rules for posts</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in POST_RULES)}</ul></section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 13mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9.2pt/1.5 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } code { font: 600 8pt "JetBrains Mono"; }
h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 18pt; } .lead { font-size: 10pt; color: #475569; }
table { border-collapse: collapse; width: 100%; } .ix td { padding: 2.2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10.5pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2.5mm; display: flex; align-items: baseline; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 3.5mm 0 1.2mm; } ul { padding-left: 5mm; margin: 0; } li { margin-bottom: 1mm; } .t td { border-bottom: 1px solid #e2e8f0; padding: 1.6mm 2mm; vertical-align: top; } .k { font-weight: 700; width: 40mm; } .c { width: 20mm; text-align: right; font: 600 7.5pt "JetBrains Mono"; color: #166534; }
pre { font: 400 7.8pt/1.45 "JetBrains Mono"; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #1d4ed8; padding: 2.5mm 3mm; white-space: pre-wrap; font-variant-ligatures: none; } .wk { border-left: 3px solid #1d4ed8; padding-left: 3mm; margin-bottom: 2mm; } .wk h3 { margin-top: 1mm; } .meta { color: #475569; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "pk.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/pk.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in ("li", "gh", "plan"))
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for t, k in [("LinkedIn", "li"), ("GitHub", "gh"), ("Posting plan", "plan")]: w.add_outline_item(t, d2[k] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Profile kit"}); w.write(str(OUT / "profile-kit.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "pk.html"): (SRC / f).unlink()
print(NP, "pages", d2, "headline lengths", [len(h) for h in HEADLINES], "about", len(ABOUT))
