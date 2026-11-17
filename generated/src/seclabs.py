"""Security labs workbook PDF. The code lives in generated/security-labs/ (tested with pytest there); the expected outputs
below were captured by running each lab on Linux on 17 Nov 2026. Run from the repo root: python3 generated/src/seclabs.py"""
import html, io, pathlib, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; LAB = OUT / "security-labs"
GH = "https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/security-labs/"
E = html.escape
for f in ("app_vulnerable.py", "app_fixed.py", "detect_bruteforce.py", "crack_lab.py", "cli_labs.sh", "test_labs.py", "README.md"): assert (LAB / f).exists(), f
LABS = [
 dict(id="perms", title="Linux permissions and SUID", mins=40, why="Every privilege-escalation write-up starts here, and interviewers ask what chmod 750 means.",
  setup="Any Linux machine, WSL or VM. Work as a normal user: root ignores permissions. Create a second user (sudo useradd -m other) to test access.",
  steps=["mkdir -m 777 /tmp/lab1 && cd /tmp/lab1", "echo \"secret notes\" > notes.txt && chmod 640 notes.txt && ls -l notes.txt", "sudo -u other cat /tmp/lab1/notes.txt        # denied: others have no read bit",
         "chmod 644 notes.txt && sudo -u other cat notes.txt   # now readable", "sudo -u other sh -c 'echo x >> /tmp/lab1/notes.txt'   # still no write bit",
         "cp /usr/bin/id myid && chmod u+s myid && ls -l myid", "sudo -u other ./myid -u     # runs with YOUR uid: that is SUID", "find /usr/bin -perm -4000 -type f      # SUID programs on the system"],
  out="-rw-r----- labuser  notes.txt\ncat: /tmp/lab1/notes.txt: Permission denied\nsecret notes\nsh: 1: cannot create /tmp/lab1/notes.txt: Permission denied\n-rwsr-xr-x  myid\n30033            <- labuser's uid, although 'other' ran it\n/usr/bin/sudo  /usr/bin/passwd  /usr/bin/su  /usr/bin/mount ...",
  note=["Permission string of each file before and after, and what each bit allowed or blocked.", "Which SUID programs exist and why each needs root (passwd edits /etc/shadow).", "One sentence: why a writable SUID root binary is a privilege-escalation hole."],
  defend="Least privilege: no SUID on custom programs, umask 027 for sensitive users, audit SUID files regularly (find / -perm -4000)."),
 dict(id="scan", title="Port scanning your own machine", mins=30, why="Shows what 'open', 'closed' and 'filtered' mean, and how a service looks from inside versus outside.",
  setup="sudo apt install nmap. Scan only 127.0.0.1 or a VM you own on a host-only network.",
  steps=["python3 -m http.server 8000 --bind 127.0.0.1 &", "ss -tlnp | grep 8000             # inside view: who listens", "nmap -sT -p 7990-8010 127.0.0.1   # outside view", "nmap -sV -p 8000 127.0.0.1        # version detection", "kill %1"],
  out="LISTEN 0 5 127.0.0.1:8000 0.0.0.0:* users:((\"python3\",...))\nPORT     STATE  SERVICE\n7999/tcp closed irdmi2\n8000/tcp open   http-alt\n8001/tcp closed vcom-tunnel\n...\n8000/tcp open  http    SimpleHTTPServer 0.6 (Python 3.13)",
  note=["The inside view (ss) and the outside view (nmap) side by side.", "Why closed ports answer at once (RST) but filtered ones time out (try with a firewall rule on a VM).", "What -sV revealed, and why version banners help attackers."],
  defend="Bind services to 127.0.0.1 unless they must be public; close what you do not use; hide version banners; firewall by default-deny."),
 dict(id="wire", title="HTTP vs HTTPS on the wire", mins=45, why="You will be asked what TLS protects. Seeing a password in a capture answers it for good.",
  setup="sudo apt install tcpdump tshark curl openssl (or use Wireshark's GUI on the loopback interface).",
  steps=["python3 -m http.server 8000 --bind 127.0.0.1 &", "sudo tcpdump -i lo -w http.pcap -U port 8000 &", "curl -s \"http://127.0.0.1:8000/?user=alice&password=hunter2\" > /dev/null; sudo kill %2",
         "tshark -r http.pcap -Y \"tcp.flags.syn==1 || http.request\" -T fields -e frame.number -e tcp.flags.str -e http.request.uri", "strings http.pcap | grep hunter2",
         "openssl req -x509 -newkey rsa:2048 -nodes -keyout k.pem -out c.pem -days 1 -subj /CN=localhost", "openssl s_server -accept 8443 -cert c.pem -key k.pem -www -quiet &",
         "sudo tcpdump -i lo -w tls.pcap -U port 8443 &   then   curl -sk https://127.0.0.1:8443/?user=alice&password=hunter2", "tshark -r tls.pcap -Y tls.handshake -T fields -e frame.number -e tls.handshake.type", "strings tls.pcap | grep -c hunter2"],
  out="1  ··········S·                       <- SYN\n2  ·······A··S·                       <- SYN-ACK\n4  ·······AP···  /?user=alice&password=hunter2\nhunter2 found in http.pcap: 1\n4  1                                  <- TLS ClientHello\n6  2                                  <- TLS ServerHello\nhunter2 found in tls.pcap: 0",
  note=["The three-way handshake frames and their flags.", "The plaintext request in the HTTP capture and its absence in the TLS capture.", "What TLS still leaks: IPs, ports, timing, sizes and (without ECH) the server name."],
  defend="HTTPS everywhere with HSTS; never send secrets in URLs (they land in logs and history even over HTTPS)."),
 dict(id="hash", title="Hashing and cracking your own test hashes", mins=30, why="Explains in numbers why passwords need salt and a slow hash, and why long passphrases win.",
  setup="python3 generated/security-labs/crack_lab.py (standard library only). It makes hashes of three test passwords and runs a 20-word dictionary attack on them.",
  steps=["python3 crack_lab.py", "Edit TEST_PASSWORDS: add one of your old weak passwords' patterns (never a real current password) and run again", "Change n=2**14 to 2**15 in scrypt() and compare the time"],
  out="sunshine        MD5, no salt     CRACKED: sunshine   tried  7      0.04 ms\nsunshine        scrypt + salt    CRACKED: sunshine   tried  7    355.11 ms\nindia123        SHA-256 + salt   CRACKED: india123   tried 18      0.03 ms\ncorrect-horse-battery-staple  scrypt + salt  not found  tried 20  909.53 ms",
  note=["Salt does not save a weak password from a dictionary attack; it stops precomputed tables and makes equal passwords hash differently.", "scrypt made each guess roughly ten thousand times slower than MD5 here: that is the whole point.", "The passphrase survived because it is not in any list, not because of the hash."],
  defend="Store passwords with Argon2id, scrypt or bcrypt and a unique salt; check new passwords against breached lists; allow long passphrases (NIST SP 800-63B)."),
 dict(id="webapp", title="Find and fix SQL injection and XSS", mins=60, why="The two web bugs every security interview and PortSwigger path starts with, found and fixed in code you control.",
  setup="pip install flask; cd generated/security-labs; python app_vulnerable.py (serves on 127.0.0.1:5000). The fixed version is app_fixed.py on port 5001.",
  steps=["curl \"http://127.0.0.1:5000/search?q=lap\"                                  # normal", "curl -G http://127.0.0.1:5000/search --data-urlencode \"q=x' UNION SELECT name, password FROM users --\"",
         "curl -X POST -d \"user=alice' --&password=anything\" http://127.0.0.1:5000/login", "curl -G http://127.0.0.1:5000/greet --data-urlencode \"name=<script>alert(1)</script>\"",
         "Repeat all three against port 5001 (app_fixed.py)", "Read the diff: parameterised queries, html.escape, Content-Security-Policy", "python -m pytest -q test_labs.py"],
  out="{\"results\": [[\"laptop\", 60000]]}\n{\"results\": [[\"alice\", \"wonderland\"], [\"bob\", \"builder\"]]}       <- passwords leaked\nwelcome                                                    <- logged in with no password\n<h1>Hello <script>alert(1)</script></h1>                  <- script runs\n--- fixed app ---\n{\"results\": []}   invalid   <h1>Hello &lt;script&gt;alert(1)&lt;/script&gt;</h1>\n7 passed",
  note=["Each payload, why it worked (the exact SQL or HTML it produced), and the one-line fix.", "Why escaping by hand is fragile and parameters are not.", "What the CSP header adds even if an escape is missed."],
  defend="Parameterised queries everywhere, output encoding by context, a strict CSP, least-privilege database accounts."),
 dict(id="detect", title="Detect a brute-force attack in a log", mins=30, why="The blue-team side: a SOC analyst writes rules like this, and it is a good small project to show.",
  setup="Run app_vulnerable.py, then try 8 wrong passwords for bob (a loop of curl -X POST). Then run detect_bruteforce.py auth.log. Repeat against app_fixed.py.",
  steps=["for p in 123456 password qwerty letmein dragon monkey sunshine iloveyou; do curl -s -o /dev/null -w \"%{http_code} \" -X POST -d \"user=bob&password=$p\" http://127.0.0.1:5000/login; done", "python detect_bruteforce.py auth.log",
         "Same loop against port 5001", "Change the rule: alert at 10 failures in 5 minutes; test it with the slow and fast examples in test_labs.py"],
  out="401 401 401 401 401 401 401 401         <- vulnerable app never slows down\nALERT brute force from 127.0.0.1 at 2026-11-17 11:43:13 (last user tried: bob)\n401 401 401 401 429 429 429 429         <- fixed app: lockout at the 5th failure from this IP\n                                          (the alice' -- attempt in Lab 5 was the first)",
  note=["The detection rule in one sentence and its false-positive risk (shared office IPs).", "Why lockout per IP is weak against password spraying from many IPs, and what helps (per-account limits, MFA).", "How you would send this alert to a SIEM."],
  defend="Rate limits per IP and per account, MFA, alerting on failure bursts, and no difference in the error message for wrong user vs wrong password."),
]
CSS = """@page { size: A4; margin: 13mm 14mm 15mm; } * { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 9pt/1.5 Inter, sans-serif; color: #1e293b; } a { color: #1d4ed8; text-decoration: none; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; } h1 { font: 700 28pt/1.05 "Space Grotesk"; margin: 0 0 3mm; color: #0f172a; } h1 span { color: #c2410c; }
h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; margin: 0 0 1mm; padding-bottom: 1.5mm; border-bottom: 2px solid #c2410c; display: flex; align-items: baseline; }
h2 .num { color: #c2410c; margin-right: 3mm; } h2 .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; color: #64748b; } h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1mm; }
section.sec { break-before: page; } .meta { font: 600 8pt "JetBrains Mono"; color: #475569; margin: 1mm 0 2mm; } table { border-collapse: collapse; width: 100%; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.2mm 2mm; text-align: left; } td { border-bottom: 1px solid #e2e8f0; padding: 1.3mm 2mm; } td.pg { text-align: right; font-family: "JetBrains Mono"; }
pre { font: 400 7.6pt/1.45 "JetBrains Mono"; background: #0f172a; color: #e2e8f0; padding: 2mm 3mm; white-space: pre-wrap; overflow-wrap: anywhere; margin: 1mm 0 2mm; font-variant-ligatures: none; }
pre.out { background: #f1f5f9; color: #0f172a; border-left: 3px solid #059669; } .legal { background: #fef2f2; border-left: 3px solid #b91c1c; padding: 2.5mm 3mm; margin: 3mm 0; }
.note { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; margin: 2mm 0; font-size: 8.6pt; } ul { padding-left: 5mm; margin: 1mm 0; } li { margin-bottom: 1mm; }"""
def body(pages):
    pg = lambda k: str(pages.get(k, "00")) if pages else "00"
    ix = "".join(f'<tr><td><a href="#{l["id"]}">Lab {n + 1}. {E(l["title"])}</a></td><td class="pg">{l["mins"]} min</td><td class="pg"><a href="#{l["id"]}">{pg(l["id"])}</a></td></tr>' for n, l in enumerate(LABS))
    files = " · ".join(f'<a href="{GH}{f}">{f}</a>' for f in ("app_vulnerable.py", "app_fixed.py", "detect_bruteforce.py", "crack_lab.py", "cli_labs.sh", "test_labs.py"))
    out = [f'''<section><p class="eb">SECURITY · HANDS-ON</p><h1>6 security labs<br><span>on your own machine</span></h1>
<p>Six labs that turn the security theory in this kit into things you have done and can talk about: permissions and SUID, port scanning, packet capture of HTTP versus HTTPS, password hashing and cracking, finding and fixing SQL injection and XSS in a small app, and writing a brute-force detection rule. Each lab lists the steps, the output you should see (captured when the labs were tested on Linux), what to write in your lab notebook, and the defence.</p>
<div class="legal"><b>Legal and ethics: read first.</b> Do these labs only on machines you own, a VM you control, or platforms that invite you (TryHackMe, Hack The Box, PortSwigger Academy). Everything here targets 127.0.0.1. In India, accessing a computer without the owner's permission is penalised under Section 43 of the Information Technology Act, 2000, and doing it dishonestly or fraudulently is an offence under Section 66 (imprisonment up to three years) (<a href="https://rm.coe.int/octocom-legal-profile-india-rev/16809e8fe5">Council of Europe legal profile of India</a>). Scanning a college or company network without written permission can end a security career before it starts.</div>
<table><thead><tr><th>Lab</th><th class="pg">Time</th><th class="pg">Page</th></tr></thead><tbody>{ix}</tbody></table>
<p class="note"><b>Code.</b> Everything is in <code>generated/security-labs/</code>: {files}. <code>test_labs.py</code> (7 tests) proves each exploit works on the vulnerable app and fails on the fixed one. Use the security lab notebook template for write-ups, then publish clean versions on GitHub.</p></section>''']
    for n, l in enumerate(LABS):
        out.append(f'''<section class="sec" id="{l["id"]}"><h2><span class="num">LAB {n + 1}</span>{E(l["title"])}<a class="back" href="#top">↑ Index</a></h2>
<p class="meta">About {l["mins"]} minutes</p><p><b>Why.</b> {E(l["why"])}</p><p><b>Setup.</b> {E(l["setup"])}</p>
<h3>Steps</h3><pre>{E(chr(10).join(l["steps"]))}</pre><h3>What you should see</h3><pre class="out">{E(l["out"])}</pre>
<h3>Write in your lab notebook</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in l["note"])}</ul><p class="note"><b>Defence.</b> {E(l["defend"])}</p></section>''')
    return "".join(out)
js = SRC / "rsl.js"
def render(pages, name):
    (SRC / "seclabs.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/seclabs.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "s1.pdf"); d2, n2 = render(d1, "s2.pdf"); assert n1 == n2 and d1 == d2
w = PdfWriter(clone_from=PdfReader(str(SRC / "s2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for n, l in enumerate(LABS): w.add_outline_item(f"Lab {n + 1}. {l['title']}", d2[l["id"]] - 1, fit=Fit.fit())
NP = len(w.pages)
for k, pg in enumerate(w.pages):
    if k == 0: continue
    buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
    cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{k + 1} / {NP}"); cv.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Security labs workbook"}); w.write(str(OUT / "security-labs-workbook.pdf"))
for f in ("s1.pdf", "s2.pdf", "rsl.js", "seclabs.html"): (SRC / f).unlink()
print(NP, "pages", d2)
