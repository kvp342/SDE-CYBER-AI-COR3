"""PortSwigger and OWASP lab map: each OWASP Top 10:2025 category mapped to free PortSwigger Web Security Academy topics, a suggested
lab order, the 2021 → 2025 changes, and 10 web-security interview questions with answers. Run from the repo root: python3 generated/src/lab_map.py"""
import html, io, pathlib, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
E = lambda s: html.escape(str(s), quote=True); PS = "https://portswigger.net/web-security/"; KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
T = {"access-control": "Access control", "ssrf": "SSRF", "csrf": "CSRF", "cors": "CORS", "file-path-traversal": "Path traversal", "information-disclosure": "Information disclosure",
     "xxe": "XXE", "clickjacking": "Clickjacking", "host-header": "HTTP Host header attacks", "jwt": "JWT attacks", "sql-injection": "SQL injection", "nosql-injection": "NoSQL injection",
     "os-command-injection": "OS command injection", "cross-site-scripting": "Cross-site scripting", "server-side-template-injection": "Server-side template injection",
     "dom-based": "DOM-based vulnerabilities", "llm-attacks": "Web LLM attacks", "logic-flaws": "Business logic vulnerabilities", "race-conditions": "Race conditions",
     "authentication": "Authentication", "oauth": "OAuth authentication", "deserialization": "Insecure deserialization", "prototype-pollution": "Prototype pollution",
     "file-upload": "File upload vulnerabilities", "web-cache-poisoning": "Web cache poisoning", "request-smuggling": "HTTP request smuggling", "api-testing": "API testing"}
OWASP = [
 ("A01", "Broken Access Control", "Users act outside their permissions: other users' data (IDOR), admin functions, forged requests. SSRF is now part of this category.", ["access-control", "ssrf", "csrf", "cors", "file-path-traversal"], "Check ownership on the server for every request; deny by default."),
 ("A02", "Security Misconfiguration", "Unsafe defaults, verbose errors, exposed admin panels, permissive parsers and headers.", ["information-disclosure", "xxe", "clickjacking", "host-header"], "Harden defaults; disable XML external entities; set security headers."),
 ("A03", "Software Supply Chain Failures", "Vulnerable or malicious dependencies, build systems and update channels.", [], "No dedicated Academy topic: practise with pip-audit or npm audit and Dependabot on your own projects."),
 ("A04", "Cryptographic Failures", "Missing or weak encryption, bad key handling, weak password hashing.", ["jwt"], "Use TLS everywhere, strong password hashing (scrypt, Argon2, bcrypt), managed keys (KMS)."),
 ("A05", "Injection", "Untrusted input interpreted as code or queries: SQL, NoSQL, OS commands, templates, XSS. Prompt injection against LLMs is tracked in OWASP's separate Top 10 for LLM Applications; the Academy's Web LLM attacks labs cover it.", ["sql-injection", "nosql-injection", "os-command-injection", "cross-site-scripting", "server-side-template-injection", "dom-based", "llm-attacks"], "Parameterise queries, encode output, never pass input to a shell or template engine."),
 ("A06", "Insecure Design", "Flaws in the design itself: missing limits, broken workflows, trust in client-side checks.", ["logic-flaws", "race-conditions"], "Threat-model features (STRIDE) and test abuse cases, not just happy paths."),
 ("A07", "Authentication Failures", "Weak login, session and token handling: brute force, enumeration, broken OAuth flows.", ["authentication", "oauth", "jwt"], "Rate limits, MFA, generic errors, short-lived tokens with a fixed algorithm."),
 ("A08", "Software or Data Integrity Failures", "Trusting data or code without checking it: unsafe deserialisation, unsigned updates, polluted objects.", ["deserialization", "prototype-pollution", "web-cache-poisoning"], "Do not deserialise untrusted data; sign and verify; freeze or validate object shapes."),
 ("A09", "Security Logging and Alerting Failures", "Attacks go unseen because nothing is logged or nobody is alerted.", [], "No lab topic: TenantWall's CloudTrail → CloudWatch → SNS alerting is your hands-on example."),
 ("A10", "Mishandling of Exceptional Conditions", "Errors handled unsafely: failing open, leaking details in error messages, inconsistent state after failures.", ["information-disclosure", "race-conditions"], "Fail closed; log details, show generic messages; test error paths."),
]
CHANGES = [("Security Misconfiguration", "5th → 2nd"), ("Software Supply Chain Failures", "new (grew out of 'Vulnerable and Outdated Components')"), ("Cryptographic Failures", "2nd → 4th"),
           ("Injection", "3rd → 5th"), ("Insecure Design", "4th → 6th"), ("SSRF", "own category in 2021 → part of Broken Access Control"),
           ("Logging", "'Monitoring' renamed 'Alerting'"), ("Mishandling of Exceptional Conditions", "new at 10th")]
