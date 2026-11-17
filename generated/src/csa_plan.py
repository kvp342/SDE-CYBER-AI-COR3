"""Cloud Solutions Architect (AWS SAA-C03) study plan: 10 weeks, 2 hours a day, with daily topics, labs and exam rules. Run: python3 generated/src/csa_plan.py"""
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

import datetime as _dt
SEC = []
def sec(id, title, body): SEC.append((id, title, body))
EXAMP = ("https://aws.amazon.com/certification/certified-solutions-architect-associate/", "AWS Certified Solutions Architect – Associate (exam page)")
GUIDE = ("https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf", "SAA-C03 exam guide (PDF)")
SB = ("https://skillbuilder.aws/", "AWS Skill Builder (free courses and the official practice question set)")
WA = ("https://aws.amazon.com/architecture/well-architected/", "AWS Well-Architected Framework")
FAQ = ("https://aws.amazon.com/faqs/", "AWS product FAQs")
FREE = ("https://aws.amazon.com/free/", "AWS Free Tier")
C = lambda x: S(*x)

WEEKS = [
 ("Cloud basics and IAM", "budget",
  ["Global infrastructure: Regions, Availability Zones, edge locations; shared responsibility model; the console, CLI and SDKs",
   "IAM users, groups, roles; access keys vs temporary credentials; MFA; root user rules",
   "Policies: identity vs resource-based, JSON elements, evaluation logic (explicit deny > allow > implicit deny)",
   "Organizations, SCPs, permission boundaries, IAM Identity Center, cross-account roles with STS AssumeRole",
   "Re-read the IAM parts of TenantWall explained: ABAC, condition keys, policy variables, Access Analyzer"],
  ["An explicit Deny anywhere wins; SCPs and boundaries limit, they never grant.", "Applications on EC2 or Lambda get a role, never access keys.", "Cross-account access = a role in the target account + AssumeRole."]),
 ("Compute", "ec2",
  ["EC2 instance families, sizing, AMIs, user data, instance metadata (IMDSv2)",
   "Purchase options: On-Demand, Savings Plans, Reserved Instances, Spot, Dedicated Hosts/Instances",
   "Block storage: EBS volume types (gp3, io2, st1, sc1), snapshots, instance store; EFS for shared files",
   "Placement groups (cluster, spread, partition), ENI, Elastic IP, hibernation",
   "Lambda basics, containers on ECS/EKS/Fargate, Elastic Beanstalk: when to choose each"],
  ["Spot = cheapest, can be interrupted: only for fault-tolerant work.", "Instance store is lost when the instance stops; EBS persists.", "EBS lives in one AZ; EFS is shared across AZs."]),
 ("Networking", "vpc",
  ["VPC, CIDR, subnets, route tables, Internet Gateway; public vs private subnets",
   "NAT gateway; security groups (stateful, allow only) vs network ACLs (stateless, allow and deny)",
   "VPC endpoints: gateway (S3, DynamoDB) vs interface (PrivateLink); VPC Flow Logs",
   "VPC peering (not transitive), Transit Gateway, Site-to-Site VPN, Direct Connect",
   "Route 53 basics: hosted zones, records, alias records"],
  ["Private subnet reaching the internet = NAT gateway in a public subnet.", "Private access to S3 without internet = gateway endpoint.", "Many VPCs + on-prem = Transit Gateway."]),
 ("Storage", "s3",
  ["S3 basics: buckets, objects, keys, prefixes, consistency, versioning, presigned URLs",
   "Storage classes (Standard, Intelligent-Tiering, Standard-IA, One Zone-IA, Glacier tiers) and lifecycle rules",
   "S3 security: Block Public Access, bucket policies, encryption (SSE-S3, SSE-KMS, client-side), Object Lock",
   "Replication (CRR/SRR), Transfer Acceleration, multipart upload, S3 event notifications",
   "FSx, Storage Gateway, DataSync, Snow family, AWS Backup"],
  ["Unknown or changing access pattern = Intelligent-Tiering.", "Write-once compliance = Object Lock (compliance mode).", "Huge offline transfer = Snow family; online sync = DataSync."]),
 ("Databases", "rds",
  ["RDS engines, Multi-AZ (availability) vs read replicas (read scaling), backups and snapshots",
   "Aurora: storage model, replicas, Aurora Serverless, Global Database",
   "DynamoDB: partition and sort keys, capacity modes, GSI/LSI, Streams, TTL, global tables",
   "ElastiCache (Redis/Memcached) and DAX: caching patterns",
   "Redshift, Athena and other purpose-built databases: which question words point to which"],
  ["Multi-AZ = failover, not read scaling; read replicas = read scaling.", "Microsecond DynamoDB reads = DAX.", "Key-value at any scale, serverless = DynamoDB."]),
 ("Resilience and scaling", "alb",
  ["Elastic Load Balancing: ALB (HTTP, path/host rules), NLB (TCP/UDP, static IP), GWLB",
   "Auto Scaling groups: launch templates, health checks, scaling policies (target tracking, step, scheduled)",
   "Route 53 routing policies: simple, weighted, latency, failover, geolocation, multivalue; health checks",
   "Disaster recovery: backup and restore, pilot light, warm standby, multi-site active-active; RPO and RTO",
   "Design a three-tier web app across two AZs on paper; check each tier for a single point of failure"],
  ["Lower RTO/RPO costs more: backup-restore < pilot light < warm standby < active-active.", "Static IP for a load balancer = NLB (or Global Accelerator).", "Failover between Regions = Route 53 failover routing + health checks."]),
 ("Decoupling and serverless", "lambda",
  ["SQS: standard vs FIFO, visibility timeout, dead-letter queues, long polling",
   "SNS topics and fan-out (SNS to several SQS queues); EventBridge rules and buses",
   "API Gateway + Lambda: limits, concurrency, cold starts; Step Functions for workflows",
   "Streaming: Kinesis Data Streams vs Data Firehose; when SQS is enough",
   "Re-architect a monolith on paper into queue-based services; mark where each service fits"],
  ["Decouple producer and consumer = SQS.", "One event to many consumers = SNS fan-out or EventBridge.", "Exactly-once, ordered processing = SQS FIFO."]),
 ("Security and monitoring", "trail",
  ["KMS (keys, key policies, envelope encryption), CloudHSM, ACM certificates",
   "Secrets Manager vs Systems Manager Parameter Store; WAF, Shield, Firewall Manager",
   "GuardDuty, Inspector, Macie, Security Hub, Detective: what each one finds",
   "CloudTrail (management vs data events), CloudWatch metrics, logs, alarms; AWS Config rules",
   "TenantWall explained: walk through your own CloudTrail, metric filters, alarms and SNS from memory"],
  ["Automatic secret rotation = Secrets Manager.", "Who did what = CloudTrail; resource configuration over time = Config.", "Sensitive data in S3 = Macie; threat detection = GuardDuty."]),
 ("Performance and cost", "teardown",
  ["CloudFront (caching, origins, OAC) vs Global Accelerator; caching at every layer",
   "Analytics: Athena, Glue, EMR, Kinesis, QuickSight, Lake Formation; when each fits",
   "Pricing: Savings Plans vs RIs vs Spot; S3 class costs; data transfer costs; NAT gateway costs",
   "Cost tools: Cost Explorer, Budgets, Cost and Usage Report, Compute Optimizer, Trusted Advisor",
   "Well-Architected: the six pillars and the questions each asks"],
  ["Static content worldwide = CloudFront; non-HTTP global performance = Global Accelerator.", "Query S3 data with SQL, no servers = Athena.", "Steady 1–3 year usage = Savings Plans or Reserved Instances."]),
 ("Exam practice", None,
  ["Practice set 1: questions 1–30 of your SAA-C03 study pack, timed (60 min); log every miss",
   "Re-read notes for each missed topic in the docs and FAQs",
   "Practice set 2: questions 31–60 of the study pack, timed",
   "Official sample questions and the free Skill Builder practice question set",
   "Weak-area day: redo all missed questions; rewrite the 'which service' table from memory"],
  ["Read the last line of the question first: cheapest, fastest, least operational overhead or most secure.", "Eliminate two answers, then compare the remaining two on that last line.", "Managed and serverless usually wins 'least operational overhead'."]),
]
LABTITLE = {"budget": "IAM: an admin group and a role for EC2 (lab 2)", "ec2": "EC2 with a security group, a role and IMDSv2 (lab 5)", "vpc": "VPC with public and private subnets (lab 4)",
            "s3": "Private S3 bucket with versioning and encryption (lab 3)", "rds": "Private RDS MySQL database (lab 7)", "alb": "Load balancer + Auto Scaling across two AZs (lab 6)",
            "lambda": "Lambda behind an HTTP API (lab 8)", "trail": "CloudTrail + root-activity alarm, KMS (labs 9–10)", "teardown": "Teardown checklist and cost check (lab 11)"}
