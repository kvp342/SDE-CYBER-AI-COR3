"""DELIBERATELY VULNERABLE practice app for Lab 5 and Lab 6. Run it only on 127.0.0.1, never on a network.
Bugs on purpose: SQL injection in /search and /login, reflected XSS in /greet, no rate limit on /login."""
import sqlite3, logging
from flask import Flask, request
app = Flask(__name__)
log = logging.getLogger("auth.vulnerable"); log.setLevel(logging.INFO); log.propagate = False   # its own log file
_h = logging.FileHandler("auth.log"); _h.setFormatter(logging.Formatter("%(asctime)s %(message)s")); log.addHandler(_h)

def db():
    c = sqlite3.connect(":memory:")
    c.executescript("""CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, secret TEXT);
    INSERT INTO users VALUES (1, 'alice', 'wonderland', 'alice-api-key'), (2, 'bob', 'builder', 'bob-api-key');
    CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER);
    INSERT INTO products VALUES (1, 'laptop', 60000), (2, 'phone', 30000), (3, 'pen', 20);""")
    return c

@app.route("/search")
def search():
    q = request.args.get("q", "")
    sql = f"SELECT name, price FROM products WHERE name LIKE '%{q}%'"            # BUG: input pasted into SQL
    rows = db().execute(sql).fetchall()
    return {"results": rows}

@app.route("/greet")
def greet():
    name = request.args.get("name", "guest")
    return f"<h1>Hello {name}</h1>"                                             # BUG: input pasted into HTML

@app.route("/login", methods=["POST"])
def login():
    u, p = request.form.get("user", ""), request.form.get("password", "")
    row = db().execute(f"SELECT id FROM users WHERE name = '{u}' AND password = '{p}'").fetchone()   # BUG: SQL injection
    log.info("login %s user=%s ip=%s", "ok" if row else "fail", u, request.remote_addr)
    return ("welcome", 200) if row else ("invalid", 401)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
