"""Interview story bank: six STAR story templates (prompts only, no invented stories) mapped to Amazon's Leadership Principles and
Google's hiring attributes, a worksheet, and 25 HR questions with answer outlines. Run from the repo root: python3 generated/src/story_bank.py"""
import html, io, pathlib, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
LPS = ["Customer Obsession", "Ownership", "Invent and Simplify", "Are Right, A Lot", "Learn and Be Curious", "Hire and Develop the Best", "Insist on the Highest Standards", "Think Big",
       "Bias for Action", "Frugality", "Earn Trust", "Dive Deep", "Have Backbone; Disagree and Commit", "Deliver Results", "Strive to be Earth's Best Employer", "Success and Scale Bring Broad Responsibility"]
GOOGLE = [("General cognitive ability", "how you learn and solve problems, not trivia"), ("Leadership", "stepping in to lead when needed and stepping back when someone else should"),
          ("Role-related knowledge", "the skills the job needs"), ("Googleyness", "comfort with ambiguity, bringing something new, intellectual humility, doing the right thing")]
STORIES = [
 ("Proud project", "TenantWall: the problem, your design and how you proved it worked", ["Ownership", "Dive Deep", "Deliver Results", "Insist on the Highest Standards"], ["Role-related knowledge", "General cognitive ability"],
  ["S: What problem did the professor or the project need solved? Why did it matter (shared resources, tenants seeing each other's data)?", "T: What exactly was your part?", "A: The design choices you made (ABAC vs one role per tenant), what you built, the tests you ran. Use 'I'.", "R: Numbers you measured (tests passed, alert delay), the paper's status, what you would change."],
  ["Why ABAC and not RBAC?", "How did you know isolation really worked?", "What broke first?"]),
 ("Failure", "Something that went wrong because of you, and what changed afterwards", ["Learn and Be Curious", "Ownership", "Earn Trust"], ["Googleyness (humility)"],
  ["S: A real setback: a failed test or OA, a bug you shipped, a missed deadline.", "T: What you were responsible for.", "A: What you did when you noticed; how you told others.", "R: The fix, and the habit you have now (for example, testing edge cases before submitting)."],
  ["What would you do differently?", "How did others react?"]),
 ("Disagreement", "You disagreed with a teammate, senior or professor, respectfully, with data", ["Have Backbone; Disagree and Commit", "Earn Trust", "Are Right, A Lot"], ["Leadership", "Googleyness"],
  ["S: The decision being made (tech choice, design, how to split work).", "T: Your view and why.", "A: How you made your case (data, a small prototype), and how you listened.", "R: The outcome; if you lost the argument, how you committed and helped anyway."],
  ["What if you had been wrong?", "How do you handle someone more senior disagreeing?"]),
 ("Learning fast", "You had to learn something new quickly to deliver", ["Learn and Be Curious", "Bias for Action", "Deliver Results"], ["General cognitive ability"],
  ["S: A new tool or subject under time pressure (AWS for TenantWall, C++ STL, FastAPI).", "T: What had to be delivered and by when.", "A: How you learned: docs, small experiments, asking the right person.", "R: What you shipped, and how fast you got productive."],
  ["How do you usually learn a new technology?", "What did you get wrong at first?"]),
 ("Going beyond", "You did more than asked: a security finding, a test suite, automation", ["Insist on the Highest Standards", "Ownership", "Customer Obsession", "Invent and Simplify"], ["Leadership", "Role-related knowledge"],
  ["S: The task as given.", "T: The gap you noticed (missing tests, an injection risk, no alerting).", "A: What you added and why it mattered to the user or the team.", "R: The measurable effect (attacks blocked, bugs caught, time saved)."],
  ["Why did you think it was worth the time?", "How did you prioritise it against your main task?"]),
 ("Helping or leading", "You helped someone grow or led a small group", ["Hire and Develop the Best", "Earn Trust", "Strive to be Earth's Best Employer"], ["Leadership"],
  ["S: A teammate who was stuck, a juniors' session, a club or hackathon team.", "T: Your role.", "A: How you helped (explained, paired, divided work fairly) without taking over.", "R: What they or the team achieved; what you learned about leading."],
  ["How did you handle someone not pulling their weight?", "What would you do differently as a leader?"]),
]
HR = [
 ("Tell me about yourself.", "90 seconds: present (degree, focus), past (two projects with one result each), future (why this role). Not your life story."),
 ("Why this company?", "Two specific reasons from the company's products, engineering blog or values, linked to your own work."),
 ("Why should we hire you?", "Match three of their needs to evidence: DSA, a project result, and how you learn."),
 ("What are your strengths?", "One or two strengths, each with a short example."),
 ("What is your weakness?", "A real but fixable weakness and what you are doing about it (for example, over-polishing; now time-boxing)."),
 ("Where do you see yourself in five years?", "Growing into a strong engineer in this area, owning bigger parts of systems; keep it about skills."),
 ("Why software engineering if your degree is in cyber security?", "Security makes you a better engineer: you build systems that are correct and safe; mention TenantWall and the backend project."),
 ("Are you planning higher studies?", "Honest answer; if not now, say you want industry experience first."),
 ("Are you willing to relocate?", "Answer honestly; if yes, say so simply."),
 ("What are your salary expectations?", "As a fresher: 'I expect the standard package for this role; learning and the work matter most to me.'"),
 ("Do you have other offers?", "Be honest and brief; do not bluff."),
 ("Tell me about a challenge you faced.", "Use story 1 or 4 in STAR form."),
 ("Tell me about a time you failed.", "Story 2."),
 ("Tell me about a conflict in a team.", "Story 3."),
 ("How do you handle pressure and deadlines?", "A real example: how you broke the work down and what you dropped."),
 ("How do you keep learning?", "Your actual routine: problems daily, docs, one project at a time, revision cards."),
 ("Describe your most challenging project.", "Story 1, with the hardest technical decision."),
 ("What do you know about our products?", "Two products and one thing you would like to work on; check recent news the day before."),
 ("How do you prioritise when everything is urgent?", "Impact and deadline first; say what you would ask your manager."),
 ("Have you worked in a team?", "Story 6 or a hackathon; what you owned."),
 ("What motivates you?", "Building things that work and that people use; solving hard problems."),
 ("Explain your project to a non-technical person.", "Practise a 30-second version of TenantWall with an everyday analogy (separate lockers in one room)."),
 ("Why did you choose your college or branch?", "Short and positive; no complaints."),
 ("Is there a gap or low score on your record?", "State it, the reason in one line, and what you did since."),
 ("Do you have any questions for us?", "Always yes: ask about the team's work, how new engineers are onboarded, and what success looks like in six months."),
]
SRCS = [("Amazon: Our Leadership Principles", "https://www.aboutamazon.com/working-at-amazon/our-leadership-principles"), ("Amazon Jobs: Leadership Principles", "https://www.amazon.jobs/content/en/our-workplace/leadership-principles"),
        ("Agile Academy: the 16 Amazon Leadership Principles", "https://www.agile-academy.com/en/agile-leader/amazon-leadership-principles/"),
        ("Business Insider: what Google grades interviewees on", "https://www.businessinsider.in/Heres-Exactly-What-Google-Grades-Interviewees-On-When-Its-Hiring/articleshow/43247184.cms"),
        ("Fast Company: Google's head of HR on hiring", "https://www.fastcompany.com/3044606/googles-head-of-hr-shares-his-hiring-secrets")]
