"""Network programming project guide. Run from the repo root: python3 generated/netproj/test_net.py && python3 generated/src/netproj.py"""
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
MAN = lambda n, sect=2: f"https://man7.org/linux/man-pages/man{sect}/{n}.{sect}.html"
RFC = ("https://www.rfc-editor.org/rfc/rfc9112", "RFC 9112: HTTP/1.1 message syntax")
sec("what", "What you build and why", UL([
 "<b>chat_server.cpp:</b> one thread serves many clients with <code>poll()</code>; each line a client sends goes to every other client. About 70 lines.",
 "<b>http_server.cpp:</b> a minimal HTTP/1.1 server with <code>GET /</code> and <code>GET /hello?name=…</code>, and 404, 405 and 400 for everything else. The request handling is a pure function, so it is easy to test.",
 "<b>test_net.py:</b> builds both with AddressSanitizer, starts them on free localhost ports and checks 11 behaviours over real sockets, including a line split across two TCP sends.",
 "<b>Why:</b> networking questions (\"what happens when you type a URL\", \"TCP vs UDP\", \"how does a server handle many clients\") come up in almost every SDE and security interview. Having written the syscalls yourself makes the answers concrete. It is also a solid small C++ project for your resume."]) +
 "<h3>Build and run (Linux, macOS or WSL)</h3><pre>" + E("""cd generated/netproj
g++ -std=c++17 -Wall -Wextra -O2 chat_server.cpp -o chat_server && ./chat_server 9000
nc 127.0.0.1 9000          # in two more terminals; type lines in each
g++ -std=c++17 -Wall -Wextra -O2 http_server.cpp -o http_server && ./http_server 8080
curl -i "127.0.0.1:8080/hello?name=Asha"
python3 test_net.py        # 11 checks""") + "</pre>")
sec("calls", "The system calls, in order", T(["Call", "What it does", "What to say in an interview"], [
 ["<a href='" + MAN("socket") + "'>socket</a>", "Creates an endpoint; returns a file descriptor", "Everything in Unix is a file descriptor; AF_INET + SOCK_STREAM means TCP over IPv4"],
 ["<a href='" + MAN("setsockopt") + "'>setsockopt</a> SO_REUSEADDR", "Lets the server bind again while old connections sit in TIME_WAIT", "Without it a quick restart fails with 'Address already in use'"],
 ["<a href='" + MAN("bind") + "'>bind</a>", "Attaches the socket to an address and port", "127.0.0.1 = this machine only; 0.0.0.0 = every interface (exposed)"],
 ["<a href='" + MAN("listen") + "'>listen</a>", "Marks it as a server socket with a backlog queue", "The kernel completes handshakes and queues them before accept"],
 ["<a href='" + MAN("accept") + "'>accept</a>", "Takes one finished connection; returns a new fd for it", "The listening fd stays open; one fd per client"],
 ["<a href='" + MAN("poll") + "'>poll</a>", "Waits until any of many fds is readable", "One thread, many clients; epoll scales better for thousands"],
 ["<a href='" + MAN("recv") + "'>recv</a>", "Reads available bytes; 0 means the peer closed", "It returns whatever has arrived, not a whole message"],
 ["<a href='" + MAN("send") + "'>send</a>", "Writes bytes; may write fewer than asked", "Loop until all are sent; MSG_NOSIGNAL avoids SIGPIPE on a closed peer"],
 ["<a href='" + MAN("close") + "'>close</a>", "Releases the fd; TCP sends FIN", "The side that closes first goes to TIME_WAIT"]]))
sec("stream", "TCP is a byte stream: framing", "<p>TCP keeps the order of bytes but not your message boundaries. One <code>send</code> of 20 bytes can arrive as two <code>recv</code>s of 10, and two sends can arrive as one. The chat server therefore keeps a buffer per client and only acts on complete lines; the test sends half a line, waits, then sends the rest, and checks it arrives whole.</p><pre>" + E("""std::string& b = inbuf[fd]; b.append(buf, n);          // keep what arrived
size_t nl;
while ((nl = b.find('\\n')) != std::string::npos) {   // act only on complete lines
    std::string line = ... b.substr(0, nl + 1); b.erase(0, nl + 1);
    for (auto& p : fds) if (p.fd != lfd && p.fd != fd) send_all(p.fd, line);
}""") + "</pre>" + UL(["Other framings: a length prefix (binary protocols), or a delimiter (HTTP headers end with a blank line, \\r\\n\\r\\n).", "send() can also be partial: send_all() loops until everything is written."]))
sec("http", "What the HTTP server shows", UL([
 "A request is a request line (<code>GET /path HTTP/1.1</code>), headers, a blank line, then an optional body. The server reads until \\r\\n\\r\\n." + S(*RFC),
 "The response needs a status line, Content-Length (or chunked encoding) and the blank line; <code>Connection: close</code> keeps it one request per connection.",
 "405 must include an <code>Allow</code> header; 400 is for requests that cannot be parsed.",
 "Security points you can mention: the server binds to 127.0.0.1 only, caps the header size at 8 KB, and never trusts the path (no file serving, so no path traversal). A real server would also add timeouts against slow clients (Slowloris)."]))
