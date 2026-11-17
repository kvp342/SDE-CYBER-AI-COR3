"""Build both servers with sanitizers, start them on free localhost ports, and test them over real sockets.
Run from this folder: python3 test_net.py"""
import http.client, os, socket, subprocess, sys, tempfile, time
HERE = os.path.dirname(os.path.abspath(__file__)); D = tempfile.mkdtemp(); ok = 0
def build(name):
    r = subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-fsanitize=address,undefined", f"{HERE}/{name}.cpp", "-o", f"{D}/{name}"], capture_output=True, text=True)
    assert r.returncode == 0 and "warning" not in r.stderr, r.stderr
def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p
def start(name):
    port = free_port(); p = subprocess.Popen([f"{D}/{name}", str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert "listening" in p.stdout.readline(); return p, port
def check(cond, what):
    global ok; assert cond, what; ok += 1; print("ok  ", what)
def recv_until(sock, text, timeout=3):
    sock.settimeout(timeout); data = b""
    while text.encode() not in data: data += sock.recv(4096)
    return data.decode()
for n in ("chat_server", "http_server"): build(n)
# ---- chat
srv, port = start("chat_server")
try:
    a = socket.create_connection(("127.0.0.1", port)); b = socket.create_connection(("127.0.0.1", port)); c = socket.create_connection(("127.0.0.1", port))
    for s in (a, b, c): recv_until(s, "welcome")
    a.sendall(b"hello everyone\n")
    check("hello everyone" in recv_until(b, "hello everyone") and "hello everyone" in recv_until(c, "hello everyone"), "a line from A reaches B and C")
    a.settimeout(0.3)
    try: echoed = a.recv(4096)
    except socket.timeout: echoed = b""
    check(echoed == b"", "the sender does not get its own line back")
    b.sendall(b"part one, "); time.sleep(0.2); b.sendall(b"part two\n")      # one line split across two TCP sends
    check("part one, part two" in recv_until(a, "part two"), "a line split across two sends arrives whole (byte-stream framing)")
    c.close(); time.sleep(0.2); a.sendall(b"still alive?\n")
    check("still alive?" in recv_until(b, "still alive?"), "server survives a client disconnecting")
    a.close(); b.close()
finally:
    srv.terminate(); err = srv.communicate()[1]
check("ERROR: AddressSanitizer" not in err and "runtime error" not in err, "chat server: no sanitizer errors")
# ---- http
srv, port = start("http_server")
try:
    def get(method, path):
        h = http.client.HTTPConnection("127.0.0.1", port, timeout=3); h.request(method, path); r = h.getresponse(); return r.status, r.read().decode(), dict(r.getheaders())
    st, body, hd = get("GET", "/"); check(st == 200 and body.startswith("hello") and hd["Content-Length"] == str(len(body)), "GET / is 200 with a correct Content-Length")
    st, body, _ = get("GET", "/hello?name=Asha%20K"); check(st == 200 and body == "Hello, Asha K\n", "query string is URL-decoded")
    st, _, _ = get("GET", "/nope"); check(st == 404, "unknown path is 404")
    st, _, hd = get("POST", "/"); check(st == 405 and hd.get("Allow") == "GET", "POST is 405 with an Allow header")
    s = socket.create_connection(("127.0.0.1", port)); s.sendall(b"garbage\r\n\r\n"); check(recv_until(s, "\r\n\r\n").startswith("HTTP/1.1 400"), "malformed request line is 400"); s.close()
finally:
    srv.terminate(); err = srv.communicate()[1]
check("ERROR: AddressSanitizer" not in err and "runtime error" not in err, "http server: no sanitizer errors")
print(f"{ok} checks passed")
