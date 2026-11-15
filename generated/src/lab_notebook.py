"""Security lab notebook PDF: write-up templates with worked examples, a STRIDE threat model of TenantWall,
a Linux and networking command sheet (each command's binary checked to exist here), and a web-security sheet by class.
Run from the repo root: python3 generated/src/lab_notebook.py"""
import html, io, pathlib, shutil, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"; PS = "https://portswigger.net/web-security/"
CTF_TEMPLATE = ["Challenge: name, platform, category, difficulty, date", "Goal: what the flag or win condition is", "Recon: what you looked at first and what you noticed",
                "Dead ends: what you tried that failed, and why (interviewers like this part)", "Solution: the steps that worked, with the commands you ran", "Root cause: the weakness in one sentence",
                "Fix: how a developer or admin would prevent it", "Learned: one technique to reuse, and a Knowledge Base page to revisit"]
CTF_EXAMPLE = [("Challenge", "OverTheWire Bandit, level 0 → 1 (Linux basics), beginner"), ("Goal", "Log in over SSH and find the password for the next level."),
               ("Recon", "The level page gives the host bandit.labs.overthewire.org, port 2220, user bandit0. After logging in, ls shows a file named readme in the home directory."),
               ("Dead ends", "ssh without -p tried port 22 and was refused: the port matters."), ("Solution", "ssh -p 2220 bandit0@bandit.labs.overthewire.org, then cat readme. The file holds the next password (not written here: the site asks players not to publish them)."),
               ("Root cause", "None: this level teaches SSH and reading files."), ("Fix", "Not applicable; later levels add permissions, hidden files and SUID binaries."),
               ("Learned", "Always read the level page for the port and hints; ls -la shows hidden files.")]
LAB_TEMPLATE = ["Lab: title and link, topic, level (Apprentice / Practitioner / Expert)", "Vulnerable feature: which request or parameter", "Hypothesis: what you expected and why",
                "Proof: the request you changed and the response that confirmed it", "Impact: what an attacker gains", "Fix: the code-level fix, plus a defence-in-depth layer", "Time taken and whether you needed the solution"]
LAB_EXAMPLE = [("Lab", "SQL injection vulnerability in WHERE clause allowing retrieval of hidden data (Apprentice)"), ("Vulnerable feature", "The product category filter: /filter?category=Gifts"),
               ("Hypothesis", "The category is concatenated into SELECT … WHERE category = '…' AND released = 1."),
               ("Proof", "A category value of ' OR 1=1-- made the condition always true and commented out the released check; unreleased products appeared."),
               ("Impact", "Reading data the application meant to hide; similar flaws can expose whole tables."), ("Fix", "Parameterised query; least-privilege database account; generic error pages."),
               ("Time", "15 minutes, no solution needed.")]
