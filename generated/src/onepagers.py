"""Core CS one-pagers: one A4 revision page each for OS, DBMS, CN, OOP, SQL and System Design.
Run from the repo root: python3 generated/src/onepagers.py"""
import html, subprocess, pathlib, io
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
E = lambda s: html.escape(str(s), quote=True)
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT#"
P = [
("os", "Operating Systems", "qa-os", [
 ("Process", "A program in execution with its own address space, PCB, registers and open files."),
 ("Thread", "A unit of execution inside a process; threads share code, heap and files but have their own stack and registers."),
 ("Context switch", "Saving one process's CPU state in its PCB and loading another's; pure overhead."),
 ("Scheduling", "FCFS, SJF/SRTF (optimal average wait, can starve), Round Robin (time quantum), Priority (aging prevents starvation)."),
 ("Deadlock", "Needs mutual exclusion, hold and wait, no preemption, circular wait. Handle by prevention, avoidance (Banker's), detection or ignoring."),
 ("Semaphore vs mutex", "Mutex: a lock with an owner. Semaphore: a counter with wait/signal; binary or counting."),
 ("Paging", "Fixed-size pages map to frames via a page table; no external fragmentation; TLB caches translations."),
 ("Virtual memory", "Demand paging lets programs exceed RAM; a page fault loads a missing page; thrashing = too few frames."),
 ("Page replacement", "FIFO (Belady's anomaly), LRU, Optimal (theoretical best), Clock (LRU approximation)."),
 ("System call", "A trap from user mode into kernel mode, e.g. fork, exec, read, write, mmap.")],
 """ new ──admit──> ready ──dispatch──> running ──exit──> terminated
                 ^  ^                  |   |
                 |  └───interrupt──────┘   |
                 └──I/O done── waiting <───┘ I/O or event wait

 virtual address = [ page number | offset ] ──TLB / page table──> [ frame | offset ]""",
 ["Process vs thread, and why threads are cheaper to switch.", "The four deadlock conditions and how Banker's algorithm avoids deadlock.", "Paging vs segmentation; internal vs external fragmentation.", "What happens on a page fault, step by step.", "Thrashing: cause (too few frames) and fixes (working set, fewer processes).", "Mutex vs semaphore; producer-consumer with empty/full/mutex.", "fork() return values: 0 in the child, child PID in the parent, −1 on error.", "Zombie (finished, not reaped) vs orphan (parent died, adopted by init).", "Round Robin quantum too large becomes FCFS; too small means switch overhead.", "User mode vs kernel mode, and how a system call crosses between them."]),
("dbms", "DBMS", "qa-dbms", [
 ("Keys", "Super key ⊇ candidate key (minimal) ⊇ primary key (chosen, unique, not null). Foreign key references another table's key."),
 ("Normalisation", "1NF atomic values; 2NF no partial dependency; 3NF no transitive dependency; BCNF every determinant is a candidate key."),
 ("ACID", "Atomicity (all or nothing, undo log), Consistency (constraints hold), Isolation (concurrency control), Durability (redo / write-ahead log)."),
 ("Isolation levels", "Read uncommitted < read committed (no dirty reads) < repeatable read (no non-repeatable reads) < serializable (no phantoms)."),
 ("Concurrency control", "Two-phase locking gives serializability; strict 2PL also avoids cascading aborts; MVCC gives readers snapshots."),
 ("Indexes", "B+ trees for range and equality lookups; hash for equality only; clustered = table order (one per table)."),
 ("Joins", "Inner, left, right, full outer, cross, self; executed as nested loop, hash join or merge join."),
 ("Transactions", "BEGIN … COMMIT / ROLLBACK; savepoints; deadlocks found with a wait-for graph."),
 ("SQL vs NoSQL", "Relational with schemas and joins vs key-value, document, column-family or graph stores that scale out easily."),
 ("CAP", "Under a network partition a distributed store chooses consistency or availability.")],
 """ Employee(emp_id, name, dept_id, dept_name)      dept_name depends on dept_id, not on the key
        └─ 3NF split ─>  Employee(emp_id, name, dept_id)   Department(dept_id, dept_name)

 B+ tree:            [ 30 | 60 ]
              /           |           \\
       [10 20] ──> [30 40 50] ──> [60 70]     leaves linked for range scans""",
 ["ACID with an example (bank transfer).", "Normal forms up to BCNF with one example each.", "Dirty read, non-repeatable read and phantom read; which isolation level stops each.", "Clustered vs non-clustered index; when an index hurts (writes, low selectivity).", "Why B+ trees for indexes (shallow, linked leaves).", "DELETE vs TRUNCATE vs DROP.", "Primary key vs unique key (NULL handling, count per table).", "Two-phase locking and deadlock handling.", "SQL vs NoSQL and when you would pick each.", "Write-ahead logging and how recovery uses undo and redo."]),
("cn", "Computer Networks", "qa-cn", [
 ("OSI / TCP-IP", "Application, (presentation, session), transport, network, data link, physical. TCP/IP merges the top three."),
 ("TCP", "Connection-oriented, reliable, ordered, flow control (receiver window) and congestion control (slow start, AIMD)."),
 ("UDP", "Connectionless, no ordering or retransmission, low overhead: DNS, video, games, QUIC underneath."),
 ("Handshake", "SYN → SYN-ACK → ACK to open; FIN / ACK in each direction to close; TIME_WAIT afterwards."),
 ("IP addressing", "IPv4 32 bits, IPv6 128 bits; CIDR /n; private ranges 10/8, 172.16/12, 192.168/16; NAT shares one public IP."),
 ("Routing", "Routers forward by longest-prefix match; RIP (distance vector), OSPF (link state), BGP between networks."),
 ("ARP, DHCP, DNS", "ARP: IP → MAC on the LAN. DHCP: Discover, Offer, Request, Ack. DNS: name → IP, mostly UDP 53, cached by TTL."),
 ("HTTP", "Stateless request/response; methods GET, POST, PUT (idempotent), PATCH, DELETE; status classes 1xx–5xx."),
 ("HTTPS / TLS", "TLS handshake agrees keys and authenticates the server with a CA-signed certificate; data then uses symmetric encryption."),
 ("Devices", "Hub (L1), switch (L2, MAC table), router (L3), load balancer (L4/L7).")],
 """ Typing a URL:  browser cache → DNS lookup (resolver → root → TLD → authoritative)
               → TCP handshake (SYN, SYN-ACK, ACK) → TLS handshake → HTTP GET
               → server response (HTML) → browser parses, fetches CSS/JS/images → renders

 Encapsulation: data → [TCP hdr | data] → [IP hdr | segment] → [Eth hdr | packet | FCS]""",
 ["What happens when you type a URL (the diagram above).", "TCP vs UDP with use cases.", "Three-way handshake and why not two.", "Flow control vs congestion control.", "Subnetting: hosts in a /26 (62), network and broadcast addresses.", "How DNS resolution works and why it uses UDP.", "HTTP vs HTTPS; how TLS uses both asymmetric and symmetric crypto.", "Switch vs router vs hub.", "What NAT does and why IPv4 needs it.", "Status codes: 200, 201, 301, 304, 400, 401, 403, 404, 429, 500, 503."]),
("oop", "OOP and design", "oop", [
 ("Encapsulation", "Keep data private and expose behaviour through methods; protects invariants."),
 ("Abstraction", "Show what an object does, hide how: interfaces and abstract classes."),
 ("Inheritance", "'Is-a' reuse; prefer composition ('has-a') when behaviour varies."),
 ("Polymorphism", "Compile-time: overloading, templates. Run-time: virtual functions via the vtable."),
 ("Virtual destructor", "Needed when deleting a derived object through a base pointer."),
 ("Rule of 3 / 5 / 0", "Destructor, copy constructor, copy assignment (+ move constructor, move assignment); or own nothing raw and need none."),
 ("SOLID", "Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion."),
 ("Patterns", "Singleton, Factory, Builder (creational); Adapter, Decorator (structural); Strategy, Observer, State (behavioural)."),
 ("Object slicing", "Copying a derived object into a base object by value loses the derived part."),
 ("Smart pointers", "unique_ptr (sole owner), shared_ptr (ref-counted), weak_ptr (breaks cycles); RAII frees resources.")],
 """ class Shape { public: virtual double area() const = 0; virtual ~Shape() = default; };
 class Circle : public Shape { double r; public: double area() const override { return 3.14159 * r * r; } };

 Shape* s = new Circle(...);   s->area();   // call goes through Circle's vtable entry (run-time polymorphism)
 Strategy:  Context ──has-a──> Strategy <<interface>> <── ConcreteA, ConcreteB""",
 ["The four pillars with a real example each.", "Abstract class vs interface (pure virtual functions in C++).", "How virtual functions work (vtable, vptr).", "Overloading vs overriding.", "Why a virtual destructor matters.", "Shallow vs deep copy; rule of three.", "Composition over inheritance: when and why.", "SOLID with one example each (often Liskov and Dependency inversion).", "Singleton: thread-safe version and why it is often a smell.", "Strategy and Observer patterns, from your LLD practice."]),
("sql", "SQL", "acid", [
 ("Order of execution", "FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT."),
 ("WHERE vs HAVING", "WHERE filters rows before grouping; HAVING filters groups and can use aggregates."),
 ("Joins", "INNER keeps matches; LEFT keeps all left rows (NULLs on the right); anti-join: LEFT JOIN … WHERE right.id IS NULL."),
 ("NULL", "Comparisons with NULL are unknown; use IS NULL; COUNT(col) skips NULLs, COUNT(*) does not; NOT IN breaks with NULLs."),
 ("Subqueries and CTEs", "Correlated subqueries run per row; WITH names an intermediate result; WITH RECURSIVE walks hierarchies."),
 ("Window functions", "ROW_NUMBER, RANK (gaps), DENSE_RANK (no gaps), LAG/LEAD, SUM() OVER (ORDER BY …) running totals."),
 ("Set operations", "UNION removes duplicates, UNION ALL keeps them; INTERSECT, EXCEPT."),
 ("Indexes", "Index columns in WHERE, JOIN and ORDER BY; check with EXPLAIN; composite index order matters (leftmost prefix)."),
 ("DDL / DML / DCL / TCL", "CREATE, ALTER, DROP / SELECT, INSERT, UPDATE, DELETE / GRANT, REVOKE / COMMIT, ROLLBACK."),
 ("Classic patterns", "Nth highest (DENSE_RANK or LIMIT OFFSET), top N per group, duplicates (GROUP BY HAVING COUNT > 1), consecutive days (date − row number).")],
 """ SELECT dept, name, salary
 FROM (SELECT d.name AS dept, e.name, e.salary,
              DENSE_RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS r
       FROM employees e JOIN departments d ON d.id = e.dept_id)
 WHERE r <= 2;                                  -- top two salaries in every department""",
 ["Second-highest or Nth-highest salary.", "Top N per group with window functions.", "Employees earning more than their manager (self join).", "Find and delete duplicates.", "Customers with no orders (anti-join or NOT EXISTS).", "RANK vs DENSE_RANK vs ROW_NUMBER.", "Running totals and month-over-month change with LAG.", "WHERE vs HAVING; logical order of execution.", "UNION vs UNION ALL; DELETE vs TRUNCATE.", "When an index is not used (functions on the column, leading wildcard LIKE, low selectivity)."]),
("sysdesign", "System Design basics", "hld", [
 ("Approach", "Clarify requirements → estimate scale → API → data model → high-level design → deep dive → bottlenecks and trade-offs."),
 ("Scaling", "Vertical (bigger machine) vs horizontal (more machines behind a load balancer); keep app servers stateless."),
 ("Load balancing", "Round robin, least connections, consistent hashing; L4 vs L7; health checks."),
 ("Caching", "Cache-aside, write-through, write-back; eviction LRU; CDN for static content; watch invalidation and stampedes."),
 ("Databases", "Replication (read replicas, failover), sharding (by key, range or hash), indexes; SQL vs NoSQL by access pattern."),
 ("Queues", "Decouple producers and consumers, absorb spikes, retry with dead-letter queues; at-least-once means idempotent consumers."),
 ("Consistency", "Strong vs eventual; CAP under partitions; quorum reads and writes (R + W > N)."),
 ("Rate limiting", "Token bucket or sliding window per user or IP at the gateway; return 429."),
 ("Reliability", "Redundancy across zones, timeouts, retries with backoff, circuit breakers, monitoring and alerts."),
 ("Numbers", "1 day ≈ 86,400 s ≈ 10^5 s; 1M requests/day ≈ 12/s average; plan for peaks of 2–10× average.")],
 """ client → DNS → CDN (static)
        → load balancer → app servers (stateless) → cache (Redis)
                                                 → database (primary → replicas, sharded by key)
                                                 → queue → workers → object storage / notifications""",
 ["Design a URL shortener (IDs, redirects, cache, analytics).", "Design a rate limiter.", "Horizontal vs vertical scaling.", "How caching works and how to invalidate.", "Replication vs sharding; choosing a shard key.", "SQL vs NoSQL for a given feature.", "Consistent hashing and why it helps.", "What a message queue buys you.", "CAP theorem with an example.", "Back-of-envelope estimates: requests per second, storage per year."]),
]
def body(pages):
    pg = lambda k: str(pages.get(k, "000")) if pages else "000"
    rows = "".join(f'<tr><td><a href="#{k}">{E(t)}</a></td><td><a class="kb" href="{KB}{kb}">Knowledge Base ↗</a></td><td class="pg"><a href="#{k}">{pg(k)}</a></td></tr>' for k, t, kb, *_ in P)
    out = [f'''<section class="cover"><p class="eb">CORE CS · REVISION ONE-PAGERS</p><h1>Six pages<br><span>to revise before any interview</span></h1>
<p class="lead">One A4 page each for Operating Systems, DBMS, Computer Networks, OOP, SQL and System Design: ten key definitions, one diagram, and the ten things interviewers ask most. Read one the night before a round; print all six for the placement season.</p>
<table class="ix"><tbody>{rows}</tbody></table>
<p class="src">For depth, use the linked Knowledge Base pages, the Core CS MCQ bank, the SQL pack and the LLD pack in this repository.</p></section>''']
    for k, t, kb, defs, diag, top in P:
        out.append(f'''<section class="sec" id="{k}"><h2>{E(t)}<a class="pat" href="{KB}{kb}">Knowledge Base ↗</a><a class="back" href="#top">↑ Index</a></h2>
<table class="defs"><tbody>{"".join(f"<tr><td class=t>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in defs)}</tbody></table>
<pre>{E(diag)}</pre><h3>Most asked</h3><ol class="top">{"".join(f"<li>{E(x)}</li>" for x in top)}</ol></section>''')
    return "".join(out)
