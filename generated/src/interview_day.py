"""Interview day kit: OA-day and interview-day checklists, what to say when stuck, email templates (placeholders only), and an offer
comparison sheet. The example offer figures are computed here, and the CSV template's formulas are evaluated to check they give the
same numbers. Run from the repo root: python3 generated/src/interview_day.py"""
import csv, html, io, pathlib, re, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
E = lambda s: html.escape(str(s), quote=True); KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
OA_DAY = ["Day before: test the platform link, webcam and microphone if proctored; read the instructions email twice (allowed languages, tab switching rules).",
          "Laptop charged and plugged in; stable internet with a phone hotspot as backup; notifications off; desk clear.",
          "Your C++ template typed and tested: fast I/O, long long, common includes (from the STL card).",
          "First 5 minutes: read every problem and its constraints; pick the order (easiest first).",
          "When stuck past your time budget: submit a correct brute force for partial marks and move on.",
          "Before each submit: run the samples plus one edge case (n = 1, all equal, maximum values).",
          "Last 10 minutes: no new problems; make sure every attempted problem has a submission."]
INT_DAY = ["Day before: reread the company file, your resume line by line, and your six story cards; prepare two questions to ask.",
           "Online: quiet room, plain background, camera at eye level, headphones, a notebook and pen; join 5 minutes early.",
           "In person: printed resume, ID, the call letter; arrive 30 minutes early.",
           "Coding round: restate the problem, ask about input size and edge cases, say a brute force and its complexity, then improve, then code, then test aloud.",
           "Design round: requirements first, then estimates, API, data model, diagram, deep dive, trade-offs (system design one-pager).",
           "Behavioural round: STAR, about 2 minutes, 'I' not 'we', a result with a number.",
           "Within an hour after: write down every question asked; send a short thank-you if you have the recruiter's email."]
STUCK = [("You do not understand the problem", "\"Let me restate it to check: … Is that right? Could you walk me through the second example?\""),
         ("No idea where to start", "\"Let me start with a brute force: … that's O(n²). The repeated work is …, so I'm thinking of a hash map to remove it.\""),
         ("Your idea might be wrong", "\"I think this works because …. Let me test it on a small case before coding.\""),
         ("You find a bug", "\"This fails when n = 1 because …. I'll fix the loop bound.\" Interviewers value finding your own bugs."),
         ("Out of time", "\"I won't finish the code, so here's the rest of the approach and its complexity: ….\""),
         ("You do not know a fact", "\"I'm not sure. My understanding is …; I'd confirm it in the documentation.\" Never bluff.")]
EMAILS = [
 ("Referral request (to an alumnus or senior)", "Subject: Referral for [Role] at [Company]\n\nHi [Name],\n\nI'm [Your name], a [year] B.Tech CSE (Cyber Security) student at [College], and I saw that you work on [team or product] at [Company]. I'm applying for [Role] ([job link or ID]).\n\nRelevant work: [one line on TenantWall with a result], [one line on another project], and [DSA or contest result].\n\nWould you be comfortable referring me? My resume is here: [link]. Happy to answer any questions, and thank you for your time either way.\n\nBest,\n[Your name]\n[LinkedIn] · [GitHub]"),
 ("Thank-you after an interview", "Subject: Thank you, [Role] interview on [date]\n\nHi [Interviewer or recruiter name],\n\nThank you for the conversation today about [team or topic]. I enjoyed discussing [one specific thing from the interview], and it made me more interested in the role.\n\n[Optional one line: a short follow-up thought on a question you discussed.]\n\nBest regards,\n[Your name]"),
 ("Follow-up on status (after the promised date)", "Subject: Following up, [Role] application\n\nHi [Recruiter name],\n\nI interviewed for [Role] on [date] and wanted to check whether there is any update on the next steps. I remain very interested in the position.\n\nThank you,\n[Your name]"),
 ("Asking for more time on an offer", "Subject: [Role] offer, timeline\n\nHi [Recruiter name],\n\nThank you for the offer for [Role]; I'm grateful and excited about it. I'm completing one more process that ends on [date]. Would it be possible to share my decision by [date]?\n\nBest regards,\n[Your name]")]