assert len(LPS) == 16 and all(lp in LPS for s in STORIES for lp in s[2]) and len(HR) == 25
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    ix = [("How to use STAR", "star"), ("Six story templates", "stories"), ("Coverage matrix", "matrix"), ("Story worksheet", "sheet"), ("25 HR questions", "hr"), ("Sources", "srcs")]
    rows = "".join(f'<tr><td><a href="#{a}">{t}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for t, a in ix)
    out = [f'''<section class="cover"><p class="eb">INTERVIEWS · BEHAVIOURAL</p><h1>Story bank<br><span>six STAR stories, 25 HR answers</span></h1>
<p class="lead">Six story templates with prompts for you to fill from your own experience, mapped to Amazon's Leadership Principles and the attributes Google says it hires for; a worksheet; and outlines for 25 common HR questions. There are no ready-made stories here on purpose: interviewers ask follow-ups, and only true stories survive them.</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    out.append(f'''<section class="sec" id="star"><h2>How to use STAR<a class="back" href="#top">↑ Index</a></h2><table class="t"><tbody>
<tr><td class=k>Situation</td><td>One or two sentences of context. Time: about 15 seconds.</td></tr><tr><td class=k>Task</td><td>Your responsibility, not the team's. About 10 seconds.</td></tr>
<tr><td class=k>Action</td><td>What you did, step by step, with "I". This is most of the answer: about 60–75 seconds.</td></tr><tr><td class=k>Result</td><td>What happened, with a number if you have one, and what you learned. About 20 seconds.</td></tr></tbody></table>
<ul><li>Two minutes per story. Practise aloud and time yourself.</li><li>Each story should serve two or three principles, so six stories cover a whole interview loop.</li><li>Keep a one-line summary of each story on a card; review the cards before every interview.</li><li>Amazon lists sixteen Leadership Principles; Google describes four hiring attributes. Both are listed with sources at the end.</li></ul>
<h3>Google's four attributes (as reported)</h3><table class="t"><tbody>{"".join(f"<tr><td class=k>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in GOOGLE)}</tbody></table>
<p class="meta">See also the <a href="{KB}star">STAR</a> Knowledge Base page and Mock 8 in the mock kit.</p></section>''')
    st = "".join(f'''<div class="story"><h3>{i + 1}. {E(t)}: <span>{E(d)}</span></h3><p class="map"><b>Amazon:</b> {E(", ".join(lp))} · <b>Google:</b> {E(", ".join(g))}</p>
<ul>{"".join(f"<li>{E(p)}</li>" for p in prompts)}</ul><p class="fu"><b>Follow-ups to prepare:</b> {E(" ".join(fu))}</p></div>''' for i, (t, d, lp, g, prompts, fu) in enumerate(STORIES))
    out.append(f'<section class="sec" id="stories"><h2>Six story templates<a class="back" href="#top">↑ Index</a></h2>{st}</section>')
    head = "".join(f"<th class=v><span>{i + 1}</span></th>" for i in range(6))
    mrows = "".join(f'<tr><td>{E(lp)}</td>{"".join("<td class=c>" + ("●" if lp in s[2] else "") + "</td>" for s in STORIES)}</tr>' for lp in LPS)
    out.append(f'<section class="sec" id="matrix"><h2>Coverage matrix: Amazon Leadership Principles<a class="back" href="#top">↑ Index</a></h2><p class="meta">Columns are the six stories. Every principle with a dot is covered; for the rest, have one extra example ready (for Frugality, a time you did more with less; for Think Big, an idea that went beyond the task; for the last principle, how you weigh the wider impact of what you build).</p><table class="m"><thead><tr><th>Principle</th>{head}</tr></thead><tbody>{mrows}</tbody></table></section>')
    sheet = "".join(f'<div class="ws"><h3>Story {i + 1}: {E(t)}</h3><table class="w"><tbody>{"".join(f"<tr><td class=k>{x}</td><td></td></tr>" for x in ("Situation", "Task", "Action", "Result", "Number", "One-line card"))}</tbody></table></div>' for i, (t, *_r) in enumerate(STORIES))
    out.append(f'<section class="sec" id="sheet"><h2>Story worksheet<a class="back" href="#top">↑ Index</a></h2><div class="sheet">{sheet}</div></section>')
    out.append(f'<section class="sec" id="hr"><h2>25 HR questions<a class="back" href="#top">↑ Index</a></h2><table class="t"><tbody>{"".join(f"<tr><td class=n>{i + 1}</td><td class=q>{E(q)}</td><td>{E(a)}</td></tr>" for i, (q, a) in enumerate(HR))}</tbody></table></section>')
    out.append(f'<section class="sec" id="srcs"><h2>Sources<a class="back" href="#top">↑ Index</a></h2><ul>{"".join(f"<li><a href={chr(34)}{u}{chr(34)}>{E(t)}</a></li>" for t, u in SRCS)}</ul><p class="meta">Principle names follow Amazon\'s published list of sixteen (two were added in 2021). Google\'s four attributes are as described by Google\'s former head of people operations in the articles above; check Google\'s careers site for its current wording.</p></section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 13mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9pt/1.45 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; }
h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 18pt; } .lead { font-size: 10pt; color: #475569; }
table { border-collapse: collapse; width: 100%; } .ix td { padding: 2.2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10.5pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2.5mm; display: flex; align-items: baseline; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
h3 { font: 700 10pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1mm; } h3 span { color: #334155; font: 400 9pt Inter; } ul { padding-left: 5mm; margin: 0; } li { margin-bottom: .8mm; } .meta { color: #475569; font-size: 8.5pt; margin: 2mm 0; }
.t td { border-bottom: 1px solid #e2e8f0; padding: 1.5mm 2mm; vertical-align: top; } .k { font-weight: 700; width: 36mm; } .n { color: #94a3b8; font-family: "JetBrains Mono"; width: 7mm; } .q { font-weight: 600; width: 62mm; }
.story { break-inside: avoid; margin-bottom: 2mm; border-left: 3px solid #1d4ed8; padding-left: 3mm; } .map { margin: 0 0 1mm; font-size: 8.3pt; color: #475569; } .fu { margin: 1mm 0 0; font-size: 8.3pt; color: #475569; }
.m td, .m th { border: 1px solid #e2e8f0; padding: 1.2mm 2mm; } .m th { font: 600 7pt "JetBrains Mono"; background: #f1f5f9; color: #64748b; } .m .c { text-align: center; color: #c2410c; width: 12mm; font-size: 11pt; }
.sheet { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; } .ws h3 { margin-top: 0; } .w td { border: 1px solid #e2e8f0; padding: 1mm 2mm; height: 11mm; vertical-align: top; font-size: 8pt; } .w .k { width: 22mm; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "sb.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/sb.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = ["star", "stories", "matrix", "sheet", "hr", "srcs"]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for t, k in [("STAR", "star"), ("Six stories", "stories"), ("Coverage matrix", "matrix"), ("Worksheet", "sheet"), ("25 HR questions", "hr"), ("Sources", "srcs")]: w.add_outline_item(t, d2[k] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Interview story bank"}); w.write(str(OUT / "interview-story-bank.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "sb.html"): (SRC / f).unlink()
print(NP, "pages", d2)