CSS = """@page { size: A4; margin: 11mm 12mm 13mm; } @page :first { margin: 0; }
* { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; } body { margin: 0; font: 400 8.6pt/1.4 Inter, sans-serif; color: #1e293b; }
a { color: #c2410c; text-decoration: none; } .cover { padding: 18mm 15mm; break-after: page; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 3mm; } h1 { font: 700 34pt/1.02 "Space Grotesk"; margin: 0 0 4mm; color: #0f172a; } h1 span { color: #c2410c; font-size: 20pt; }
.lead { font-size: 10pt; color: #475569; } table { border-collapse: collapse; width: 100%; } .ix td { padding: 2.4mm 2mm; border-bottom: 1px solid #e2e8f0; font-size: 11pt; } .ix td a { color: #0f172a; font-weight: 600; } .ix a.kb { color: #c2410c; font: 600 8pt "JetBrains Mono"; } .ix .pg { text-align: right; } .ix .pg a { color: #c2410c; font-family: "JetBrains Mono"; }
.src { font-size: 8pt; color: #64748b; margin-top: 4mm; } .sec { break-before: page; } h2 { font: 700 16pt "Space Grotesk"; color: #0f172a; border-bottom: 3px solid #c2410c; padding-bottom: 1.5mm; margin: 0 0 2.5mm; display: flex; align-items: baseline; gap: 3mm; }
.pat { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; } .back { font: 600 7.5pt "JetBrains Mono"; border: 1px solid #fdba74; background: #fff7ed; border-radius: 99px; padding: 0 7px; }
.defs td { border-bottom: 1px solid #eef2f7; padding: 1.25mm 2mm; vertical-align: top; } .defs .t { font-weight: 700; color: #0f172a; width: 34mm; }
pre { font: 400 7.3pt/1.4 "JetBrains Mono"; background: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #16a34a; padding: 2.2mm 3mm; white-space: pre-wrap; margin: 3mm 0; font-variant-ligatures: none; }
h3 { font: 700 10pt "Space Grotesk"; color: #1d4ed8; margin: 2mm 0 1mm; } .top { column-count: 2; column-gap: 7mm; padding-left: 5mm; margin: 0; } .top li { margin-bottom: 1mm; break-inside: avoid; }"""
js = SRC / "r.js"
def render(pages, name):
    (SRC / "op.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/op.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "p1.pdf"); d2, n2 = render(d1, "p2.pdf"); assert n1 == n2 and all(d1[k] == d2[k] for k, *_ in P)
assert n2 == 7, f"each topic must fit on one page, got {n2} pages {d2}"
w = PdfWriter(clone_from=PdfReader(str(SRC / "p2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for k, t, *_ in P: w.add_outline_item(t, d2[k] - 1, fit=Fit.fit())
NP = len(w.pages)
for i, pg in enumerate(w.pages):
    if i == 0: continue
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); c.setFont("Helvetica", 7.5); c.setFillGray(.55)
    c.drawRightString(float(pg.mediabox.width) - 26, 14, f"{i + 1} / {NP}"); c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "Core CS one-pagers"}); w.write(str(OUT / "core-cs-one-pagers.pdf"))
for f in ("p1.pdf", "p2.pdf", "r.js", "op.html"): (SRC / f).unlink()
print(NP, "pages", d2)
