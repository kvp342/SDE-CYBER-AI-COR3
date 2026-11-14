"""Print version of the knowledge base: contents + one block per topic, internal links between topics."""
import json, pathlib, html, re
D = pathlib.Path(__file__).parent
src = (D / "kb.html").read_text()
data = json.loads(re.search(r"const TOPICS = (\[.*?\]);\nconst LV", src, re.S).group(1).replace("<\\/", "</"))
E = lambda s: html.escape(s, quote=True)
LV = [("L0", "Foundation", "#15803d"), ("L1", "Core", "#0e7490"), ("L2", "Interview-ready", "#1d4ed8"), ("L3", "Advanced", "#6d28d9"), ("L4", "Elite", "#c2410c")]
CATS = ["Method", "DSA", "Problems", "Core CS", "Q&A", "Design", "Security", "Cloud", "AI", "Elite", "Career"]
by = {t["id"]: t for t in data}
chip = lambda l: f'<span class="chip" style="--k:{LV[l][2]}">{LV[l][0]} · {LV[l][1]}</span>'
host = lambda u: re.sub(r"^www\.", "", re.sub(r"^https?://([^/]+).*", r"\1", u))

toc = []
for c in CATS:
    ts = [t for t in data if t["cat"] == c]
    if ts: toc.append(f'<div class="tc"><h3>{E(c)}</h3><ol>' + "".join(f'<li><a href="#{t["id"]}">{E(t["title"])}</a> {chip(t["lvl"])}</li>' for t in ts) + '</ol></div>')

body = []
for c in CATS:
    for t in [t for t in data if t["cat"] == c]:
        k = LV[t["lvl"]][2]
        b = [f'<article class="tp" id="{t["id"]}" style="--k:{k}"><p class="mt">{chip(t["lvl"])} <span>{E(t["cat"])}</span></p><h2>{E(t["title"])}</h2>',
             f'<div class="why"><b>Why it matters for you</b><p>{E(t["why"])}</p></div>',
             f'<h4>{"The idea" if c == "Problems" else "The concept"}</h4>' + "".join(f"<p>{E(p)}</p>" for p in t["core"])]
        if t.get("qa"): b.append('<h4>Questions and model answers</h4>' + "".join(f'<div class="qa"><p class="q">{i + 1:02d}. {E(qq)}</p><p class="a">{E(aa)}</p></div>' for i, (qq, aa) in enumerate(t["qa"])))
        if t["points"]: b.append(f'<h4>{"Steps" if c == "Problems" else "Key points"}</h4><ul>' + "".join(f"<li>{E(p)}</li>" for p in t["points"]) + "</ul>")
        if t["code"]: b.append(f'<h4>{"Code" if c in ("DSA", "Core CS", "Design") else "Example"}</h4><pre>{E(t["code"])}</pre>')
        if t["pit"]: b.append('<h4>Common mistakes</h4><ul class="pit">' + "".join(f"<li>{E(p)}</li>" for p in t["pit"]) + "</ul>")
        if t["ask"]: b.append(f'<h4>{"Follow-up questions" if c == "Problems" else "Interview questions"}</h4><ul class="ask">' + "".join(f"<li>{E(p)}</li>" for p in t["ask"]) + "</ul>")
        links = [("Practise", t["prac"]), ("Learn from", t["learn"])]
        for h, arr in links:
            if arr: b.append(f'<h4>{h}</h4><p class="lk">' + " · ".join(f'<a href="{E(u)}">{E(n)}</a> <span>({E(host(u))})</span>' for n, u in arr) + "</p>")
        if t["rel"]: b.append('<p class="rel"><b>Related:</b> ' + " · ".join(f'<a href="#{r}">{E(by[r]["title"])}</a>' for r in t["rel"]) + "</p>")
        b.append("</article>")
        body.append("".join(b))

