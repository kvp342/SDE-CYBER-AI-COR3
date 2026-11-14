// node render.js config.json  → renders one document with an injected, page-numbered index and back-links.
// config: {mode, src, out, prefix, pages: {id: absPage} | null, kbLink: bool, entriesOut}
const { chromium } = require('playwright');
const fs = require('fs');
const S = '/tmp/claude-0/-home-user-intrusion-detection-and-prevention/407ceb01-6118-5f31-bc48-b59633a24cee/scratchpad/';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const KB = 'https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT';
const ALIASES = JSON.parse(fs.readFileSync(S + 'kb/aliases.json', 'utf8'));
const linkerSrc = fs.readFileSync(S + 'pdf/render_linked.js', 'utf8').match(/function linker\([\s\S]*?\n}\n/)[0];

const PRINT_EXTRA = '@page{size:A4;margin:12mm} html{-webkit-print-color-adjust:exact;print-color-adjust:exact} *{animation:none!important;transition:none!important} pre,code{white-space:pre-wrap!important;overflow-wrap:anywhere!important;overflow:visible!important} pre{font-size:7.5pt!important}';
const FLAT = '@page{size:A4;margin:10mm} html{-webkit-print-color-adjust:exact;print-color-adjust:exact} *{animation:none!important;transition:none!important} canvas,video{display:none!important} *,*::before,*::after{box-shadow:none!important;text-shadow:none!important;filter:none!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important;mix-blend-mode:normal!important;background-image:none!important;mask:none!important;-webkit-mask:none!important;opacity:1!important} body::before,body::after,html::before,html::after,.today::before,.today::after{display:none!important} pre,code{white-space:pre-wrap!important;overflow-wrap:anywhere!important}';
const IDX_CSS = `
@page { @bottom-right { content: none !important; } }
.pdfidx { break-after: page; break-before: auto; padding: 4mm 0 0; font-family: Inter, system-ui, sans-serif; color: #1e293b; background: #fff; }
.pdfidx h2 { font: 700 24pt/1.1 "Space Grotesk", Inter, sans-serif; color: #0f172a; margin: 0 0 2mm; border: 0; padding: 0; }
.pdfidx .ixsub { font-size: 9.5pt; color: #475569; margin: 0 0 5mm; max-width: 160mm; }
.pdfidx .ixl { columns: var(--cols, 1); column-gap: 9mm; }
.pdfidx a.ix { display: flex; align-items: baseline; gap: 5px; text-decoration: none !important; border: 0 !important; color: #1e293b !important; padding: 1.4px 0; break-inside: avoid; font-size: 8.8pt; }
.pdfidx a.ix.l1 { font-weight: 700; font-size: 10pt; margin-top: 7px; color: #0f172a !important; }
.pdfidx a.ix.l1:first-child { margin-top: 0; }
.pdfidx a.ix.l2 { padding-left: 13px; color: #334155 !important; }
.pdfidx a.ix .dt { flex: 1; border-bottom: 1px dotted #94a3b8; transform: translateY(-3px); min-width: 10px; }
.pdfidx a.ix .n { font: 600 8.4pt "JetBrains Mono", ui-monospace, monospace; color: #c2410c; font-variant-numeric: tabular-nums; }
a.pdfback { display: inline-block; vertical-align: middle; margin-left: 8px; font: 600 7.5pt "JetBrains Mono", ui-monospace, monospace !important; letter-spacing: 0 !important; text-transform: none !important;
  color: #c2410c !important; border: 1px solid #fdba74 !important; background: #fff7ed; border-radius: 99px; padding: 0 7px; text-decoration: none !important; white-space: nowrap; }
`;

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1100, height: 1400 }, colorScheme: 'light' });
  if (cfg.mode === 'playbook') {
    await ctx.addInitScript(() => { try { localStorage.setItem('pb:theme', 'cafe'); localStorage.setItem('pb:mode', 'laptop'); } catch (e) {} });
    await ctx.route(/(cdnjs|jsdelivr)/, r => r.abort());
  }
  const p = await ctx.newPage();
  await p.goto('file://' + S + cfg.src, { waitUntil: cfg.mode === 'playbook' ? 'load' : 'networkidle', timeout: 60000 });
  if (cfg.mode === 'playbook') await p.waitForTimeout(1500);
  await p.evaluate(() => document.fonts.ready);
  if (['cheat', 'roadmap', 'playbook'].includes(cfg.mode)) {
    await p.evaluate(() => { document.documentElement.setAttribute('data-theme', document.documentElement.dataset.theme === 'cafe' ? 'cafe' : 'light');
      document.querySelectorAll('details').forEach(d => d.open = true);
      document.querySelectorAll('[hidden]').forEach(e => e.removeAttribute('hidden')); });
  }
  if (cfg.mode === 'playbook') {
    await p.evaluate(() => { document.documentElement.setAttribute('data-theme', 'cafe');
      for (const e of document.querySelectorAll('body *')) { const ps = getComputedStyle(e).position;
        if (ps === 'fixed') e.style.setProperty('display', 'none', 'important'); else if (ps === 'sticky') e.style.setProperty('position', 'static', 'important'); } });
    await p.addStyleTag({ content: FLAT });
  } else if (cfg.mode === 'cheat' || cfg.mode === 'roadmap') await p.addStyleTag({ content: PRINT_EXTRA });

  if (cfg.kbLink) { const linker = eval('(' + linkerSrc + ')'); await p.evaluate(linker, { KB, ALIASES }); }

  const entries = await p.evaluate(({ mode, prefix }) => {
    // 1) prefix every id and internal href so merged PDFs never collide
    for (const e of document.querySelectorAll('[id]')) e.id = prefix + e.id;
    for (const a of document.querySelectorAll('a[href^="#"]')) { const h = a.getAttribute('href'); if (h.length > 1) a.setAttribute('href', '#' + prefix + h.slice(1)); }
    const T = s => (s || '').replace(/\s+/g, ' ').trim();
    const ent = []; let k = 0;
    const need = (el) => { if (!el.id) el.id = prefix + 'x' + (k++); return el.id; };
    const add = (el, title, lvl, back, headEl) => { ent.push({ id: need(el), title, lvl }); if (back && headEl) headEl.dataset.back = '1'; };
    if (mode === 'guide') {
      document.querySelectorAll('section.pg').forEach((s, i) => { if (s.classList.contains('cover')) return;
        const no = T(s.querySelector('.sh .no')?.textContent), h = s.querySelector('.sh h1');
        add(s, (no ? no + '  ' : '') + T(h?.textContent), 1, true, h); });
    } else if (mode === 'cheat') {
      document.querySelectorAll('section.sec').forEach(s => { const h = s.querySelector('h2'); add(s, T(h?.textContent), 1, true, h); });
    } else if (mode === 'roadmap') {
      document.querySelectorAll('section.sec, section.intro').forEach(s => { const h = s.querySelector('h2, h1'); add(s, T(h?.textContent), 1, true, h);
        if (s.id.endsWith('weeks')) {
          for (const d of s.querySelectorAll('details')) { if (d.parentElement.closest('details')) continue;
            const sm = d.querySelector(':scope > summary'); if (!sm) continue;
            const kids = [...sm.children].map(c => T(c.textContent)).filter(Boolean);
            const lab = kids.length >= 2 ? kids[0] + ' · ' + kids[1] : T(sm.textContent).slice(0, 60);
            add(d, lab, 2, false); } } });
    } else if (mode === 'playbook') {
      const td = document.getElementById(prefix + 'today'); if (td) { const h = td.querySelector('h1, h2'); add(td, 'Today', 1, true, h); }
      document.querySelectorAll('.part').forEach(pt => { const no = T(pt.querySelector('.ph .pn')?.textContent), h = pt.querySelector('.ph h1');
        add(pt, (no ? no + '  ' : '') + T(h?.textContent), 1, true, h);
        pt.querySelectorAll('section.sec[id]').forEach(s => { const h2 = s.querySelector('h2'); if (h2) add(s, T(h2.textContent), 2, false); }); });
    } else if (mode === 'kb') {
      document.querySelector('.toc')?.remove();
      let cat = null;
      document.querySelectorAll('article.tp').forEach(a => { const c = T(a.querySelector('.mt > span:not(.chip)')?.textContent);
        if (c !== cat) { cat = c; ent.push({ id: a.id, title: c, lvl: 1 }); }
        const h = a.querySelector('h2'); ent.push({ id: a.id, title: T(h.textContent), lvl: 2 }); h.dataset.back = '1'; });
    }
    return ent;
  }, { mode: cfg.mode, prefix: cfg.prefix });

  const meta = { guide: ['Index', 'Placement Field Guide. Tap any line to jump; every page has ↑ Index to come back.', 1],
    cheat: ['Index', 'Prep Cheat Sheet. Tap a line to jump; ↑ Index on each section brings you back.', 1],
    roadmap: ['Index', 'Placement Roadmap. Sections, then every week and month of the plan. Tap to jump.', 2],
    playbook: ['Index', 'DSA Placement Playbook: Today, all 13 parts and their sections. Tap to jump; ↑ Index on each part brings you back.', 2],
    kb: ['Index', 'All 167 pages by category: concepts, 43 worked solutions, model answers, the Elite pages, 8 mock interviews and 10 company files. Tap to jump; ↑ Index on each page brings you back.', 2] }[cfg.mode];
  await p.evaluate(({ entries, pages, meta, prefix, mode }) => {
    const pad = n => String(n);
    const box = document.createElement('section'); box.className = 'pdfidx'; box.id = prefix + 'pdf-index'; box.style.setProperty('--cols', meta[2]);
    box.innerHTML = `<h2>${meta[0]}</h2><p class="ixsub">${meta[1]}</p><div class="ixl"></div>`;
    const list = box.querySelector('.ixl');
    for (const e of entries) { const a = document.createElement('a'); a.className = 'ix l' + e.lvl; a.href = '#' + e.id;
      const t = document.createElement('span'); t.textContent = e.title; const d = document.createElement('span'); d.className = 'dt';
      const n = document.createElement('span'); n.className = 'n'; n.textContent = pages && pages[e.id] ? pad(pages[e.id]) : '000';
      a.append(t, d, n); list.append(a); }
    if (mode === 'guide' || mode === 'kb') { const cover = document.querySelector('section.cover'); cover.after(box); }
    else if (mode === 'playbook') { const td = document.getElementById(prefix + 'today'); (td ? td.parentElement.insertBefore(box, td) : document.body.prepend(box)); }
    else { const first = document.querySelector('section.sec, section.intro'); first.parentElement.insertBefore(box, first); }
    for (const h of document.querySelectorAll('[data-back="1"]')) { const a = document.createElement('a'); a.className = 'pdfback'; a.href = '#' + prefix + 'pdf-index'; a.textContent = '↑ Index'; h.append(a); }
  }, { entries, pages: cfg.pages, meta, prefix: cfg.prefix, mode: cfg.mode });
  await p.addStyleTag({ content: IDX_CSS });
  await p.waitForTimeout(400);
  await p.pdf({ path: S + cfg.out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  fs.writeFileSync(S + cfg.entriesOut, JSON.stringify(entries));
  await b.close();
})();
