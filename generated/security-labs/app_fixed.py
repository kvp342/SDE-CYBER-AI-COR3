"""The same app with the bugs fixed: parameterised SQL, escaped output plus a Content-Security-Policy, and a simple
per-IP lockout after 5 failed logins in 60 seconds. Run it only on 127.0.0.1."""
import sqlite3, logging, time
from collections import defaultdict, deque
from html import escape
from flask import Flask, request
app = Flask(__name__)
log = logging.getLogger("auth.fixed"); log.setLevel(logging.INFO); log.propagate = False   # its own log file
_h = logging.FileHandler("auth.log"); _h.setFormatter(logging.Formatter("%(asctime)s %(message)s")); log.addHandler(_h)
FAILS = defaultdict(deque)                                   # ip -> times of recent failures

def db():
    c = sqlite3.connect(":memory:")
    c.executescript("""CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, secret TEXT);
    INSERT INTO users VALUES (1, 'alice', 'wonderland', 'alice-api-key'), (2, 'bob', 'builder', 'bob-api-key');
    CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER);
    INSERT INTO products VALUES (1, 'laptop', 60000), (2, 'phone', 30000), (3, 'pen', 20);""")
    return c

@app.after_request
def headers(resp):
    resp.headers["Content-Security-Policy"] = "default-src 'self'"
    return resp

@app.route("/search")
def search():
    q = request.args.get("q", "")
    rows = db().execute("SELECT name, price FROM products WHERE name LIKE ?", (f"%{q}%",)).fetchall()   # FIX: parameter
    return {"results": rows}

@app.route("/greet")
def greet():
    return f"<h1>Hello {escape(request.args.get('name', 'guest'))}</h1>"          # FIX: escape before HTML

@app.route("/login", methods=["POST"])
def login():
    ip, now = request.remote_addr, time.time()
    recent = FAILS[ip]
    while recent and now - recent[0] > 60: recent.popleft()
    if len(recent) >= 5: return ("too many attempts, wait a minute", 429)       # FIX: lockout
    u, p = request.form.get("user", ""), request.form.get("password", "")
    row = db().execute("SELECT id FROM users WHERE name = ? AND password = ?", (u, p)).fetchone()   # FIX: parameters
    log.info("login %s user=%s ip=%s", "ok" if row else "fail", u, ip)
    if not row: recent.append(now)
    return ("welcome", 200) if row else ("invalid", 401)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