ORDER = [("Weeks 1–2", ["sql-injection", "authentication", "access-control", "file-path-traversal"]), ("Weeks 3–4", ["os-command-injection", "logic-flaws", "information-disclosure", "file-upload"]),
         ("Weeks 5–6", ["ssrf", "xxe", "race-conditions", "nosql-injection", "api-testing"]), ("Weeks 7–8", ["cross-site-scripting", "csrf", "cors", "clickjacking", "dom-based"]),
         ("Weeks 9–10", ["jwt", "oauth", "deserialization", "server-side-template-injection", "prototype-pollution"]), ("Later (Practitioner and Expert)", ["host-header", "web-cache-poisoning", "request-smuggling", "llm-attacks"])]
QA = [("What is the difference between authentication and authorisation?", "Authentication proves who you are (login); authorisation decides what you may do. Broken access control (A01) is an authorisation failure: logged in, but allowed too much."),
      ("How do you prevent SQL injection?", "Parameterised queries so input is never parsed as SQL; least-privilege database accounts; input validation as a second layer. Escaping by hand is fragile."),
      ("Stored vs reflected vs DOM-based XSS?", "Stored is saved on the server and shown to others; reflected comes back in the response to the attacker's link; DOM-based happens entirely in client-side JavaScript. Fix with context-aware output encoding and a Content Security Policy."),
      ("How does CSRF work and how do you stop it?", "The browser sends cookies automatically, so another site can trigger state-changing requests. Use anti-CSRF tokens, SameSite cookies and re-authentication for sensitive actions."),
      ("What is SSRF and why is it dangerous in the cloud?", "The server fetches a URL the attacker controls, reaching internal services or the cloud metadata endpoint, which can expose credentials. Allowlist destinations and block internal ranges; on AWS require IMDSv2."),
      ("What is IDOR?", "Insecure direct object reference: changing an id in a request returns someone else's data because the server does not check ownership. Check ownership on every request (as the backend starter does)."),
      ("How should passwords be stored?", "A slow, salted hash (Argon2id, scrypt or bcrypt), compared in constant time; never plain text or a fast hash such as SHA-256 alone."),
      ("What makes a JWT implementation insecure?", "Accepting alg: none or switching algorithms, weak HMAC secrets, not checking expiry, or trusting unverified claims. Fix the algorithm list and verify signature and expiry."),
      ("What is the same-origin policy, and what does CORS change?", "Scripts can only read responses from their own origin; CORS lets a server allow named other origins. Reflecting any Origin with credentials allowed defeats the protection."),
      ("How would you find vulnerabilities in a web app you are allowed to test?", "Map it (Burp proxy, every request), list inputs and trust boundaries, test each OWASP category on the riskiest features first, confirm impact safely, and write up the fix. Only with permission.")]