STRIDE = [
 ("Spoofing", "Stolen tenant credentials or long-lived access keys used by someone else", "Roles with temporary credentials; MFA on human users; short session duration; no access keys in code"),
 ("Tampering", "A tenant re-tags a resource or itself to another tenant; someone edits or deletes log files", "Explicit deny on tag changes (aws:TagKeys); CloudTrail log file validation; S3 Object Lock or a separate log account"),
 ("Repudiation", "A tenant denies having accessed or changed data", "CloudTrail management and S3 data events; logs in a bucket tenants cannot write to"),
 ("Information disclosure", "Tenant A reads tenant B's objects; a bucket becomes public; data read over plain HTTP", "ABAC prefix and tag conditions plus explicit deny; S3 Block Public Access; bucket policy denying aws:SecureTransport = false; SSE-KMS"),
 ("Denial of service", "A tenant deletes or overwrites another's data, or runs up costs (data events, requests)", "Isolation as above; S3 versioning; AWS Budgets alerts; CloudWatch alarms on unusual request counts"),
 ("Elevation of privilege", "A tenant attaches policies to itself or passes a more powerful role", "No iam:Attach*/Put*/PassRole for tenant roles; permission boundaries; Access Analyzer checks; the AccessDenied alarm catches attempts"),
]
CMDS = [
 ("Files", [("ls -la", "list all files, including hidden ones, with permissions"), ("find / -perm -4000 -type f 2>/dev/null", "SUID binaries (privilege escalation check)"), ("grep -rni 'password' .", "search recursively, case-insensitive, with line numbers"), ("chmod 600 key.pem", "owner read/write only"), ("file x; strings x | less", "what a file is; readable text inside a binary"), ("sha256sum x", "hash to check integrity")]),
 ("Processes and users", [("ps aux", "every process with its owner"), ("sudo -l", "what you may run with sudo"), ("id; whoami", "your user and groups"), ("journalctl -u ssh --since today", "service logs (systemd)"), ("tail -f /var/log/auth.log", "follow login attempts (Debian/Ubuntu)")]),
 ("Network", [("ip a", "interfaces and addresses"), ("ss -tulpn", "listening ports and the process behind each"), ("ping -c 4 host", "reachability"), ("traceroute host", "path to a host"), ("dig example.com A +short", "DNS lookup"), ("curl -sI https://example.com", "response headers only"), ("nc -zv host 1-1024", "simple port check (only on systems you may test)"), ("nmap -sV -p- target", "service scan (only on systems you are allowed to scan)"), ("tcpdump -i any port 53", "capture DNS packets (needs root)")]),
 ("Encoding and transfer", [("echo aGk= | base64 -d", "decode base64"), ("xxd file | head", "hex dump"), ("ssh -p 2220 user@host", "SSH to a non-default port"), ("scp -P 2220 user@host:file .", "copy a file over SSH (capital P)")]),
]
WEB = [
 ("SQL injection", "sql-injection", "Input concatenated into a SQL query", "Quote or boolean changes alter results or errors", "Parameterised queries; least-privilege DB user"),
 ("Cross-site scripting", "cross-site-scripting", "Unescaped input rendered as HTML or JavaScript", "Input reflected in the page or DOM unencoded", "Context-aware output encoding; CSP; HttpOnly cookies"),
 ("CSRF", "csrf", "A site performs actions using cookies the browser sends automatically", "State-changing requests without a token or SameSite cookies", "CSRF tokens; SameSite=Lax/Strict; re-auth for sensitive actions"),
 ("Access control / IDOR", "access-control", "The app checks login but not ownership", "Change an id in a URL or body and see another user's data", "Check ownership on every request server-side; deny by default"),
 ("Authentication", "authentication", "Weak login, reset or session handling", "No rate limit, user enumeration, predictable reset tokens", "Rate limits, MFA, generic errors, strong session handling"),
 ("SSRF", "ssrf", "The server fetches a URL the user controls", "A URL parameter that the server requests", "Allowlist destinations; block internal ranges and metadata endpoints"),
 ("Path traversal", "file-path-traversal", "File names from input reach the file system", "../ sequences change which file is read", "Map ids to files; canonicalise and check the base directory"),
 ("OS command injection", "os-command-injection", "Input reaches a shell command", "Separators such as ; or | change behaviour", "Avoid the shell; pass arguments as a list; validate strictly"),
 ("XXE", "xxe", "XML parser resolves external entities", "XML input accepted with a DOCTYPE", "Disable DTDs and external entities in the parser"),
 ("Insecure deserialization", "deserialization", "Untrusted data turned into objects", "Serialised objects in cookies or parameters", "Do not deserialise untrusted data; use JSON with schemas; sign data"),
 ("File upload", "file-upload", "Uploaded files executed or served unsafely", "Upload accepts any type or keeps the name", "Allowlist types, rename, store outside the web root, scan"),
 ("CORS misconfiguration", "cors", "Any origin allowed to read responses with credentials", "Access-Control-Allow-Origin reflects the request origin", "Fixed allowlist; never * with credentials"),
 ("JWT flaws", "jwt", "Token signature not verified properly", "alg changes accepted, weak secrets, no expiry check", "Fix the algorithm list, strong secret or keys, check exp"),
]
def binaries_present():
    want = ["ls", "find", "grep", "chmod", "file", "strings", "sha256sum", "ps", "sudo", "id", "whoami", "journalctl", "tail", "ip", "ss", "ping", "traceroute", "dig", "curl", "nc", "nmap", "tcpdump", "base64", "xxd", "ssh", "scp"]
    return {b: shutil.which(b) is not None for b in want}
