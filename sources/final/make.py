"""Two-pass render with page-numbered indexes, then: start page with links, merge, bookmarks, page-number stamps."""
import json, subprocess, pathlib, io, sys
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
S = pathlib.Path("/tmp/claude-0/-home-user-intrusion-detection-and-prevention/407ceb01-6118-5f31-bc48-b59633a24cee/scratchpad")
F = S / "final"

def dests(pdf):
    r = PdfReader(str(pdf)); return {k.lstrip("/"): r.get_destination_page_number(v) for k, v in r.named_destinations.items()}, len(r.pages)

def render(mode, src, prefix, offset, kblink, tag):
    out, ent = F / f"{tag}.pdf", F / f"{tag}.json"
    cfg = dict(mode=mode, src=src, out=str(out.relative_to(S)), prefix=prefix, pages=None, kbLink=kblink, entriesOut=str(ent.relative_to(S)))
    for attempt in (1, 2):
        (F / "cfg.json").write_text(json.dumps(cfg))
        subprocess.run(["node", str(F / "render.js"), str(F / "cfg.json")], check=True)
        d, n = dests(out)
        entries = json.loads(ent.read_text())
        pages = {e["id"]: offset + d[e["id"]] + 1 for e in entries if e["id"] in d}
        missing = [e["id"] for e in entries if e["id"] not in d]
        if attempt == 1: n1, cfg["pages"] = n, pages
    assert n == n1, f"{tag}: page count changed {n1} -> {n}"
    assert pages == cfg["pages"], f"{tag}: pages moved between passes"
    print(f"{tag}: {n} pages, {len(entries)} index entries, missing {len(missing)}")
    return out, entries, pages, n

def stamp(writer, skip, label=lambda i, n: f"{i + 1} / {n}"):
    n = len(writer.pages)
    for i, pg in enumerate(writer.pages):
        if i in skip: continue
        w, h = float(pg.mediabox.width), float(pg.mediabox.height)
        buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(w, h)); c.setFont("Helvetica", 7.5); c.setFillGray(0.55)
        c.drawRightString(w - 26, 14, label(i, n)); c.save(); buf.seek(0)
        pg.merge_page(PdfReader(buf).pages[0])
        pg.compress_content_streams(level=9)

def outline(writer, entries, pages, parent=None, base=0):
    cur = None
    for e in entries:
        if e["id"] not in pages: continue
        pi = pages[e["id"]] - 1 + base
        if e["lvl"] == 1: cur = writer.add_outline_item(e["title"], pi, parent=parent, fit=Fit.fit())
        else: writer.add_outline_item(e["title"], pi, parent=cur or parent, fit=Fit.fit())

def check_links(path):
    r = PdfReader(str(path)); names = set(k.lstrip("/") for k in r.named_destinations); bad = 0; internal = 0
    for pg in r.pages:
        for a in pg.get("/Annots") or []:
            o = a.get_object(); d = o.get("/Dest") or (o.get("/A") or {}).get("/D")
            if d is None: continue
            internal += 1
            if isinstance(d, str) or hasattr(d, "lstrip"):
                if str(d).lstrip("/") not in names: bad += 1
    print(f"  {path.name}: {internal} internal links, {bad} broken")

def single(mode, src, prefix, kblink, tag, final_name, skip_first=True):
    out, entries, pages, n = render(mode, src, prefix, 0, kblink, tag)
    w = PdfWriter(clone_from=PdfReader(str(out)))
    outline(w, [{"id": prefix + "pdf-index", "title": "Index", "lvl": 1}] + entries, {**pages, prefix + "pdf-index": dests(out)[0][prefix + "pdf-index"] + 1})
    stamp(w, {0} if skip_first else set())
    w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    dst = S / "final" / final_name; w.write(str(dst)); check_links(dst); return dst

if __name__ == "__main__":
    which = sys.argv[1:] or ["playbook", "kb", "complete"]
    if "playbook" in which: single("playbook", "playbook.html", "pb-", False, "pb", "DSA-Placement-Playbook.pdf", skip_first=False)
    if "kb" in which: single("kb", "kb/kb-print.html", "kb-", False, "kbp", "Placement-Knowledge-Base.pdf")
    if "complete" in which:
        import start
        START_PAGES = 1
        g = render("guide", "pdf/placement-field-guide.html", "g-", START_PAGES, True, "g")
        c = render("cheat", "cheat/prep-cheat-sheet-offline.html", "c-", START_PAGES + g[3], True, "c")
        r = render("roadmap", "roadmap/placement-roadmap-offline.html", "r-", START_PAGES + g[3] + c[3], True, "r")
        sp, links = start.build(g, c, r, START_PAGES)
        w = PdfWriter()
        for part in [sp, g[0], c[0], r[0]]: w.append(str(part))
        for pi, rect, target in links: w.add_annotation(page_number=pi, annotation=Link(rect=rect, target_page_index=target - 1))
        top = [("Start here", 1, None), ("1 · Placement Field Guide", 1 + START_PAGES, g), ("2 · Prep Cheat Sheet", 1 + START_PAGES + g[3], c), ("3 · Placement Roadmap", 1 + START_PAGES + g[3] + c[3], r)]
        for title, pg, doc in top:
            par = w.add_outline_item(title, pg - 1, fit=Fit.fit())
            if doc:
                pre = doc[1][0]["id"].split("-")[0] + "-"
                idx = dests(doc[0])[0][pre + "pdf-index"] + pg
                w.add_outline_item("Index", idx - 1, parent=par, fit=Fit.fit())
                outline(w, doc[1], doc[2], parent=par)
        stamp(w, {0, START_PAGES})
        w.add_metadata({"/Title": "Placement Prep — Complete (Guide + Cheat Sheet + Roadmap)"})
        w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
        dst = F / "Placement-Prep-Complete.pdf"; w.write(str(dst)); check_links(dst)
