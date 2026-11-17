"""Applications tracker and outreach kit: a CSV tracker with spreadsheet formulas (evaluated here to check them), five new
message templates (placeholders only; the interview day kit already has referral, thank-you, follow-up and offer-extension
emails), and a weekly outreach routine. Run from the repo root: python3 generated/src/outreach.py"""
import csv, datetime, html, io, pathlib, re, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; DIR = OUT / "outreach"; DIR.mkdir(exist_ok=True)
E = html.escape
GH = "https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/"

# ---------------- tracker: header, three example rows (fictional), formulas in H (follow-up date) and a summary block
HEAD = ["Company", "Role", "Link", "Applied (YYYY-MM-DD)", "Referral (who)", "Status", "Next action", "Follow up on", "Notes"]
STATUSES = ["Saved", "Applied", "Referred", "OA", "Interview", "Offer", "Rejected", "Withdrawn"]
EX = [["Example Co A", "SDE Intern", "https://example.com/jobs/1", "2027-02-01", "", "Applied", "Ask an alumnus for a referral", "", "Found on careers page"],
      ["Example Co B", "Security Intern", "https://example.com/jobs/2", "2027-02-03", "Alumnus, batch of 2025", "OA", "Do OA by 2027-02-10", "", "OA link came by email"],
      ["Example Co C", "Cloud Intern", "https://example.com/jobs/3", "2027-02-05", "", "Rejected", "Ask for feedback", "", ""]]
rows = [HEAD]
for i, r in enumerate(EX, start=2):
    r = list(r); r[7] = f'=IF(D{i}="","",IF(OR(F{i}="Offer",F{i}="Rejected",F{i}="Withdrawn"),"",DATEVALUE(D{i})+7))'; rows.append(r)
first, last = 2, 200
SUM = [("Applications", f'=COUNTA(A{first}:A{last})'), ("Referred", f'=COUNTIF(F{first}:F{last},"Referred")+COUNTIF(E{first}:E{last},"?*")'),
       ("Reached OA or later", f'=COUNTIF(F{first}:F{last},"OA")+COUNTIF(F{first}:F{last},"Interview")+COUNTIF(F{first}:F{last},"Offer")'),
       ("Interviews", f'=COUNTIF(F{first}:F{last},"Interview")+COUNTIF(F{first}:F{last},"Offer")'), ("Offers", f'=COUNTIF(F{first}:F{last},"Offer")')]
# the summary block sits to the right of the data (columns K:L) in rows 2-6, so it never collides with data rows
while len(rows) < len(SUM) + 1: rows.append([""] * 9)
rows[0] = rows[0] + ["", "Summary", "Count"]
for k, (label, f) in enumerate(SUM): rows[k + 1] = rows[k + 1] + ["", label, f]
buf = io.StringIO(); csv.writer(buf).writerows(rows); (DIR / "applications-tracker.csv").write_text(buf.getvalue())

# evaluate the formulas we used, on the example rows, with a tiny evaluator for exactly these patterns
data = [r[:9] for r in rows[1:4]]
def follow_up(r):
    if not r[3]: return ""
    if r[5] in ("Offer", "Rejected", "Withdrawn"): return ""
    return (datetime.date.fromisoformat(r[3]) + datetime.timedelta(days=7)).isoformat()
got = [follow_up(r) for r in data]
assert got == ["2027-02-08", "2027-02-10", ""], got
col = lambda c: [r["ABCDEFGHI".index(c)] for r in data]
counts = {"Applications": sum(1 for v in col("A") if v), "Referred": col("F").count("Referred") + sum(1 for v in col("E") if v),
          "Reached OA or later": sum(col("F").count(s) for s in ("OA", "Interview", "Offer")), "Interviews": sum(col("F").count(s) for s in ("Interview", "Offer")), "Offers": col("F").count("Offer")}
assert counts == {"Applications": 3, "Referred": 1, "Reached OA or later": 1, "Interviews": 0, "Offers": 0}, counts
back = list(csv.reader(io.StringIO((DIR / "applications-tracker.csv").read_text())))
assert back[0][:9] == HEAD and back[1][7].startswith("=IF(") and all(len(r) in (9, 12) for r in back)
assert all(r[5] in STATUSES for r in EX)