START = _dt.date(2026, 11, 23)
rows = [[d.strftime("%a %d %b"), "W0", t] for d, t in zip([_dt.date(2026, 11, 18) + _dt.timedelta(days=k) for k in range(5)], [
 "<b>Start-up:</b> secure the account: MFA on the root user, an admin IAM user, and the budget alert (lab 1 in the AWS lab workbook)",
 "Read the SAA-C03 exam guide: the four domains and the task statements; skim the list of in-scope services",
 "Install and configure the AWS CLI with the admin profile; run aws sts get-caller-identity; Free Tier limits",
 "<b>Lab:</b> nothing new to build: re-read sections 1–4 of TenantWall explained (IAM and policies)",
 "<b>Review:</b> plan the 10 weeks; put the 2-hour slot in your calendar every day"])]
for w, (title, lab, days, traps) in enumerate(WEEKS):
    for d in range(7):
        day = START + _dt.timedelta(days=7 * w + d); ds = day.strftime("%a %d %b")
        if d < 5: rows.append([ds, f"W{w + 1}", E(days[d])])
        elif d == 5: rows.append([ds, f"W{w + 1}", ("<b>Lab:</b> " + E(LABTITLE[lab]) + " in the AWS lab workbook; delete everything after") if lab else "<b>Full mock:</b> 65 questions in 130 minutes (all 60 pack questions + 5 official samples)"])
        else: rows.append([ds, f"W{w + 1}", "<b>Review:</b> recall test on this week's three exam rules, redo the week's missed questions, plan next week" if w < 9 else "<b>Decide:</b> score 80%+ twice → book the exam; else repeat weeks 8–10 practice"])
