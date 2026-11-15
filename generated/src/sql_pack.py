"""SQL pack: runs every query in SQLite, writes generated/sql-pack.sql and generated/sql-pack.pdf. Run from the repo root: python3 generated/src/sql_pack.py"""
import html, subprocess, pathlib, io, sys, sqlite3
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
sys.path.insert(0, str(SRC)); from sql_data import SCHEMA, Q
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
TOPICS = ["Basics", "Joins", "Aggregation", "Subqueries", "Window functions", "Performance"]
db = sqlite3.connect(":memory:"); db.executescript(SCHEMA); RES = []
for i, (t, l, top, q, sql, ex, exp) in enumerate(Q, 1):
    st = [s for s in sql.split(";") if s.strip()]
    for s in st[:-1]: db.execute(s)
    cur = db.execute(st[-1]); rows = cur.fetchall(); cols = [c[0] for c in cur.description]
    assert (rows[0] if rows else None) == exp or (exp is None and "USING INDEX" in rows[-1][-1]), (i, t, rows[:3])
    RES.append((cols, rows))
assert len(Q) == 40
# .sql file
sq = ["-- SQL interview pack: sample database and 40 questions. Tested with SQLite " + sqlite3.sqlite_version + ".", "-- Load: sqlite3 practice.db < sql-pack.sql   (or paste the schema into any SQL playground)", "", SCHEMA.strip(), ""]
for i, (t, l, top, q, sql, ex, exp) in enumerate(Q, 1):
    sq += [f"-- Q{i}. {t} [{top}, L{l}]", f"-- {q}", sql, ""]
(OUT / "sql-pack.sql").write_text("\n".join(sq))
def table(cols, rows):
    if not rows: return '<p class="empty">(no rows)</p>'
    fmt = lambda v: "NULL" if v is None else (f"{v:g}" if isinstance(v, float) else v)
    return '<table class="res"><thead><tr>' + "".join(f"<th>{E(c)}</th>" for c in cols) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f'<td class="{"nul" if v is None else ""}">{E(fmt(v))}</td>' for v in r) + "</tr>" for r in rows) + "</tbody></table>"
def schema_html():
    out = []
    for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY rowid"):
        cur = db.execute(f"SELECT * FROM {name}"); rows = cur.fetchall(); cols = [c[0] for c in cur.description]
        out.append(f'<div class="tb"><h3>{name} <span>{len(rows)} rows</span></h3>{table(cols, rows)}</div>')
    return "".join(out)
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td class="n">{i}</td><td><a href="#q{i}">{E(t)}</a></td><td>{E(top)}</td><td class="c"><span class="l{l}">L{l}</span></td><td class="pg"><a href="#q{i}">{pg(f"q{i}")}</a></td></tr>' for i, (t, l, top, *_r) in enumerate(Q, 1))
    out = [f'''<section class="cover"><p class="eb">SQL · INTERVIEW PACK</p><h1>40 SQL questions<br><span>run on a real database</span></h1>
<p class="lead">From filters and joins to window functions, on one small company database (employees, departments, customers, orders, products, logins). Every query was run in SQLite {sqlite3.sqlite_version}; the output shown under it is what it returned. The same schema, data and queries are in <b>sql-pack.sql</b> next to this PDF.</p>
<p class="how"><b>How to use.</b> Read the question, cover the answer, write your query, then compare. Practise online for free on the <a href="https://leetcode.com/studyplan/top-sql-50/">LeetCode SQL 50 study plan</a> or <a href="https://sqlbolt.com/">SQLBolt</a>. Dialect differences (SQLite, MySQL, PostgreSQL) are noted where they matter. <a href="#schema">Sample database →</a></p>
<table class="ix"><thead><tr><th>#</th><th>Question</th><th>Topic</th><th>Level</th><th>Page</th></tr></thead><tbody>{rows}</tbody></table></section>
<section class="sec" id="schema"><h2>The sample database<a class="back" href="#top">↑ Index</a></h2><p class="meta">Small enough to check every answer by hand. Sara has no department, Research has no employees, Farah never ordered, order 3 was cancelled and user 3 has a duplicate login: each is there for a question. See also the <a href="{KB}normalisation">Knowledge Base DBMS pages</a>.</p><div class="schema">{schema_html()}</div></section>''']
    last = None
    for i, ((t, l, top, q, sql, ex, exp), (cols, rs)) in enumerate(zip(Q, RES), 1):
        head = f'<h2 class="tp">{E(top)}<a class="back" href="#top">↑ Index</a></h2>' if top != last else ""
        cls = "sec" if top != last else ""
        last = top
        out.append(f'''<div class="{cls}">{head}<div class="q" id="q{i}"><h3><span class="num">Q{i}</span>{E(t)} <span class="l{l}">L{l}</span><a class="back" href="#top">↑</a></h3><p class="qq">{E(q)}</p>
<pre>{E(sql)}</pre><div class="out"><span class="lb">Output</span>{table(cols, rs)}</div><p class="ex">{E(ex)}</p></div></div>''')
    return "".join(out)