OFFER_ROWS = ["Base salary (annual)", "Joining bonus (one time)", "Performance bonus (annual, target)", "Stocks / RSUs (total grant)", "Vesting years", "Relocation (one time)", "Bond or service agreement (months)", "Notice period (days)", "City", "Role and team"]
EXAMPLE = {"A": dict(base=1800000, joining=200000, bonus_pct=10, rsu=2400000, vest=4), "B": dict(base=2200000, joining=0, bonus_pct=0, rsu=0, vest=1)}
def first_year(o): return o["base"] + o["joining"] + o["base"] * o["bonus_pct"] / 100 + o["rsu"] / o["vest"]
def recurring(o): return o["base"] + o["base"] * o["bonus_pct"] / 100 + o["rsu"] / o["vest"]
FY = {k: first_year(v) for k, v in EXAMPLE.items()}; RE = {k: recurring(v) for k, v in EXAMPLE.items()}
assert FY == {"A": 2780000.0, "B": 2200000.0} and RE == {"A": 2580000.0, "B": 2200000.0}
# CSV template with spreadsheet formulas (works when opened in Google Sheets or Excel); evaluated below to check it.
CSV_ROWS = [["Item", "Offer A", "Offer B", "Notes"],
            ["Base salary (annual)", 1800000, 2200000, "Fixed pay per year"],
            ["Joining bonus (one time)", 200000, 0, "Often repayable if you leave within a year"],
            ["Performance bonus %", 10, 0, "Target, not guaranteed"],
            ["Stocks / RSUs (total grant)", 2400000, 0, "Value at grant; can change"],
            ["Vesting years", 4, 1, "Use 1 if there are no stocks"],
            ["First-year cash + stock", "=B2+B3+B2*B4/100+B5/B6", "=C2+C3+C2*C4/100+C5/C6", "What year one is worth"],
            ["Recurring yearly", "=B2+B2*B4/100+B5/B6", "=C2+C2*C4/100+C5/C6", "Year two onwards, before raises"],
            ["Bond (months)", 0, 0, "Penalty if you leave early"], ["City", "", "", "Rent and cost of living differ a lot"], ["Role and team", "", "", "Learning and growth matter more than a small pay gap"]]
def eval_formula(f, rows):
    def cell(m):
        col, r = m.group(1), int(m.group(2)); return str(rows[r - 1]["ABC".index(col)])
    return eval(re.sub(r"([A-C])(\d+)", cell, f[1:]))
for r, label in ((6, "first"), (7, "recurring")):
    a, b = eval_formula(CSV_ROWS[r][1], CSV_ROWS), eval_formula(CSV_ROWS[r][2], CSV_ROWS)
    want = FY if label == "first" else RE
    assert (a, b) == (want["A"], want["B"]), (label, a, b)
