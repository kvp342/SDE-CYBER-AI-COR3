"""roadmap.sh checklists mapped to the placement kit. Run from the repo root: python3 generated/src/roadmapsh.py"""
import html, subprocess, pathlib, io
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
E = lambda s: html.escape(s, quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
# (map slug, title, why for Path A, [(group, [(topic, kb id or None, note)])])
MAPS = [
("backend", "Backend", "Your SDE lane: what a backend developer is expected to know.", [
 ("Internet and the web", [("How the internet works, HTTP, DNS, domains, hosting", "url-flow", ""), ("HTTPS and TLS", "http-tls", "")]),
 ("A language and its ecosystem", [("One backend language in depth (your C++ plus one of Java, Go, Node or Python for web work)", None, "Pick one for the backend project; C++ alone is uncommon for web APIs"), ("Package managers and project layout", None, "")]),
 ("Version control", [("Git: branching, merging, rebasing, pull requests", None, "Practise on your project repos")]),
 ("Databases", [("Relational: SQL, schema design, normalisation", "normalisation", ""), ("Transactions, ACID, isolation", "acid", ""), ("Indexes and query plans", "indexing", ""), ("NoSQL types and when to use them", "cap", "Covered as SQL vs NoSQL in the DBMS Q&A"), ("ORMs and N+1 queries", None, "")]),
 ("APIs", [("REST design and status codes", "http-tls", ""), ("Authentication: sessions, JWT, OAuth basics", "xss", "JWT used in the plan's backend project"), ("GraphQL and gRPC (awareness)", None, "")]),
 ("Caching and scaling", [("Caching: cache-aside, Redis, CDN", "caching", ""), ("Load balancing, replication, sharding", "load-balancing", ""), ("Message queues", "hld", "")]),
 ("Testing and security", [("Unit and integration tests", None, "Write tests for the backend project"), ("Web security: OWASP Top 10", "owasp", ""), ("Hashing and password storage", "crypto-basics", "")]),
 ("Deploying", [("Linux basics and the shell", "ctf", "Bandit levels in the cyber track"), ("Containers (Docker) basics", None, "Gap: one evening to containerise the backend project"), ("CI/CD basics", None, "Gap: a GitHub Actions workflow that runs your tests"), ("Cloud deployment", "aws-core", "")]),
]),
("cyber-security", "Cyber Security", "Your edge: where your 20-week lab track and TenantWall sit on the full map.", [
 ("Fundamentals", [("Networking: OSI, TCP/IP, ports and protocols", "osi-tcpip", ""), ("Operating systems: Linux and Windows basics", "process-thread", "Windows internals are a gap"), ("Common tools: nmap, Wireshark, Burp Suite", "ctf", "Lab weeks 3 to 6")]),
 ("Security concepts", [("CIA triad, AAA, least privilege", "iam", ""), ("Cryptography: hashing, symmetric, asymmetric, PKI", "crypto-basics", ""), ("Threat modelling", "threat-modelling", "")]),
 ("Web and application security", [("OWASP Top 10", "owasp", ""), ("SQL injection, XSS, CSRF, SSRF, access control", "sqli", "PortSwigger labs")]),
 ("Cloud security", [("IAM, policies, ABAC", "abac", "TenantWall"), ("Logging and monitoring (CloudTrail, CloudWatch)", "cloudtrail", "TenantWall")]),
 ("Offensive basics", [("CTFs", "ctf", ""), ("Binary exploitation basics", "binary-exploitation", "Binary taster in May"), ("Bug bounty and disclosure", "bug-bounty", "")]),
 ("Defensive basics", [("SIEM, log analysis, incident response", None, "Lab weeks 15 to 17"), ("MITRE ATT&CK", None, "Lab week 16")]),
 ("Certifications (optional)", [("CompTIA Security+ or eJPT", None, "Listed in many fresher job posts; after AWS SAA")]),
]),
("aws", "AWS", "Your cloud lane and the SAA-C03 exam in the week of 19 Apr.", [
 ("Core services", [("IAM", "iam", ""), ("EC2, Auto Scaling, load balancers", "aws-core", ""), ("S3 and storage classes", "aws-core", ""), ("VPC: subnets, routing, NAT, security groups", "aws-core", ""), ("RDS, DynamoDB", "aws-core", "")]),
 ("Integration and serverless", [("SQS, SNS", "aws-core", ""), ("Lambda and API Gateway", "aws-core", "")]),
 ("Operations and security", [("CloudWatch and CloudTrail", "cloudtrail", ""), ("KMS and encryption", "aws-core", ""), ("Cost management and billing alarms", "aws-core", "Week 1 of the AWS track")]),
 ("Architecture", [("Well-Architected Framework", None, "Read its six pillars before exam prep"), ("High availability and disaster recovery", "load-balancing", "")]),
]),
("computer-science", "Computer Science", "The Core CS and DSA side of every interview.", [
 ("Data structures", [("Arrays, linked lists, stacks, queues, hash tables", "hashing", ""), ("Trees, BST, heaps, tries", "trees", ""), ("Graphs", "bfs", "")]),
 ("Algorithms", [("Complexity and Big-O", "complexity", ""), ("Sorting and searching", "binary-search", ""), ("Recursion, backtracking, greedy, DP", "dp", ""), ("Graph algorithms", "dijkstra", ""), ("String algorithms", "string-algos", "")]),
 ("Systems", [("Processes, threads, scheduling, deadlock", "process-thread", ""), ("Memory and virtual memory", "virtual-memory", ""), ("Networking", "tcp-udp", ""), ("Databases", "acid", "")]),
 ("Design", [("OOP and SOLID", "oop", ""), ("Design patterns", "solid", ""), ("System design basics", "hld", "")]),
]),
("system-design", "System Design", "Light HLD for Big Tech, plus LLD for product companies.", [
 ("Fundamentals", [("Performance vs scalability, latency vs throughput", "hld", ""), ("CAP and consistency patterns", "cap", ""), ("Availability patterns: fail-over, replication", "load-balancing", "")]),
 ("Building blocks", [("DNS, CDN, load balancers, reverse proxies", "url-flow", ""), ("Databases: SQL, NoSQL, sharding, replication", "load-balancing", ""), ("Caching", "caching", ""), ("Queues and asynchronism", "hld", ""), ("Rate limiting", "hld", "Mock 7 deep dive")]),
 ("Practice", [("URL shortener", "mock-7", ""), ("Parking lot (LLD)", "mock-6", ""), ("Chat app, news feed, notification service", None, "Gap: two more designs in the sprint")]),
]),
("devops", "DevOps (basics only)", "Not a target role, but these basics make your projects deployable and your resume stronger.", [
 ("Basics worth one week each", [("Linux command line and shell scripting", "ctf", ""), ("Git and GitHub workflows", None, ""), ("Docker basics", None, "Gap"), ("CI/CD with GitHub Actions", None, "Gap"), ("Monitoring basics", "cloudtrail", "")]),
 ("Skip for now", [("Kubernetes, Terraform, service meshes", None, "Not needed for fresher SDE or security roles")]),
]),
]
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    tot = sum(len(t) for _, _, _, gs in MAPS for _, t in gs)
    cov = sum(1 for _, _, _, gs in MAPS for _, t in gs for _, k, _ in t if k)
    rows = "".join(f'<tr><td><a href="#{s}">{E(t)}</a></td><td>{E(w)}</td><td class="c">{sum(len(x) for _, x in gs)}</td><td class="c">{sum(1 for _, x in gs for _, k, _ in x if k)}</td><td class="pg"><a href="#{s}">{pg(s)}</a></td></tr>' for s, t, w, gs in MAPS)
    out = [f'<section class="cover"><p class="eb">ROADMAP.SH · MAPPED TO YOUR PLAN</p><h1>roadmap.sh<br><span>checklists</span></h1><p class="lead">Six roadmap.sh maps that fit Path A, cut to what a fresher needs. Each topic shows where your kit already covers it (tap to open the Knowledge Base page) or marks it as a gap. {cov} of {tot} topics are covered; the gaps are listed in each section.</p><h2>Index</h2><table class="ix"><thead><tr><th>Map</th><th>Why it matters</th><th>Topics</th><th>Covered</th><th>Page</th></tr></thead><tbody>{rows}</tbody></table><p class="src">Topic lists summarised from the public maps at <a href="https://roadmap.sh">roadmap.sh</a> (Backend, Cyber Security, AWS, Computer Science, System Design, DevOps). Open each map for its full detail and resources. Knowledge Base links open the online version.</p></section>']
    for s, t, w, gs in MAPS:
        out.append(f'<section class="sec" id="{s}"><h2>{E(t)} <a class="map" href="https://roadmap.sh/{s}">roadmap.sh/{s}</a><a class="back" href="#top">↑ Index</a></h2><p class="sub">{E(w)}</p>')
        for g, items in gs:
            out.append(f'<h3>{E(g)}</h3><table class="it"><tbody>')
            for name, k, note in items:
                where = f'<a href="{KB}{k}">Knowledge Base</a>' if k else '<span class="gap">Gap</span>'
                out.append(f'<tr><td class="box">☐</td><td class="t">{E(name)}</td><td class="w">{where}</td><td class="n">{E(note)}</td></tr>')
            out.append('</tbody></table>')
        out.append('</section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 9pt/1.45 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } h1 { font: 700 34pt/1 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; }
.lead { font-size: 10pt; color: #475569; max-width: 165mm; } h2 { font: 700 13pt "Space Grotesk"; color: #0f172a; margin: 5mm 0 2mm; }
table { width: 100%; border-collapse: collapse; } .ix th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.5mm 2mm; text-align: left; }
.ix td { padding: 1.5mm 2mm; border-bottom: 1px solid #e2e8f0; } .ix td a { color: #0f172a; font-weight: 600; } .ix .c { text-align: center; font-family: "JetBrains Mono"; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.src { font-size: 7.8pt; color: #64748b; margin-top: 4mm; } .sec { break-before: page; }
.sec h2 { font-size: 17pt; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin-top: 0; display: flex; align-items: baseline; gap: 4mm; }
.map { font: 600 8pt "JetBrains Mono"; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
.sub { color: #475569; } h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 4mm 0 1mm; } .it td { padding: 1.3mm 1.5mm; border-bottom: 1px solid #eef2f7; vertical-align: top; }
.it .box { width: 5mm; color: #94a3b8; font-size: 10pt; } .it .t { font-weight: 600; color: #0f172a; } .it .w { width: 32mm; white-space: nowrap; } .it .n { width: 62mm; color: #64748b; font-size: 8pt; }
.gap { font: 600 7pt "JetBrains Mono"; color: #b42318; background: #fde2e1; border-radius: 4px; padding: 0 5px; }"""
def render(pages, name):
    (SRC / "roadmapsh.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js = SRC / "r.js"; js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/roadmapsh.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[s] == d2[s] for s, *_ in MAPS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for s, t, *_ in MAPS: w.add_outline_item(t, d2[s] - 1, fit=Fit.fit())
N = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {N}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "roadmap.sh checklists mapped to the placement kit"}); w.write(str(OUT / "roadmapsh-checklists.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js"): (SRC / f).unlink()
print(N, "pages")
