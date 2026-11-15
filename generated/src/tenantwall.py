"""TenantWall helpers: architecture diagram and method flowchart (SVG + PNG) and a PDF summary.
Run from the repo root: python3 generated/tenantwall/check_policies.py && python3 generated/src/tenantwall.py"""
import html, json, subprocess, pathlib, io
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; TW = OUT / "tenantwall"
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
DOC = "https://docs.aws.amazon.com/"
FONT = "font-family='Inter, Arial, sans-serif'"
C = dict(ink="#0f172a", mute="#64748b", sec="#dd344c", mgmt="#e7157b", stor="#3f8624", comp="#ed7100", app="#8c4fff", ok="#16a34a", no="#dc2626", line="#334155")
def box(x, y, w, h, title, sub="", col=C["ink"], fill="#ffffff"):
    t = f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='8' fill='{fill}' stroke='{col}' stroke-width='2'/><rect x='{x}' y='{y}' width='{w}' height='6' rx='3' fill='{col}'/>"
    t += f"<text x='{x + w / 2}' y='{y + 26}' text-anchor='middle' {FONT} font-size='14' font-weight='700' fill='{C['ink']}'>{E(title)}</text>"
    for i, s in enumerate(sub.split("|") if sub else []):
        t += f"<text x='{x + w / 2}' y='{y + 45 + i * 16}' text-anchor='middle' {FONT} font-size='11.5' fill='{C['mute']}'>{E(s)}</text>"
    return t
def arrow(x1, y1, x2, y2, col=C["line"], dash=False, label="", lx=None, ly=None):
    d = " stroke-dasharray='6 5'" if dash else ""
    t = f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='2'{d} marker-end='url(#m{col[1:]})'/>"
    if label: t += f"<text x='{lx if lx is not None else (x1 + x2) / 2}' y='{ly if ly is not None else (y1 + y2) / 2 - 6}' text-anchor='middle' {FONT} font-size='11' font-weight='600' fill='{col}'>{E(label)}</text>"
    return t
def svg(w, h, body):
    marks = "".join(f"<marker id='m{c[1:]}' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='{c}'/></marker>" for c in set(C.values()))
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}'><defs>{marks}</defs><rect width='{w}' height='{h}' fill='#ffffff'/>{body}</svg>"
def architecture():
    b = f"<rect x='250' y='20' width='830' height='600' rx='10' fill='#f8fafc' stroke='#94a3b8' stroke-width='1.5' stroke-dasharray='8 6'/>"
    b += f"<text x='266' y='44' {FONT} font-size='13' font-weight='700' fill='{C['mute']}'>AWS account · Region ap-south-1</text>"
    b += box(20, 120, 200, 78, "Tenant A principal", "IAM role|tag tenant = tenant-a", C["app"]) + box(20, 300, 200, 78, "Tenant B principal", "IAM role|tag tenant = tenant-b", C["app"])
    b += box(300, 175, 230, 150, "IAM policy evaluation", "ABAC allow: resource matches|${aws:PrincipalTag/tenant}|Explicit deny: other tenants,|tag changes, HTTP (bucket policy)", C["sec"])
    b += box(620, 70, 430, 110, "S3 bucket tenantwall-data", "prefix tenant-a/  ·  prefix tenant-b/|Block Public Access on, SSE-KMS or SSE-S3|bucket policy: deny aws:SecureTransport = false", C["stor"])
    b += box(620, 215, 430, 90, "EC2 instances", "i-… tag tenant = tenant-a|i-… tag tenant = tenant-b", C["comp"])
    b += box(300, 410, 190, 92, "CloudTrail trail", "management events|+ S3 data events", C["mgmt"]) + box(540, 410, 190, 92, "CloudWatch Logs", "log group|/tenantwall/cloudtrail", C["mgmt"])
    b += box(780, 410, 270, 92, "Metric filter + alarm", "errorCode AccessDenied* or|*UnauthorizedOperation · Sum ≥ 1 / 5 min", C["mgmt"])
    b += box(780, 530, 125, 70, "SNS topic", "tenantwall-alerts", C["app"]) + box(925, 530, 125, 70, "Email", "security owner", C["ink"])
    b += box(300, 530, 190, 70, "S3 log bucket", "trail files (retained)", C["stor"])
    b += arrow(220, 159, 298, 220, C["ok"], label="request", lx=236, ly=206) + arrow(220, 339, 298, 290, C["line"], label="request", lx=236, ly=296)
    b += arrow(530, 205, 618, 125, C["ok"], label="allow: own prefix", lx=556, ly=126) + arrow(530, 240, 618, 255, C["ok"], label="allow: own tag", lx=575, ly=238)
    b += arrow(530, 300, 618, 290, C["no"], True, "deny: other tenant", 566, 322)
    b += arrow(415, 325, 400, 408, C["line"], label="every API call", lx=448, ly=372)
    b += arrow(490, 456, 538, 456) + arrow(730, 456, 778, 456) + arrow(915, 502, 860, 528) + arrow(905, 565, 923, 565) + arrow(395, 502, 395, 528)
    b += f"<text x='20' y='470' {FONT} font-size='12' font-weight='700' fill='{C['ink']}'>Legend</text>"
    for i, (c, t) in enumerate([(C["ok"], "allowed path"), (C["no"], "denied path (logged)"), (C["line"], "logging / alert flow")]):
        b += f"<line x1='20' y1='{490 + i * 22}' x2='60' y2='{490 + i * 22}' stroke='{c}' stroke-width='2'{' stroke-dasharray=\"6 5\"' if c == C['no'] else ''}/><text x='68' y='{494 + i * 22}' {FONT} font-size='11.5' fill='{C['ink']}'>{t}</text>"
    return svg(1100, 640, b)
