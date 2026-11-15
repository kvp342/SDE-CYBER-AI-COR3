"""Weekly planner: one printable page per week from Mon 16 Nov 2026 to Sun 30 May 2027, following the plan's dates.
Run from the repo root: python3 generated/src/planner.py"""
import datetime as dt, html, io, pathlib, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
E = html.escape; D = dt.date
START, END = D(2026, 11, 16), D(2027, 5, 30)
assert START.weekday() == 0 and END.weekday() == 6
# Fixed dates from the plan (agent/AGENT.md) and the packs built from it.
EVENTS = {D(2026, 11, 16): "C++ refresh starts (2 days)", D(2026, 11, 18): "Striver A2Z core starts (classic 18 steps)", D(2027, 1, 30): "A2Z core target finish",
          D(2027, 2, 8): "Hard pass starts", D(2027, 2, 13): "OA set 1", D(2027, 2, 27): "OA set 2", D(2027, 3, 13): "OA set 3", D(2027, 3, 21): "TenantWall paper deadline",
          D(2027, 3, 22): "Semester exams start: DSA paused", D(2027, 4, 5): "AWS final revision starts (light during exams)", D(2027, 4, 7): "Exams end",
          D(2027, 4, 8): "Hard pass resumes", D(2027, 4, 19): "AWS SAA-C03 exam week", D(2027, 4, 24): "OA set 4", D(2027, 5, 1): "AI-security project month",
          D(2027, 5, 8): "OA set 5", D(2027, 5, 19): "Hard pass ends", D(2027, 5, 22): "OA set 6", D(2027, 5, 30): "Placement sprint starts tomorrow"}
def phase(d):
    if d < D(2026, 11, 18): return "C++ refresh", "C++ syntax, STL card, 10 easy problems"
    if d <= D(2027, 1, 30): return "Striver A2Z core", "5–6 A2Z problems a day, in sheet order"
    if d < D(2027, 2, 8): return "Buffer and revision", "Redo marked A2Z problems; catch up on anything skipped"
    if D(2027, 3, 22) <= d <= D(2027, 4, 7): return "Semester exams", "Exams first; 30 minutes of revision cards only"
    if d <= D(2027, 5, 19): return "Hard pass", "Hard and medium problems by pattern; redo failures after 3, 7, 21 days"
    return "Hard pass done", "Mixed revision and OA practice"
def side(d):
    s = ["AWS 30 min" if d < D(2027, 4, 19) else "AWS done: review notes once a week"]
    if D(2026, 12, 1) <= d <= D(2027, 3, 21): s.append("TenantWall: build Dec–Jan, test and write Feb–Mar")
    if d >= D(2027, 5, 1): s.append("AI-security project (see its 4-week plan)")
    return s
