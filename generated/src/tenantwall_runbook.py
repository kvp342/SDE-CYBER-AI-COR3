"""TenantWall one-day runbook: the professor's five changes, the paper updates and the demo. Run from the repo root: python3 generated/src/tenantwall_runbook.py"""
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

SEC = []
def sec(id, title, body): SEC.append((id, title, body))
D = lambda url, label: S(url, label)
EVAL = ("https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html", "AWS IAM: policy evaluation logic (explicit vs implicit deny)")
SIM = ("https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html", "AWS IAM: testing policies with the IAM policy simulator")
DEC = ("https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html", "AWS STS: DecodeAuthorizationMessage")
GEN = ("https://awspolicygen.s3.amazonaws.com/policygen.html", "AWS Policy Generator")
AA = ("https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html", "IAM Access Analyzer policy validation")
CTD = ("https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html", "AWS CloudTrail: logging data events")
CTW = ("https://docs.aws.amazon.com/awscloudtrail/latest/userguide/send-cloudtrail-events-to-cloudwatch-logs.html", "AWS CloudTrail: sending events to CloudWatch Logs")
ALM = ("https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html", "AWS CloudTrail: CloudWatch alarms for CloudTrail events")
ICO = ("https://aws.amazon.com/architecture/icons/", "AWS Architecture Icons (official)")
CW = ("https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html", "CloudWatch Logs Insights query syntax")
RB = "generated/tenantwall/runbook/"

sec("plan", "Tomorrow at a glance", "<p>Your professor's five requests, done in one day in an order where each step feeds the next. Times are working time; take the breaks.</p>" +
 T(["Time", "Step", "Done when"], [
  ["0:00–0:20", "Before you start (Section 2)", "Signed in as your admin IAM user, right region, budget alert on"],
  ["0:20–1:05", "<b>1. Explicit vs implicit deny</b> (Section 3)", "Simulator screenshots for both kinds; test table has a deny-type column"],
  ["1:05–1:50", "<b>2. Policy Generator + Access Analyzer</b> (Section 4)", "Bucket policy regenerated; all three policies validate with no errors"],
  ["1:50–2:35", "<b>3. CloudTrail with S3 data events</b> (Section 5)", "Trail logging; refused GetObject visible in CloudWatch Logs"],
  ["Break", "", ""],
  ["2:50–3:50", "<b>4. CloudWatch alarms + email</b> (Section 6)", "Both alarms fired and the emails arrived"],
  ["3:50–4:50", "<b>5. Architecture diagram + flowchart</b> (Section 7)", "Two diagrams exported as PNG"],
  ["4:50–5:30", "Update the paper (Section 8)", "New subsections and test-table column written"],
  ["5:30–6:00", "Rehearse the demo (Section 9)", "You can show everything in 10 minutes"]]) +
 '<p class="note"><b>Names used here are your real ones:</b> tag key <code>Team</code>, policies <code>TenantABAC_EC2</code> and <code>TenantABAC_S3</code>, the bucket policy with <code>DenyNonTLS</code> and one prefix Deny per team, and <code>tenantwall_tests.py</code> (14 tests). The sample JSON in ' + K("generated/tenantwall/policies/", "generated/tenantwall/policies/") + ' uses a lowercase <code>tenant</code> placeholder: do not paste those over your working policies.</p>')

sec("before", "Before you start (20 minutes)", UL([
 "<b>Sign in as your admin IAM user</b>, not the root user. Check the region at the top right is the one your TenantWall resources are in.",
 "<b>Budget alert:</b> if you have none, Billing → Budgets → Create budget → monthly cost budget, 1 USD, your email. Data events and logs cost a little; this catches surprises.",
 "<b>Re-run your tests first:</b> <code>python3 tenantwall_tests.py</code> should still show 14 of 14 passing. If not, fix that before adding anything.",
 "<b>Make a screenshots folder</b> and name files as in Section 9 (S1, S2 …) so the paper and the demo use the same evidence.",
 "<b>Write down:</b> account ID, region, bucket name, one user from team A (call it USER_A) and one from team B, an object key under team B's prefix, and your email for alerts.",
 "<b>Optional, for the CLI appendix:</b> AWS CLI v2 configured with your admin profile (<code>aws sts get-caller-identity</code> shows your admin user)."]))