def diamond(cx, cy, w, h, text):
    t = f"<polygon points='{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}' fill='#fff7ed' stroke='{C['comp']}' stroke-width='2'/>"
    for i, s in enumerate(text.split("|")): t += f"<text x='{cx}' y='{cy - 4 + i * 15 - (len(text.split('|')) - 1) * 6}' text-anchor='middle' {FONT} font-size='12' font-weight='600' fill='{C['ink']}'>{E(s)}</text>"
    return t
def flowchart():
    b = box(330, 15, 300, 60, "Tenant principal sends API request", "S3 or EC2, signed with role credentials", C["app"])
    b += arrow(480, 75, 480, 103) + diamond(480, 160, 300, 110, "Explicit Deny matches?|(other tenant, tag change, HTTP)")
    b += arrow(630, 160, 728, 160, C["no"], label="yes") + box(730, 120, 220, 80, "AccessDenied", "explicit deny wins", C["no"])
    b += arrow(480, 215, 480, 248, label="no", lx=496, ly=236) + diamond(480, 305, 300, 110, "Allow matches with|resource tag or prefix = principal tag?")
    b += arrow(330, 305, 232, 305, C["ok"], label="yes") + box(10, 265, 220, 80, "Access granted", "own tenant's data only", C["ok"])
    b += arrow(630, 305, 728, 305, C["no"], label="no") + box(730, 265, 220, 80, "AccessDenied", "implicit deny (default)", C["no"])
    b += arrow(120, 345, 120, 430) + arrow(840, 345, 840, 375) + f"<polyline points='950,160 990,160 990,405' fill='none' stroke='{C['no']}' stroke-width='2'/>" + arrow(990, 405, 952, 405, C["no"])
    b += box(560, 375, 390, 60, "CloudTrail records event with errorCode", "delivered to CloudWatch Logs", C["mgmt"])
    b += box(10, 432, 220, 60, "CloudTrail records event", "audit evidence", C["mgmt"])
    b += arrow(755, 435, 755, 463) + diamond(755, 520, 300, 110, "Metric filter count|≥ 1 in 5 minutes?")
    b += arrow(605, 520, 520, 520, label="yes") + box(290, 490, 230, 60, "Alarm → SNS → email", "within minutes", C["app"])
    b += arrow(405, 550, 405, 578) + box(290, 580, 230, 60, "Investigate and record", "who, what, source IP, time", C["ink"])
    b += arrow(905, 520, 960, 520, label="no", lx=932, ly=512) + f"<text x='965' y='524' {FONT} font-size='11.5' fill='{C['mute']}'>keep watching</text>"
    return svg(1060, 660, b)
