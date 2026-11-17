# Core CS

[All categories](README.md) · 16 topics

## Topics

- [Processes and threads](#processes-and-threads)
- [CPU scheduling](#cpu-scheduling)
- [Deadlock](#deadlock)
- [Synchronisation: mutex, semaphore, race conditions](#synchronisation-mutex-semaphore-race-conditions)
- [Memory management and virtual memory](#memory-management-and-virtual-memory)
- [Normalisation and keys](#normalisation-and-keys)
- [Transactions, ACID and isolation](#transactions-acid-and-isolation)
- [Indexing and B+ trees](#indexing-and-b-trees)
- [SQL for interviews](#sql-for-interviews)
- [OSI and TCP/IP models](#osi-and-tcpip-models)
- [TCP vs UDP and the handshake](#tcp-vs-udp-and-the-handshake)
- [HTTP, HTTPS and TLS](#http-https-and-tls)
- [What happens when you type a URL](#what-happens-when-you-type-a-url)
- [OOP: the four pillars](#oop-the-four-pillars)
- [Virtual functions and the vtable](#virtual-functions-and-the-vtable)
- [SOLID and design patterns](#solid-and-design-patterns)

## Processes and threads

*Level 1: Core*

The most-asked OS question in every technical round, product or service company.

**Key idea**

A process is a running program with its own address space (code, data, heap, stack), file descriptors and a PCB (process control block) in the kernel.

A thread is a unit of execution inside a process. Threads share the process's code, data, heap and files, but each has its own stack, registers and program counter.

Threads are cheaper because creating one and switching between threads of the same process don't need a new address space or a TLB flush. The cost of sharing is that one thread's bug (or a missing lock) can corrupt the whole process.


**Points**

- Process states: new, ready, running, waiting, terminated
- fork() copies the process (copy-on-write); exec() replaces its image
- User-level vs kernel-level threads
- Zombie: finished but parent hasn't called wait(); orphan: parent died first

**Traps**

- Saying threads share the stack (they don't)

**Interviewers ask**

- Process vs thread, and why threads are cheaper?
- What happens on a context switch?
- What is a zombie process?

**Learn more**

- [OSTEP (free OS book)](https://pages.cs.wisc.edu/~remzi/OSTEP/)
- [GfG: process vs thread](https://www.geeksforgeeks.org/operating-systems/difference-between-process-and-thread/)
- [Gate Smashers (YouTube)](https://www.youtube.com/@GateSmashers)

**Related:** [CPU scheduling](#cpu-scheduling) · [Synchronisation: mutex, semaphore, race conditions](#synchronisation-mutex-semaphore-race-conditions) · [Memory management and virtual memory](#memory-management-and-virtual-memory)

[Back to the topic list](#topics)

## CPU scheduling

*Level 1: Core*

Numerical questions in OAs (compute waiting time) and conceptual ones in interviews.

**Key idea**

The scheduler picks which ready process runs next. Goals: high CPU use and throughput, low waiting, turnaround and response time, fairness.

FCFS (convoy effect), SJF/SRTF (optimal average waiting, needs burst estimates, can starve long jobs), priority (starvation fixed by ageing), round robin (time quantum; good response time), multilevel feedback queues (what real systems approximate). Linux uses CFS, which tracks virtual runtime in a red-black tree.


**Points**

- Turnaround = completion − arrival; waiting = turnaround − burst
- Preemptive vs non-preemptive
- Quantum too small → too many context switches; too big → FCFS

**Traps**

- Mixing up turnaround and response time

**Interviewers ask**

- Compare round robin and SJF.
- What is starvation and how does ageing fix it?

**Learn more**

- [OSTEP (free OS book)](https://pages.cs.wisc.edu/~remzi/OSTEP/)
- [Gate Smashers (YouTube)](https://www.youtube.com/@GateSmashers)

**Related:** [Processes and threads](#processes-and-threads)

[Back to the topic list](#topics)

## Deadlock

*Level 1: Core*

Top-5 OS question. Also asked in DBMS (transaction deadlocks).

**Key idea**

A set of processes each waiting for a resource held by another in the set, so none can proceed.

Coffman conditions, all four needed: mutual exclusion, hold and wait, no preemption, circular wait.

Handling: prevention (break one condition, e.g. always lock resources in a fixed global order to stop circular wait), avoidance (Banker's algorithm keeps the system in a safe state), detection + recovery (wait-for graph, kill or roll back), or ignore it (most OSes).


**Points**

- Fixed lock ordering is the practical fix in code
- Livelock: processes keep changing state but make no progress
- Starvation ≠ deadlock

**Traps**

- Listing only three conditions

**Interviewers ask**

- Four conditions of deadlock?
- How would you prevent deadlock in your code?
- Explain Banker's algorithm.

**Learn more**

- [OSTEP (free OS book)](https://pages.cs.wisc.edu/~remzi/OSTEP/)
- [GfG: deadlock](https://www.geeksforgeeks.org/operating-systems/introduction-of-deadlock-in-operating-system/)
- [Gate Smashers (YouTube)](https://www.youtube.com/@GateSmashers)

**Related:** [Synchronisation: mutex, semaphore, race conditions](#synchronisation-mutex-semaphore-race-conditions) · [Transactions, ACID and isolation](#transactions-acid-and-isolation)

[Back to the topic list](#topics)

## Synchronisation: mutex, semaphore, race conditions

*Level 2: Interview-ready*

Asked in OS rounds and C++/HFT interviews; producer-consumer is a classic whiteboard question.

**Key idea**

A race condition happens when the result depends on the timing of threads touching shared data. The code that touches it is the critical section; it needs mutual exclusion, progress and bounded waiting.

A mutex is a lock with an owner: only the thread that locked it unlocks it. A semaphore is a counter: wait() decrements and blocks at 0, signal() increments. A binary semaphore looks like a mutex but has no owner; a counting semaphore guards N identical resources.

Producer-consumer with a bounded buffer: semaphores empty = N and full = 0, plus a mutex for the buffer. Condition variables let a thread sleep until a predicate becomes true (always wait in a loop).


**Points**

- Spinlock: busy-waits, good for very short sections
- Atomics avoid locks for single variables
- Readers-writers and dining philosophers are the other classics

```cpp
std::mutex m; std::condition_variable cv; std::queue<int> q;
void produce(int x) { { std::lock_guard<std::mutex> g(m); q.push(x); } cv.notify_one(); }
int consume() { std::unique_lock<std::mutex> g(m); cv.wait(g, [] { return !q.empty(); });
    int x = q.front(); q.pop(); return x; }
```

**Traps**

- Using if instead of while around a condition wait (spurious wake-ups)

**Interviewers ask**

- Mutex vs semaphore with an example.
- Write producer-consumer.
- What is a race condition?

**Learn more**

- [OSTEP (free OS book)](https://pages.cs.wisc.edu/~remzi/OSTEP/)
- [cppreference: thread support](https://en.cppreference.com/w/cpp/thread)

**Related:** [Deadlock](#deadlock) · [Processes and threads](#processes-and-threads)

[Back to the topic list](#topics)

## Memory management and virtual memory

*Level 2: Interview-ready*

Second most-asked OS area after processes. Also needed for binary exploitation (stack, heap, ASLR).

**Key idea**

Each process sees its own virtual address space. The MMU translates virtual pages to physical frames using page tables; the TLB caches recent translations.

Why: isolation (one process can't read another's memory), programs bigger than RAM, simpler loading, and sharing (shared libraries, copy-on-write after fork).

A page fault happens when a page isn't in RAM: the OS loads it from disk and may evict another (FIFO, LRU, optimal; Belady's anomaly hits FIFO). Thrashing is when the system spends more time paging than running because working sets don't fit.


**Points**

- Internal fragmentation (paging) vs external (segmentation)
- Multi-level page tables save memory
- Effective access time with TLB hit ratio

**Traps**

- Confusing virtual memory with swap space only

**Interviewers ask**

- Why do we need virtual memory?
- What happens on a page fault?
- What is thrashing?
- LRU page replacement: implement it (→ LRU cache).

**Learn more**

- [OSTEP (free OS book)](https://pages.cs.wisc.edu/~remzi/OSTEP/)
- [Gate Smashers (YouTube)](https://www.youtube.com/@GateSmashers)

**Related:** [Processes and threads](#processes-and-threads) · [Binary exploitation basics](security.md#binary-exploitation-basics)

[Back to the topic list](#topics)

## Normalisation and keys

*Level 1: Core*

The standard DBMS opener in interviews and a frequent OA MCQ.

**Key idea**

Keys: a super key identifies a row; a candidate key is a minimal super key; the primary key is the chosen candidate; a foreign key references another table's key.

Normalisation removes redundancy that causes insert, update and delete anomalies. 1NF: atomic values. 2NF: 1NF and no partial dependency on part of a composite key. 3NF: 2NF and no transitive dependency (non-key → non-key). BCNF: every determinant is a candidate key.

Denormalisation trades redundancy for faster reads, common in analytics and NoSQL.


**Points**

- Example: Student(roll, name, dept, dept\_head) → dept\_head depends on dept → split into Student and Dept for 3NF
- Lossless join and dependency preservation
- ER diagram → tables

**Traps**

- Not giving a concrete table example

**Interviewers ask**

- Explain 1NF to 3NF with one table.
- Difference between 3NF and BCNF?
- Primary vs unique key?

**Learn more**

- [GfG: normal forms](https://www.geeksforgeeks.org/dbms/normal-forms-in-dbms/)
- [Gate Smashers (YouTube)](https://www.youtube.com/@GateSmashers)
- [CMU 15-445 (free lectures)](https://15445.courses.cs.cmu.edu)

**Related:** [Transactions, ACID and isolation](#transactions-acid-and-isolation) · [Indexing and B+ trees](#indexing-and-b-trees) · [SQL for interviews](#sql-for-interviews)

[Back to the topic list](#topics)

## Transactions, ACID and isolation

*Level 2: Interview-ready*

Asked at every product company, especially fintechs like Razorpay where money moves.

**Key idea**

Atomicity (all or nothing, via undo logs), Consistency (constraints hold before and after), Isolation (concurrent transactions behave as if run in some order), Durability (committed data survives crashes, via write-ahead logging).

Anomalies: dirty read, non-repeatable read, phantom read. Isolation levels: Read Uncommitted (allows all), Read Committed (stops dirty reads), Repeatable Read (also stops non-repeatable reads), Serializable (stops phantoms).

Implementations use locks (two-phase locking) or MVCC (each transaction reads a snapshot; PostgreSQL, MySQL InnoDB).


**Points**

- Read Committed prevents dirty reads
- 2PL: growing phase then shrinking phase
- Deadlocks between transactions are detected and one is rolled back

**Traps**

- Saying 'Consistency' means the same as in CAP (it doesn't)

**Interviewers ask**

- Explain ACID with a bank transfer.
- Which isolation level prevents dirty reads?
- What is MVCC?

**Learn more**

- [GfG: ACID](https://www.geeksforgeeks.org/dbms/acid-properties-in-dbms/)
- [CMU 15-445](https://15445.courses.cs.cmu.edu)

**Related:** [Normalisation and keys](#normalisation-and-keys) · [Deadlock](#deadlock) · [CAP theorem and consistency](design.md#cap-theorem-and-consistency)

[Back to the topic list](#topics)

## Indexing and B+ trees

*Level 2: Interview-ready*

'Why is my query slow?' is a real-job question and a favourite follow-up in backend interviews.

**Key idea**

An index is a separate structure that maps column values to row locations so the database avoids scanning the whole table.

Most databases use B+ trees: wide, shallow trees (each node holds hundreds of keys, sized to a disk page) with all values in linked leaves. A lookup touches about 3–4 pages for millions of rows, and range scans walk the leaves.

A clustered index stores rows in key order (one per table, usually the primary key); secondary indexes point to it. Composite indexes follow the leftmost-prefix rule.


**Points**

- Indexes speed reads but slow writes and use space
- Covering index answers a query from the index alone
- Hash indexes: equality only, no ranges
- Use EXPLAIN to see the query plan

**Traps**

- Indexing low-cardinality columns (gender) expecting gains
- Applying a function to an indexed column in WHERE stops index use

**Interviewers ask**

- How does an index speed up a query?
- Why B+ tree and not a binary tree or hash?
- Clustered vs non-clustered?

**Learn more**

- [Use The Index, Luke (free)](https://use-the-index-luke.com)
- [CMU 15-445](https://15445.courses.cs.cmu.edu)

**Related:** [Normalisation and keys](#normalisation-and-keys) · [SQL for interviews](#sql-for-interviews)

[Back to the topic list](#topics)

## SQL for interviews

*Level 1: Core*

Many OAs include 1–2 SQL questions; analyst-flavoured and backend roles always do.

**Key idea**

Order of evaluation: FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT. WHERE filters rows, HAVING filters groups.

Joins: INNER (matches only), LEFT (all left rows), self-join (employee–manager), anti-join (LEFT JOIN … WHERE right.id IS NULL).

Window functions compute over a partition without collapsing rows: ROW\_NUMBER, RANK, DENSE\_RANK, LAG/LEAD, running SUM() OVER (ORDER BY …).


**Points**

- DENSE\_RANK for 'Nth highest' with ties
- COUNT(col) ignores NULLs, COUNT(\*) doesn't
- Parameterised queries prevent SQL injection

```text
SELECT dept, name, salary FROM (
  SELECT d.name AS dept, e.name, e.salary,
         DENSE_RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS r
  FROM employee e JOIN department d ON d.id = e.dept_id
) t WHERE r = 2;
```

**Traps**

- Using WHERE with an aggregate
- Forgetting NULL handling in comparisons

**Interviewers ask**

- Second-highest salary per department.
- Find duplicate emails.
- Difference between RANK and DENSE\_RANK?

**Practise**

- [LeetCode SQL 50](https://leetcode.com/studyplan/top-sql-50/)
- [SQLBolt](https://sqlbolt.com)

**Learn more**

- [SQLBolt](https://sqlbolt.com)
- [Mode SQL tutorial](https://mode.com/sql-tutorial/)

**Related:** [Indexing and B+ trees](#indexing-and-b-trees) · [SQL injection](security.md#sql-injection)

[Back to the topic list](#topics)

## OSI and TCP/IP models

*Level 1: Core*

The first Computer Networks question in most interviews, and the vocabulary for everything in security.

**Key idea**

OSI has 7 layers: Physical, Data link (MAC, switches), Network (IP, routers), Transport (TCP/UDP, ports), Session, Presentation, Application. TCP/IP merges them into 4: Link, Internet, Transport, Application.

Each layer wraps the one above with its own header (encapsulation): HTTP data → TCP segment → IP packet → Ethernet frame.


**Points**

- Devices: hub (L1), switch (L2), router (L3)
- ARP maps IP → MAC
- Subnetting: /24 = 256 addresses, 254 usable hosts

**Traps**

- Putting TLS or HTTP at the wrong layer without explaining

**Interviewers ask**

- Explain the OSI model.
- Which layer does a router work at?
- What is ARP?

**Learn more**

- [Gate Smashers (YouTube)](https://www.youtube.com/@GateSmashers)
- [Computer Networking: A Top-Down Approach (Kurose)](https://gaia.cs.umass.edu/kurose_ross/index.php)

**Related:** [TCP vs UDP and the handshake](#tcp-vs-udp-and-the-handshake) · [What happens when you type a URL](#what-happens-when-you-type-a-url)

[Back to the topic list](#topics)

## TCP vs UDP and the handshake

*Level 1: Core*

Asked in nearly every CN round; the 'why not 2-way?' follow-up catches people out.

**Key idea**

TCP is connection-oriented and reliable: ordered delivery, retransmission, flow control (receiver window) and congestion control (slow start, congestion avoidance, fast retransmit). UDP is connectionless with no guarantees but low overhead and latency.

Handshake: client SYN (seq x) → server SYN-ACK (seq y, ack x+1) → client ACK (ack y+1). Three steps are needed so both sides confirm the other received their initial sequence number; two would leave the server unsure the client saw its SYN, and stale duplicate SYNs could open ghost connections.

Closing uses FIN/ACK in four steps; TIME\_WAIT keeps the socket around to absorb late packets.


**Points**

- Use UDP for video calls, games, DNS, live streams; QUIC builds reliability on UDP
- Flow control protects the receiver; congestion control protects the network
- SYN flood attack exploits half-open connections (SYN cookies defend)

**Traps**

- Mixing flow and congestion control

**Interviewers ask**

- Why a 3-way and not 2-way handshake?
- When would you choose UDP?
- Flow vs congestion control?

**Learn more**

- [Kurose & Ross](https://gaia.cs.umass.edu/kurose_ross/index.php)
- [Gate Smashers (YouTube)](https://www.youtube.com/@GateSmashers)

**Related:** [OSI and TCP/IP models](#osi-and-tcpip-models) · [HTTP, HTTPS and TLS](#http-https-and-tls)

[Back to the topic list](#topics)

## HTTP, HTTPS and TLS

*Level 2: Interview-ready*

Bridges CN and security. Your AppSec and cloud work depends on it.

**Key idea**

HTTP is a stateless request/response protocol: methods (GET, POST, PUT, DELETE, PATCH), status codes (2xx ok, 3xx redirect, 4xx client error, 5xx server error), headers, cookies for state.

HTTPS is HTTP over TLS. In TLS 1.3 the client and server agree keys with an ephemeral Diffie-Hellman exchange, the server proves its identity with a certificate signed by a trusted CA, and then traffic is encrypted with a fast symmetric cipher (AES-GCM or ChaCha20).

HTTP/2 multiplexes streams over one TCP connection; HTTP/3 runs over QUIC (UDP) to avoid head-of-line blocking.


**Points**

- Asymmetric crypto for key exchange/auth, symmetric for bulk data
- Security headers: HSTS, CSP, X-Frame-Options
- Idempotent methods: GET, PUT, DELETE

**Traps**

- Saying HTTPS encrypts with the server's public key directly (old RSA key exchange, not TLS 1.3)

**Interviewers ask**

- How does HTTPS work?
- Difference between HTTP/1.1, 2 and 3?
- What are cookies and how are they secured?

**Learn more**

- [The Illustrated TLS 1.3 Connection](https://tls13.xargs.org)
- [MDN HTTP docs](https://developer.mozilla.org/en-US/docs/Web/HTTP)

**Related:** [TCP vs UDP and the handshake](#tcp-vs-udp-and-the-handshake) · [What happens when you type a URL](#what-happens-when-you-type-a-url) · [Hashing, encryption and passwords](security.md#hashing-encryption-and-passwords)

[Back to the topic list](#topics)

## What happens when you type a URL

*Level 2: Interview-ready*

The single most popular CN interview question. It lets you show breadth from DNS to rendering.

**Key idea**

1) Browser checks its caches and parses the URL. 2) DNS resolution: browser → OS → resolver → root → TLD (.com) → authoritative server, giving an IP. 3) TCP handshake (or QUIC). 4) TLS handshake. 5) HTTP request sent; it may pass through a CDN, load balancer and reverse proxy. 6) The server builds a response (app server, cache, database). 7) The browser parses HTML, fetches CSS/JS/images, builds the DOM and CSSOM, lays out and paints.

Go deeper on whichever layer the interviewer prods: DNS record types (A, AAAA, CNAME, MX), TTL caching, ARP on the local network, keep-alive.


**Points**

- DNS uses UDP port 53 (TCP for large responses)
- Mention a CDN and load balancer to show system awareness
- Security add-on: HSTS, certificate validation

**Traps**

- Skipping DNS or TLS
- Going so deep on one step you never finish

**Interviewers ask**

- What happens when you type google.com and press Enter?
- How does DNS resolution work?

**Learn more**

- [alex/what-happens-when (GitHub)](https://github.com/alex/what-happens-when)

**Related:** [OSI and TCP/IP models](#osi-and-tcpip-models) · [TCP vs UDP and the handshake](#tcp-vs-udp-and-the-handshake) · [HTTP, HTTPS and TLS](#http-https-and-tls) · [Caching and CDNs](design.md#caching-and-cdns)

[Back to the topic list](#topics)

## OOP: the four pillars

*Level 1: Core*

Asked in every service-company interview and most product ones, often with 'show me in C++'.

**Key idea**

Encapsulation: bundle data with methods and hide internals (private members, public interface). Abstraction: expose what an object does, not how (abstract classes, interfaces). Inheritance: a class reuses and extends another ('is-a'). Polymorphism: one interface, many forms; compile-time (overloading, templates) and run-time (virtual functions).

Prefer composition ('has-a') over deep inheritance trees.


**Points**

- Overloading = same name, different parameters (compile time)
- Overriding = derived class redefines a virtual function (run time)
- Abstract class has at least one pure virtual function

```text
struct Shape { virtual double area() const = 0; virtual ~Shape() = default; };
struct Circle : Shape { double r; explicit Circle(double r) : r(r) {}
    double area() const override { return 3.14159 * r * r; } };
std::unique_ptr<Shape> s = std::make_unique<Circle>(2.0); // runtime polymorphism
```

**Traps**

- Forgetting a virtual destructor in a base class

**Interviewers ask**

- Explain the four pillars with examples.
- Overloading vs overriding?
- Abstract class vs interface?

**Learn more**

- [learncpp.com: OOP chapters](https://www.learncpp.com)
- [GfG: OOP in C++](https://www.geeksforgeeks.org/cpp/object-oriented-programming-in-cpp/)

**Related:** [Virtual functions and the vtable](#virtual-functions-and-the-vtable) · [SOLID and design patterns](#solid-and-design-patterns) · [Low-level design (LLD)](design.md#low-level-design-lld)

[Back to the topic list](#topics)

## Virtual functions and the vtable

*Level 2: Interview-ready*

A C++-specific depth question that separates prepared candidates, and essential for HFT and binary exploitation.

**Key idea**

Each class with virtual functions has a vtable: an array of function pointers to its versions of those functions. Each object stores a hidden vptr pointing to its class's vtable.

A virtual call loads the vptr, indexes the vtable and jumps: one extra indirection, and it usually blocks inlining (why low-latency C++ avoids virtual calls on hot paths, using templates/CRTP instead).

Constructors set the vptr, so calling a virtual function inside a constructor uses the current class's version, not the derived one.


**Points**

- Virtual destructor needed for delete through a base pointer
- Object slicing: copying a derived object into a base by value
- Overwriting a vptr is a classic exploitation primitive

**Traps**

- Thinking vtables are per object (they're per class)

**Interviewers ask**

- How does a virtual function call work?
- Why should base destructors be virtual?
- What is object slicing?

**Learn more**

- [learncpp: the virtual table](https://www.learncpp.com/cpp-tutorial/the-virtual-table/)

**Related:** [OOP: the four pillars](#oop-the-four-pillars) · [Binary exploitation basics](security.md#binary-exploitation-basics)

[Back to the topic list](#topics)

## SOLID and design patterns

*Level 2: Interview-ready*

The vocabulary of every LLD round.

**Key idea**

S: single responsibility. O: open for extension, closed for modification. L: Liskov substitution (a subclass must work wherever the base does). I: interface segregation (small, focused interfaces). D: dependency inversion (depend on abstractions, inject dependencies).

Patterns to know cold: Singleton (one instance; thread-safe via a function-local static in C++11), Factory (create objects without naming concrete classes), Strategy (swap algorithms at runtime), Observer (subscribers notified of events), plus Decorator and Adapter.


**Points**

- Square-Rectangle is the classic Liskov violation
- Strategy = pass a pricing/parking-fee policy object
- Observer = notification systems

**Traps**

- Naming patterns without a concrete use case

**Interviewers ask**

- Explain SOLID with examples.
- Implement a thread-safe singleton.
- Where would you use the strategy pattern?

**Learn more**

- [Refactoring.Guru design patterns (free)](https://refactoring.guru/design-patterns)
- [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design)

**Related:** [OOP: the four pillars](#oop-the-four-pillars) · [Low-level design (LLD)](design.md#low-level-design-lld)

[Back to the topic list](#topics)
