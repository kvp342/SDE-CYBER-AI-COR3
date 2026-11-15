"""Architecture diagram for generated/backend-starter (SVG + PNG). Run from the repo root: python3 generated/src/backend_diagram.py"""
import html, pathlib, subprocess
D = pathlib.Path(__file__).resolve().parents[1] / "backend-starter"; E = html.escape
F = "font-family='Inter, Arial, sans-serif'"
def box(x, y, w, h, t, sub, col):
    s = f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='8' fill='#fff' stroke='{col}' stroke-width='2'/><rect x='{x}' y='{y}' width='{w}' height='6' rx='3' fill='{col}'/><text x='{x+w/2}' y='{y+27}' text-anchor='middle' {F} font-size='14' font-weight='700' fill='#0f172a'>{E(t)}</text>"
    return s + "".join(f"<text x='{x+w/2}' y='{y+46+i*16}' text-anchor='middle' {F} font-size='11.5' fill='#64748b'>{E(l)}</text>" for i, l in enumerate(sub))
def arr(x1, y1, x2, y2, lab="", lx=None, ly=None):
    s = f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='#334155' stroke-width='2' marker-end='url(#a)'/>"
    return s + (f"<text x='{lx or (x1+x2)/2}' y='{ly or (y1+y2)/2-7}' text-anchor='middle' {F} font-size='11' font-weight='600' fill='#334155'>{E(lab)}</text>" if lab else "")
b = "<defs><marker id='a' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='#334155'/></marker></defs><rect width='1000' height='470' fill='#fff'/>"
b += box(20, 150, 170, 90, "Client", ["browser, curl or", "mobile app"], "#8c4fff")
b += f"<rect x='240' y='20' width='520' height='430' rx='10' fill='#f8fafc' stroke='#94a3b8' stroke-dasharray='8 6'/><text x='256' y='44' {F} font-size='13' font-weight='700' fill='#64748b'>FastAPI app (uvicorn)</text>"
b += box(270, 60, 220, 92, "Middleware", ["security headers", "(nosniff, frame deny, no-store)"], "#dd344c")
b += box(270, 180, 220, 108, "Auth routes", ["/auth/register  /auth/login", "scrypt hashes, rate limit", "JWT HS256, 30 min"], "#dd344c")
b += box(520, 180, 220, 108, "Topic routes", ["/topics  /topics/{id}  /stats", "Bearer token required", "queries scoped to user_id"], "#ed7100")
b += box(270, 320, 470, 100, "Validation (Pydantic)", ["email format, password 10–128 chars, title 1–200 chars,", "category and status from fixed lists → 422 on bad input"], "#1d4ed8")
b += box(810, 180, 170, 108, "SQLite", ["users, topics", "parameterised SQL", "foreign keys on"], "#3f8624")
b += arr(190, 195, 268, 110, "HTTPS (behind a proxy)", 160, 122) + arr(190, 205, 268, 230) + arr(490, 234, 518, 234) + arr(740, 234, 808, 234, "SQL", 774, 226) + arr(380, 290, 380, 318) + arr(630, 290, 630, 318)
(D / "architecture.svg").write_text(f"<svg xmlns='http://www.w3.org/2000/svg' width='1000' height='470' viewBox='0 0 1000 470'>{b}</svg>")
js = D / "_r.js"; js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 2 }); await p.goto('file://' + __dirname + '/architecture.svg'); await (await p.$('svg')).screenshot({ path: __dirname + '/architecture.png' }); await b.close(); })();")
subprocess.run(["node", str(js)], check=True); js.unlink(); print("ok")
