"""Anki decks built only from material already checked elsewhere in the kit, plus a one-page import guide.
Run from the repo root: python3 generated/src/anki.py"""
import csv, html, io, pathlib, re, subprocess, sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"; DECKS = OUT / "anki"
sys.path[:0] = [str(SRC), str(ROOT / "sources" / "kb")]
import t_qa, t_sec, mcq_data, mcq2_data, aws_data, apti_data, apti2_data, secbank_data, t_probs, t_probs2, t_probs3
from pattern_stl import TREE, STL, BUGS            # importing builds that PDF too; cheap and keeps one source of truth
from onepagers import P as ONEPAGERS
E = html.escape
def clean(s): return re.sub(r"\s+", " ", str(s)).strip()

def sol_card(p):
    pattern = p["why"].split(".")[0].replace("Pattern: ", "")
    cx = next((x.replace("Complexity: ", "") for x in p["points"] if str(x).startswith("Complexity")), "")
    return (f"{p['title']}: which pattern, and what is the key idea?", f"Pattern: {pattern}. {' '.join(p['core'])}" + (f" Complexity: {cx}." if cx else ""))
decks = {
 "solutions": ("Worked solutions (123 problems)", [sol_card(p) for p in t_probs.P + t_probs2.P + t_probs3.P]),
 "core-cs": ("Core CS", [(q, a) for t in t_qa.TOPICS if t["id"] != "qa-security" for q, a in t["qa"]]
             + [(f"{t}: {term}?", d) for k, t, kb, defs, *_ in ONEPAGERS if k != "sysdesign" for term, d in defs]
             + [(q[0] + ("\n" + q[6].split("\n", 2)[2] if len(q) > 6 else ""), f"{q[1]}. {q[5]}") for s in mcq_data.SECTIONS for q in s["qs"]]
             + [(q[0] + ("\n" + q[6].split("\n", 2)[2] if len(q) > 6 else ""), f"{q[1]}. {q[5]}") for s in mcq2_data.SECTIONS for q in s["qs"]]),
 "patterns": ("DSA patterns and C++", [(f"Problem signal: {sig}. Which pattern?", f"{pat}  ({q})") for q, items in TREE for sig, pat, _ in items]
              + [(f"C++ bug: {a}. What goes wrong?", f"{b}. Fix: {c}") for a, b, c in BUGS]),
 "complexity": ("Complexity facts", [(f"{t}: {op}", cx) for t, ops in STL for op, cx in ops if cx]),
 "security": ("Security", [(q, a) for t in t_qa.TOPICS if t["id"] == "qa-security" for q, a in t["qa"]]
              + [(f"Explain: {t['title']}", " ".join(t["core"])) for t in t_sec.TOPICS]
              + [(q, a) for s in secbank_data.SECTIONS for q, a in s["qs"]]),
 "aws": ("AWS SAA-C03", [(f"Which AWS service? {need}", svc) for need, svc in aws_data.NEED]
         + [(q[0], f"{q[1]}. {q[5]}") for k in aws_data.QS for q in aws_data.QS[k]]
         + [(f"SAA-C03 domain '{t}' ({w}): key points?", " • ".join(n)) for k, t, w, kb, n in aws_data.DOMAINS]),
 "aptitude": ("Aptitude shortcuts", [(q["q"], f"{q['a']}. {q['why']}") for key, (t, s, qs) in apti_data.SECTIONS.items() if key != "verbal" for q in qs]
              + [(q["q"] if not q.get("data") else q["data"] + "\n" + q["q"], f"{q['a']}. {q['why']}") for key, (t, s, qs) in apti2_data.SECTIONS.items() for q in qs]),
}
DECKS.mkdir(exist_ok=True); counts = {}
for slug, (name, cards) in decks.items():
    seen, rows = set(), []
    for front, back in cards:
        f, b = clean(front), clean(back)
        if f and b and f not in seen: seen.add(f); rows.append((f, b))
    with open(DECKS / f"{slug}.csv", "w", newline="", encoding="utf-8") as fh:
        fh.write(f"#separator:Semicolon\n#html:false\n#notetype:Basic\n#deck:Placement::{name}\n#tags:placement {slug}\n")
        csv.writer(fh, delimiter=";", quoting=csv.QUOTE_MINIMAL).writerows(rows)
    with open(DECKS / f"{slug}.csv", encoding="utf-8") as fh:          # read back: every card has exactly two fields
        data = [r for r in csv.reader((l for l in fh if not l.startswith("#")), delimiter=";")]
    assert len(data) == len(rows) and all(len(r) == 2 for r in data), slug
    counts[slug] = (name, len(rows))