CSS = """@page { size: A4; margin: 12mm 12mm 14mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.8pt/1.42 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 12mm 15mm 8mm; break-after: page; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } h1 { font: 700 28pt/1.05 "Space Grotesk"; margin: 0 0 3mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 18pt; }
.lead { font-size: 9.3pt; color: #475569; margin: 0 0 2mm; } .how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; font-size: 8.5pt; margin: 0 0 3mm; }
table { border-collapse: collapse; } th { font: 600 6.8pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: .8mm 2mm; text-align: left; }
.ix { width: 100%; } .ix td { padding: .25mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 7.9pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .n { color: #94a3b8; font-family: "JetBrains Mono"; } .ix .c { text-align: center; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.l1, .l2, .l3 { font: 600 6.8pt "JetBrains Mono"; border-radius: 4px; padding: 0 5px; } .l1 { background: #dcfce7; color: #166534; } .l2 { background: #fef3c7; color: #92400e; } .l3 { background: #fde2e1; color: #b42318; }
.sec { break-before: page; } h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 3mm; display: flex; align-items: baseline; }
.back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; white-space: nowrap; } .meta { color: #475569; }
.schema { column-count: 2; column-gap: 6mm; } .tb { break-inside: avoid; margin-bottom: 3mm; } .tb h3 { font: 700 9.5pt "JetBrains Mono"; color: #1d4ed8; margin: 0 0 1mm; } .tb h3 span { font: 400 7pt Inter; color: #94a3b8; }
.res td { border-bottom: 1px solid #eef2f7; padding: .5mm 2mm; font: 400 7.2pt "JetBrains Mono"; } .res td.nul { color: #94a3b8; font-style: italic; } .res th { font-size: 6.5pt; text-transform: none; }
.q { break-inside: avoid; margin: 0 0 4.5mm; } .q h3 { font: 700 10.5pt "Space Grotesk"; color: #0f172a; margin: 0 0 1mm; display: flex; align-items: baseline; gap: 2mm; } .num { font: 600 8pt "JetBrains Mono"; color: #c2410c; }
.qq { margin: 0 0 1.5mm; font-size: 9.2pt; } pre { font: 400 7.6pt/1.4 "JetBrains Mono"; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #1d4ed8; padding: 1.8mm 2.5mm; white-space: pre-wrap; margin: 0 0 1.5mm; }
pre { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; } .res td { font-variant-ligatures: none; }
.out { display: flex; gap: 3mm; align-items: flex-start; } .lb { font: 600 6.8pt "JetBrains Mono"; color: #166534; background: #dcfce7; border-radius: 4px; padding: 0 5px; margin-top: .6mm; } .empty { margin: 0; color: #64748b; }
.ex { color: #475569; font-size: 8.3pt; margin: 1.5mm 0 0; }"""
def render(pages, name):
    (SRC / "sql.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js = SRC / "r.js"; js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/sql.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
KEYS = ["schema"] + [f"q{i}" for i in range(1, 41)]
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in KEYS)
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit()); w.add_outline_item("Sample database", d2["schema"] - 1, fit=Fit.fit())
par = {}
for i, (t, l, top, *_r) in enumerate(Q, 1):
    if top not in par: par[top] = w.add_outline_item(top, d2[f"q{i}"] - 1, fit=Fit.fit())
    w.add_outline_item(f"Q{i}. {t}", d2[f"q{i}"] - 1, parent=par[top], fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "SQL interview pack: 40 questions"}); w.write(str(OUT / "sql-pack.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "sql.html"): (SRC / f).unlink()
print(NP, "pages")