sec("questions", "Interview questions this prepares you for", T(["Question", "Short answer"], [
 ["How does one thread serve many clients?", "I/O multiplexing: poll/epoll waits on all sockets and the loop handles whichever are ready; no thread per client."],
 ["poll vs epoll?", "poll passes the whole list every call (O(n)); epoll keeps the set in the kernel and returns only ready fds, so it scales to many thousands."],
 ["What does recv returning 0 mean?", "The peer closed its side cleanly (FIN). Negative means an error."],
 ["Why can send write fewer bytes than asked?", "The kernel send buffer is full; loop, or use non-blocking sockets and wait for POLLOUT."],
 ["What is TIME_WAIT and why SO_REUSEADDR?", "The side that closes first waits 2 × MSL so late packets die; SO_REUSEADDR lets a server rebind meanwhile."],
 ["Threads vs event loop?", "Threads are simple but cost memory and context switches; an event loop is cheap per connection but every handler must be non-blocking."],
 ["What happens when you type a URL?", "DNS lookup, TCP handshake, TLS handshake, HTTP request, server work, response, rendering. Your server implements the HTTP step."]]))
sec("next", "Extend it and put it on your resume", UL([
 "Non-blocking sockets and epoll; a thread pool for the HTTP server; keep-alive; serving files safely (realpath and a base-directory check).",
 "Usernames and /commands in the chat; a load test (many clients) with timings.",
 "Resume line: \"Built a single-threaded poll()-based chat server and an HTTP/1.1 server in C++17, with framing and partial-send handling, tested over real sockets under AddressSanitizer.\"",
 "Related: " + K("generated/linux-git-debugging-sheet.pdf", "Linux and debugging sheet") + ", " + K("generated/security-labs-workbook.pdf", "security labs (packet capture)") + "."]))
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
    out = [f'''<section><p class="eb">PROJECT · NETWORK PROGRAMMING IN C++</p><h1>Sockets from scratch<br><span>a chat server and an HTTP server</span></h1>
<p class="lead">A small, complete C++ project that turns networking theory into code you wrote: a poll()-based multi-client chat server and a minimal HTTP/1.1 server, with tests over real sockets. Each page explains what the code shows and what to say about it in an interview.</p>
<table class="ix"><thead><tr><th>Section</th><th class="pg">Page</th></tr></thead><tbody>{ix}</tbody></table>
<p class="note">Code: <code>generated/netproj/</code> (chat_server.cpp, http_server.cpp, test_net.py). All 11 socket tests pass under AddressSanitizer and UndefinedBehaviorSanitizer.</p></section>''']
    for n, (i, t, b) in enumerate(SEC):
        out.append(f'<section class="sec" id="{i}"><h2><span class="num">{n + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2>{b}</section>')
    out.append('<section class="sec" id="src"><h2><span class="num">··</span>Sources<a class="back" href="#top">↑ Index</a></h2><p>Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.</p><ol class="src">'
               + "".join(f'<li><a href="{u}">{E(l)}</a><br>{E(u)}</li>' for u, l in SOURCES) + "</ol></section>")
    return "".join(out)
js = SRC / "rn.js"
def render(pages, name):
    (SRC / "net.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/net.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "n1.pdf"); d2, n2 = render(d1, "n2.pdf"); assert n1 == n2 and all(d1[i] == d2[i] for i, _, _ in SEC)
w = PdfWriter(clone_from=PdfReader(str(SRC / "n2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for n, (i, t, _) in enumerate(SEC): w.add_outline_item(f"{n + 1}. {t}", d2[i] - 1, fit=Fit.fit())
w.add_outline_item("Sources", d2["src"] - 1, fit=Fit.fit())
NP = len(w.pages)
for k, pg in enumerate(w.pages):
    if k == 0: continue
    buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
    cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{k + 1} / {NP}"); cv.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Network programming project"}); w.write(str(OUT / "network-programming-project.pdf"))
for f in ("n1.pdf", "n2.pdf", "rn.js", "net.html"): (SRC / f).unlink()
print(NP, "pages;", len(USED), "kit links;", len(SOURCES), "sources;", d2)
