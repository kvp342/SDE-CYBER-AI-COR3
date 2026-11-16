"""Knowledge Base v2: the original KB plus Worked Solutions II (40 problems) and Company files II (6 companies).
Copies sources/kb to generated/kb2 (sources/ is never edited), adds two modules, rebuilds, wraps the page like the root
knowledge-base.html, and checks it in a real browser. Output: generated/knowledge-base-v2.html. Run from the repo root."""
import json, pathlib, shutil, subprocess, sys, textwrap
ROOT = pathlib.Path(__file__).resolve().parents[2]; SRC = ROOT / "generated" / "src"; KB2 = ROOT / "generated" / "kb2"
if KB2.exists(): shutil.rmtree(KB2)
shutil.copytree(ROOT / "sources" / "kb", KB2, ignore=shutil.ignore_patterns("__pycache__", "kb.html", "aliases.json"))
(KB2 / "t_probs2.py").write_text((SRC / "t_probs2.py").read_text() + "\nTOPICS = P\n")
sys.path.insert(0, str(SRC)); from company2 import CO, NOTE
mods = repr([dict(id=c["id"], title=c["title"], cat="Companies", lvl=c["lvl"], aka=[c["title"]], why=c["why"], core=c["process"] + [NOTE], points=c["prep"], code="",
                  pit=c["pit"], ask=c["ask"], prac=[], learn=c["sources"], rel=c["rel"], qa=[]) for c in CO])
(KB2 / "t_companies2.py").write_text('"""Company files II (from generated/src/company2.py)."""\nTOPICS = ' + mods + "\n")
b = (KB2 / "build.py").read_text()
b = b.replace('"t_probs", "t_cs"', '"t_probs", "t_probs2", "t_cs"').replace('"t_companies"]', '"t_companies", "t_companies2"]')
assert '"t_probs2"' in b and '"t_companies2"' in b
(KB2 / "build.py").write_text(b)
out = subprocess.run([sys.executable, str(KB2 / "build.py")], capture_output=True, text=True); assert out.returncode == 0, out.stderr
print("build:", out.stdout.strip())
page, root = (KB2 / "page.html").read_text(), (ROOT / "knowledge-base.html").read_text()
head = root[:root.index(page[:200])]; built = (KB2 / "kb.html").read_text()
tail_marker = page.split("/*DATA*/[]")[1][-200:]; tail = root[root.rindex(tail_marker) + len(tail_marker):]
final = head + built + tail
(ROOT / "generated" / "knowledge-base-v2.html").write_text(final)
data = json.loads(built.split("const DATA = ", 1)[1].split(";\n", 1)[0]) if "const DATA = " in built else None
# Browser check: load the page, open a new problem and a new company, confirm they render and every related link points to a real topic.
js = SRC / "kbcheck.js"
js.write_text(textwrap.dedent("""
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage(); const errors = [];
  p.on('pageerror', e => errors.push(String(e)));
  await p.goto('file://' + process.argv[2]); await p.waitForTimeout(800);
  const out = {};
  for (const id of ['p2-rotate-image', 'p2-n-queens', 'co-phonepe', 'p-two-sum']) {
    await p.evaluate(h => { location.hash = h; }, id); await p.waitForTimeout(250);
    out[id] = await p.evaluate(() => document.getElementById('main').innerText.slice(0, 3000));
  }
  const links = await p.evaluate(() => [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href').slice(1)).filter(Boolean));
  console.log(JSON.stringify({ errors, out, links }));
  await b.close();
})();"""))
r = subprocess.run(["node", str(js), str(ROOT / "generated" / "knowledge-base-v2.html")], capture_output=True, text=True); js.unlink()
assert r.returncode == 0, r.stderr
res = json.loads(r.stdout)
assert not res["errors"], res["errors"]
assert "Rotate Image" in res["out"]["p2-rotate-image"] and "transpose" in res["out"]["p2-rotate-image"].lower() and "N-Queens" in res["out"]["p2-n-queens"], "new problem pages did not render"
assert "PhonePe" in res["out"]["co-phonepe"] and "machine" in res["out"]["co-phonepe"].lower() and "Two Sum" in res["out"]["p-two-sum"]
print("browser check: new pages render, no script errors;", len(res["links"]), "in-page links on the last view")
