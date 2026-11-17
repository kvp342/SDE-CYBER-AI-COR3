"""HTML → GitHub Markdown with no HTML left in it. Internal #links are rewritten to GitHub's heading anchors,
table cells are flattened so tables stay Markdown tables, page-number columns and scripts are dropped."""
import re, subprocess
from bs4 import BeautifulSoup, NavigableString

TAG = re.compile(r"</?[a-zA-Z][a-zA-Z0-9-]*(\s[^<>]*)?/?>")

def slugify(text, seen):
    """GitHub's heading anchor: lower-case, drop punctuation except - and _, spaces to -, number duplicates."""
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)            # links → their text
    t = re.sub(r"[`*~]", "", t)                                       # Markdown markers are not part of the anchor
    s = re.sub(r"[^\w\- ]", "", t.strip().lower()).replace(" ", "-")
    n = seen.get(s, 0); seen[s] = n + 1
    return s if n == 0 else f"{s}-{n}"

def no_html_outside_code(md):
    out, fence = [], False
    for line in md.splitlines():
        if line.lstrip().startswith("```"): fence = not fence; continue
        if not fence: out.append(re.sub(r"`[^`]*`", "", line))
    return [l for l in out if TAG.search(l)]

def convert(html, drop=()):
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "head", "noscript", "link", "meta", "svg", "button", "input", "select", "canvas"]): t.decompose()
    for sel in (".pg", "a.back", ".back") + tuple(drop):
        for t in soup.select(sel): t.decompose()
    for table in soup.find_all("table"):                       # drop columns that are empty in every body row (page numbers)
        rows = [r.find_all(["td", "th"], recursive=False) for r in table.find_all("tr")]
        body = [r for r in rows if r and all(c.name == "td" for c in r)]
        if body:
            n = max(len(r) for r in rows)
            empty = [k for k in range(n) if all(k >= len(r) or not r[k].get_text(strip=True) for r in body)]
            for r in rows:
                for k in sorted(empty, reverse=True):
                    if k < len(r): r[k].decompose()
    for t in soup.select("h1 .num, h2 .num, h3 .num"):
        t.append(NavigableString(". "))
    heads = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    hidx = {id(h): k for k, h in enumerate(heads)}
    target = {}
    for el in soup.find_all(id=True):                          # an id points at its own heading or the first heading inside it
        h = el if el.name in ("h1", "h2", "h3", "h4", "h5", "h6") else el.find(["h1", "h2", "h3", "h4", "h5", "h6"])
        if h is None:                                          # e.g. <div id="top"> before everything: the first heading after it
            h = el.find_next(["h1", "h2", "h3", "h4", "h5", "h6"])
        if h is not None: target[el["id"]] = hidx[id(h)]
    if heads: target.setdefault("top", 0)
    for a in soup.find_all("a", href=True):
        if a["href"].startswith("#"):
            k = target.get(a["href"][1:])
            if k is None: a.unwrap()
            else: a["href"] = f"#__H{k}__"
    for img in soup.find_all("img"): img.decompose()
    for cell in soup.find_all(["td", "th"]):                   # one line per cell
        for br in cell.find_all("br"): br.replace_with(" ")
        for li in cell.find_all("li"): li.insert(0, NavigableString(" • ")); li.unwrap()
        for pre in cell.find_all("pre"): pre.name = "code"
        for b in cell.find_all(["p", "div", "ul", "ol", "section", "h3", "h4", "table", "tbody", "tr"]): b.insert_after(NavigableString(" ")); b.unwrap()
    for d in soup.find_all(["details", "summary"]): d.unwrap()
    for pre in soup.find_all("pre"):                           # fenced code blocks, with a language where it is clear
        txt = pre.get_text()
        lang = ("cpp" if re.search(r"#include|vector<|int main|class \w+ *\{|std::|cout", txt) else "sql" if re.search(r"\bSELECT\b|\bCREATE TABLE\b", txt)
                else "python" if re.search(r"^\s*(def|import|from) ", txt, re.M) else "bash" if re.search(r"^\s*(aws|git|docker|sudo|ls|cd|chmod|grep|curl|pip|python3?|ss|ps|nmap) ", txt, re.M) else "text")
        pre.clear(); code = soup.new_tag("code"); code.string = txt; pre.append(code); pre["class"] = [lang]
    md = subprocess.run(["pandoc", "-f", "html", "-t", "gfm-raw_html", "--wrap=none"], input=str(soup), capture_output=True, text=True, check=True).stdout
    seen, slugs, fence = {}, [], False
    for line in md.splitlines():
        if line.startswith("```"): fence = not fence
        m = None if fence else re.match(r"^(#{1,6})\s+(.*)$", line)
        if m: slugs.append(slugify(m.group(2), seen))
    md = re.sub(r"#__H(\d+)__", lambda m: "#" + slugs[int(m.group(1))] if int(m.group(1)) < len(slugs) else "", md)
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    bad = no_html_outside_code(md)
    assert not bad, "HTML left in Markdown: " + " | ".join(bad[:3])
    assert len(slugs) == len(heads), f"heading count changed: {len(heads)} in HTML, {len(slugs)} in Markdown"
    return md