PRESENT = binaries_present()
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    ix = [("CTF write-up template and example", "ctf"), ("PortSwigger lab note template and example", "lab"), ("STRIDE threat model of TenantWall", "stride"), ("Linux and networking commands", "cmds"), ("Web security by vulnerability class", "web")]
    rows = "".join(f'<tr><td><a href="#{a}">{t}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for t, a in ix)
    out = [f'''<section class="cover"><p class="eb">SECURITY · LAB NOTEBOOK</p><h1>Security lab<br><span>notebook</span></h1>
<p class="lead">Templates for writing up CTF challenges and PortSwigger labs (with a worked example of each), a STRIDE threat model of TenantWall, a command sheet for labs, and a web-security sheet by vulnerability class. Good write-ups are the evidence behind "security" on your resume: publish them on GitHub or a blog.</p>
<p class="how"><b>Rules.</b> Practise only on platforms built for it (OverTheWire, PortSwigger Web Security Academy, picoCTF, TryHackMe, your own VMs) or systems you have written permission to test. Do not publish flags or passwords that a platform asks you to keep private.</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    kv = lambda pairs: "".join(f"<tr><td class=k>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in pairs)
    out.append(f'<section class="sec" id="ctf"><h2>CTF write-up<a class="back" href="#top">↑ Index</a></h2><h3>Template</h3><ol>{"".join(f"<li>{E(x)}</li>" for x in CTF_TEMPLATE)}</ol><h3>Worked example</h3><table class="kv"><tbody>{kv(CTF_EXAMPLE)}</tbody></table><p class="meta">Level page: <a href="https://overthewire.org/wargames/bandit/">overthewire.org/wargames/bandit</a>. Knowledge Base: <a href="{KB}ctf">CTF</a>.</p></section>')
    out.append(f'<section class="sec" id="lab"><h2>PortSwigger lab note<a class="back" href="#top">↑ Index</a></h2><h3>Template</h3><ol>{"".join(f"<li>{E(x)}</li>" for x in LAB_TEMPLATE)}</ol><h3>Worked example</h3><table class="kv"><tbody>{kv(LAB_EXAMPLE)}</tbody></table><p class="meta">All labs: <a href="{PS}all-labs">portswigger.net/web-security/all-labs</a>. Knowledge Base: <a href="{KB}sqli">SQL injection</a>.</p></section>')
    out.append(f'<section class="sec" id="stride"><h2>STRIDE threat model: TenantWall<a class="back" href="#top">↑ Index</a></h2><p class="meta">Asset: each tenant\'s objects and instances. Attacker: a tenant, or anyone with a stolen tenant credential. Trust boundary: the IAM policy evaluation between tenant roles and shared resources.</p><table class="t"><thead><tr><th>Threat</th><th>Example in TenantWall</th><th>Mitigation</th></tr></thead><tbody>{"".join(f"<tr><td class=k>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in STRIDE)}</tbody></table><p class="meta">Use this table in the paper\'s threat-model section; the mitigations map to the policies in <code>generated/tenantwall/</code>. Knowledge Base: <a href="{KB}threat-modelling">threat modelling</a>, <a href="{KB}tenantwall">TenantWall</a>.</p></section>')
    cm = "".join(f'<h3>{E(g)}</h3><table class="t"><tbody>{"".join(f"<tr><td class=c><code>{E(c)}</code></td><td>{E(d)}</td></tr>" for c, d in items)}</tbody></table>' for g, items in CMDS)
    out.append(f'<section class="sec" id="cmds"><h2>Linux and networking commands<a class="back" href="#top">↑ Index</a></h2>{cm}<p class="meta">Scanning tools (nmap, nc, tcpdump) only on machines you own or are allowed to test.</p></section>')
    out.append(f'<section class="sec" id="web"><h2>Web security by vulnerability class<a class="back" href="#top">↑ Index</a></h2><table class="t"><thead><tr><th>Class</th><th>Cause</th><th>How to spot it</th><th>Fix</th></tr></thead><tbody>{"".join(f"<tr><td class=k><a href={chr(34)}{PS}{s}{chr(34)}>{E(n)}</a></td><td>{E(c)}</td><td>{E(h)}</td><td>{E(f)}</td></tr>" for n, s, c, h, f in WEB)}</tbody></table><p class="meta">Each class links to its PortSwigger Web Security Academy topic, which has free labs. Knowledge Base: <a href="{KB}owasp">OWASP Top 10</a>.</p></section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.8pt/1.45 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } code { font: 400 7.6pt "JetBrains Mono"; font-variant-ligatures: none; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; }
.lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; } table { border-collapse: collapse; width: 100%; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
.ix td { padding: 2.2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2.5mm; display: flex; align-items: baseline; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
h3 { font: 700 10pt "Space Grotesk"; color: #1d4ed8; margin: 3.5mm 0 1.2mm; } ol { padding-left: 5mm; margin: 0; } li { margin-bottom: 1mm; } .meta { color: #475569; font-size: 8.4pt; margin-top: 3mm; }
.kv td, .t td { border-bottom: 1px solid #e2e8f0; padding: 1.5mm 2mm; vertical-align: top; } .k { font-weight: 700; color: #0f172a; width: 34mm; } .c { width: 78mm; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "lab.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/lab.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = ["ctf", "lab", "stride", "cmds", "web"]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for t, k in [("CTF write-up", "ctf"), ("Lab note", "lab"), ("STRIDE: TenantWall", "stride"), ("Commands", "cmds"), ("Web security", "web")]: w.add_outline_item(t, d2[k] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Security lab notebook"}); w.write(str(OUT / "security-lab-notebook.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "lab.html"): (SRC / f).unlink()
print(NP, "pages", d2, "binaries present here:", sum(PRESENT.values()), "/", len(PRESENT), "missing:", [b for b, ok in PRESENT.items() if not ok])
