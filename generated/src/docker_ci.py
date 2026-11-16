"""One-page guide to the Dockerfiles and CI workflows of the two starters. Run from the repo root: python3 generated/src/docker_ci.py"""
import html, pathlib, subprocess
from pypdf import PdfReader, PdfWriter
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; E = html.escape
DF = [("FROM python:3.12-slim", "Start from a small official Python image."), ("ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1", "No .pyc files; logs appear immediately."),
      ("WORKDIR /app", "All later paths are relative to /app."), ("COPY requirements.txt . / RUN pip install …", "Install dependencies first, so Docker can reuse this layer when only your code changes."),
      ("COPY app ./app", "Then copy the code (the .dockerignore keeps .venv, caches and databases out)."), ("RUN useradd … / USER appuser", "Run as a non-root user: a bug in the app cannot act as root inside the container."),
      ("VOLUME [\"/data\"] and DB_PATH", "Keep the SQLite file outside the image so it survives restarts."), ("EXPOSE 8000 / CMD [\"uvicorn\", …]", "Document the port and start the server; secrets such as JWT_SECRET come from -e at run time, never from the image."),
      ("HEALTHCHECK …", "Docker marks the container unhealthy if /health stops answering.")]
WF = [("on: push, pull_request", "Run on every push and every pull request."), ("runs-on: ubuntu-latest", "A fresh Linux machine from GitHub for each job."),
      ("actions/checkout@v4", "Get your code."), ("actions/setup-python@v5 (python-version 3.12, cache: pip)", "Install Python and cache downloaded packages between runs."),
      ("pip install / pytest -q (or the unittest and suite commands)", "Install and test; a failing test turns the commit red."), ("docker job, needs: test", "Only after tests pass, check that the image still builds.")]
rows = lambda xs: "".join(f"<tr><td><code>{E(a)}</code></td><td>{E(b)}</td></tr>" for a, b in xs)
HTML = f'''<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>
@page {{ size: A4; margin: 12mm 13mm; }} body {{ font: 400 8.8pt/1.45 Inter, sans-serif; color: #1e293b; margin: 0; }} .eb {{ font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; }}
h1 {{ font: 700 22pt "Space Grotesk"; margin: 0 0 2mm; color: #0f172a; }} h2 {{ font: 700 11.5pt "Space Grotesk"; color: #1d4ed8; margin: 3.5mm 0 1.2mm; }} table {{ border-collapse: collapse; width: 100%; }}
td {{ border-bottom: 1px solid #e2e8f0; padding: 1.2mm 2mm; vertical-align: top; }} td:first-child {{ width: 46%; }} code {{ font: 400 7.6pt "JetBrains Mono"; font-variant-ligatures: none; }} pre {{ font: 400 7.6pt/1.4 "JetBrains Mono"; background: #f8fafc; border-left: 3px solid #1d4ed8; padding: 2mm 3mm; margin: 0; }}
.note {{ background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; margin-top: 3mm; }}</style></head><body>
<p class="eb">PROJECTS · DOCKER AND CI</p><h1>Docker and GitHub Actions for both starters</h1>
<p>Both starters now have a <code>Dockerfile</code>, a <code>.dockerignore</code> and <code>.github/workflows/tests.yml</code>. Copy a starter folder into its own GitHub repository and every push runs the tests and builds the image: a green tick on your commits is something recruiters notice.</p>
<h2>Dockerfile, line by line (backend starter)</h2><table><tbody>{rows(DF)}</tbody></table>
<h2>Workflow, step by step</h2><table><tbody>{rows(WF)}</tbody></table>
<h2>Commands</h2><pre>docker build -t study-tracker generated/backend-starter
docker run -p 8000:8000 -e JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))") -v study-data:/data study-tracker
docker build -t secrag generated/ai-security-starter &amp;&amp; docker run --rm secrag</pre>
<p class="note"><b>Checked.</b> Both images were built and run with Docker 29: the backend's 10 tests pass inside the image, the API answers /health and refuses to start without a strong JWT_SECRET; secrag's tests pass and its suite reports 12/12 baseline and 0/12 defended. Both run as a non-root user. Workflow files were parsed and checked as YAML; they have not yet run on GitHub.</p></body></html>'''
(SRC / "dc.html").write_text(HTML); js = SRC / "r.js"
js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/dc.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/dc.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
subprocess.run(["node", str(js)], check=True); r = PdfReader(str(SRC / "dc.pdf")); assert len(r.pages) == 1, len(r.pages)
w = PdfWriter(clone_from=r); w.add_metadata({"/Title": "Docker and CI guide"}); w.write(str(OUT / "docker-ci-guide.pdf"))
for f in ("dc.html", "dc.pdf", "r.js"): (SRC / f).unlink()
print("1 page")