sec("deny", "Step 1: explicit vs implicit deny (45 minutes)", "<p><b>The idea in one line:</b> an <i>explicit deny</i> is a Deny statement that matches the request; it wins over every Allow. An <i>implicit deny</i> is the default when no Allow matches at all. Both refuse the request, but for different reasons, and the paper should show which one stopped each attack." + D(*EVAL) + "</p>" +
 "<h3>Show both kinds in the IAM policy simulator</h3><ol>" +
 "<li>IAM → Policy simulator (or open the simulator from the user's page). Choose <b>USER_A</b>.</li>" +
 "<li><b>Explicit deny:</b> service S3, action <code>GetObject</code>, resource <code>arn:aws:s3:::BUCKET/TEAM_B/…</code> with the bucket policy included. Expect <i>denied</i>, matched by your per-team prefix Deny. Screenshot <b>S1</b>.</li>" +
 "<li><b>Explicit deny (identity side):</b> IAM <code>TagUser</code> on USER_A itself: matched by <code>NoSelfPromotion</code>. Screenshot <b>S2</b>.</li>" +
 "<li><b>Implicit deny:</b> an action none of your policies allows, for example EC2 <code>CreateVpc</code>. Expect <i>denied</i> with no matching statement. Screenshot <b>S3</b>.</li></ol>" + S(*SIM) +
 "<h3>Confirm from a real refusal</h3><p>When an EC2 call is refused, the error carries an encoded message. Decode it as admin: <code>aws sts decode-authorization-message --encoded-message …</code>. The decoded JSON says whether the request was allowed, whether it was an <code>explicitDeny</code>, and which statements matched." + D(*DEC) + " Screenshot <b>S4</b>.</p>" +
 "<h3>Add a column to your test table</h3>" + T(["Test", "Expected", "Result", "Deny type", "Stopped by"], [
  ["Team A reads team B's object", "Refused", "Refused", "Explicit", "Bucket policy prefix Deny"],
  ["Team A tags itself into team B", "Refused", "Refused", "Explicit", "NoSelfPromotion"],
  ["Team A creates a VPC", "Refused", "Refused", "Implicit", "No Allow matched"],
  ["Team A reads own object", "Allowed", "Allowed", "—", "TenantABAC_S3 Allow"]]) +
 '<p class="note">Fill the real rows from your 14 tests; the four above are examples of each kind. <b>Ask your professor</b> (Section 9) whether "something explicit" meant exactly this, as your notes say to confirm.</p>')

sec("aa", "Step 2: Policy Generator and Access Analyzer (45 minutes)", "<ol>" +
 "<li>Open the <b>AWS Policy Generator</b>" + D(*GEN) + ". Type: <i>S3 Bucket Policy</i>.</li>" +
 "<li>Add the <code>DenyNonTLS</code> statement: Effect Deny, Principal <code>*</code>, Actions <i>All Actions</i>, ARN of the bucket and <code>bucket/*</code>, condition <i>Bool</i> <code>aws:SecureTransport</code> = <code>false</code>.</li>" +
 "<li>Add one statement per team: Effect Deny, the object actions, ARN <code>bucket/TEAM_X/*</code>, and the condition that excludes that team and your admin ARN, exactly as in your current bucket policy.</li>" +
 "<li>Generate the JSON. Compare it with your current bucket policy line by line; the generator may order keys differently but the meaning must be the same. Screenshot the generator page <b>S5</b>.</li>" +
 "<li>S3 → bucket → Permissions → Bucket policy → Edit → paste. The editor runs <b>IAM Access Analyzer policy checks</b> automatically" + D(*AA) + ": fix any <i>errors</i> and <i>security warnings</i>, then save. Screenshot the clean checks <b>S6</b>.</li>" +
 "<li>Open <code>TenantABAC_EC2</code> and <code>TenantABAC_S3</code> in IAM → Policies → Edit (JSON) and read the Access Analyzer findings panel for each. Screenshot <b>S7</b>. Do not save changes you do not understand.</li>" +
 "<li>Re-run <code>tenantwall_tests.py</code>: still 14 of 14.</li></ol>" +
 '<p class="note">Sentence for the paper: "The bucket policy was produced with the AWS Policy Generator and, with both identity policies, validated by IAM Access Analyzer, which reported no errors or security warnings."</p>')

