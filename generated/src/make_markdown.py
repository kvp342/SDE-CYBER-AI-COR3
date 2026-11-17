"""Make the whole kit readable directly on GitHub: plain Markdown in generated/read/, no HTML anywhere.
Run from the repo root: python3 generated/src/make_markdown.py
It builds every PDF builder and page in a throw-away copy of the repo, keeps the HTML they render from,
converts it with to_markdown.convert, and writes the knowledge base and A2Z sheets straight from their data."""
import json, pathlib, re, shutil, subprocess, sys, tempfile, collections
ROOT = pathlib.Path(__file__).resolve().parents[2]; SRC = ROOT / "generated" / "src"; OUT = ROOT / "generated" / "read"
sys.path.insert(0, str(SRC)); from to_markdown import convert, slugify, no_html_outside_code
GH = "https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/"
TREE = "https://github.com/kvp342/intrusion-detection-and-prevention/tree/ccr-ca7232a7-t7lq94/"
KBURL = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT"

# builder → the HTML file it renders the PDF from (its last write of that name is the final pass)
BUILDERS = {"ai_starter": "ai.html", "anki": "anki.html", "apti": "apti.html", "aws_pack": "aws.html", "awslab": "awslab.html", "cli_sheet": "cli.html",
 "company2": "co.html", "company3": "co3.html", "cp_ladder": "cp.html", "docker_ci": "dc.html", "elite_pack": "el.html", "final_plan": "final_plan.html",
 "index_all": "ia.html", "interview_day": "id.html", "lab_map": "lm.html", "lab_notebook": "lab.html", "lld_pack": "lld.html", "mcq": "mcq.html",
 "mock_scripts": "ms.html", "mock_scripts2": "ms2.html", "oa_packs": "oa.html", "oa_packs2": "oa2.html", "onepagers": "op.html", "paper_outline": "po.html",
 "pattern_stl": "ps.html", "planner": "pl.html", "profile_kit": "pk.html", "resume_kit": "rk.html", "roadmapsh": "roadmapsh.html", "secbank": "secbank.html",
 "sql_pack": "sql.html", "story_bank": "sb.html", "sysdesign": "sd.html", "tenantwall": "tw.html", "worked2": "w2.html", "worked3": "w3.html"}
CAPTURE = '''import pathlib, runpy, sys
path, name, stash = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
orig = pathlib.Path.write_text
def wt(self, data, *a, **k):
    r = orig(self, data, *a, **k)
    if str(self).endswith(".html"): orig(stash / f"{name}__{self.name}", data)
    return r
pathlib.Path.write_text = wt
import pypdf
ow = pypdf.PdfWriter.write
def w(self, stream):
    if isinstance(stream, (str, pathlib.Path)):
        with open(stash / f"{name}.pdfs", "a") as fh: fh.write(str(stream) + "\\n")
    return ow(self, stream)
pypdf.PdfWriter.write = w
sys.argv = [path]; runpy.run_path(path, run_name="__main__")
'''
def capture(stash):
    """Run every builder (one at a time: they share temporary file names) in a copy of the repo."""
    tmp = pathlib.Path(tempfile.mkdtemp()); repo = tmp / "repo"; repo.mkdir()
    subprocess.run(f"git -C {ROOT} archive HEAD | tar -x -C {repo}", shell=True, check=True)
    for f in ("to_markdown.py",): shutil.copy(SRC / f, repo / "generated" / "src" / f)
    (tmp / "capture.py").write_text(CAPTURE)
    for b in BUILDERS:
        r = subprocess.run([sys.executable, str(tmp / "capture.py"), f"generated/src/{b}.py", b, str(stash)], cwd=repo, capture_output=True, text=True)
        assert r.returncode == 0, f"{b} failed:\n{r.stderr[-1500:]}"
    r = subprocess.run([sys.executable, "build.py"], cwd=repo / "sources" / "guide", capture_output=True, text=True); assert r.returncode == 0, r.stderr[-800:]
    shutil.copy(repo / "sources" / "guide" / "placement-field-guide.html", stash / "guide__placement-field-guide.html")
    shutil.rmtree(tmp)

E = lambda s: re.sub(r"([\\`*_<>\[\]|])", r"\\\1", str(s))          # escape Markdown and angle brackets in plain text
LV = {0: "Foundation", 1: "Core", 2: "Interview-ready", 3: "Advanced", 4: "Elite"}