TOTAL = sum(n for _, n in counts.values())
rows = "".join(f"<tr><td><code>generated/anki/{s}.csv</code></td><td>{E(n)}</td><td class=c>{c}</td></tr>" for s, (n, c) in counts.items())
HTML = f'''<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>
@page {{ size: A4; margin: 13mm 14mm; }} body {{ font: 400 9.4pt/1.5 Inter, sans-serif; color: #1e293b; margin: 0; }} -webkit-print-color-adjust: exact;
.eb {{ font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; }} h1 {{ font: 700 24pt "Space Grotesk"; margin: 0 0 2mm; color: #0f172a; }} h2 {{ font: 700 12pt "Space Grotesk"; color: #1d4ed8; margin: 4mm 0 1.5mm; }}
table {{ border-collapse: collapse; width: 100%; }} th {{ font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.2mm 2mm; text-align: left; }} td {{ border-bottom: 1px solid #e2e8f0; padding: 1.3mm 2mm; }} .c {{ text-align: right; font-family: "JetBrains Mono"; }}
code {{ font: 600 8pt "JetBrains Mono"; }} ol {{ padding-left: 5mm; margin: 0; }} li {{ margin-bottom: 1mm; }} .note {{ background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; margin-top: 4mm; }}</style></head><body>
<p class="eb">SPACED REPETITION · ANKI DECKS</p><h1>{TOTAL} flashcards, ready to import</h1>
<p>Seven decks made from material already checked elsewhere in this kit (all 123 worked solutions, Core CS Q&amp;A, one-pagers, both MCQ banks, the pattern tree, the STL card, the 30 bugs, the security pages and interview bank, the AWS pack and both aptitude packs). Anki shows each card just before you would forget it, so 15–20 minutes a day keeps everything fresh until placements.</p>
<table><thead><tr><th>File</th><th>Deck</th><th class="c">Cards</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Android: AnkiDroid (free)</h2><ol><li>Download the .csv files from the repository on your phone (open the file on GitHub, then Raw, then save).</li><li>In AnkiDroid: menu → Import → choose the file. Check that the type is Basic, the separator is semicolon, and Field 1 is Front, Field 2 is Back.</li><li>Repeat for each file. Each lands in its own deck under "Placement".</li></ol>
<h2>iPhone: AnkiMobile (paid) or AnkiWeb (free in the browser)</h2><ol><li>Easiest: import on a computer with Anki desktop (free), then sync to a free AnkiWeb account, then sync on the phone.</li><li>AnkiMobile can also import the file from the Files app via the share sheet.</li></ol>
<h2>Computer: Anki desktop (free)</h2><ol><li>File → Import → pick a .csv. The first lines of each file tell Anki the separator, note type, deck and tags, so the defaults should already be right.</li><li>If your Anki is older and shows lines starting with # as cards, delete those cards; they are only settings.</li></ol>
<h2>Daily routine</h2><ol><li>New cards per day: 15 (Settings → New cards/day). Reviews come back on their own.</li><li>Answer honestly: Again if you could not say it out loud; Good if you could.</li><li>When a card keeps failing, open the matching Knowledge Base page and rewrite the card in your own words.</li><li>Add your own cards for every DSA problem you got wrong: front = problem name and signal, back = the key idea in one line.</li></ol>
<p class="note">Anki is free on desktop, Android and the web. The decks are plain text, so you can also open them in any spreadsheet app.</p></body></html>'''
(SRC / "anki.html").write_text(HTML)
js = SRC / "r.js"; js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/anki.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/anki.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
subprocess.run(["node", str(js)], check=True)
r = PdfReader(str(SRC / "anki.pdf")); assert len(r.pages) == 1, f"guide must be one page, got {len(r.pages)}"
w = PdfWriter(clone_from=r); w.add_metadata({"/Title": "Anki decks: import guide"}); w.write(str(OUT / "anki-decks-guide.pdf"))
for f in ("anki.html", "anki.pdf", "r.js"): (SRC / f).unlink()
print(TOTAL, counts)