sec("trail", "Step 3: CloudTrail with S3 data events (45 minutes)", "<p>Event history only keeps management events. Object reads such as <code>GetObject</code> are <b>data events</b>, which are recorded only by a trail that asks for them." + D(*CTD) + "</p><ol>" +
 "<li>CloudTrail → Trails → <b>Create trail</b>. Name <code>tenantwall-trail</code>. Storage: a <b>new</b> S3 bucket for logs (separate from the tenant bucket).</li>" +
 "<li><b>CloudWatch Logs: Enabled</b>, new log group <code>/tenantwall/cloudtrail</code>, <b>new IAM role</b> (the console creates the role CloudTrail needs to write logs)." + D(*CTW) + "</li>" +
 "<li>Events: Management events on (Read and Write). <b>Data events on</b>: S3, limited to <b>your tenant bucket only</b> (not all buckets: that costs more and adds noise).</li>" +
 "<li>Create. Check the trail shows <i>Logging: On</i>. Screenshot the trail settings <b>S8</b>.</li>" +
 "<li>Wait 5 minutes, then re-run <code>tenantwall_tests.py</code> so refused calls happen while the trail records.</li>" +
 "<li>CloudWatch → Logs Insights → log group <code>/tenantwall/cloudtrail</code> → paste the query below → Run. You should see the refused <code>GetObject</code> with USER_A's ARN, team B's key and <code>AccessDenied</code>. Screenshot <b>S9</b>." + D(*CW) + "</li></ol><pre>" + E(open(ROOT / RB / "insights-query.txt").read().strip()) + "</pre>" +
 '<p class="note">Records reach CloudWatch Logs after a delay, often a few minutes. If nothing shows after 15 minutes, see Section 10.</p>')

sec("alarm", "Step 4: CloudWatch alarms and email (60 minutes)", "<ol>" +
 "<li><b>SNS:</b> SNS → Topics → Create topic (Standard) <code>tenantwall-alerts</code> → Create subscription → Email → your address. <b>Open the email and click Confirm subscription</b>, or no alert will ever arrive.</li>" +
 "<li><b>Metric filter 1 (refused calls):</b> CloudWatch → Log groups → <code>/tenantwall/cloudtrail</code> → Metric filters → Create. Pattern below. Namespace <code>TenantWall</code>, metric <code>AccessDeniedCount</code>, value 1, default 0." + D(*ALM) + "</li>" +
 "<li><b>Metric filter 2 (tag tampering):</b> same log group, second pattern below, metric <code>TagChangeCount</code>.</li>" +
 "<li><b>Alarm 1:</b> on <code>AccessDeniedCount</code>, statistic Sum, period 5 minutes, <b>≥ 3</b> (your professor's threshold), missing data = not breaching, action: notify <code>tenantwall-alerts</code>.</li>" +
 "<li><b>Alarm 2:</b> on <code>TagChangeCount</code>, Sum over 5 minutes, <b>≥ 1</b>, same topic.</li>" +
 "<li><b>Trigger them:</b> as USER_A, try three or more refused reads of team B's objects; then, as admin, add and remove a test tag on a spare instance. Wait up to about 15 minutes.</li>" +
 "<li>Screenshot both alarms in <i>In alarm</i> state <b>S10</b> and the two emails <b>S11</b>.</li></ol>" +
 "<h3>Filter patterns (checked syntax; also in the runbook folder)</h3><pre>" + E("Refused calls:\n" + open(ROOT / RB / "filter-denied.txt").read().strip() + "\n\nTag tampering:\n" + open(ROOT / RB / "filter-tags.txt").read().strip()) + "</pre>" +
 '<p class="note">Sentence for the paper: TenantWall now <b>prevents</b> cross-team access (policies) and <b>detects</b> attempts (CloudTrail → CloudWatch metric filter → alarm → email within minutes).</p>')

sec("diagrams", "Step 5: architecture diagram and flowchart (60 minutes)", UL([
 "Open <a href='https://app.diagrams.net'>draw.io (diagrams.net)</a> → More Shapes → enable the <b>AWS</b> shape library (it contains the official AWS architecture icons" + D(*ICO) + ").",
 "<b>Architecture diagram:</b> the AWS account as a big box; inside it IAM (users tagged Team=A / Team=B, the Tenants group, the two identity policies), the S3 bucket with team prefixes and its bucket policy, EC2 instances tagged by team, and the new path CloudTrail → S3 log bucket and CloudWatch Logs → metric filters → alarms → SNS → email. Draw allowed paths in green, refused ones in red.",
 "<b>Method flowchart:</b> request → does an explicit Deny match? (yes → refused, explicit) → does an Allow match with Team equal to the resource's team or prefix? (no → refused, implicit; yes → allowed) → in every case CloudTrail records it → refused calls counted → alarm.",
 "Use " + K("generated/tenantwall/architecture.png", "architecture.png") + " and " + K("generated/tenantwall/flowchart.png", "flowchart.png") + " as a starting sketch, but redraw them with the official icons, since that is what your professor asked for.",
 "Export both as PNG at 300 DPI (File → Export as → PNG → zoom 300%) and save the .drawio files too: <b>S12</b>, <b>S13</b>."]))

