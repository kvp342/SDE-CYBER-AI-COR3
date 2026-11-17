"""SOC log-analysis project guide. Run from the repo root: (cd generated/soc-log-analyzer && python3 -m unittest test_logsentry) && python3 generated/src/socproj.py"""
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
ATT = lambda t, name: (f"https://attack.mitre.org/techniques/{t.replace('.', '/')}/", f"MITRE ATT&CK {t} {name}")
sec("what", "What it is and why it helps", UL([
 "<b>logsentry</b> reads SSH auth logs and web access logs, applies six detection rules and writes JSON alerts, each with a severity, an ATT&CK technique and the evidence lines. About 120 lines of standard-library Python in " + K("generated/soc-log-analyzer/", "generated/soc-log-analyzer/") + ".",
 "<b>Why:</b> SOC and security-engineering interviews ask how you would detect brute force, scanning or injection attempts. This project lets you answer with a rule you wrote, tested and can explain, including its limits.",
 "<b>Pairs with:</b> the security labs workbook (Lab 6 is a simpler version of the first rule) and the TenantWall alerting work on AWS."]) +
 "<h3>Run</h3><pre>" + E("""cd generated/soc-log-analyzer
python3 -m logsentry --auth samples/auth.log --web samples/access.log --out alerts.json
python3 -m unittest -v test_logsentry      # 11 tests""") + "</pre><h3>Output on the sample logs</h3><pre>" + E("""parsed 23 auth events and 45 web requests; 8 alerts
[CRITICAL] ssh-success-after-failures from 192.0.2.99 (T1078 Valid Accounts)
[HIGH] ssh-bruteforce from 203.0.113.50 (T1110.001 Password Guessing)
[HIGH] sql-injection from 192.0.2.150 (T1190 Exploit Public-Facing Application)
[HIGH] path-traversal from 198.51.100.34 (T1190)
[MEDIUM] scanner-user-agent from 203.0.113.77 (gobuster) and 192.0.2.150 (sqlmap)
[MEDIUM] web-scanning from 203.0.113.77 (T1595 Active Scanning)
[MEDIUM] xss from 198.51.100.33 (T1190)""") + "</pre>")
sec("rules", "The six rules", T(["Rule", "Logic", "ATT&CK"], [
 ["ssh-bruteforce", "Sliding 60 s window per IP over failed logins; fire once at 5", "T1110.001 Password Guessing" + S(*ATT("T1110.001", "Password Guessing"))],
 ["ssh-success-after-failures", "A success from an IP that had 5+ failures in the previous 10 minutes (critical: the guess may have worked)", "T1078 Valid Accounts" + S(*ATT("T1078", "Valid Accounts"))],
 ["web-scanning", "Sliding 60 s window per IP over 403/404 responses; fire at 20", "T1595 Active Scanning" + S(*ATT("T1595", "Active Scanning"))],
 ["scanner-user-agent", "User agent contains a known tool name", "T1595"],
 ["sql-injection, xss, path-traversal", "Decode the URL twice (attackers double-encode), then match patterns", "T1190 Exploit Public-Facing Application" + S(*ATT("T1190", "Exploit Public-Facing Application"))]]) +
 "<h3>The sliding-window core</h3><pre>" + E("""def burst(events, key, threshold, window):
    q, fired = defaultdict(deque), set()
    for e in sorted(events, key=lambda e: e["ts"]):
        k = key(e); d = q[k]; d.append(e)
        while (e["ts"] - d[0]["ts"]).total_seconds() > window: d.popleft()
        if len(d) >= threshold and k not in fired: fired.add(k); yield k, list(d)""") + "</pre>")
sec("tests", "How it is tested", UL([
 "The sample logs mix attacks with normal activity on purpose: a normal login, a user mistyping a password 3 times, ordinary browsing, a harmless query string. The test asserts exactly the 8 expected alerts and none for the normal IPs.",
 "Edges: 4 failures do not alert and 5 do; 10 failures spread over 10 minutes are not a burst; a second success after the alert does not alert again.",
 "Evasion and false positives: a double-encoded <code>%252e%252e%252f</code> traversal is caught; <code>O'Brien</code>, <code>union station</code> and normal query strings are not.",
 "The command line writes valid JSON and exits with 2 when a critical alert is raised, so it can fail a cron job or CI step.",
 "IPs come from the documentation ranges (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24), so the samples never point at real hosts."]))
sec("limits", "Limits, and how to talk about them", T(["Limit", "Better approach"], [
 ["Per-IP thresholds miss password spraying from many IPs", "Add a per-account rule; combine with MFA"],
 ["Shared NAT or office IPs cause false positives", "Allow-lists, and alerting on success-after-failure rather than failures alone"],
 ["Regex payload matching is easy to evade and noisy", "Log rejected input in the app; use a WAF; treat these alerts as low-confidence signals"],
 ["No state between runs; files only", "Ship logs to a SIEM and run the rules continuously"],
 ["Syslog has no year or time zone", "Use structured JSON logs with ISO timestamps"]]) +
 '<p class="note">Interviewers value honest limits more than big claims. "It catches a burst from one IP; spraying across IPs needs a per-account rule" is a strong answer.</p>')
sec("resume", "On your resume and GitHub", UL([
 "Resume line: \"Built logsentry, a Python log-analysis tool that detects SSH brute force, account compromise, web scanning and injection attempts, mapped to MITRE ATT&CK, with 11 tests including false-positive cases.\"",
 "Push it as its own repository with the README, the samples and a screenshot of the output. Add a GitHub Actions workflow that runs the tests (see " + K("generated/docker-ci-guide.pdf", "the Docker and CI guide") + ").",
 "Next steps: per-account and impossible-travel rules, a Sigma rule export, and an Elastic or Splunk import of the JSON alerts.",
 "Related: " + K("generated/security-labs-workbook.pdf", "security labs workbook") + ", " + K("generated/cyber-security-interview-bank.pdf", "cyber-security interview bank") + "."]))
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
    out = [f'''<section><p class="eb">PROJECT · SECURITY OPERATIONS</p><h1>logsentry<br><span>detect attacks in logs</span></h1>
<p class="lead">A portfolio project for SOC and security-engineering roles: a Python tool that finds SSH brute force, a likely compromised account, web scanning and injection attempts in real log formats, maps each alert to MITRE ATT&amp;CK, and is tested against both attacks and normal activity.</p>
<table class="ix"><thead><tr><th>Section</th><th class="pg">Page</th></tr></thead><tbody>{ix}</tbody></table>
<p class="note">Code: <code>generated/soc-log-analyzer/</code>. 11 tests pass; on the sample logs the tool raises exactly the 8 expected alerts and none for normal activity.</p></section>''']
    for n, (i, t, b) in enumerate(SEC):
        out.append(f'<section class="sec" id="{i}"><h2><span class="num">{n + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2>{b}</section>')
    out.append('<section class="sec" id="src"><h2><span class="num">··</span>Sources<a class="back" href="#top">↑ Index</a></h2><p>Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.</p><ol class="src">'
               + "".join(f'<li><a href="{u}">{E(l)}</a><br>{E(u)}</li>' for u, l in SOURCES) + "</ol></section>")
    return "".join(out)
js = SRC / "rsoc.js"
def render(pages, name):
    (SRC / "soc.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/soc.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
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
w.add_metadata({"/Title": "SOC log-analysis project"}); w.write(str(OUT / "soc-log-analysis-project.pdf"))
for f in ("c1.pdf", "c2.pdf", "rsoc.js", "soc.html"): (SRC / f).unlink()
print(NP, "pages;", len(USED), "kit links;", len(SOURCES), "sources;", d2)