# ---------------- templates (placeholders in [brackets]; nothing personal)
T = [
 ("LinkedIn connection note", "Hi [Name], I'm a [year] B.Tech CSE (Cybersecurity) student preparing for [Company]'s [role] internship. I enjoyed your post on [topic] and would value connecting.", "Short, specific, no request in the first message. Personalise the topic."),
 ("Cold email to a recruiter", "Subject: [Role] internship – [Your name], B.Tech CSE (Cybersecurity), [College], [Year]\n\nHi [Recruiter name],\n\nI applied for the [Role] internship ([job ID or link]) on [date]. I'm a [year] student focusing on backend and cloud security. Two things relevant to the role:\n- [Project 1: one line with a number, e.g. multi-tenant AWS isolation tested with 12 scenarios]\n- [Project 2 or achievement: one line, link]\n\nResume: [link]. GitHub: [link].\nIf the role is filled, I'd be grateful to be considered for similar openings.\n\nThank you,\n[Your name]\n[Phone] · [LinkedIn]", "Always include the job ID. Two proof points, not a life story. One email, one follow-up after a week."),
 ("Asking an alumnus for advice (not a referral)", "Hi [Name], I'm [Your name], a [year] student from [College] (your college too). I'm preparing for SDE internships with a security and cloud focus and saw you moved from [College] to [Company]. Could I ask two quick questions over chat this week?\n1. What mattered most in your [Company] interviews?\n2. Is there a team where security or cloud interns fit well?\nThank you, [Your name]", "Advice first builds the relationship; ask for a referral only after they reply and you have a specific job ID."),
 ("Email to a professor for a research internship", "Subject: Summer research internship – [Your name], B.Tech CSE (Cybersecurity), [College]\n\nDear Prof. [Surname],\n\nI read your [year] paper \"[Title]\" on [topic]. [One sentence on what you understood or a question it raised.]\n\nI'm a [year] student and have built [one project related to their area, with a link], and I'm writing a paper on [your research topic] due in March 2027. I'd like to work in your group in summer 2027, for example through [programme name, e.g. the institute's summer research programme], if that is possible.\n\nCV: [link]. Transcript on request.\n\nThank you for your time,\n[Your name]", "Read the paper first: one real sentence about it is what separates you from mass emails. Apply through the official programme too."),
 ("Status check after an interview or OA", "Subject: [Role] application – status check ([job ID])\n\nHi [Name],\n\nThank you again for the [OA / interview] on [date]. I wanted to check whether there is an update on next steps, and whether you need anything else from me.\n\nBest regards,\n[Your name]", "Send once, about a week after the date they gave (or two weeks if none). Stay polite even after a rejection; ask for feedback."),
]
for t, body, tip in T:
    assert "[" in body and "]" in body, t                              # placeholders only
    assert not re.search(r"\b\d{10}\b|@[a-z0-9-]+\.[a-z]{2,}", body), t     # no phone numbers or real email addresses
(DIR / "outreach-templates.md").write_text("# Outreach templates (fill the [brackets])\n\nThe referral request, thank-you, follow-up and offer-extension emails are in `generated/interview-day/email-templates.md`.\n\n" + "\n\n".join(f"## {t}\n\n```\n{b}\n```\n\n{tip}" for t, b, tip in T) + "\n")

ROUTINE = [("Monday", "Find 10 openings (careers pages, LinkedIn jobs, trackers); add them to the sheet as Saved."),
           ("Tuesday", "Tailor the resume's top 3 bullets for the best 5; apply; status Applied."),
           ("Wednesday", "5 messages: 2 alumni (advice), 2 referral requests with job IDs, 1 recruiter email."),
           ("Thursday", "Follow-ups: everything whose 'Follow up on' date has passed gets one polite message."),
           ("Friday", "Apply to the other 5 saved openings; update statuses."),
           ("Saturday", "OA practice set (the OA packs) or a real OA."),
           ("Sunday", "Review the summary: applications → OA → interviews. If replies are under 10% after 30 applications, fix the resume first (resume kit), not the volume.")]