END = START + _dt.timedelta(days=69); FIRST = _dt.date(2026, 11, 18)

sec("why", "What this plan is", UL([
 "<b>Course assumed:</b> AWS Certified Solutions Architect – Associate (exam code SAA-C03). If your sir's course is a different one, keep the daily routine and swap the weekly topics for his modules." + C(EXAMP),
 "<b>Length:</b> 10 weeks, 2 hours every day, from " + FIRST.strftime("%a %d %b %Y") + " to " + END.strftime("%a %d %b %Y") + ". A 5-day start-up (W0), then weeks 1–9 (Monday to Sunday) teach the four exam domains; week 10 is practice.",
 "<b>Exam:</b> 65 questions (50 scored, 15 unscored), 130 minutes, pass mark 720 on a scale of 100–1000. Domains: Secure 30%, Resilient 26%, High-performing 24%, Cost-optimised 20%." + C(GUIDE),
 "<b>Your other files:</b> notes and 60 practice questions are in " + K("generated/aws-saa-c03-study-pack.pdf", "the SAA-C03 study pack") + "; the hands-on labs are in " + K("generated/aws-lab-workbook.pdf", "the AWS lab workbook") + "; your own project is explained in " + K("generated/tenantwall-explained.pdf", "TenantWall explained") + ".",
 "<b>Fit with the final plan:</b> the final plan gives AWS 30 min/day and books the exam for the week of 19 April. These 2 hours replace that slot for 10 weeks. If you finish week 10 scoring 80% or more twice, you can book the exam earlier, in February."]))