CSS = """@page { size: A4; margin: 13mm 14mm 15mm; @bottom-right { content: counter(page); font: 500 8pt 'JetBrains Mono'; color: #94a3b8; } }
@page :first { @bottom-right { content: none; } }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 9.4pt/1.5 Inter, sans-serif; color: #1e293b; }
h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif; margin: 0; color: #0f172a; }
a { color: #c2410c; text-decoration: none; }
.chip { display: inline-block; font: 600 7pt 'JetBrains Mono', monospace; color: var(--k); border: 1px solid color-mix(in srgb, var(--k) 45%, #fff); background: color-mix(in srgb, var(--k) 10%, #fff); border-radius: 99px; padding: 0 6px; white-space: nowrap; }
.cover { break-after: page; }
.cover .eb { font: 500 8.5pt 'JetBrains Mono'; letter-spacing: .14em; color: #c2410c; margin: 30mm 0 6mm; }
.cover h1 { font-size: 40pt; line-height: 1; letter-spacing: -.02em; }
.cover h1 span { color: #c2410c; }
.cover .s { font-size: 11pt; color: #475569; max-width: 150mm; margin: 6mm 0 8mm; }
.lv { display: grid; grid-template-columns: repeat(5, 1fr); gap: 5px; margin-bottom: 8mm; }
.lv div { border-top: 4px solid var(--k); background: color-mix(in srgb, var(--k) 8%, #fff); border-radius: 6px; padding: 6px 8px; font-size: 8pt; color: #475569; }
.lv b { display: block; font: 700 14pt 'Space Grotesk'; color: var(--k); }
.toc { columns: 2; column-gap: 8mm; }
.tc { break-inside: avoid; margin-bottom: 4mm; }
.tc h3 { font-size: 11pt; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 2px; margin-bottom: 3px; }
.tc ol { margin: 0; padding-left: 17px; font-size: 8.6pt; }
.tc li { margin-bottom: 1.5px; } .tc a { color: #1e293b; } .tc .chip { font-size: 6pt; }
.tp { break-before: page; }
.mt { margin: 0 0 3px; font: 600 7.5pt 'JetBrains Mono'; color: #64748b; letter-spacing: .08em; text-transform: uppercase; }
.tp h2 { font-size: 22pt; line-height: 1.1; padding-bottom: 6px; border-bottom: 3px solid var(--k); margin-bottom: 8px; }
.why { padding: 8px 11px; border-left: 4px solid var(--k); background: color-mix(in srgb, var(--k) 7%, #fff); border-radius: 0 7px 7px 0; margin-bottom: 4px; }
.why b { font: 600 7.5pt 'JetBrains Mono'; letter-spacing: .1em; text-transform: uppercase; color: var(--k); }
.why p { margin: 1px 0 0; }
h4 { font-size: 10.5pt; margin: 10px 0 3px; color: var(--k); break-after: avoid; }
p { margin: 0 0 5px; } ul { margin: 0; padding-left: 17px; } li { margin-bottom: 2px; }
ul.pit li::marker { content: '✗  '; color: #dc2626; } ul.ask li::marker { content: '☐  '; color: var(--k); }
pre { font: 500 7.8pt/1.45 'JetBrains Mono', monospace; background: #0e1424; color: #e3e8f2; border-radius: 7px; padding: 8px 10px; white-space: pre-wrap; overflow-wrap: anywhere; margin: 0; break-inside: avoid; }
.lk { font-size: 8.8pt; } .lk span { color: #94a3b8; font: 500 7pt 'JetBrains Mono'; }
.qa { break-inside: avoid; margin-bottom: 5px; } .qa .q { font-weight: 700; margin: 0 0 1px; color: #0f172a; } .qa .a { margin: 0 0 4px; }
.rel { margin-top: 10px; padding-top: 6px; border-top: 1px solid #e2e8f0; font-size: 8.8pt; }"""

lv = "".join(f'<div style="--k:{c}"><b>{t}</b>{n}</div>' for t, n, c in LV)
doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Placement Knowledge Base</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet"><style>{CSS}</style></head><body>
<section class="cover"><p class="eb">COMPANION TO YOUR PLACEMENT PDF</p><h1>Placement<br><span>Knowledge Base</span></h1>
<p class="s">{len(data)} pages, one topic each: the concept in depth, why it matters for your plan, key points, code, common mistakes, interview questions, practice problems and free resources. Tap a name below to jump to it; "Related" links at the end of each page jump between topics.</p>
<div class="lv">{lv}</div><div class="toc">{"".join(toc)}</div></section>
{"".join(body)}</body></html>'''
(D / "kb-print.html").write_text(doc)
print(len(data), "topics")
