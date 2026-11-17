CORE CS · REVISION ONE-PAGERS

# Six pages to revise before any interview

One A4 page each for Operating Systems, DBMS, Computer Networks, OOP, SQL and System Design: ten key definitions, one diagram, and the ten things interviewers ask most. Read one the night before a round; print all six for the placement season.

|                                  |                                                                               |
|----------------------------------|-------------------------------------------------------------------------------|
| [Operating Systems](#operating-systemsknowledge-base-)     | [Knowledge Base ↗](knowledge-base/q-a.md#operating-systems-model-answers)   |
| [DBMS](#dbmsknowledge-base-)                  | [Knowledge Base ↗](knowledge-base/q-a.md#dbms-and-sql-model-answers) |
| [Computer Networks](#computer-networksknowledge-base-)     | [Knowledge Base ↗](knowledge-base/q-a.md#computer-networks-model-answers)   |
| [OOP and design](#oop-and-designknowledge-base-)        | [Knowledge Base ↗](knowledge-base/core-cs.md#oop-the-four-pillars)     |
| [SQL](#sqlknowledge-base-)                   | [Knowledge Base ↗](knowledge-base/core-cs.md#transactions-acid-and-isolation)    |
| [System Design basics](#system-design-basicsknowledge-base-) | [Knowledge Base ↗](knowledge-base/design.md#high-level-system-design-hld)     |

For depth, use the linked Knowledge Base pages, the Core CS MCQ bank, the SQL pack and the LLD pack in this repository.

## Operating Systems[Knowledge Base ↗](knowledge-base/q-a.md#operating-systems-model-answers)

|                    |                                                                                                                                         |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| Process            | A program in execution with its own address space, PCB, registers and open files.                                                       |
| Thread             | A unit of execution inside a process; threads share code, heap and files but have their own stack and registers.                        |
| Context switch     | Saving one process's CPU state in its PCB and loading another's; pure overhead.                                                         |
| Scheduling         | FCFS, SJF/SRTF (optimal average wait, can starve), Round Robin (time quantum), Priority (aging prevents starvation).                    |
| Deadlock           | Needs mutual exclusion, hold and wait, no preemption, circular wait. Handle by prevention, avoidance (Banker's), detection or ignoring. |
| Semaphore vs mutex | Mutex: a lock with an owner. Semaphore: a counter with wait/signal; binary or counting.                                                 |
| Paging             | Fixed-size pages map to frames via a page table; no external fragmentation; TLB caches translations.                                    |
| Virtual memory     | Demand paging lets programs exceed RAM; a page fault loads a missing page; thrashing = too few frames.                                  |
| Page replacement   | FIFO (Belady's anomaly), LRU, Optimal (theoretical best), Clock (LRU approximation).                                                    |
| System call        | A trap from user mode into kernel mode, e.g. fork, exec, read, write, mmap.                                                             |

``` text
 new ──admit──> ready ──dispatch──> running ──exit──> terminated
                 ^  ^                  |   |
                 |  └───interrupt──────┘   |
                 └──I/O done── waiting <───┘ I/O or event wait

 virtual address = [ page number | offset ] ──TLB / page table──> [ frame | offset ]
```

### Most asked

1.  Process vs thread, and why threads are cheaper to switch.
2.  The four deadlock conditions and how Banker's algorithm avoids deadlock.
3.  Paging vs segmentation; internal vs external fragmentation.
4.  What happens on a page fault, step by step.
5.  Thrashing: cause (too few frames) and fixes (working set, fewer processes).
6.  Mutex vs semaphore; producer-consumer with empty/full/mutex.
7.  fork() return values: 0 in the child, child PID in the parent, −1 on error.
8.  Zombie (finished, not reaped) vs orphan (parent died, adopted by init).
9.  Round Robin quantum too large becomes FCFS; too small means switch overhead.
10. User mode vs kernel mode, and how a system call crosses between them.

## DBMS[Knowledge Base ↗](knowledge-base/q-a.md#dbms-and-sql-model-answers)

|                     |                                                                                                                                             |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| Keys                | Super key ⊇ candidate key (minimal) ⊇ primary key (chosen, unique, not null). Foreign key references another table's key.                   |
| Normalisation       | 1NF atomic values; 2NF no partial dependency; 3NF no transitive dependency; BCNF every determinant is a candidate key.                      |
| ACID                | Atomicity (all or nothing, undo log), Consistency (constraints hold), Isolation (concurrency control), Durability (redo / write-ahead log). |
| Isolation levels    | Read uncommitted \< read committed (no dirty reads) \< repeatable read (no non-repeatable reads) \< serializable (no phantoms).             |
| Concurrency control | Two-phase locking gives serializability; strict 2PL also avoids cascading aborts; MVCC gives readers snapshots.                             |
| Indexes             | B+ trees for range and equality lookups; hash for equality only; clustered = table order (one per table).                                   |
| Joins               | Inner, left, right, full outer, cross, self; executed as nested loop, hash join or merge join.                                              |
| Transactions        | BEGIN … COMMIT / ROLLBACK; savepoints; deadlocks found with a wait-for graph.                                                               |
| SQL vs NoSQL        | Relational with schemas and joins vs key-value, document, column-family or graph stores that scale out easily.                              |
| CAP                 | Under a network partition a distributed store chooses consistency or availability.                                                          |

``` text
 Employee(emp_id, name, dept_id, dept_name)      dept_name depends on dept_id, not on the key
        └─ 3NF split ─>  Employee(emp_id, name, dept_id)   Department(dept_id, dept_name)

 B+ tree:            [ 30 | 60 ]
              /           |           \
       [10 20] ──> [30 40 50] ──> [60 70]     leaves linked for range scans
```

### Most asked

1.  ACID with an example (bank transfer).
2.  Normal forms up to BCNF with one example each.
3.  Dirty read, non-repeatable read and phantom read; which isolation level stops each.
4.  Clustered vs non-clustered index; when an index hurts (writes, low selectivity).
5.  Why B+ trees for indexes (shallow, linked leaves).
6.  DELETE vs TRUNCATE vs DROP.
7.  Primary key vs unique key (NULL handling, count per table).
8.  Two-phase locking and deadlock handling.
9.  SQL vs NoSQL and when you would pick each.
10. Write-ahead logging and how recovery uses undo and redo.

## Computer Networks[Knowledge Base ↗](knowledge-base/q-a.md#computer-networks-model-answers)

|                |                                                                                                                           |
|----------------|---------------------------------------------------------------------------------------------------------------------------|
| OSI / TCP-IP   | Application, (presentation, session), transport, network, data link, physical. TCP/IP merges the top three.               |
| TCP            | Connection-oriented, reliable, ordered, flow control (receiver window) and congestion control (slow start, AIMD).         |
| UDP            | Connectionless, no ordering or retransmission, low overhead: DNS, video, games, QUIC underneath.                          |
| Handshake      | SYN → SYN-ACK → ACK to open; FIN / ACK in each direction to close; TIME_WAIT afterwards.                                  |
| IP addressing  | IPv4 32 bits, IPv6 128 bits; CIDR /n; private ranges 10/8, 172.16/12, 192.168/16; NAT shares one public IP.               |
| Routing        | Routers forward by longest-prefix match; RIP (distance vector), OSPF (link state), BGP between networks.                  |
| ARP, DHCP, DNS | ARP: IP → MAC on the LAN. DHCP: Discover, Offer, Request, Ack. DNS: name → IP, mostly UDP 53, cached by TTL.              |
| HTTP           | Stateless request/response; methods GET, POST, PUT (idempotent), PATCH, DELETE; status classes 1xx–5xx.                   |
| HTTPS / TLS    | TLS handshake agrees keys and authenticates the server with a CA-signed certificate; data then uses symmetric encryption. |
| Devices        | Hub (L1), switch (L2, MAC table), router (L3), load balancer (L4/L7).                                                     |

``` text
 Typing a URL:  browser cache → DNS lookup (resolver → root → TLD → authoritative)
               → TCP handshake (SYN, SYN-ACK, ACK) → TLS handshake → HTTP GET
               → server response (HTML) → browser parses, fetches CSS/JS/images → renders

 Encapsulation: data → [TCP hdr | data] → [IP hdr | segment] → [Eth hdr | packet | FCS]
```

### Most asked

1.  What happens when you type a URL (the diagram above).
2.  TCP vs UDP with use cases.
3.  Three-way handshake and why not two.
4.  Flow control vs congestion control.
5.  Subnetting: hosts in a /26 (62), network and broadcast addresses.
6.  How DNS resolution works and why it uses UDP.
7.  HTTP vs HTTPS; how TLS uses both asymmetric and symmetric crypto.
8.  Switch vs router vs hub.
9.  What NAT does and why IPv4 needs it.
10. Status codes: 200, 201, 301, 304, 400, 401, 403, 404, 429, 500, 503.

## OOP and design[Knowledge Base ↗](knowledge-base/core-cs.md#oop-the-four-pillars)

|                    |                                                                                                                        |
|--------------------|------------------------------------------------------------------------------------------------------------------------|
| Encapsulation      | Keep data private and expose behaviour through methods; protects invariants.                                           |
| Abstraction        | Show what an object does, hide how: interfaces and abstract classes.                                                   |
| Inheritance        | 'Is-a' reuse; prefer composition ('has-a') when behaviour varies.                                                      |
| Polymorphism       | Compile-time: overloading, templates. Run-time: virtual functions via the vtable.                                      |
| Virtual destructor | Needed when deleting a derived object through a base pointer.                                                          |
| Rule of 3 / 5 / 0  | Destructor, copy constructor, copy assignment (+ move constructor, move assignment); or own nothing raw and need none. |
| SOLID              | Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion.                  |
| Patterns           | Singleton, Factory, Builder (creational); Adapter, Decorator (structural); Strategy, Observer, State (behavioural).    |
| Object slicing     | Copying a derived object into a base object by value loses the derived part.                                           |
| Smart pointers     | unique_ptr (sole owner), shared_ptr (ref-counted), weak_ptr (breaks cycles); RAII frees resources.                     |

``` cpp
 class Shape { public: virtual double area() const = 0; virtual ~Shape() = default; };
 class Circle : public Shape { double r; public: double area() const override { return 3.14159 * r * r; } };

 Shape* s = new Circle(...);   s->area();   // call goes through Circle's vtable entry (run-time polymorphism)
 Strategy:  Context ──has-a──> Strategy <<interface>> <── ConcreteA, ConcreteB
```

### Most asked

1.  The four pillars with a real example each.
2.  Abstract class vs interface (pure virtual functions in C++).
3.  How virtual functions work (vtable, vptr).
4.  Overloading vs overriding.
5.  Why a virtual destructor matters.
6.  Shallow vs deep copy; rule of three.
7.  Composition over inheritance: when and why.
8.  SOLID with one example each (often Liskov and Dependency inversion).
9.  Singleton: thread-safe version and why it is often a smell.
10. Strategy and Observer patterns, from your LLD practice.

## SQL[Knowledge Base ↗](knowledge-base/core-cs.md#transactions-acid-and-isolation)

|                       |                                                                                                                                           |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Order of execution    | FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT.                                                             |
| WHERE vs HAVING       | WHERE filters rows before grouping; HAVING filters groups and can use aggregates.                                                         |
| Joins                 | INNER keeps matches; LEFT keeps all left rows (NULLs on the right); anti-join: LEFT JOIN … WHERE right.id IS NULL.                        |
| NULL                  | Comparisons with NULL are unknown; use IS NULL; COUNT(col) skips NULLs, COUNT(\*) does not; NOT IN breaks with NULLs.                     |
| Subqueries and CTEs   | Correlated subqueries run per row; WITH names an intermediate result; WITH RECURSIVE walks hierarchies.                                   |
| Window functions      | ROW_NUMBER, RANK (gaps), DENSE_RANK (no gaps), LAG/LEAD, SUM() OVER (ORDER BY …) running totals.                                          |
| Set operations        | UNION removes duplicates, UNION ALL keeps them; INTERSECT, EXCEPT.                                                                        |
| Indexes               | Index columns in WHERE, JOIN and ORDER BY; check with EXPLAIN; composite index order matters (leftmost prefix).                           |
| DDL / DML / DCL / TCL | CREATE, ALTER, DROP / SELECT, INSERT, UPDATE, DELETE / GRANT, REVOKE / COMMIT, ROLLBACK.                                                  |
| Classic patterns      | Nth highest (DENSE_RANK or LIMIT OFFSET), top N per group, duplicates (GROUP BY HAVING COUNT \> 1), consecutive days (date − row number). |

``` sql
 SELECT dept, name, salary
 FROM (SELECT d.name AS dept, e.name, e.salary,
              DENSE_RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS r
       FROM employees e JOIN departments d ON d.id = e.dept_id)
 WHERE r <= 2;                                  -- top two salaries in every department
```

### Most asked

1.  Second-highest or Nth-highest salary.
2.  Top N per group with window functions.
3.  Employees earning more than their manager (self join).
4.  Find and delete duplicates.
5.  Customers with no orders (anti-join or NOT EXISTS).
6.  RANK vs DENSE_RANK vs ROW_NUMBER.
7.  Running totals and month-over-month change with LAG.
8.  WHERE vs HAVING; logical order of execution.
9.  UNION vs UNION ALL; DELETE vs TRUNCATE.
10. When an index is not used (functions on the column, leading wildcard LIKE, low selectivity).

## System Design basics[Knowledge Base ↗](knowledge-base/design.md#high-level-system-design-hld)

|                |                                                                                                                           |
|----------------|---------------------------------------------------------------------------------------------------------------------------|
| Approach       | Clarify requirements → estimate scale → API → data model → high-level design → deep dive → bottlenecks and trade-offs.    |
| Scaling        | Vertical (bigger machine) vs horizontal (more machines behind a load balancer); keep app servers stateless.               |
| Load balancing | Round robin, least connections, consistent hashing; L4 vs L7; health checks.                                              |
| Caching        | Cache-aside, write-through, write-back; eviction LRU; CDN for static content; watch invalidation and stampedes.           |
| Databases      | Replication (read replicas, failover), sharding (by key, range or hash), indexes; SQL vs NoSQL by access pattern.         |
| Queues         | Decouple producers and consumers, absorb spikes, retry with dead-letter queues; at-least-once means idempotent consumers. |
| Consistency    | Strong vs eventual; CAP under partitions; quorum reads and writes (R + W \> N).                                           |
| Rate limiting  | Token bucket or sliding window per user or IP at the gateway; return 429.                                                 |
| Reliability    | Redundancy across zones, timeouts, retries with backoff, circuit breakers, monitoring and alerts.                         |
| Numbers        | 1 day ≈ 86,400 s ≈ 10^5 s; 1M requests/day ≈ 12/s average; plan for peaks of 2–10× average.                               |

``` text
 client → DNS → CDN (static)
        → load balancer → app servers (stateless) → cache (Redis)
                                                 → database (primary → replicas, sharded by key)
                                                 → queue → workers → object storage / notifications
```

### Most asked

1.  Design a URL shortener (IDs, redirects, cache, analytics).
2.  Design a rate limiter.
3.  Horizontal vs vertical scaling.
4.  How caching works and how to invalidate.
5.  Replication vs sharding; choosing a shard key.
6.  SQL vs NoSQL for a given feature.
7.  Consistent hashing and why it helps.
8.  What a message queue buys you.
9.  CAP theorem with an example.
10. Back-of-envelope estimates: requests per second, storage per year.
