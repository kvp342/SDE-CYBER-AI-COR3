"""Linux, Git and debugging cheat sheet. Every command is run in a throw-away sandbox (its own temp folder and git repo) and must
succeed with the expected output before it goes on the sheet; commands whose tool is missing here are marked 'not run'.
Run from the repo root: python3 generated/src/cli_sheet.py"""
import html, io, os, pathlib, shutil, subprocess, tempfile
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
E = lambda s: html.escape(str(s), quote=True)
BOX = pathlib.Path(tempfile.mkdtemp())
ENV = {**os.environ, "GIT_AUTHOR_NAME": "Student", "GIT_AUTHOR_EMAIL": "student@example.com", "GIT_COMMITTER_NAME": "Student", "GIT_COMMITTER_EMAIL": "student@example.com", "HOME": str(BOX)}
def sh(cmd, cwd=BOX):
    r = subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True, text=True, env=ENV, timeout=60); return r.returncode, r.stdout + r.stderr
# (command shown, what it does, setup run first, check: substring expected in output or None for 'exit code 0')
SECTIONS = [
 ("Files and text", [
  ("ls -la", "List all files with permissions, including hidden ones", "touch .hidden", ".hidden"),
  ("mkdir -p a/b/c && tree a || find a", "Create nested folders; show them", "", "a/b/c"),
  ("cp -r a backup && mv backup a_old", "Copy a folder recursively; rename it", "", None),
  ("grep -rn \"TODO\" .", "Search recursively, with line numbers", "mkdir -p src && printf 'x\\n// TODO fix\\n' > src/m.cpp", "src/m.cpp:2"),
  ("find . -name \"*.cpp\" -mtime -1", "Files by name changed in the last day", "", "m.cpp"),
  ("wc -l src/m.cpp", "Count lines", "", "2"),
  ("sort data.txt | uniq -c | sort -rn | head -3", "Most frequent lines", "printf 'b\\na\\nb\\nc\\nb\\na\\n' > data.txt", "3 b"),
  ("awk -F, '{s += $2} END {print s}' marks.csv", "Sum a CSV column", "printf 'asha,70\\nravi,80\\n' > marks.csv", "150"),
  ("sed -i 's/old/new/g' notes.txt", "Replace text in a file", "echo 'old old' > notes.txt", None),
  ("jq '.name' package.json", "Read a JSON field", "echo '{\"name\": \"tracker\"}' > package.json", "tracker"),
  ("tar -czf src.tgz src && tar -tzf src.tgz", "Make and list a compressed archive", "", "src/m.cpp"),
  ("chmod +x run.sh && ./run.sh", "Make a script executable and run it", "printf '#!/bin/bash\\necho ran\\n' > run.sh", "ran"),
  ("find . -name '*.log' -print0 | xargs -0 rm -f", "Delete matching files safely (handles spaces)", "touch 'a b.log' c.log", None)]),
 ("Processes and system", [
  ("ps aux | head -5", "Running processes", "", "PID"),
  ("sleep 30 & echo $! > pid; kill $(cat pid)", "Start a background job; stop it by PID", "", None),
  ("df -h . && du -sh src", "Disk free; size of a folder", "", "src"),
  ("lsof -p $$ | head -3", "Files open by a process (here: this shell)", "", "COMMAND"),
  ("env | grep ^HOME=", "Environment variables", "", "HOME="),
  ("command -v g++", "Where a program is installed", "", "g++"),
  ("ulimit -n", "Open-file limit for this shell", "", None)]),
 ("Git: everyday", [
  ("git init -q demo && cd demo && git status -s", "Start a repository", "", None),
  ("git add file.txt && git commit -qm \"Add file\" && git log --oneline", "Stage and commit; short history", "cd demo && echo v1 > file.txt", "Add file"),
  ("git switch -c feature && git branch", "Create and switch to a branch", "cd demo", "* feature"),
  ("git diff", "Unstaged changes", "cd demo && echo v2 >> file.txt", "+v2"),
  ("git stash && git stash list && git stash pop", "Put work aside and bring it back", "cd demo", "stash@{0}"),
  ("git commit -qam \"Edit\" && git switch -q main 2>/dev/null || git switch -q master; git merge -q feature && git log --oneline | head -2", "Merge a branch into main", "cd demo", "Edit"),
  ("git log --oneline --graph --all | head -5", "History as a graph", "cd demo", "*")]),
 ("Git: undo safely", [
  ("git restore file.txt", "Throw away unstaged edits to a file", "cd demo && echo junk >> file.txt", None),
  ("git restore --staged file.txt", "Unstage a file (keep the edit)", "cd demo && echo more >> file.txt && git add file.txt", None),
  ("git commit -q --amend -m \"Better message\" && git log -1 --format=%s", "Fix the last commit message (before pushing)", "cd demo && git checkout -q -- file.txt", "Better message"),
  ("git reset --soft HEAD~1 && git status -s", "Undo the last commit, keep its changes staged", "cd demo", "M  file.txt"),
  ("git commit -qm again && git revert --no-edit HEAD >/dev/null && git log --oneline | head -2", "Undo a pushed commit with a new commit", "cd demo", "Revert"),
  ("git reflog | head -3", "Find 'lost' commits after a bad reset", "cd demo", "HEAD@{0}")]),
 ("Debugging C++", [
  ("g++ -std=c++17 -g -O0 -Wall -Wextra -Wshadow bug.cpp -o bug", "Build with debug info and warnings", "printf '#include <vector>\\nint main(){std::vector<int> v(3); int s=0; for(int i=0;i<=3;i++) s+=v[i]; return s;}\\n' > bug.cpp", None),
  ("g++ -std=c++17 -g -fsanitize=address,undefined bug.cpp -o bug_san && ./bug_san", "Find out-of-bounds reads at the exact line (AddressSanitizer)", "", "heap-buffer-overflow"),
  ("gdb -batch -ex run -ex bt ./crash", "Run in gdb and print the stack after a crash", "printf 'int main(){int* p=nullptr; return *p;}\\n' > crash.cpp && g++ -g -O0 crash.cpp -o crash", "main"),
  ("gdb -batch -ex 'break main' -ex run -ex next -ex 'info locals' ./bug", "Breakpoint, step, show local variables", "", "Breakpoint 1"),
  ("valgrind --leak-check=full -q ./leak", "Find memory leaks", "printf 'int main(){new int[10]; return 0;}\\n' > leak.cpp && g++ -g leak.cpp -o leak", "definitely lost"),
  ("strace -c -f ./hello 2>&1 | tail -4", "Count the system calls a program makes", "printf '#include <cstdio>\\nint main(){puts(\"hi\");}\\n' > hello.cpp && g++ hello.cpp -o hello", "total"),
  ("time ./hello", "Measure wall-clock and CPU time", "", "real")]),
]
results, ran, skipped = [], 0, 0
for title, cmds in SECTIONS:
    rows = []
    for cmd, desc, setup, expect in cmds:
        tool = cmd.split()[0]
        if tool in ("gdb", "valgrind", "strace", "lsof", "jq") and not shutil.which(tool): rows.append((cmd, desc, "not run")); skipped += 1; continue
        if setup:
            c, o = sh(setup); assert c == 0, (setup, o)
        workdir = "cd demo && " if setup.startswith("cd demo") or cmd.startswith("git ") and not cmd.startswith("git init") else ""
        code, out = sh(workdir + cmd)
        ok = (expect in out) if expect else code == 0
        if cmd.startswith("g++") and "bug_san" in cmd: ok = expect in out          # the sanitizer run is supposed to fail with a report
        if cmd.startswith("gdb -batch -ex run"): ok = expect in out and "SIGSEGV" in out
        assert ok, f"{cmd!r} failed:\n{out[-800:]}"
        rows.append((cmd, desc, "tested")); ran += 1
    results.append((title, rows))