TW.mkdir(exist_ok=True)
(TW / "architecture.svg").write_text(architecture()); (TW / "flowchart.svg").write_text(flowchart())
js = SRC / "r.js"
js.write_text("""const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 2 });
for (const n of ['architecture', 'flowchart']) { await p.goto('file://' + process.argv[2] + '/' + n + '.svg'); const s = await p.$('svg'); await s.screenshot({ path: process.argv[2] + '/' + n + '.png' }); }
await b.close(); })();""")
subprocess.run(["node", str(js), str(TW)], check=True)
POL = [("tenant-abac-identity.json", "Identity policy attached to every tenant role. Grants access only where the object prefix or the instance's tenant tag equals the caller's own tenant tag. One policy serves all tenants: adding a tenant means adding a tagged role, not a new policy."),
       ("tenant-explicit-deny.json", "Explicit denies that hold even if someone later attaches a broad allow: other tenants' objects and instances, changing the tenant tag on instances or principals, and object or bucket tagging."),
       ("bucket-policy-secure-transport.json", "Bucket policy on the data bucket that refuses any request not made over TLS."),
       ("cloudtrail-bucket-policy.json", "Bucket policy that lets CloudTrail write log files to the log bucket, limited to this trail by aws:SourceArn."),
       ("data-event-selectors.json", "Event selectors that add S3 object-level (data) events for the TenantWall bucket only, so GetObject and PutObject calls are logged without paying for every bucket.")]
TESTS = [("Tenant A reads own object", "Allow", "Object returned"), ("Tenant A reads tenant B's object", "AccessDenied (explicit)", "CLI error, CloudTrail event, alarm email"),
         ("Tenant A writes into tenant-b/", "AccessDenied (explicit)", "Same as above"), ("Tenant A lists tenant-b/ prefix", "AccessDenied (implicit)", "CLI error, CloudTrail event"),
         ("Tenant A stops tenant B's instance", "UnauthorizedOperation", "CloudTrail event, alarm email"), ("Tenant A re-tags an instance to tenant-b", "UnauthorizedOperation", "Tag unchanged"),
         ("Tenant A changes its own tenant tag", "AccessDenied", "Tag unchanged"), ("Plain HTTP request to the bucket", "AccessDenied", "Request refused"),
         ("No denied calls for 5 minutes", "Alarm returns to OK", "Alarm history")]
CHECK = ["State the threat model: a tenant (or a stolen tenant credential) trying to read, change or re-tag another tenant's resources.",
         "Show the trail configuration: multi-Region or single-Region, management events, S3 data events limited to the TenantWall bucket, log file validation on.",
         "Explain where logs go and how long they are kept (S3 log bucket retention, CloudWatch Logs retention period).",
         "Give the exact metric filter pattern and why it covers both S3 (AccessDenied) and EC2 (UnauthorizedOperation) errors.",
         "Give the alarm settings: statistic, period, threshold, evaluation periods, missing-data treatment, SNS action. Justify the threshold (one denied call is already suspicious in a tenant-isolated design).",
         "Report measured detection latency: time from the denied call to the email, over several trials (CloudTrail delivery adds minutes; say so).",
         "Include evidence: CLI output of each denied test, the CloudTrail event JSON (redact the account id), the metric graph and the alarm email screenshot.",
         "Discuss false positives (for example a misconfigured script) and how to tune: per-tenant dimensions, higher threshold, or an EventBridge rule for specific events.",
         "Discuss limits: tags as a trust anchor, eventual consistency of IAM changes, CloudTrail delivery delay, cost of data events.",
         "Name the checks used on the policies: IAM Access Analyzer policy validation and the IAM policy simulator, plus the offline check script in the repository.",
         "Map the design to standards in one line each: least privilege, defence in depth (explicit deny plus bucket policy), and OWASP A09 logging and monitoring.",
         "List cleanup steps so readers do not leave billable resources running."]