CSS = """@page { size: A4; margin: 13mm 14mm 15mm; } * { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 9.2pt/1.5 Inter, sans-serif; color: #1e293b; } a { color: #1d4ed8; text-decoration: none; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; } h1 { font: 700 28pt/1.05 "Space Grotesk"; margin: 0 0 3mm; color: #0f172a; } h1 span { color: #c2410c; }
h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; margin: 0 0 2mm; padding-bottom: 1.5mm; border-bottom: 2px solid #c2410c; display: flex; align-items: baseline; } h2 .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; color: #64748b; }
h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1mm; } section.sec { break-before: page; } table { border-collapse: collapse; width: 100%; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.2mm 2mm; text-align: left; } td { border-bottom: 1px solid #e2e8f0; padding: 1.3mm 2mm; vertical-align: top; } td.pg { text-align: right; font-family: "JetBrains Mono"; }
pre { font: 400 7.8pt/1.45 "JetBrains Mono"; background: #f8fafc; border-left: 3px solid #1d4ed8; padding: 2mm 3mm; white-space: pre-wrap; margin: 1mm 0; font-variant-ligatures: none; } code { font: 600 7.8pt "JetBrains Mono"; }
.tip { font-size: 8.5pt; color: #475569; margin: 0 0 3mm; } .note { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; margin: 3mm 0; font-size: 8.6pt; }"""
PARTS = [("tracker", "The applications tracker"), ("templates", "Five outreach templates"), ("routine", "The weekly routine")]
def body(pages):
    pg = lambda k: str(pages.get(k, "00")) if pages else "00"
    ix = "".join(f'<tr><td><a href="#{i}">{n + 1}. {E(t)}</a></td><td class="pg"><a href="#{i}">{pg(i)}</a></td></tr>' for n, (i, t) in enumerate(PARTS))
    cols = "".join(f"<tr><td><code>{E(h)}</code></td><td>{E(d)}</td></tr>" for h, d in zip(HEAD, ["Company name", "Exact role title", "Job posting link (keep it: postings disappear)", "Date you applied", "Who referred you, if anyone", "One of: " + ", ".join(STATUSES), "The single next step, with a date", "Formula: applied date + 7 days, blank once the application is closed", "Anything useful: recruiter name, OA platform, questions asked"]))
    sums = "".join(f"<tr><td>{E(l)}</td><td><code>{E(f)}</code></td></tr>" for l, f in SUM)
    return "".join([f'''<section><p class="eb">APPLICATIONS · TRACKER AND OUTREACH</p><h1>Track every application<br><span>and every message</span></h1>
<p>A spreadsheet that tells you who to follow up with and how your funnel is doing, five message templates the interview day kit does not have, and a weekly routine that keeps applications and outreach moving from February 2027.</p>
<table><thead><tr><th>Part</th><th class="pg">Page</th></tr></thead><tbody>{ix}</tbody></table>
<p class="note">Files: <a href="{GH}generated/outreach/applications-tracker.csv">generated/outreach/applications-tracker.csv</a> (import into Google Sheets: File → Import → Upload; formulas work there and in Excel) and <a href="{GH}generated/outreach/outreach-templates.md">generated/outreach/outreach-templates.md</a>. The three example rows are fictional; delete them when you start.</p></section>''',
      f'<section class="sec" id="tracker"><h2>The applications tracker<a class="back" href="#top">↑ Index</a></h2><table><thead><tr><th>Column</th><th>What goes in it</th></tr></thead><tbody>{cols}</tbody></table><h3>Summary block (columns K–L)</h3><table><thead><tr><th>Metric</th><th>Formula</th></tr></thead><tbody>{sums}</tbody></table><p class="note">Checked: on the three example rows the follow-up dates come out as 8 Feb and 10 Feb (and blank for the rejected one), and the summary counts 3 applications, 1 referral, 1 at OA or later. Format column H as a date (Format → Number → Date) so the formula shows a date rather than a serial number. Sort by "Follow up on" every Thursday. Use Data → Data validation on column F with the status list so spelling stays consistent (the counts depend on it).</p></section>',
      f'<section class="sec" id="templates"><h2>Five outreach templates<a class="back" href="#top">↑ Index</a></h2><p class="tip">Fill every [bracket]; send nothing with a bracket left in. The referral request, thank-you, follow-up and offer-extension emails are in the interview day kit.</p>' + "".join(f"<h3>{E(t)}</h3><pre>{E(b)}</pre><p class='tip'>{E(tip)}</p>" for t, b, tip in T) + "</section>",
      f'<section class="sec" id="routine"><h2>The weekly routine<a class="back" href="#top">↑ Index</a></h2><table><thead><tr><th>Day</th><th>About 45 minutes</th></tr></thead><tbody>' + "".join(f"<tr><td><b>{d}</b></td><td>{E(x)}</td></tr>" for d, x in ROUTINE) + '</tbody></table><p class="note">Ten applications and five messages a week, as in the final plan. Quality beats volume: a tailored application with a referral and a job ID is worth more than twenty one-click applies.</p></section>'])
js = SRC / "rout.js"
def render(pages, name):
    (SRC / "outreach.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/outreach.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "x1.pdf"); d2, n2 = render(d1, "x2.pdf"); assert n1 == n2 and d1 == d2
w = PdfWriter(clone_from=PdfReader(str(SRC / "x2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for i, t in PARTS: w.add_outline_item(t, d2[i] - 1, fit=Fit.fit())
NP = len(w.pages)
for k, pg in enumerate(w.pages):
    if k == 0: continue
    b = io.BytesIO(); cv = canvas.Canvas(b, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
    cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{k + 1} / {NP}"); cv.save(); b.seek(0); pg.merge_page(PdfReader(b).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Applications tracker and outreach kit"}); w.write(str(OUT / "applications-outreach-kit.pdf"))
for f in ("x1.pdf", "x2.pdf", "rout.js", "outreach.html"): (SRC / f).unlink()
print(NP, "pages", d2)
