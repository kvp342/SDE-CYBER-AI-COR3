"""Pattern decision tree (1 page), C++ STL card (2 pages) and 30 common C++ contest bugs.
Every STL call on the card is compiled and run in stl_check.cpp first. Run from the repo root: python3 generated/src/pattern_stl.py"""
import html, subprocess, pathlib, io, tempfile
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
# (question, [(signal, pattern, kb id)])
TREE = [
 ("Is the input sorted, or can you sort it?", [("Find a pair or triple with a target sum", "Two pointers", "two-pointers"), ("Find a value, first/last position, or insert point", "Binary search", "binary-search"), ("Minimise the maximum / 'smallest X such that …' with a monotone check", "Binary search on the answer", "binary-search"), ("Merge or count overlapping ranges", "Sort + sweep (intervals)", "intervals")]),
 ("Contiguous subarray or substring?", [("Longest/shortest window with a condition", "Sliding window (variable)", "sliding-window"), ("Every window of size k", "Sliding window (fixed); monotonic deque for max/min", "sliding-window"), ("Subarray sum equals k, with negatives", "Prefix sum + hash map", "prefix-sum"), ("Maximum subarray sum", "Kadane", "dp")]),
 ("Next greater/smaller, spans, histograms?", [("Next greater element, stock span, daily temperatures", "Monotonic stack", "monotonic-stack"), ("Matching brackets, undo, expression evaluation", "Stack", "stack-queue")]),
 ("Top k, k-th largest, running median, merge k lists?", [("Need repeated min/max", "Heap (priority_queue)", "heap"), ("Running median", "Two heaps", "heap")]),
 ("Graph or grid?", [("Shortest path, unweighted / levels", "BFS", "bfs"), ("Shortest path, non-negative weights", "Dijkstra", "dijkstra"), ("Connected components, islands, cycle in undirected graph", "DFS / BFS / DSU", "dsu"), ("Ordering with prerequisites, cycle in directed graph", "Topological sort", "topo-sort"), ("Minimum spanning tree", "Kruskal (sort + DSU)", "dsu")]),
 ("Tree?", [("Depth, diameter, path sums, LCA", "DFS returning values up", "trees"), ("Level by level", "BFS by levels", "bfs"), ("Sorted order or k-th smallest in a BST", "Inorder traversal", "bst")]),
 ("All combinations, permutations, subsets, boards?", [("Generate everything, n ≤ 20", "Backtracking", "recursion"), ("n ≤ 20 and states of a subset", "Bitmask DP", "bitmask-dp")]),
 ("Count ways, min/max cost, overlapping subproblems?", [("Choices at each index or cell", "1-D / 2-D DP", "dp"), ("Two strings: LCS, edit distance", "String DP", "lcs"), ("Pick items under a capacity", "Knapsack DP", "dp")]),
 ("Prefix lookups, autocomplete, word search?", [("Many words sharing prefixes", "Trie", "trie")]),
 ("Local best choice provably leads to global best?", [("Intervals, jumps, scheduling", "Greedy (prove with exchange argument)", "greedy")]),
]
STL = [
 ("vector<T>", [("push_back / pop_back / back", "O(1) amortised"), ("operator[] / at", "O(1)"), ("insert / erase in the middle", "O(n)"), ("reserve(n)", "avoids reallocations"), ("sort(v.begin(), v.end())", "O(n log n)"), ("lower_bound / upper_bound (sorted)", "O(log n)")]),
 ("string", [("s.substr(pos, len)", "O(len), copies"), ("s.find(t)", "O(n·m) worst"), ("to_string(x) / stoi(s) / stoll(s)", "conversions"), ("s += c / s.push_back(c)", "O(1) amortised")]),
 ("deque<T>", [("push_front / push_back / pop_front / pop_back", "O(1)"), ("operator[]", "O(1)")]),
 ("stack<T> / queue<T>", [("push / pop / top / front", "O(1)"), ("empty() before top()/front()", "required")]),
 ("priority_queue<T>", [("push / pop", "O(log n)"), ("top", "O(1), largest by default"), ("min-heap: priority_queue<int, vector<int>, greater<int>>", ""), ("custom: priority_queue<T, vector<T>, decltype(cmp)> pq(cmp)", "")]),
 ("set / map (red-black tree)", [("insert / erase / find / count", "O(log n)"), ("lower_bound(x) / upper_bound(x)", "O(log n)"), ("iterate in sorted order", "O(n)"), ("multiset: erase(s.find(x)) removes one copy", "erase(x) removes all")]),
 ("unordered_set / unordered_map", [("insert / erase / find / count", "O(1) average, O(n) worst"), ("m[key] inserts a default if missing", "use find/count to check"), ("reserve(n)", "fewer rehashes")]),
 ("<algorithm>", [("sort / stable_sort", "O(n log n)"), ("reverse / rotate", "O(n)"), ("next_permutation", "O(n)"), ("accumulate (<numeric>), use 0LL for long long", "O(n)"), ("min_element / max_element", "O(n)"), ("unique (after sort) + erase", "O(n)"), ("binary_search", "O(log n)"), ("__gcd / gcd (C++17 <numeric>)", "O(log n)")]),
 ("Others", [("pair<int,int>, tuple; structured bindings auto [a, b]", ""), ("bitset<N>: count, set, test", "O(N/64)"), ("iota(v.begin(), v.end(), 0)", "fill 0,1,2…"), ("__builtin_popcount / __builtin_popcountll", "GCC bit count")]),
]
BUGS = [
 ("int overflow", "a * b with ints near 1e9; sums of 1e5 numbers up to 1e9", "Use long long; write 1LL * a * b"),
 ("accumulate with 0", "accumulate(v.begin(), v.end(), 0) on long longs truncates", "Pass 0LL"),
 ("Signed/unsigned loop", "for (int i = 0; i < v.size() - 1; i++) with an empty v: size() − 1 wraps to a huge value", "Cast: (int)v.size() - 1"),
 ("Out-of-bounds index", "a[i + 1] at the last index; grid neighbours off the edge", "Check bounds before indexing"),
 ("Uninitialised variables", "int ans; then ans = max(ans, x)", "Initialise every variable"),
 ("Global vs local arrays", "Large local array (1e6 ints) overflows the stack", "Make it global or use vector"),
 ("Reset between test cases", "Globals or containers keep old data across t test cases", "Clear or re-create per test"),
 ("endl in loops", "endl flushes every line: slow output", "Use '\\n'"),
 ("Slow I/O", "cin/cout without sync off on 1e6 numbers", "ios::sync_with_stdio(false); cin.tie(nullptr);"),
 ("Mixing scanf and cin after sync off", "Undefined interleaving once sync is off", "Use one style"),
 ("map[key] creates keys", "if (m[x]) inserts x and can grow the map in a loop", "Use m.count(x) or m.find(x)"),
 ("Iterator invalidation", "Erasing from a vector or map while iterating with the same iterator", "it = v.erase(it), or collect then erase"),
 ("Modifying a container in range-for", "push_back while iterating a vector", "Iterate by index over the old size"),
 ("Comparator not strict", "sort with a <= b crashes or misorders", "Comparators must be strict: a < b"),
 ("priority_queue order", "Expecting smallest on top", "Default is max-heap; use greater<> for min"),
 ("multiset erase(value)", "Removes every copy", "erase(s.find(x)) to remove one"),
 ("Integer division and modulo with negatives", "-7 / 2 == -3 and -7 % 2 == -1", "For a positive mod: ((a % m) + m) % m"),
 ("Modular arithmetic", "Forgetting % after each multiply", "Reduce after every operation; use long long"),
 ("Floating point equality", "if (x == 0.3)", "Compare with an epsilon, or use integers"),
 ("pow() for integers", "pow(10, 9) returns double and can round down", "Write a binary exponentiation for integers"),
 ("Wrong INF", "INT_MAX + 1 overflows during relaxations", "Use 1e18 as long long or check before adding"),
 ("memset with non-zero values", "memset(a, 1, sizeof a) sets bytes, not ints", "Only 0 and -1 are safe; use fill"),
 ("Recursion depth", "DFS 1e6 deep overflows the stack", "Iterative DFS or BFS"),
 ("Passing big containers by value", "void f(vector<int> v) copies on every call", "Pass by const reference"),
 ("string += in a loop with s = s + c", "s = s + c copies each time: O(n²)", "Use s += c or s.push_back(c)"),
 ("substr in a loop", "s.substr inside a loop copies: hidden O(n²)", "Use indices or string_view"),
 ("Off-by-one in binary search", "while (lo < hi) with mid rounding the wrong way loops forever", "Pick one template and stick to it"),
 ("Shadowed variables", "Declaring n again inside a block hides the outer n", "Compile with -Wall -Wshadow"),
 ("Edge cases", "n = 1, empty input, all equal, all negative, maximum values", "Test them before submitting"),
 ("Reading the wrong constraints", "O(n²) for n = 2e5", "From n, decide the target complexity first"),
]
CHECK = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    vector<int> v{5, 3, 1}; v.reserve(10); v.push_back(4); v.pop_back(); assert(v.back() == 1 && v.at(0) == 5);
    v.insert(v.begin() + 1, 9); v.erase(v.begin() + 1); sort(v.begin(), v.end()); assert((v == vector<int>{1, 3, 5}));
    assert(*lower_bound(v.begin(), v.end(), 3) == 3 && *upper_bound(v.begin(), v.end(), 3) == 5 && binary_search(v.begin(), v.end(), 5));
    string s = "hello"; assert(s.substr(1, 3) == "ell" && s.find("ll") == 2 && to_string(42) == "42" && stoi("17") == 17 && stoll("10000000000") == 10000000000LL);
    s += '!'; s.push_back('?'); assert(s == "hello!?");
    deque<int> d; d.push_front(1); d.push_back(2); assert(d[0] == 1); d.pop_front(); d.pop_back(); assert(d.empty());
    stack<int> st; st.push(1); assert(!st.empty() && st.top() == 1); queue<int> q; q.push(2); assert(q.front() == 2); q.pop();
    priority_queue<int> mx; mx.push(1); mx.push(3); assert(mx.top() == 3);
    priority_queue<int, vector<int>, greater<int>> mn; mn.push(1); mn.push(3); assert(mn.top() == 1);
    auto cmp = [](const pair<int,int>& a, const pair<int,int>& b) { return a.second > b.second; };
    priority_queue<pair<int,int>, vector<pair<int,int>>, decltype(cmp)> pq(cmp); pq.push({1, 9}); pq.push({2, 4}); assert(pq.top().first == 2);
    set<int> se{4, 1, 7}; assert(*se.lower_bound(2) == 4 && *se.upper_bound(4) == 7 && se.count(1) && se.find(9) == se.end());
    multiset<int> ms{2, 2, 2}; ms.erase(ms.find(2)); assert(ms.size() == 2); ms.erase(2); assert(ms.empty());
    map<string, int> m; m["a"] = 1; assert(m.count("b") == 0); (void)m["b"]; assert(m.size() == 2);   // operator[] inserted "b"
    unordered_map<int, int> um; um.reserve(100); um[3]++; assert(um.find(3)->second == 1);
    vector<int> w{3, 1, 2}; reverse(w.begin(), w.end()); assert((w == vector<int>{2, 1, 3}));
    rotate(w.begin(), w.begin() + 1, w.end()); assert((w == vector<int>{1, 3, 2})); next_permutation(w.begin(), w.end()); assert((w == vector<int>{2, 1, 3}));
    vector<long long> big{2000000000LL, 2000000000LL}; assert(accumulate(big.begin(), big.end(), 0LL) == 4000000000LL);
    assert(*min_element(w.begin(), w.end()) == 1 && *max_element(w.begin(), w.end()) == 3);
    vector<int> u{1, 1, 2, 2, 3}; u.erase(unique(u.begin(), u.end()), u.end()); assert(u.size() == 3);
    assert(gcd(12, 18) == 6 && __gcd(12, 18) == 6);
    stable_sort(u.begin(), u.end()); auto [a, b] = make_pair(1, 2); assert(a + b == 3); tuple<int, char> t{1, 'x'}; assert(get<1>(t) == 'x');
    bitset<8> bs; bs.set(1); bs.set(3); assert(bs.count() == 2 && bs.test(3));
    vector<int> io(4); iota(io.begin(), io.end(), 0); assert(io[3] == 3); assert(__builtin_popcount(7) == 3 && __builtin_popcountll(1LL << 40) == 1);
    assert(-7 / 2 == -3 && -7 % 2 == -1 && ((-7 % 3) + 3) % 3 == 2);   // bug 17
    vector<int> e; assert((int)e.size() - 1 == -1);                       // bug 3, the safe form
    puts("stl ok");
}
'''
def check():
    d = tempfile.mkdtemp(); (pathlib.Path(d) / "c.cpp").write_text(CHECK)
    c = subprocess.run(["g++", "-std=c++17", "-Wall", "-fsanitize=address,undefined", "-fno-sanitize-recover=all", f"{d}/c.cpp", "-o", f"{d}/c"], capture_output=True, text=True)
    assert c.returncode == 0 and "warning" not in c.stderr, c.stderr
    r = subprocess.run([f"{d}/c"], capture_output=True, text=True); assert r.stdout.strip() == "stl ok", r.stderr
check()
(OUT / "stl_check.cpp").write_text(CHECK)
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{a}">{t}</a></td><td class="pg"><a href="#{a}">{pg(a)}</a></td></tr>' for t, a in [("Pattern decision tree", "tree"), ("C++ STL card", "stl"), ("30 common C++ contest bugs", "bugs")])
    out = [f'''<section class="cover"><p class="eb">DSA · QUICK REFERENCE</p><h1>Patterns, STL<br><span>and 30 bugs to avoid</span></h1>