SRCS = [("ABAC in IAM", DOC + "IAM/latest/UserGuide/introduction_attribute-based-access-control.html"), ("Policy evaluation logic", DOC + "IAM/latest/UserGuide/reference_policies_evaluation-logic.html"),
        ("CloudTrail data events", DOC + "awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html"), ("Sending CloudTrail events to CloudWatch Logs", DOC + "awscloudtrail/latest/userguide/send-cloudtrail-events-to-cloudwatch-logs.html"),
        ("CloudWatch alarms for CloudTrail", DOC + "awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html"), ("Metric filter pattern syntax", DOC + "AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html"),
        ("S3 bucket policy for CloudTrail", DOC + "awscloudtrail/latest/userguide/create-s3-bucket-policy-for-cloudtrail.html"), ("Access Analyzer policy validation", DOC + "IAM/latest/UserGuide/access-analyzer-policy-validation.html"),
        ("Testing policies with the IAM policy simulator", DOC + "IAM/latest/UserGuide/access_policies_testing-policies.html"), ("S3 security best practices (secure transport)", DOC + "AmazonS3/latest/userguide/security-best-practices.html"),
        ("AWS architecture icons (for the final diagram)", "https://aws.amazon.com/architecture/icons/")]
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    ix = [("Architecture diagram", "arch"), ("Method flowchart", "flow"), ("IAM and bucket policies", "pol"), ("Audit and alerting setup", "alert"), ("Isolation test plan", "tests"), ("Checklist for the paper's audit and alerting section", "check"), ("Sources", "srcs")]
    rows = "".join(f'<tr><td><a href="#{a}">{t}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for t, a in ix)
    out = [f'''<section class="cover"><p class="eb">TENANTWALL · HELPERS FOR THE PAPER</p><h1>TenantWall<br><span>diagrams, policies, alerting</span></h1>
<p class="lead">Ready-to-adapt material for the requests on the project: an architecture diagram and a method flowchart, sample IAM policies (ABAC allow, explicit denies, deny insecure transport), the CloudTrail and CloudWatch alerting setup, a test plan and a checklist for the audit and alerting section. All account ids, bucket names and emails are placeholders.</p>
<p class="how"><b>Files.</b> Everything is in <code>generated/tenantwall/</code>: <code>architecture.svg/.png</code>, <code>flowchart.svg/.png</code>, <code>policies/*.json</code>, <code>alerting/setup-alerting.sh</code>, <code>alerting/alarm-settings.json</code> and <code>check_policies.py</code>. See also the <a href="{KB}tenantwall">TenantWall</a>, <a href="{KB}abac">ABAC</a> and <a href="{KB}cloudtrail">CloudTrail</a> Knowledge Base pages.</p>
<table class="ix"><tbody>{rows}</tbody></table>
<p class="src">Confirm details such as the exact meaning of "explicit deny" with your professor. Redraw the diagram with the official AWS icon set in diagrams.net for the paper; the layout here is the content to copy.</p></section>''']
    out.append(f'<section class="sec" id="arch"><h2>Architecture diagram<a class="back" href="#top">↑ Index</a></h2><img src="file://{TW}/architecture.png" style="width:100%"><p class="cap">Two tenant roles share one bucket and one fleet. IAM evaluates every request against tag-matched allows and explicit denies. Every call, allowed or denied, reaches CloudTrail; denied calls become a metric, an alarm and an email.</p></section>')
    out.append(f'<section class="sec" id="flow"><h2>Method flowchart<a class="back" href="#top">↑ Index</a></h2><img src="file://{TW}/flowchart.png" style="width:100%"><p class="cap">Order of evaluation follows the AWS policy evaluation logic: an explicit deny wins; otherwise a matching allow is needed; otherwise the request is implicitly denied.</p></section>')
    pol = "".join(f'<h3>{E(n)}</h3><p>{E(d)}</p><pre>{E((TW / "policies" / n).read_text().strip())}</pre>' for n, d in POL)
    out.append(f'<section class="sec" id="pol"><h2>IAM and bucket policies<a class="back" href="#top">↑ Index</a></h2><p class="meta">Replace 111122223333, the bucket names and the Region. Before using them, run IAM Access Analyzer policy validation on each file and test with the IAM policy simulator. <code>check_policies.py</code> checks the JSON structure offline and simulates the isolation cases with a simplified evaluator (all 29 checks pass).</p>{pol}'
               '<p class="meta"><b>Design notes.</b> ec2:DescribeInstances does not support resource-level permissions, so tenants can see instance metadata of others; if that matters for the paper, say so as a limitation or filter by tag in the application. S3 isolation uses tenant prefixes because object-tag conditions apply only to some actions; prefixes are simpler to reason about.</p></section>')
    al = json.loads((TW / "alerting" / "alarm-settings.json").read_text())
    rows = "".join(f"<tr><td>{E(k)}</td><td>{E(v)}</td></tr>" for k, v in {**al["MetricFilter"], **al["Alarm"]}.items())
    out.append(f'<section class="sec" id="alert"><h2>Audit and alerting setup<a class="back" href="#top">↑ Index</a></h2><ol><li>Create a log bucket and give CloudTrail permission to write to it (<code>cloudtrail-bucket-policy.json</code>).</li><li>Create a trail with management events plus S3 data events for the TenantWall bucket only (<code>data-event-selectors.json</code>), delivering to a CloudWatch Logs group.</li><li>Add a metric filter that counts AccessDenied and UnauthorizedOperation errors.</li><li>Create an SNS topic with an email subscription and confirm the subscription email.</li><li>Create an alarm on the metric that notifies the topic.</li></ol><p><code>alerting/setup-alerting.sh</code> does these steps with the AWS CLI once you fill in the placeholders. It never stores credentials; it uses your CLI profile.</p><table class="kv"><tbody>{rows}</tbody></table><p class="meta">CloudTrail usually delivers events within minutes, so the email arrives minutes after the denied call, not instantly. Measure it for the paper.</p></section>')
    out.append(f'<section class="sec" id="tests"><h2>Isolation test plan<a class="back" href="#top">↑ Index</a></h2><table class="t"><thead><tr><th>#</th><th>Test (run as the tenant A role)</th><th>Expected</th><th>Evidence to capture</th></tr></thead><tbody>{"".join(f"<tr><td>{i + 1}</td><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for i, (a, b, c) in enumerate(TESTS))}</tbody></table><p class="meta">Repeat tests 2 and 5 several times and record the time from the call to the email. Then clean up: delete the trail, alarm, topic, log group, buckets and instances.</p></section>')
    out.append(f'<section class="sec" id="check"><h2>Checklist for the audit and alerting section<a class="back" href="#top">↑ Index</a></h2><table class="chk"><tbody>{"".join(f"<tr><td class=box>☐</td><td>{E(x)}</td></tr>" for x in CHECK)}</tbody></table></section>')
    out.append(f'<section class="sec" id="srcs"><h2>Sources<a class="back" href="#top">↑ Index</a></h2><ul>{"".join(f"<li><a href={chr(34)}{u}{chr(34)}>{E(t)}</a> <span class=u>{E(u)}</span></li>" for t, u in SRCS)}</ul><p class="meta">Policies and settings follow the AWS documentation above; the metric filter pattern is the one AWS documents for unauthorised API calls.</p></section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9pt/1.45 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } code { font: 600 7.8pt "JetBrains Mono"; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 20pt; }
.lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; } table { border-collapse: collapse; width: 100%; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
.ix td { padding: 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.src { font-size: 8pt; color: #64748b; margin-top: 4mm; } .sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 3mm; display: flex; align-items: baseline; }
.back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; } h3 { font: 700 10pt "JetBrains Mono"; color: #1d4ed8; margin: 4mm 0 1mm; }
.cap, .meta { color: #475569; font-size: 8.6pt; } pre { font: 400 7pt/1.35 "JetBrains Mono"; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #1d4ed8; padding: 1.8mm 2.5mm; white-space: pre-wrap; margin: 0 0 1mm; break-inside: avoid; }
pre { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; } ol, ul { padding-left: 5mm; } li { margin-bottom: 1.2mm; }
.kv td { border-bottom: 1px solid #e2e8f0; padding: 1.3mm 2mm; font-size: 8.4pt; } .kv td:first-child { font-weight: 600; width: 45mm; } .kv td:last-child { font-family: "JetBrains Mono"; font-size: 7.6pt; }
.t td { border-bottom: 1px solid #e2e8f0; padding: 1.8mm 2mm; vertical-align: top; } .chk td { border-bottom: 1px solid #e2e8f0; padding: 2mm; vertical-align: top; font-size: 9.4pt; } .chk .box { width: 6mm; color: #94a3b8; }
.u { display: block; font: 400 7pt "JetBrains Mono"; color: #94a3b8; }"""
def render(pages, name):
    (SRC / "tw.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/tw.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = ["arch", "flow", "pol", "alert", "tests", "check", "srcs"]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for t, k in [("Architecture diagram", "arch"), ("Method flowchart", "flow"), ("Policies", "pol"), ("Audit and alerting", "alert"), ("Test plan", "tests"), ("Paper checklist", "check"), ("Sources", "srcs")]: w.add_outline_item(t, d2[k] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "TenantWall helpers"}); w.write(str(OUT / "tenantwall-helpers.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "tw.html"): (SRC / f).unlink()
print(NP, "pages", {k: d2[k] for k in KEYS})
