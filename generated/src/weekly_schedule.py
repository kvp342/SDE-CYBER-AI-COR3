"""Week-by-week schedule, 16 Nov 2026 – 28 Feb 2027: A2Z steps and Core CS/cyber topics from the Playbook data, cloud at 1 h a day, Saturday cyber, contests; plus the 19 Nov cloud day. Run: python3 generated/src/weekly_schedule.py"""
import html, io, pathlib, re, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
GH = "https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/"
TREE = "https://github.com/kvp342/intrusion-detection-and-prevention/tree/ccr-ca7232a7-t7lq94/"
E = html.escape
USED = set()
def K(path, label=None):
    """Link to a kit file; every path is checked to exist before the PDF is built."""
    USED.add(path)
    url = (TREE + path.rstrip("/")) if path.endswith("/") else GH + path
    return f'<a class="kit" href="{url}">{E(label or path.replace("generated/", ""))}</a>'
def L(url, label): return f'<a href="{url}">{E(label)}</a>'
SOURCES = []
def S(url, label):
    """Cite an outside source: numbered in the Sources section."""
    if (url, label) not in SOURCES: SOURCES.append((url, label))
    n = SOURCES.index((url, label)) + 1
    return f'<sup><a href="#src">[{n}]</a></sup>'
def T(head, rows, cls=""):
    return f'<table class="{cls}"><thead><tr>{"".join(f"<th>{h}</th>" for h in head)}</tr></thead><tbody>' + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>"
def UL(items): return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

import json, datetime as _dt
SEC = []
def sec(id, title, body): SEC.append((id, title, body))
_h = (ROOT / "playbook.html").read_text(encoding="utf-8")
PB = json.loads(_h[_h.index("\nvar D=") + 7: _h.index("};", _h.index("\nvar D=")) + 1])
COD = "https://codolio.com/question-tracker/sheet/strivers-a2z-dsa-sheet"
CLOUD = [(_dt.date(2026, 11, 20), "Storage (S3 classes, lifecycle, encryption, FSx, Backup)"), (_dt.date(2026, 12, 4), "Databases (RDS, Aurora, DynamoDB, caching)"),
         (_dt.date(2026, 12, 18), "Resilience and scaling (ELB, Auto Scaling, Route 53, DR)"), (_dt.date(2027, 1, 1), "Decoupling and serverless (SQS, SNS, Lambda, API Gateway)"),
         (_dt.date(2027, 1, 15), "Security and monitoring (KMS, WAF, GuardDuty, CloudTrail)"), (_dt.date(2027, 1, 29), "Performance and cost (CloudFront, analytics, pricing)"),
         (_dt.date(2027, 2, 12), "Exam practice (study-pack questions, mocks)"), (_dt.date(2027, 2, 26), "Book the AWS exam if 80%+; revise weak areas")]
def cloud_for(d):
    t = CLOUD[0][1]
    for s, n in CLOUD:
        if d >= s: t = n
    return t
rows = []
mon = _dt.date(2026, 11, 16)
while mon <= _dt.date(2027, 2, 22):
    days = [mon + _dt.timedelta(days=i) for i in range(7)]
    steps, cs, cy, n = [], [], [], 0
    for d in days:
        v = PB.get(d.isoformat(), {})
        for s in v.get("steps", []):
            if s not in steps: steps.append(s)
        n += len(v.get("due", []))
        if v.get("cs"):
            t = f'{v["cs"][0]}: {v["cs"][2][0]}'
            if t not in cs: cs.append(t)
        if v.get("cy") and v["cy"][1] not in cy: cy.append(v["cy"][1])
    sun = days[-1]
    dsa = ("Steps " + ", ".join(f"{a} ({E(b)})" for a, b in steps) + f": about {n} problems") if steps else f"A2Z done: LeetCode + Codeforces practice (hard pass){'; ' + str(n) + ' redo problems' if n else ''}"
    if mon == _dt.date(2026, 11, 16): dsa = "C++ refresh; from Fri 20 Nov: " + dsa
    contest = "LeetCode contest Sun 8:00" if sun >= _dt.date(2026, 12, 6) else "—"
    cyber = ("Sat 2 h: " if mon < _dt.date(2027, 2, 1) else "Daily 1–1.5 h: ") + E(", ".join(cy))
    cl = "Thu 19 Nov: long cloud day (weeks 0–3)" if mon == _dt.date(2026, 11, 16) else E(cloud_for(mon + _dt.timedelta(days=3))) + (" → " + E(cloud_for(mon + _dt.timedelta(days=4))).split(" (")[0] + " from Fri" if cloud_for(mon + _dt.timedelta(days=3)) != cloud_for(mon + _dt.timedelta(days=4)) else "")
    rows.append([f'{mon.strftime("%d %b")} – {sun.strftime("%d %b")}', dsa, E(" · ".join(cs)), cl, cyber, contest])
    mon += _dt.timedelta(days=7)