shutil.rmtree(BOX, ignore_errors=True)
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    secs = "".join(f'<h2 class="h">{E(t)}</h2><table class="t"><tbody>{"".join(f"<tr><td class=c><code>{E(c)}</code></td><td>{E(d)}</td><td class=s>{E(s)}</td></tr>" for c, d, s in rows)}</tbody></table>' for t, rows in results)
    return f'''<section class="cover" id="sheet"><p class="eb">TOOLS · DAILY COMMANDS</p><h1>Linux, Git and debugging</h1>
<p class="lead">Commands you will use in labs, projects and contests. Each one marked "tested" was run in a throw-away folder and its output checked ({ran} of {ran + skipped}). Copy them, but read what a command does before running it, especially anything that deletes or rewrites history.</p>
<p class="how"><b>Git rule.</b> Rewrite history (amend, reset) only on commits you have not pushed; for pushed commits use <code>git revert</code>. Never commit keys or <code>.env</code> files.</p>{secs}
<h2 class="h">Debugging routine</h2><ol><li>Reproduce with the smallest input.</li><li>Compile with <code>-g -Wall -Wextra -fsanitize=address,undefined</code>; most contest bugs show up here.</li><li>For crashes, run in gdb and read <code>bt</code>; for wrong answers, print state at the first suspicious line.</li><li>Fix one thing, rerun the same input, then the edge cases.</li></ol></section>'''
CSS = """@page { size: A4; margin: 11mm 12mm 13mm; } * { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.4pt/1.38 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; } .eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; } h1 { font: 700 24pt "Space Grotesk"; margin: 0 0 2mm; color: #0f172a; } .lead { color: #475569; margin: 0 0 2mm; }
.how { background: #fff7ed; border-left: 3px solid #c2410c; padding: 1.6mm 3mm; margin: 0 0 1mm; } h2.h { font: 700 11pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1mm; break-after: avoid; } table { border-collapse: collapse; width: 100%; }
.t td { border-bottom: 1px solid #eef2f7; padding: .9mm 1.6mm; vertical-align: top; } .c { width: 54%; } code { font: 400 7.5pt "JetBrains Mono"; font-variant-ligatures: none; } .s { width: 12mm; font: 600 6.8pt "JetBrains Mono"; color: #166534; } ol { padding-left: 5mm; margin: 0; }"""
js = SRC / "r.js"
(SRC / "cli.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>{body(None)}</body></html>')
js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/cli.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/cli.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
subprocess.run(["node", str(js)], check=True)
w = PdfWriter(clone_from=PdfReader(str(SRC / "cli.pdf"))); NP = len(w.pages)
for i, pg in enumerate(w.pages):
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
for t, _ in results: pass
w.add_outline_item("Linux, Git and debugging", 0, fit=Fit.fit()); w.add_metadata({"/Title": "Linux, Git and debugging cheat sheet"}); w.write(str(OUT / "linux-git-debugging-sheet.pdf"))
for f in ("cli.html", "cli.pdf", "r.js"): (SRC / f).unlink()
print(NP, "pages;", ran, "commands tested,", skipped, "not run")