sec("routine", "The 2-hour routine (every day)", T(["Block", "Time", "What you do"], [
 ["1. Learn", "50 min", "Your sir's lecture or the matching AWS Skill Builder module, then the AWS FAQ page for that day's service. Write one-line notes: what it is, when to choose it, one limit." + C(SB) + C(FAQ)],
 ["2. Do", "50 min", "Weekdays: build it in the console or CLI (Free Tier) or draw the architecture on paper; then 5 practice questions on the topic. Saturday: one full lab." + C(FREE)],
 ["3. Recall", "20 min", "Close the notes and write the day's topic from memory; turn every mistake into an Anki card; tick the day in the table."]]) +
 '<p class="note"><b>Cost rule:</b> set the budget alert on day 1 (lab 1), and on every lab day delete what you created before you stop. NAT gateways, load balancers, RDS and unattached Elastic IPs bill by the hour.</p>' +
 "<h3>Weekly shape</h3>" + UL(["Mon–Fri: the five topics of the week.", "Saturday: the week's lab from the lab workbook (2 hours).", "Sunday: review, the week's three exam rules, and missed questions."]))

for n, (a, b, part) in enumerate([(0, 40, "0–5"), (40, 75, "6–10")]):
    sec(f"days{n + 1}", f"Day by day, weeks {part}", T(["Date", "Week", "Topic (2 hours)"], rows[a:b], "days"))

sec("weeks", "Each week's exam rules (learn these by heart)", T(["Week", "Topic", "Rules the exam keeps testing"],
 [[f"W{n + 1}", E(t), "<br>".join(E(x) for x in tr)] for n, (t, _, _, tr) in enumerate(WEEKS)]))

sec("check", "Checkpoints and how to know you are ready", T(["When", "Check", "Pass mark"], [
 ["End of W3", "Explain IAM evaluation, EC2 pricing options and a public/private VPC with no notes", "All three from memory"],
 ["End of W5", "Draw a three-tier app (ALB, EC2 Auto Scaling, RDS Multi-AZ, S3) and list each storage class", "Under 10 minutes"],
 ["End of W7", "Questions 1–34 in the study pack", "75% or more"],
 ["End of W9", "Questions 35–60 in the study pack; Well-Architected pillars from memory", "75% or more; all 6 pillars"],
 ["End of W10", "Two full timed practice sets", "80% or more twice → book the exam"]]) +
 "<h3>The six Well-Architected pillars</h3>" + UL(["Operational excellence", "Security", "Reliability", "Performance efficiency", "Cost optimisation", "Sustainability"]) + C(WA))