REVIEW = ["How many problems did I solve, and how many without hints?", "Which pattern was hardest? Which problems go on the redo list?", "Did I keep the AWS and project time?", "What will I do differently next week?"]
weeks = []
d = START
while d <= END:
    days = [d + dt.timedelta(i) for i in range(7)]
    weeks.append((len(weeks) + 1, days, [(x, EVENTS[x]) for x in days if x in EVENTS]))
    d += dt.timedelta(7)
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<a class="w" href="#w{n}"><b>W{n}</b> {days[0].strftime("%d %b")}<span>{E(phase(days[0])[0])}</span><i>{pg(f"w{n}")}</i></a>' for n, days, ev in weeks)
    out = [f'''<section class="cover"><p class="eb">PLAN · WEEKLY PAGES</p><h1>Weekly planner<br><span>16 Nov 2026 – 30 May 2027</span></h1>
<p class="lead">{len(weeks)} weeks, one page each, following the plan's dates: C++ refresh, Striver A2Z core, the Hard pass, the exam break, AWS SAA-C03 in the week of 19 April, the TenantWall deadline on 21 March, the OA practice sets and the May AI-security project. Print a week on Sunday evening, tick the boxes during the week, and answer the review questions at the end.</p>
<div class="grid">{rows}</div></section>''']
    for n, days, ev in weeks:
        ph, goal = phase(days[3])
        evs = "".join(f"<li><b>{x.strftime('%a %d %b')}</b> {E(t)}</li>" for x, t in ev) or "<li>No fixed dates this week.</li>"
        drows = "".join(f'<tr class="{"we" if x.weekday() >= 5 else ""}"><td class="day">{x.strftime("%a")}<br><span>{x.strftime("%d %b")}</span></td><td class="bx">☐ DSA ____ / ____</td><td class="bx">☐ {"Codeforces or contest" if x.weekday() in (1, 3) else ("Weekly review" if x.weekday() == 6 else "Revision cards (15 min)")}</td><td class="bx">{"<br>".join("☐ " + E(s) for s in side(x))}</td><td class="notes"></td></tr>' for x in days)
        out.append(f'''<section class="sec" id="w{n}"><h2><span class="num">WEEK {n}</span>{days[0].strftime("%d %b")} – {days[6].strftime("%d %b %Y")}<a class="back" href="#top">↑ Index</a></h2>
<div class="top"><div><h3>{E(ph)}</h3><p>{E(goal)}</p></div><div><h3>Dates this week</h3><ul>{evs}</ul></div></div>
<table class="days"><thead><tr><th></th><th>DSA (solved / target)</th><th>Habit</th><th>Side tracks</th><th>Notes</th></tr></thead><tbody>{drows}</tbody></table>
<h3>Weekly review</h3><table class="rev"><tbody>{"".join(f"<tr><td>{E(q)}</td><td class=ans></td></tr>" for q in REVIEW)}</tbody></table></section>''')
    return "".join(out)
CSS = """@page { size: A4; margin: 11mm 12mm 13mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.6pt/1.4 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 14mm 14mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; }
h1 { font: 700 30pt/1.02 "Space Grotesk"; margin: 0 0 3mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 18pt; } .lead { font-size: 9.5pt; color: #475569; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.6mm; margin-top: 4mm; } .w { display: flex; gap: 1.5mm; align-items: baseline; border: 1px solid #e2e8f0; border-radius: 5px; padding: 1.3mm 2mm; color: #0f172a; font-size: 8pt; }
.w span { color: #64748b; font-size: 7pt; flex: 1; } .w i { font: 600 7.5pt "JetBrains Mono"; color: #c2410c; font-style: normal; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2.5mm; display: flex; align-items: baseline; gap: 3mm; }
.num { font: 600 9pt "JetBrains Mono"; color: #c2410c; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
h3 { font: 700 10pt "Space Grotesk"; color: #1d4ed8; margin: 2mm 0 1mm; } .top { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; } .top p { margin: 0; } ul { margin: 0; padding-left: 4mm; }
table { border-collapse: collapse; width: 100%; } th { font: 600 6.8pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.2mm 2mm; text-align: left; }
.days td { border: 1px solid #e2e8f0; padding: 1.8mm 2mm; vertical-align: top; height: 25mm; font-size: 8pt; } .days .day { font-weight: 700; width: 14mm; } .days .day span { font: 400 7pt "JetBrains Mono"; color: #64748b; }
.days .notes { width: 46mm; } .days tr.we td { background: #f8fafc; } .rev td { border: 1px solid #e2e8f0; padding: 1.6mm 2mm; height: 9mm; vertical-align: top; } .rev td:first-child { width: 72mm; font-size: 8pt; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "pl.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/pl.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = [f"w{n}" for n, *_ in weeks]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
assert n2 == len(weeks) + 1, f"each week must be exactly one page: {n2} pages for {len(weeks)} weeks"
assert all(START <= x <= END for x in EVENTS), "every fixed date must fall inside the planner"
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for n, days, ev in weeks: w.add_outline_item(f"Week {n}: {days[0].strftime('%d %b')}", d2[f"w{n}"] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Weekly planner 16 Nov 2026 - 30 May 2027"}); w.write(str(OUT / "weekly-planner.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "pl.html"): (SRC / f).unlink()
print(NP, "pages,", len(weeks), "weeks")