sec("paper", "Step 6: update the paper (40 minutes)", T(["Where", "Add"], [
 ["Abstract and introduction", "TenantWall now prevents and detects: one sentence on CloudTrail data events and CloudWatch alarms."],
 ["Design", "The architecture diagram (S12); a paragraph on explicit versus implicit deny with the evaluation-logic citation."],
 ["Implementation", "Policy Generator and Access Analyzer validation (S5–S7); the trail settings (S8); the two metric filters and alarms."],
 ["Evaluation", "The test table with the new deny-type column; the refused GetObject record (S9); alarm and email evidence (S10–S11) with the measured delay from the refused call to the email."],
 ["Method", "The flowchart (S13)."],
 ["Limitations", "Alerts arrive after a delay of minutes; data events add cost; per-team prefix Deny statements grow the bucket policy."]]) +
 '<p class="note">The paper outline (' + K("generated/tenantwall-paper-outline.pdf", "tenantwall-paper-outline.pdf") + ') and the LaTeX skeleton (' + K("generated/tenantwall/paper/main.tex", "main.tex") + ') already have places for these.</p>')

sec("demo", "Showing it to your professor (10 minutes)", T(["Minute", "Show", "Say"], [
 ["0–1", "Architecture diagram (S12)", "\"Teams share one account; one tag-based policy set isolates them, and the new path on the right detects attempts.\""],
 ["1–3", "Test table with the deny-type column; simulator S1–S3", "\"Each refusal is now labelled explicit or implicit. Is this what you meant by 'something explicit'?\""],
 ["3–4", "Policy Generator S5 and Access Analyzer S6–S7", "\"The bucket policy came from the Policy Generator and all policies validate with no errors.\""],
 ["4–6", "Run one refused read live; show the Logs Insights result (S9)", "\"The trail records object reads, so the refused GetObject is visible with who, what and when.\""],
 ["6–8", "Alarm in ALARM state and the email (S10–S11)", "\"Three refusals in five minutes, or any tag change, email the admin within minutes.\""],
 ["8–10", "Flowchart (S13); next steps", "\"Next: paper update by 12 Dec, then choose a venue and submit before 21 March. Which venue would you suggest?\""]]) +
 "<h3>Evidence checklist</h3>" + T(["#", "Screenshot"], [[f"S{i}", t] for i, t in enumerate(["Simulator: explicit deny, bucket policy", "Simulator: explicit deny, NoSelfPromotion", "Simulator: implicit deny", "Decoded EC2 authorization message", "Policy Generator", "Bucket policy with clean Access Analyzer checks", "Identity policies' Access Analyzer findings", "Trail settings (data events, CloudWatch Logs)", "Logs Insights: refused GetObject", "Both alarms in ALARM", "Alert emails", "Architecture diagram (official icons)", "Method flowchart"], 1)]) +
 '<p class="note">If live AWS is slow in his office, show the screenshots: they are the same evidence. Keep the trail and alarms running until after the meeting.</p>')

sec("trouble", "If something goes wrong, costs and cleanup", T(["Problem", "Fix"], [
 ["No alert email", "Did you confirm the SNS subscription? Check the alarm's History tab and that its action points at the topic."],
 ["Nothing in CloudWatch Logs", "Trail must show Logging: On with CloudWatch Logs enabled; same region; wait 10–15 minutes; check the trail's role was created."],
 ["No GetObject records", "Data events must be on for your tenant bucket (and the right bucket ARN); management events alone never show object reads."],
 ["Alarm never leaves INSUFFICIENT_DATA", "No matching records yet: trigger refused calls again; default value 0 on the metric filter helps."],
 ["Access Analyzer errors after pasting", "Do not save; compare with your old policy. Keep the old JSON in a text file before editing."],
 ["Tests start failing", "Undo the last policy change from your saved copy, re-run the tests, then change one statement at a time."]]) +
 UL(["<b>Cost:</b> the first copy of management events is free; S3 data events, CloudWatch Logs storage and alarms are billed in small amounts. For a demo week this is usually a few rupees, and the budget alert covers you.",
     "<b>After the paper evidence is captured:</b> stop logging or delete the trail, delete the alarms, metric filters, log group, SNS topic and the trail's log bucket (empty it first). Keep the screenshots and the .drawio files.",
     "<b>CLI versions</b> of every step are in " + K(RB + "cli_commands.txt", "runbook/cli_commands.txt") + " (18 commands, checked against the AWS service models and the AWS CLI's own parser)."]))