# ------------------------------------------------------------------ build
for p in USED: assert (ROOT / p.rstrip("/")).exists(), p        # every kit link points at a real file
CSS = """@page { size: A4; margin: 13mm 14mm 15mm; } * { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 9.2pt/1.5 Inter, sans-serif; color: #1e293b; } a { color: #1d4ed8; text-decoration: none; } a.kit { font: 600 7.8pt "JetBrains Mono"; color: #0f766e; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; } h1 { font: 700 30pt/1.05 "Space Grotesk"; margin: 0 0 3mm; color: #0f172a; } h1 span { color: #c2410c; }
h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; margin: 0 0 3mm; padding-bottom: 1.5mm; border-bottom: 2px solid #c2410c; display: flex; align-items: baseline; }
h2 .num { color: #c2410c; margin-right: 3mm; } h2 .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; color: #64748b; } h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1.5mm; }
section.sec { break-before: page; } table { border-collapse: collapse; width: 100%; margin: 1mm 0 2mm; break-inside: auto; } tr { break-inside: avoid; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; letter-spacing: .05em; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
table.days td:first-child { white-space: nowrap; width: 24mm; } table.days td { padding: .9mm 2mm; font-size: 8.4pt; } td { border-bottom: 1px solid #e2e8f0; padding: 1.4mm 2mm; vertical-align: top; } table.km td:first-child { width: 45%; } ul { padding-left: 5mm; margin: 1mm 0; } li { margin-bottom: 1.6mm; }
.note { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; margin: 3mm 0; font-size: 8.6pt; } .lead { font-size: 10.5pt; } sup a { font: 600 6.5pt "JetBrains Mono"; color: #c2410c; }
table.ix td { padding: 1.6mm 2mm; } td.pg { text-align: right; font-family: "JetBrains Mono"; width: 14mm; } ol.src { font-size: 7.8pt; padding-left: 6mm; } ol.src li { margin-bottom: 1mm; word-break: break-all; }"""
def body(pages):
    pg = lambda k: str(pages.get(k, "00")) if pages else "00"
    ix = "".join(f'<tr><td><a href="#{i}">{n + 1}. {E(t)}</a></td><td class="pg"><a href="#{i}">{pg(i)}</a></td></tr>' for n, (i, t, _) in enumerate(SEC))
    ix += f'<tr><td><a href="#src">Sources ({len(SOURCES)})</a></td><td class="pg"><a href="#src">{pg("src")}</a></td></tr>'
    out = [f'''<section><p class="eb">CLOUD SOLUTIONS ARCHITECT · 2 HOURS A DAY</p><h1>Solutions Architect<br><span>in 10 weeks, 2 hours a day</span></h1>
<p class="lead">A day-by-day plan for the Cloud Solutions Architect course (AWS SAA-C03): one fixed 2-hour routine, a topic for every day, a lab every Saturday, a review every Sunday, the rules the exam keeps testing, and checkpoints that tell you when to book the exam.</p>
<table class="ix"><thead><tr><th>Section</th><th class="pg">Page</th></tr></thead><tbody>{ix}</tbody></table>
<p class="note">Day 1 is Wed 18 Nov 2026 (a 5-day start-up); week 1 starts Mon 23 Nov. Missed a day? Do not double up: move the rest of the table by one day and keep going.</p></section>''']
    for n, (i, t, b) in enumerate(SEC):
        out.append(f'<section class="sec" id="{i}"><h2><span class="num">{n + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2>{b}</section>')
    out.append('<section class="sec" id="src"><h2><span class="num">··</span>Sources<a class="back" href="#top">↑ Index</a></h2><p>Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.</p><ol class="src">'
               + "".join(f'<li><a href="{u}">{E(l)}</a><br>{E(u)}</li>' for u, l in SOURCES) + "</ol></section>")
    return "".join(out)
js = SRC / "rcsa.js"
def render(pages, name):
    (SRC / "csaplan.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/csaplan.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "c1.pdf"); d2, n2 = render(d1, "c2.pdf"); assert n1 == n2 and all(d1[i] == d2[i] for i, _, _ in SEC)
w = PdfWriter(clone_from=PdfReader(str(SRC / "c2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for n, (i, t, _) in enumerate(SEC): w.add_outline_item(f"{n + 1}. {t}", d2[i] - 1, fit=Fit.fit())
w.add_outline_item("Sources", d2["src"] - 1, fit=Fit.fit())
NP = len(w.pages)
for k, pg in enumerate(w.pages):
    if k == 0: continue
    buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
    cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{k + 1} / {NP}"); cv.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Solutions Architect in 10 weeks"}); w.write(str(OUT / "cloud-architect-2h-plan.pdf"))
for f in ("c1.pdf", "c2.pdf", "rcsa.js", "csaplan.html"): (SRC / f).unlink()
print(NP, "pages;", len(USED), "kit links;", len(SOURCES), "sources;", d2)