(OUT / "interview-day").mkdir(exist_ok=True)
with open(OUT / "interview-day" / "offer-comparison.csv", "w", newline="") as fh: csv.writer(fh).writerows(CSV_ROWS)
(OUT / "interview-day" / "email-templates.md").write_text("# Email templates (fill the [brackets])\n\n" + "\n\n".join(f"## {t}\n\n```\n{b}\n```" for t, b in EMAILS) + "\n")
inr = lambda x: "₹" + f"{x / 1e5:,.1f}" + " lakh"
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{a}">{t}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for t, a in [("OA day and interview day checklists", "check"), ("What to say when you are stuck", "stuck"), ("Email templates", "mail"), ("Comparing offers", "offer")])
    li = lambda xs: "".join(f"<tr><td class=box>☐</td><td>{E(x)}</td></tr>" for x in xs)
    out = [f'''<section class="cover"><p class="eb">PLACEMENTS · THE DAY ITSELF</p><h1>Interview<br><span>day kit</span></h1>
<p class="lead">Checklists for online-assessment days and interview days, phrases for the moments you get stuck, four email templates (referral request, thank-you, follow-up, more time on an offer), and a way to compare offers fairly. The templates are also in <code>generated/interview-day/email-templates.md</code>; the offer sheet is <code>generated/interview-day/offer-comparison.csv</code> (opens in Google Sheets with its formulas).</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    out.append(f'<section class="sec" id="check"><h2>Checklists<a class="back" href="#top">↑ Index</a></h2><h3>Online assessment day</h3><table class="t">{li(OA_DAY)}</table><h3>Interview day</h3><table class="t">{li(INT_DAY)}</table><p class="meta">See also the <a href="{KB}oa-tactics">OA tactics</a> and <a href="{KB}star">STAR</a> pages, the company files and the mock interview scripts.</p></section>')
    out.append(f'<section class="sec" id="stuck"><h2>What to say when you are stuck<a class="back" href="#top">↑ Index</a></h2><table class="t"><tbody>{"".join(f"<tr><td class=k>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in STUCK)}</tbody></table><p class="meta">Silence is the main thing to avoid: interviewers can only give credit and hints for thinking they can hear.</p></section>')
    out.append(f'<section class="sec" id="mail"><h2>Email templates<a class="back" href="#top">↑ Index</a></h2>{"".join(f"<h3>{E(t)}</h3><pre>{E(b)}</pre>" for t, b in EMAILS)}</section>')
    ex = "".join(f"<tr><td>{E(k)}</td><td class=v>{E(a)}</td><td class=v>{E(b)}</td></tr>" for k, a, b in [
        ("Base salary", inr(EXAMPLE["A"]["base"]), inr(EXAMPLE["B"]["base"])), ("Joining bonus", inr(EXAMPLE["A"]["joining"]), inr(EXAMPLE["B"]["joining"])),
        ("Performance bonus (target)", f'{EXAMPLE["A"]["bonus_pct"]}%', f'{EXAMPLE["B"]["bonus_pct"]}%'), ("Stocks over vesting", f'{inr(EXAMPLE["A"]["rsu"])} over {EXAMPLE["A"]["vest"]} years', "none"),
        ("First-year value", inr(FY["A"]), inr(FY["B"])), ("Recurring yearly value", inr(RE["A"]), inr(RE["B"]))])
    out.append(f'''<section class="sec" id="offer"><h2>Comparing offers<a class="back" href="#top">↑ Index</a></h2>
<p>A "CTC" figure often adds one-time and uncertain parts to fixed pay. Compare offers on two numbers: what year one is worth, and what a normal year after that is worth. Then weigh the parts money does not show.</p>
<h3>What to ask for, item by item</h3><table class="t"><tbody>{"".join(f"<tr><td class=box>☐</td><td>{E(x)}</td></tr>" for x in OFFER_ROWS)}</tbody></table>
<h3>Worked example (made-up numbers)</h3><table class="t ex"><thead><tr><th></th><th>Offer A</th><th>Offer B</th></tr></thead><tbody>{ex}</tbody></table>
<p class="meta">First-year value = base + joining bonus + base × bonus% + stock grant ÷ vesting years. Recurring = the same without the joining bonus. Offer A has the larger "CTC" but part of it is a one-time bonus and stock that may change in value; Offer B is all fixed pay. Neither is automatically better: also weigh the bond, the city's cost of living, the team and what you will learn. These numbers are computed by the build script and match the formulas in the CSV.</p>
<h3>Rules</h3><ul><li>Get the offer in writing, with the breakdown, before deciding.</li><li>Ask politely about any part that is unclear (vesting schedule, bonus conditions, bond terms).</li><li>Do not accept an offer you intend to break; companies and colleges remember.</li><li>Follow your college placement cell's rules on accepting offers (many allow only one).</li></ul></section>''')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 13mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9pt/1.45 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } code { font: 600 7.8pt "JetBrains Mono"; }
h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; } .lead { font-size: 10pt; color: #475569; }
table { border-collapse: collapse; width: 100%; } .ix td { padding: 2.2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10.5pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2.5mm; display: flex; align-items: baseline; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 4mm 0 1.2mm; } th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.2mm 2mm; text-align: left; }
.t td { border-bottom: 1px solid #e2e8f0; padding: 1.6mm 2mm; vertical-align: top; } .box { width: 6mm; color: #94a3b8; } .k { font-weight: 700; width: 46mm; } .v { font: 600 8.5pt "JetBrains Mono"; font-variant-numeric: tabular-nums; }
pre { font: 400 7.8pt/1.45 "JetBrains Mono"; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #1d4ed8; padding: 2.5mm 3mm; white-space: pre-wrap; margin: 0; break-inside: avoid; font-variant-ligatures: none; }
.meta { color: #475569; font-size: 8.4pt; margin: 2mm 0; } ul { padding-left: 5mm; } li { margin-bottom: 1.2mm; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "id.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/id.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = ["check", "stuck", "mail", "offer"]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for t, k in [("Checklists", "check"), ("When stuck", "stuck"), ("Email templates", "mail"), ("Comparing offers", "offer")]: w.add_outline_item(t, d2[k] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Interview day kit"}); w.write(str(OUT / "interview-day-kit.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "id.html"): (SRC / f).unlink()
print(NP, "pages", d2, "first-year", FY, "recurring", RE)