sec("how", "How to use this (read once)", UL([
 "<b>One row per week.</b> Look at this week's row on Monday; that is all you need to plan the week.",
 "<b>Exact problems for today:</b> open the Playbook (playbook.html, Today tab) or continue on " + L(COD, "Codolio") + S(COD, "Codolio: Striver A2Z DSA sheet tracker") + " from the first unticked problem. This table only says which A2Z steps the week should finish.",
 "<b>Every day:</b> DSA 3–4 h (A2Z problems + 1–2 LeetCode on the same topic), Cloud 1 h, Core CS 1 h, Anki 15 min.",
 "<b>Behind?</b> Never double up on weekdays. Use Sunday afternoon to catch up, and if a week slips, slide the rest; the 30 Jan A2Z checkpoint can move by a week without harm.",
 "<b>Cyber:</b> Saturdays 2 h until A2Z is done, then daily from February. The topic column comes from the Playbook's cyber track.",
 "<b>Deadlines and contests</b> are also in your Google Calendar. LeetCode weekly contests run on Sundays at 8:00 am IST." + S("https://leetcode.com/contest/", "LeetCode contests")]))

sec("tomorrow", "Thursday 19 Nov: the long cloud day", T(["Time", "Block", "Topic (cloud plan weeks)", "Done when you can…"], [
 ["9:00 – 11:00", "1", "Start-up (W0): account security, exam guide, global infrastructure, shared responsibility, CLI", "Explain Region vs AZ vs edge location, and who secures what"],
 ["11:15 – 1:15", "2", "IAM (W1): users, groups, roles, policies, evaluation, Organizations and SCPs", "Explain explicit deny vs implicit deny, and why EC2 uses a role, not keys"],
 ["2:15 – 4:15", "3", "Compute (W2): EC2 families, pricing options, EBS vs instance store vs EFS, Lambda", "Pick On-Demand, Spot, Savings Plans or RI for 4 situations"],
 ["4:30 – 6:30", "4", "Networking (W3): VPC, subnets, route tables, IGW, NAT, SG vs NACL, endpoints", "Draw a VPC with public and private subnets and a NAT gateway"],
 ["7:30 – 8:30", "5 (optional)", "Storage start (W4): S3 basics and storage classes", "Name each S3 class and when to use it"],
 ["9:00 – 10:00", "DSA", "1 hour of Striver (first problems of Step 1)", "Tick them on Codolio"]]) +
 '<p class="note">Each block: 50 min course or Skill Builder video, 50 min hands-on or 5 practice questions from the SAA-C03 study pack, 20 min recall from memory. You already know IAM well from TenantWall, so block 2 will feel easy: use the spare time on practice questions. Skip block 5 if you are tired.</p>')

sec("weeks", "Week by week, 16 Nov 2026 – 28 Feb 2027", T(["Week", "DSA (A2Z steps)", "Core CS (1 h/day)", "Cloud (1 h/day)", "Cyber", "Contest"], rows, "wk"))

sec("after", "After February", UL([
 "<b>March:</b> AWS exam (early March if ready), TenantWall paper by 21 March, hard DSA pass, Codeforces 1400 target, applications.",
 "<b>22 Mar – 7 Apr:</b> college exams: Anki only.",
 "<b>May:</b> AI-security project (generated/ai-security-starter/).",
 "<b>31 May – 31 Jul:</b> placement sprint: mocks, OA sets, applying. <b>Aug onwards:</b> placements.",
 "The final plan and the one-page overview hold the full detail for these months."]))