def link(slug): return f'<a href="{PS}{slug}">{E(T[slug])}</a>'
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{a}">{t}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for t, a in [("OWASP Top 10:2025 mapped to PortSwigger topics", "map"), ("What changed since 2021", "chg"), ("Suggested lab order", "order"), ("10 interview questions", "qa")])
    out = [f'''<section class="cover"><p class="eb">SECURITY · LAB MAP</p><h1>OWASP Top 10<br><span>mapped to free PortSwigger labs</span></h1>
<p class="lead">Each category of the OWASP Top 10:2025 (released in November 2025, final in January 2026), what it means, which free PortSwigger Web Security Academy topics teach it, and the fix to remember, with a tick box. Then a 10-week lab order and ten interview questions with answers.</p>
<p class="how"><b>Note.</b> The Knowledge Base still describes the 2021 list; interviewers may use either, so learn both names (see the changes page). Topic links go to PortSwigger's topic pages; if one has moved, use <a href="{PS}all-topics">the all-topics page</a>.</p>
<table class="ix"><tbody>{rows}</tbody></table></section>''']
    mrows = "".join(f'<tr><td class=box>☐</td><td class=id>{a}</td><td><b>{E(n)}</b><div class=d>{E(d)}</div></td><td>{"<br>".join(link(s) for s in slugs) or "<i>no dedicated topic</i>"}</td><td class=fx>{E(fx)}</td></tr>' for a, n, d, slugs, fx in OWASP)
    out.append(f'<section class="sec" id="map"><h2>OWASP Top 10:2025 → PortSwigger topics<a class="back" href="#top">↑ Index</a></h2><table class="t"><thead><tr><th></th><th>#</th><th>Category</th><th>Academy topics</th><th>Remember</th></tr></thead><tbody>{mrows}</tbody></table></section>')
    out.append(f'<section class="sec" id="chg"><h2>What changed since 2021<a class="back" href="#top">↑ Index</a></h2><table class="t"><tbody>{"".join(f"<tr><td class=k>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in CHANGES)}</tbody></table><p class="meta">Broken Access Control stays first. Sources: OWASP Top 10:2025 introduction and summaries from Orca Security, Invicti and GitLab (links on the last page).</p></section>')
    orows = "".join(f'<tr><td class=k>{E(w)}</td><td>{" · ".join("☐ " + link(s) for s in slugs)}</td></tr>' for w, slugs in ORDER)
    out.append(f'<section class="sec" id="order"><h2>Suggested lab order<a class="back" href="#top">↑ Index</a></h2><p class="meta">PortSwigger suggests starting with server-side topics, which are simpler, then client-side. Do the Apprentice labs of each topic first; one write-up per topic in your lab notebook (see the security lab notebook).</p><table class="t"><tbody>{orows}</tbody></table><p class="meta">This fits the cyber track in your plan alongside DSA; about 3–4 hours a week.</p></section>')
    out.append(f'<section class="sec" id="qa"><h2>10 web-security interview questions<a class="back" href="#top">↑ Index</a></h2><table class="t"><tbody>{"".join(f"<tr><td class=n>{i + 1}</td><td class=q>{E(q)}</td><td>{E(a)}</td></tr>" for i, (q, a) in enumerate(QA))}</tbody></table>'
               f'<h3>Sources</h3><ul class="src"><li><a href="https://owasp.org/Top10/2025/0x00_2025-Introduction/">OWASP Top 10:2025 introduction</a></li><li><a href="https://orca.security/resources/blog/owasp-top-10-2025-key-changes/">Orca Security: OWASP Top 10 2025 key changes</a></li><li><a href="https://about.gitlab.com/blog/2025-owasp-top-10-whats-changed-and-why-it-matters/">GitLab: 2025 OWASP Top 10, what changed</a></li><li><a href="{PS}all-topics">PortSwigger: all Web Security Academy topics</a></li></ul><p class="meta">See also the <a href="{KB}owasp">OWASP</a> Knowledge Base page.</p></section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.7pt/1.42 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 16mm 15mm; break-after: page; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; }
h1 { font: 700 32pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 18pt; } .lead { font-size: 10pt; color: #475569; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; }
table { border-collapse: collapse; width: 100%; } .ix td { padding: 2.2mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 10.5pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2.5mm; display: flex; align-items: baseline; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.2mm 2mm; text-align: left; } .t td { border-bottom: 1px solid #e2e8f0; padding: 1.5mm 2mm; vertical-align: top; }
.box { width: 5mm; color: #94a3b8; } .id { font: 700 8pt "JetBrains Mono"; color: #c2410c; width: 9mm; } .d { color: #475569; font-size: 8pt; } .fx { color: #166534; width: 46mm; font-size: 8pt; } .k { font-weight: 700; width: 44mm; } .n { color: #94a3b8; font-family: "JetBrains Mono"; width: 6mm; } .q { font-weight: 600; width: 56mm; }
h3 { font: 700 10pt "Space Grotesk"; color: #1d4ed8; margin: 4mm 0 1mm; } .meta { color: #475569; font-size: 8.4pt; margin: 2mm 0; } .src { font-size: 8.2pt; padding-left: 5mm; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "lm.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/lm.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
assert len(OWASP) == 10 and len(QA) == 10 and all(s in T for *_, slugs, _ in OWASP for s in slugs) and all(s in T for _, slugs in ORDER for s in slugs)
assert set(T) == {s for _, slugs in ORDER for s in slugs}, "every topic should appear once in the lab order"
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in ("map", "chg", "order", "qa"))
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for t, k in [("OWASP map", "map"), ("Changes since 2021", "chg"), ("Lab order", "order"), ("Interview questions", "qa")]: w.add_outline_item(t, d2[k] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "PortSwigger and OWASP lab map"}); w.write(str(OUT / "owasp-portswigger-lab-map.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "lm.html"): (SRC / f).unlink()
print(NP, "pages", d2)