<p class="lead">A one-page decision tree from what a problem says to the pattern to try, a two-page C++ STL card with complexities, and the thirty C++ mistakes that most often cost an accepted answer in contests and online assessments. Every STL call on the card was compiled and run (<code>generated/stl_check.cpp</code>).</p>
<table class="ix"><tbody>{rows}</tbody></table><p class="src">Start every problem by reading the constraints: n ≤ 20 → exponential is fine; n ≤ 5000 → O(n²); n ≤ 2·10<sup>5</sup> → O(n log n); n ≤ 10<sup>7</sup> → O(n).</p></section>''']
    tree = "".join(f'<div class="node"><div class="qn">{E(q)}</div><table class="br"><tbody>{"".join(f"<tr><td class=sig>{E(s)}</td><td class=arrow>→</td><td><a href={chr(34)}{KB}{k}{chr(34)}>{E(p)}</a></td></tr>" for s, p, k in items)}</tbody></table></div>' for q, items in TREE)
    out.append(f'<section class="sec" id="tree"><h2>Pattern decision tree<a class="back" href="#top">↑ Index</a></h2><p class="meta">Ask the questions top to bottom; the first match is usually the pattern. Each pattern links to its Knowledge Base page.</p><div class="tree">{tree}</div></section>')
    stl = "".join(f'<div class="card"><h3>{E(t)}</h3><table><tbody>{"".join(f"<tr><td><code>{E(a)}</code></td><td class=cx>{E(b)}</td></tr>" for a, b in ops)}</tbody></table></div>' for t, ops in STL)
    out.append(f'<section class="sec" id="stl"><h2>C++ STL card<a class="back" href="#top">↑ Index</a></h2><div class="cards">{stl}</div></section>')
    bugs = "".join(f"<tr><td class=n>{i + 1}</td><td class=t>{E(a)}</td><td>{E(b)}</td><td class=fix>{E(c)}</td></tr>" for i, (a, b, c) in enumerate(BUGS))
    out.append(f'<section class="sec" id="bugs"><h2>30 common C++ contest bugs<a class="back" href="#top">↑ Index</a></h2><table class="bugs"><thead><tr><th>#</th><th>Bug</th><th>What goes wrong</th><th>Fix</th></tr></thead><tbody>{bugs}</tbody></table><p class="meta">Compile practice code with <code>g++ -std=c++17 -Wall -Wextra -Wshadow -fsanitize=address,undefined</code>: the sanitizers catch bugs 3, 4, 6 and 12 at the line where they happen.</p></section>')
    return "".join(out)
CSS = """@page { size: A4; margin: 11mm 12mm 13mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.4pt/1.38 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 18mm 15mm; break-after: page; } code { font: 400 7.5pt "JetBrains Mono"; font-variant-ligatures: none; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 20pt; }
.lead { font-size: 10pt; color: #475569; } table { border-collapse: collapse; width: 100%; } .ix td { padding: 2.4mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 11pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.src { font-size: 8.5pt; color: #475569; margin-top: 5mm; background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; } .sec { break-before: page; }
h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2mm; display: flex; align-items: baseline; } .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
.meta { color: #475569; margin: 0 0 2mm; } .node { border-left: 3px solid #1d4ed8; padding: .6mm 0 .6mm 3mm; margin-bottom: 1.6mm; break-inside: avoid; } .qn { font: 700 9pt "Space Grotesk"; color: #1d4ed8; }
.br td { padding: .25mm 1.5mm; vertical-align: top; } .br .sig { width: 58%; color: #334155; } .br .arrow { width: 5mm; color: #94a3b8; } .br a { font-weight: 600; }
.cards { column-count: 2; column-gap: 6mm; } .card { break-inside: avoid; margin-bottom: 3mm; } .card h3 { font: 700 9.5pt "JetBrains Mono"; color: #1d4ed8; margin: 0 0 1mm; } .card td { border-bottom: 1px solid #eef2f7; padding: .7mm 1.5mm; vertical-align: top; } .card .cx { color: #166534; font-size: 7.6pt; width: 30%; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; color: #64748b; background: #f1f5f9; padding: 1.2mm 2mm; text-align: left; } .bugs td { border-bottom: 1px solid #eef2f7; padding: .85mm 2mm; vertical-align: top; font-size: 7.9pt; } .bugs .n { color: #94a3b8; font-family: "JetBrains Mono"; } .bugs .t { font-weight: 700; width: 36mm; } .bugs .fix { color: #166534; width: 52mm; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "ps.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/ps.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k in ("tree", "stl", "bugs"))
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for t, k in [("Pattern decision tree", "tree"), ("STL card", "stl"), ("30 C++ bugs", "bugs")]: w.add_outline_item(t, d2[k] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Pattern decision tree, STL card and 30 C++ bugs"}); w.write(str(OUT / "patterns-stl-card.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "ps.html"): (SRC / f).unlink()
print(NP, "pages", d2)