def kb_files():
    """The 213-topic knowledge base, one Markdown file per category, from the data inside knowledge-base-v2.html."""
    s = (ROOT / "generated" / "knowledge-base-v2.html").read_text(); data, _ = json.JSONDecoder().raw_decode(s[s.index('[{"id"'):])
    cats = list(collections.OrderedDict.fromkeys(d["cat"] for d in data))
    fname = {c: re.sub(r"[^a-z0-9]+", "-", c.lower()).strip("-") + ".md" for c in cats}
    where, seen = {}, {c: {} for c in cats}
    for c in cats: slugify(f"{c}", seen[c]); slugify("Topics", seen[c])     # the file's own headings come first
    for d in data: where[d["id"]] = (fname[d["cat"]], slugify(d["title"], seen[d["cat"]]))
    files = {}
    for c in cats:
        items = [d for d in data if d["cat"] == c]
        out = [f"# {E(c)}", "", f"[All categories](README.md) · {len(items)} topics", "", "## Topics", ""]
        out += [f"- [{E(d['title'])}](#{where[d['id']][1]})" for d in items]
        for d in items:
            out += ["", f"## {E(d['title'])}", "", f"*Level {d['lvl']}: {LV.get(d['lvl'], '')}*", "", E(d["why"])]
            if d["core"]: out += ["", "**Key idea**", ""] + [E(x) + "\n" for x in d["core"]]
            if d["points"]: out += ["", "**Points**", ""] + [f"- {E(x)}" for x in d["points"]]
            if d["code"]: out += ["", "```cpp" if re.search(r"#include|vector<|class |int ", d["code"]) else "```text", d["code"].rstrip(), "```"]
            if d["qa"]: out += ["", "**Questions and model answers**", ""] + [f"**Q. {E(q)}**\n\n{E(a)}\n" for q, a in d["qa"]]
            if d["pit"]: out += ["", "**Traps**", ""] + [f"- {E(x)}" for x in d["pit"]]
            if d["ask"]: out += ["", "**Interviewers ask**", ""] + [f"- {E(x)}" for x in d["ask"]]
            if d["prac"]: out += ["", "**Practise**", ""] + [f"- [{E(l)}]({u})" for l, u in d["prac"]]
            if d["learn"]: out += ["", "**Learn more**", ""] + [f"- [{E(l)}]({u})" for l, u in d["learn"]]
            if d["rel"]:
                rel = [f"[{E(next(x['title'] for x in data if x['id'] == r))}]({'' if where[r][0] == fname[c] else where[r][0]}#{where[r][1]})" for r in d["rel"] if r in where]
                out += ["", "**Related:** " + " · ".join(rel)]
            out += ["", "[Back to the topic list](#topics)"]
        files[fname[c]] = "\n".join(out) + "\n"
    idx = ["# Knowledge base", "", f"{len(data)} topics in {len(cats)} categories: methods, DSA patterns, 83 worked problems, Core CS, security, cloud, design, careers, mock interviews and company files.", "",
           "| Category | Topics |", "|---|---|"] + [f"| [{E(c)}]({fname[c]}) | {sum(d['cat'] == c for d in data)} |" for c in cats]
    files["README.md"] = "\n".join(idx) + "\n"
    return files, where

def a2z_files():
    """Both Striver A2Z sheets as Markdown tables (problem, difficulty, links)."""
    g = json.load(open(ROOT / "sources" / "a2z-classic" / "g2.json")); out = ["# Striver A2Z DSA sheet (classic)", "", f"{len(g)} problems in sheet order. Source: [takeuforward.org](https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2).", ""]
    for cat in collections.OrderedDict.fromkeys(x["category"] for x in g):
        out += [f"## {E(cat)}", "", "| # | Problem | Difficulty | Links |", "|---|---|---|---|"]
        for x in sorted((x for x in g if x["category"] == cat), key=lambda x: x["order"]):
            links = " · ".join(f"[{n}]({u})" for n, u in (("LeetCode", x.get("leetcode")), ("Article", x.get("article")), ("Video", x.get("youtube"))) if u)
            out.append(f"| {x['order']} | {E(x['name'])} | {x.get('difficulty') or ''} | {links} |")
        out.append("")
    classic = "\n".join(out)
    d = json.load(open(ROOT / "sources" / "a2z" / "syllabus.json")); F = d["fields"]
    rows = [dict(zip(F[r[0]], r[1:])) for r in d["rows"]]
    out = ["# Striver A2Z DSA sheet (2026 version)", "", "Topic tree with every problem. Source: [takeuforward.org](https://takeuforward.org/).", ""]; n = 0
    def walk(i, depth):
        nonlocal n
        r = rows[i]; kids = r.get("children") or []
        if kids:
            out.extend([f"{'#' * min(depth + 2, 6)} {E(r['label'])}", ""])
            leaves = [rows[k] for k in kids if not rows[k].get("children")]
            if leaves:
                out.extend(["| Problem | Difficulty | Links |", "|---|---|---|"])
                for x in leaves:
                    n += 1
                    links = " · ".join(f"[{nm}]({u})" for nm, u in (("LeetCode", x.get("leetcode_link")), ("Article", x.get("free_blog_link")), ("Video", x.get("yt_video"))) if u and str(u).startswith("http"))
                    out.append(f"| {E(x['label'])} | {x.get('difficulty') or ''} | {links} |")
                out.append("")
            for k in kids:
                if rows[k].get("children"): walk(k, depth + 1)
    for root in d["roots"]: walk(root, 0)
    return classic, "\n".join(out) + "\n", n