# ------------------------------------------------------------------ build
for p in USED: assert (ROOT / p.rstrip("/")).exists(), p        # every kit link points at a real file
CSS = """@page { size: A4; margin: 13mm 14mm 15mm; } * { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 9.2pt/1.5 Inter, sans-serif; color: #1e293b; } a { color: #1d4ed8; text-decoration: none; } a.kit { font: 600 7.8pt "JetBrains Mono"; color: #0f766e; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; } h1 { font: 700 30pt/1.05 "Space Grotesk"; margin: 0 0 3mm; color: #0f172a; } h1 span { color: #c2410c; }
h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; margin: 0 0 3mm; padding-bottom: 1.5mm; border-bottom: 2px solid #c2410c; display: flex; align-items: baseline; }
h2 .num { color: #c2410c; margin-right: 3mm; } h2 .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; color: #64748b; } h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1.5mm; }
section.sec { break-before: page; } table { border-collapse: collapse; width: 100%; margin: 1mm 0 2mm; break-inside: auto; } tr { break-inside: avoid; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; letter-spacing: .05em; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
table.wk td { font-size: 7.6pt; padding: 1.1mm 1.4mm; } table.wk td:first-child { white-space: nowrap; font-weight: 600; } td { border-bottom: 1px solid #e2e8f0; padding: 1.4mm 2mm; vertical-align: top; } table.km td:first-child { width: 45%; } ul { padding-left: 5mm; margin: 1mm 0; } li { margin-bottom: 1.6mm; }
.note { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; margin: 3mm 0; font-size: 8.6pt; } .lead { font-size: 10.5pt; } sup a { font: 600 6.5pt "JetBrains Mono"; color: #c2410c; }
table.ix td { padding: 1.6mm 2mm; } td.pg { text-align: right; font-family: "JetBrains Mono"; width: 14mm; } ol.src { font-size: 7.8pt; padding-left: 6mm; } ol.src li { margin-bottom: 1mm; word-break: break-all; }"""
def body(pages):
    pg = lambda k: str(pages.get(k, "00")) if pages else "00"
    ix = "".join(f'<tr><td><a href="#{i}">{n + 1}. {E(t)}</a></td><td class="pg"><a href="#{i}">{pg(i)}</a></td></tr>' for n, (i, t, _) in enumerate(SEC))
    ix += f'<tr><td><a href="#src">Sources ({len(SOURCES)})</a></td><td class="pg"><a href="#src">{pg("src")}</a></td></tr>'
    out = [f'''<section><p class="eb">YOUR ROUTINE · WEEK BY WEEK</p><h1>What to do<br><span>each week until March</span></h1>
<p class="lead">One row per week from 16 November to 28 February: which Striver A2Z steps to finish, the Core CS topic, the cloud topic at 1 hour a day, the Saturday cyber lab and the LeetCode contest. Plus an hour-by-hour plan for the long cloud day on 19 November.</p>
<table class="ix"><thead><tr><th>Section</th><th class="pg">Page</th></tr></thead><tbody>{ix}</tbody></table>
<p class="note">The A2Z, Core CS and cyber columns are summarised from the Playbook's daily data, so they always agree with the Today tab.</p></section>''']
    for n, (i, t, b) in enumerate(SEC):
        out.append(f'<section class="sec" id="{i}"><h2><span class="num">{n + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2>{b}</section>')
    out.append('<section class="sec" id="src"><h2><span class="num">··</span>Sources<a class="back" href="#top">↑ Index</a></h2><p>Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.</p><ol class="src">'
               + "".join(f'<li><a href="{u}">{E(l)}</a><br>{E(u)}</li>' for u, l in SOURCES) + "</ol></section>")
    return "".join(out)
js = SRC / "rws.js"
def render(pages, name):
    (SRC / "wsched.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/wsched.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "w1.pdf"); d2, n2 = render(d1, "w2.pdf"); assert n1 == n2 and all(d1[i] == d2[i] for i, _, _ in SEC)
w = PdfWriter(clone_from=PdfReader(str(SRC / "w2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for n, (i, t, _) in enumerate(SEC): w.add_outline_item(f"{n + 1}. {t}", d2[i] - 1, fit=Fit.fit())
w.add_outline_item("Sources", d2["src"] - 1, fit=Fit.fit())
NP = len(w.pages)
for k, pg in enumerate(w.pages):
    if k == 0: continue
    buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
    cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{k + 1} / {NP}"); cv.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "What to do each week"}); w.write(str(OUT / "weekly-schedule.pdf"))
for f in ("w1.pdf", "w2.pdf", "rws.js", "wsched.html"): (SRC / f).unlink()
print(NP, "pages;", len(USED), "kit links;", len(SOURCES), "sources;", d2)