# ------------------------------------------------------------------ build
for p in USED: assert (ROOT / p.rstrip("/")).exists(), p        # every kit link points at a real file
CSS = """@page { size: A4; margin: 13mm 14mm 15mm; } * { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 9.2pt/1.5 Inter, sans-serif; color: #1e293b; } a { color: #1d4ed8; text-decoration: none; } a.kit { font: 600 7.8pt "JetBrains Mono"; color: #0f766e; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; } h1 { font: 700 30pt/1.05 "Space Grotesk"; margin: 0 0 3mm; color: #0f172a; } h1 span { color: #c2410c; }
h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; margin: 0 0 3mm; padding-bottom: 1.5mm; border-bottom: 2px solid #c2410c; display: flex; align-items: baseline; }
h2 .num { color: #c2410c; margin-right: 3mm; } h2 .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; color: #64748b; } h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1.5mm; }
section.sec { break-before: page; } table { border-collapse: collapse; width: 100%; margin: 1mm 0 2mm; break-inside: auto; } tr { break-inside: avoid; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; letter-spacing: .05em; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
td { border-bottom: 1px solid #e2e8f0; padding: 1.4mm 2mm; vertical-align: top; } table.km td:first-child { width: 45%; } ul { padding-left: 5mm; margin: 1mm 0; } li { margin-bottom: 1.6mm; }
.note { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; margin: 3mm 0; font-size: 8.6pt; } .lead { font-size: 10.5pt; } sup a { font: 600 6.5pt "JetBrains Mono"; color: #c2410c; }
table.ix td { padding: 1.6mm 2mm; } td.pg { text-align: right; font-family: "JetBrains Mono"; width: 14mm; } ol.src { font-size: 7.8pt; padding-left: 6mm; } ol.src li { margin-bottom: 1mm; word-break: break-all; }"""
def body(pages):
    pg = lambda k: str(pages.get(k, "00")) if pages else "00"
    ix = "".join(f'<tr><td><a href="#{i}">{n + 1}. {E(t)}</a></td><td class="pg"><a href="#{i}">{pg(i)}</a></td></tr>' for n, (i, t, _) in enumerate(SEC))
    ix += f'<tr><td><a href="#src">Sources ({len(SOURCES)})</a></td><td class="pg"><a href="#src">{pg("src")}</a></td></tr>'
    out = [f'''<section><p class="eb">TENANTWALL · ONE-DAY RUNBOOK</p><h1>Your professor's five changes<br><span>done in one day</span></h1>
<p class="lead">Everything to finish TenantWall's requested changes tomorrow and show them: (1) explicit vs implicit deny, (2) Policy Generator and Access Analyzer, (3) CloudTrail with S3 data events, (4) CloudWatch alarms with email, (5) an AWS-style architecture diagram and a method flowchart. Then the paper changes, a 10-minute demo script, the screenshots to take, and fixes for what usually goes wrong.</p>
<table class="ix"><thead><tr><th>Section</th><th class="pg">Page</th></tr></thead><tbody>{ix}</tbody></table>
<p class="note">Work in the order of the sections; each step produces evidence the next one uses. Files: <code>generated/tenantwall/runbook/</code> (CLI commands, filter patterns, Logs Insights query).</p></section>''']
    for n, (i, t, b) in enumerate(SEC):
        out.append(f'<section class="sec" id="{i}"><h2><span class="num">{n + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2>{b}</section>')
    out.append('<section class="sec" id="src"><h2><span class="num">··</span>Sources<a class="back" href="#top">↑ Index</a></h2><p>Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.</p><ol class="src">'
               + "".join(f'<li><a href="{u}">{E(l)}</a><br>{E(u)}</li>' for u, l in SOURCES) + "</ol></section>")
    return "".join(out)
js = SRC / "rtwr.js"
def render(pages, name):
    (SRC / "twrunbook.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/twrunbook.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "t1.pdf"); d2, n2 = render(d1, "t2.pdf"); assert n1 == n2 and all(d1[i] == d2[i] for i, _, _ in SEC)
w = PdfWriter(clone_from=PdfReader(str(SRC / "t2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for n, (i, t, _) in enumerate(SEC): w.add_outline_item(f"{n + 1}. {t}", d2[i] - 1, fit=Fit.fit())
w.add_outline_item("Sources", d2["src"] - 1, fit=Fit.fit())
NP = len(w.pages)
for k, pg in enumerate(w.pages):
    if k == 0: continue
    buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
    cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{k + 1} / {NP}"); cv.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "TenantWall one-day runbook"}); w.write(str(OUT / "tenantwall-one-day-runbook.pdf"))
for f in ("t1.pdf", "t2.pdf", "rtwr.js", "twrunbook.html"): (SRC / f).unlink()
print(NP, "pages;", len(USED), "kit links;", len(SOURCES), "sources;", d2)
