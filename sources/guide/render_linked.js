// Render guide, cheat sheet and roadmap to PDF with every known topic name linked to the knowledge base.
const { chromium } = require('playwright');
const fs = require('fs');
const S = '/tmp/claude-0/-home-user-intrusion-detection-and-prevention/407ceb01-6118-5f31-bc48-b59633a24cee/scratchpad/';
const KB = 'https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT';
const ALIASES = JSON.parse(fs.readFileSync(S + 'kb/aliases.json', 'utf8'));

function linker({ KB, ALIASES }) {
  const SKIP_CONTAINS = new Set(['foundation', 'core', 'advanced', 'elite', 'sprint', 'batch', 'interview-ready', 'cache', 'heap', 'stack', 'contests', 'mocks', 'maths', 'resume', 'referral', 'stl', 'trees', 'crypto', 'track it', 'low energy', 'full force', 'exam mode', 'college day', 'hft', 'offer', 'open source', 'ai', 'aws', 'dns', 'tls', 'http', 'sql', 'oop', 'dbms', 'os', 'cn', 'dsa', 'dp', 'bfs', 'dfs', 'dsu', 'lld', 'hld', 'hr', 'rag', 'iam', 'lcs', 'cp', 'bst', 'ctf', 'ctfs', 'xss', 'csrf', 'ssrf', 'idor', 'sqli', 'abac']);
  const norm = s => s.replace(/\s+/g, ' ').trim().toLowerCase().replace(/[.:;,]+$/, '');
  const exact = new Map(), cont = [];
  for (const [id, names] of Object.entries(ALIASES)) for (const n of names) {
    const k = norm(n); if (!exact.has(k)) exact.set(k, id);
    if (k.length >= 5 && !SKIP_CONTAINS.has(k)) cont.push([k, id]);
  }
  // short acronyms are safe to link inside text only with exact case + word boundaries
  const ACR = { 'DP': 'dp', 'BFS': 'bfs', 'DFS': 'dfs', 'DSU': 'dsu', 'LLD': 'lld', 'HLD': 'hld', 'RAG': 'llm-rag', 'IAM': 'iam', 'LCS': 'lcs', 'BST': 'bst', 'XSS': 'xss', 'CSRF': 'xss', 'SSRF': 'ssrf', 'IDOR': 'access-control', 'ABAC': 'abac', 'SQLi': 'sqli', 'STL': 'cpp-stl', 'OWASP': 'owasp', 'CloudTrail': 'cloudtrail', 'TenantWall': 'tenantwall', 'Dijkstra': 'dijkstra', 'KMP': 'string-algos', 'ACID': 'acid', 'SOLID': 'solid', 'STAR': 'star', 'CSES': 'cp', 'Codeforces': 'cp', 'GSoC': 'open-source', 'UMPIRE': 'umpire', 'Anki': 'spaced-repetition' };
  cont.sort((a, b) => b[0].length - a[0].length);
  const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const reCont = new RegExp('(^|[^a-z0-9])(' + cont.map(c => esc(c[0])).join('|') + ')(?![a-z0-9])', 'i');
  const contId = new Map(cont);
  const reAcr = new RegExp('\\b(' + Object.keys(ACR).map(esc).join('|') + ')\\b');
  const bad = el => el.closest('a, pre, code, .chip, .cover, script, style, nav, header.top, .tl .d, th, .src');
  const mk = (id, txt) => { const a = document.createElement('a'); a.href = KB + '#' + id; a.className = 'kbl'; a.textContent = txt; return a; };
  let nExact = 0, nCont = 0;
  // 1) exact names on short elements
  for (const e of document.querySelectorAll('h1, h2, h3, h4, b, strong, td, li, summary, dt, em, p')) {
    if (bad(e) || e.querySelector('a, pre, code, table, ul, ol')) continue;
    const id = exact.get(norm(e.textContent)); if (!id) continue;
    const a = mk(id, ''); while (e.firstChild) a.append(e.firstChild); e.append(a); nExact++;
  }
  // 2) names inside running text: up to 3 links per element, distinct topics
  for (const e of document.querySelectorAll('td, li, p, dd')) {
    if (bad(e)) continue;
    const used = new Set([...e.querySelectorAll('a.kbl')].map(a => a.href)); let count = 0;
    const walker = document.createTreeWalker(e, NodeFilter.SHOW_TEXT, { acceptNode: n => bad(n.parentElement) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
    const nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
    for (let node of nodes) {
      let guard = 0;
      while (node && count < 3 && guard++ < 6) {
        const t = node.nodeValue; let m = reCont.exec(t), id, start, len;
        if (m) { id = contId.get(m[2].toLowerCase()); start = m.index + m[1].length; len = m[2].length; }
        const m2 = reAcr.exec(t);
        if (m2 && (!m || m2.index < start)) { id = ACR[m2[1]]; start = m2.index; len = m2[1].length; }
        if (!id) break;
        const href = KB + '#' + id;
        if (used.has(href)) { // skip this occurrence: continue after it
          const rest = node.splitText(start + len); node = rest; continue; }
        const mid = node.splitText(start); const rest = mid.splitText(len);
        mid.replaceWith(mk(id, mid.nodeValue)); used.add(href); count++; nCont++; node = rest;
      }
    }
  }
  if (!document.getElementById('kbl-style')) { const s = document.createElement('style'); s.id = 'kbl-style';
    s.textContent = 'a.kbl{color:inherit!important;text-decoration:none!important;border-bottom:1px dotted #c2410c!important}'; document.head.append(s); }
  return [nExact, nCont];
}

(async () => {
  const b = await chromium.launch();
  const jobs = [
    ['pdf/placement-field-guide.html', 'pdf/linked-guide.pdf', false],
    ['cheat/prep-cheat-sheet-offline.html', 'pdf/linked-cheat.pdf', true],
    ['roadmap/placement-roadmap-offline.html', 'pdf/linked-roadmap.pdf', true],
  ];
  for (const [src, out, extra] of jobs) {
    const p = await b.newPage({ colorScheme: 'light', viewport: { width: 1100, height: 1400 } });
    await p.goto('file://' + S + src, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    if (extra) {
      await p.evaluate(() => { document.documentElement.setAttribute('data-theme', 'light');
        document.querySelectorAll('details').forEach(d => d.open = true);
        document.querySelectorAll('[hidden]').forEach(e => e.removeAttribute('hidden')); });
      await p.addStyleTag({ content: '@page{size:A4;margin:12mm} html{-webkit-print-color-adjust:exact;print-color-adjust:exact} *{animation:none!important;transition:none!important} pre,code{white-space:pre-wrap!important;overflow-wrap:anywhere!important;overflow:visible!important} pre{font-size:7.5pt!important}' });
    }
    const n = await p.evaluate(linker, { KB, ALIASES });
    console.log(out, 'links exact/contains', n);
    await p.waitForTimeout(500);
    await p.pdf({ path: S + out, format: 'A4', printBackground: true, preferCSSPageSize: true });
    await p.close();
  }
  await b.close();
})();