def main(stash=None):
    own = stash is None
    stash = pathlib.Path(stash or tempfile.mkdtemp())
    if own: capture(stash)
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / "knowledge-base").mkdir(parents=True); (OUT / "a2z").mkdir()
    docs = {}                                                                  # md name → markdown
    pdf_of = {}                                                                # repo path of the original → md name
    for b, h in BUILDERS.items():
        pdf = [l for l in (stash / f"{b}.pdfs").read_text().split() if b != "anki" or "anki" in l][-1]
        name = pathlib.Path(pdf).stem; docs[name + ".md"] = convert((stash / f"{b}__{h}").read_text()); pdf_of[f"generated/{name}.pdf"] = name + ".md"
    docs["resume-template.md"] = convert((stash / "resume_kit__resume-template.html").read_text()); pdf_of["generated/resume/resume-template.html"] = "resume-template.md"
    docs["placement-field-guide.md"] = convert((stash / "guide__placement-field-guide.html").read_text()); pdf_of["Tier3-to-Top-Offer-Placement-Guide.pdf"] = "placement-field-guide.md"
    for f, m in (("index.html", "home.md"), ("playbook.html", "playbook.md"), ("roadmap.html", "roadmap.md"), ("cheat-sheet.html", "cheat-sheet.md")):
        docs[m] = convert((ROOT / f).read_text()); pdf_of[f] = m
    pdf_of["DSA-Placement-Playbook.pdf"] = "playbook.md"
    kb, where = kb_files(); classic, a2z26, n26 = a2z_files()
    for f in ("knowledge-base.html", "generated/knowledge-base-v2.html", "Placement-Knowledge-Base.pdf"): pdf_of[f] = "knowledge-base/README.md"
    pdf_of["Striver-A2Z-DSA-Sheet-Classic.pdf"] = "a2z/classic.md"; pdf_of["Striver-A2Z-DSA-Sheet-2026.pdf"] = "a2z/a2z-2026.md"
    def relink(md, here):                                                      # GitHub file links and Knowledge Base links → the Markdown copies
        up = "../" * here.count("/")
        def gh(m):
            p = m.group(2); return f"]({up}{pdf_of[p]}{m.group(3) or ''})" if p in pdf_of else m.group(0)
        md = re.sub(r"\]\((" + re.escape(GH) + r"|" + re.escape(TREE) + r")([^)#]+?)(#[^)]*)?\)", gh, md)
        md = re.sub(re.escape(KBURL) + r"#([\w-]+)", lambda m: f"{up}knowledge-base/{where[m.group(1)][0]}#{where[m.group(1)][1]}" if m.group(1) in where else m.group(0), md)
        md = re.sub(r"\]\(([^)#:\s]+)(#[^)]*)?\)", lambda m: f"]({up}{pdf_of[m.group(1)]})" if m.group(1) in pdf_of else m.group(0), md)   # relative links to the original pages
        return md.replace(f"]({KBURL})", f"]({up}knowledge-base/README.md)")
    for name, md in docs.items(): (OUT / name).write_text(relink(md, name))
    for name, md in kb.items(): (OUT / "knowledge-base" / name).write_text(relink(md, "knowledge-base/" + name))
    (OUT / "a2z" / "classic.md").write_text(classic); (OUT / "a2z" / "a2z-2026.md").write_text(a2z26)
    # index: the same groups as the index of everything, then everything else
    readme = (ROOT / "README.md").read_text()
    desc = dict(re.findall(r"^\| `([^`]+)` \| (.*?) \|$", readme, re.M))
    import ast                                                                 # read GROUPS from index_all.py without running its build
    tree = ast.parse((SRC / "index_all.py").read_text())
    node = next(n.value for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "GROUPS")
    GROUPS = eval(compile(ast.Expression(node), "index_all", "eval"), {"SELF": "generated/index-of-everything.pdf"})
    lines = ["# Read everything here", "", "Every guide, pack and plan in this repository as plain Markdown that GitHub shows directly: no downloads, no HTML, no PDF viewer. Links between files work, and Knowledge Base links open the Markdown knowledge base. The PDFs and web pages are still in the repository for printing and offline use.", "",
             "Start with [Your final plan](final-plan.md), then [the Playbook](playbook.md) for the daily plan.", ""]
    listed = set()
    TITLES = {"home.md": "Home", "playbook.md": "DSA Placement Playbook (daily plan and every lesson)", "roadmap.md": "Roadmap: Nov 2026 to Jun 2028"}
    def title_of(m):                                                           # the file's first heading, as plain text
        if m in TITLES: return TITLES[m]
        h = next((l[2:] for l in (OUT / m).read_text().splitlines() if l.startswith("# ")), m)
        return E(re.sub(r"\\(.)", r"\1", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", h)).strip())
    for gid, title, note, paths in GROUPS:
        rows = [(p, pdf_of[p]) for p in paths if p in pdf_of and pdf_of[p] not in listed]
        if gid == "start": rows = [(p, m) for p, m in rows] + [(None, "knowledge-base/README.md"), (None, "a2z/classic.md"), (None, "a2z/a2z-2026.md")]
        if not rows: continue
        lines += [f"## {title}", "", note, "", "| Read | What it is |", "|---|---|"]
        for p, m in rows:
            if m in listed: continue
            listed.add(m); d = {"playbook.md": "Every lesson and the day-by-day plan (the web version adds ticks and XP)", "knowledge-base/README.md": "The knowledge base: 213 topics with model answers, worked problems and company files"}.get(m) or (desc.get(p, "") if p else None) if p else {"knowledge-base/README.md": "The knowledge base: 213 topics with model answers, worked problems and company files", "a2z/classic.md": f"Striver A2Z classic sheet: {len(json.load(open(ROOT / 'sources/a2z-classic/g2.json')))} problems with links", "a2z/a2z-2026.md": f"Striver A2Z 2026 sheet: {n26} problems with links"}[m]
            lines.append(f"| [{title_of(m)}]({m}) | {E(re.sub(r'`', '', d))} |")
        lines.append("")
    rest = sorted(set(docs) | {"knowledge-base/README.md"} - listed - {"home.md"})
    rest = [m for m in sorted(docs) if m not in listed and m != "home.md"]
    if rest: lines += ["## More", "", "| Read |", "|---|"] + [f"| [{title_of(m)}]({m}) |" for m in rest] + [""]
    (OUT / "README.md").write_text("\n".join(lines))
    # checks: no HTML anywhere, every relative link points at a file that exists, every #anchor exists in its target
    allmd = list(OUT.rglob("*.md")); anchors = {}
    for f in allmd:
        seen, fence = {}, False; a = set()
        for line in f.read_text().splitlines():
            if line.startswith("```"): fence = not fence
            m = None if fence else re.match(r"^(#{1,6})\s+(.*)$", line)
            if m: a.add(slugify(m.group(2), seen))
        anchors[f.resolve()] = a
    broken = []
    for f in allmd:
        md = f.read_text(); assert not no_html_outside_code(md), f"HTML in {f}: {no_html_outside_code(md)[:2]}"
        for link in re.findall(r"\]\(([^)\s]+)\)", md):
            if re.match(r"[a-z]+:", link): continue
            path, _, frag = link.partition("#"); tgt = (f.parent / path).resolve() if path else f.resolve()
            if not tgt.exists() or (frag and frag not in anchors.get(tgt, set())): broken.append(f"{f.relative_to(OUT)} → {link}")
    assert not broken, f"{len(broken)} broken links, e.g. {broken[:8]}"
    print(len(allmd), "Markdown files;", sum(len(re.findall(r'\]\(', f.read_text())) for f in allmd), "links; 0 broken; no HTML")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
