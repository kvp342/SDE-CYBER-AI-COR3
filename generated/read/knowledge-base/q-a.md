# Q&A

[All categories](README.md) · 5 topics

## Topics

- [Operating systems: model answers](#operating-systems-model-answers)
- [DBMS and SQL: model answers](#dbms-and-sql-model-answers)
- [Computer networks: model answers](#computer-networks-model-answers)
- [OOP and C++: model answers](#oop-and-c-model-answers)
- [Security and cloud: model answers](#security-and-cloud-model-answers)

## Operating systems: model answers

*Level 2: Interview-ready*

OS is asked in nearly every technical round. These are the questions that come up most.

**Key idea**

Read the question, answer it out loud from memory, then open the model answer and compare. Mark the ones you missed and re-do them in 3 days.


**Questions and model answers**

**Q. What is the difference between a process and a thread?**

A process is a running program with its own address space, open files and a process control block. A thread is a unit of execution inside a process; threads of the same process share code, heap and files but each has its own stack, registers and program counter. Threads are cheaper to create and switch between because no new address space is needed and the TLB isn't flushed. The cost is safety: a bug or race in one thread can corrupt the whole process, so shared data needs synchronisation.

**Q. What happens during a context switch?**

The kernel saves the running task's CPU state (registers, program counter, stack pointer) into its PCB or thread control block, picks the next task with the scheduler, restores that task's saved state and, if it belongs to another process, switches the page tables, which also invalidates TLB entries. Context switches are pure overhead, which is why too small a round-robin time quantum hurts throughput.

**Q. What are the four conditions for deadlock, and how do you prevent it?**

Mutual exclusion, hold and wait, no preemption and circular wait; all four must hold. Prevention breaks one of them. In practice the easiest is circular wait: acquire locks in one fixed global order. Others: request all resources at once (breaks hold and wait), or allow preemption. Avoidance (Banker's algorithm) only grants a request if the system stays in a safe state. Detection builds a wait-for graph and recovers by killing or rolling back a process.

**Q. Mutex vs semaphore?**

A mutex is a lock with an owner: one thread locks it and the same thread must unlock it, giving mutual exclusion for a critical section. A semaphore is a counter with wait (decrement, block at zero) and signal (increment). A counting semaphore lets up to N threads use N identical resources, like a pool of 5 database connections. A binary semaphore looks like a mutex but has no owner, so it's also used for signalling between threads, for example producer to consumer.

**Q. What is virtual memory and why is it used?**

Each process sees a private, contiguous address space. The MMU translates virtual pages to physical frames through page tables, with the TLB caching recent translations. Benefits: isolation between processes, running programs larger than RAM by keeping only the working set in memory, simpler loading and linking, and sharing (shared libraries, copy-on-write after fork). The cost is translation overhead and page faults.

**Q. What is a page fault and what is thrashing?**

A page fault occurs when a process touches a page that isn't in RAM. The OS traps, finds the page on disk, picks a victim frame with a replacement policy such as LRU, loads the page, updates the page table and restarts the instruction. Thrashing is when the combined working sets don't fit in memory, so the system spends most of its time paging instead of executing. Fixes: reduce the degree of multiprogramming or add memory.

**Q. Compare FCFS, SJF and round robin scheduling.**

FCFS runs jobs in arrival order; simple but short jobs wait behind long ones (convoy effect). SJF picks the shortest burst and gives the minimum average waiting time, but needs burst estimates and can starve long jobs. Round robin gives each process a time quantum in turn: good response time for interactive systems; the quantum must be large relative to the context-switch cost. Real systems use multilevel feedback queues or Linux's CFS.

**Q. What is a race condition, and what is a critical section?**

A race condition is when the result depends on the timing of threads accessing shared data, for example two threads doing count++ (load, add, store) and losing an update. The critical section is the code that touches the shared data. A correct solution needs mutual exclusion, progress and bounded waiting, implemented with locks, semaphores or atomic operations.

**Q. What are zombie and orphan processes?**

A zombie has finished but its parent hasn't called wait() to read its exit status, so its process-table entry remains. An orphan's parent died first; it's re-parented to init or systemd, which reaps it. Many zombies can exhaust process IDs, so parents must wait() or handle SIGCHLD.

**Q. What do fork() and exec() do?**

fork() creates a child that is a copy of the parent; modern kernels share pages copy-on-write until either side writes. It returns 0 in the child and the child's PID in the parent. exec() replaces the current process image with a new program, keeping the PID and open file descriptors. A shell runs a command with fork, then exec in the child, while the parent waits.

**Q. Internal vs external fragmentation?**

Internal fragmentation is wasted space inside an allocated block, for example the unused part of the last page. External fragmentation is enough total free memory split into pieces too small to use, typical of variable-size allocation and segmentation. Paging removes external fragmentation at the cost of some internal fragmentation.


**Learn more**

- [OSTEP (free book)](https://pages.cs.wisc.edu/~remzi/OSTEP/)

**Related:** [Processes and threads](core-cs.md#processes-and-threads) · [Deadlock](core-cs.md#deadlock) · [Memory management and virtual memory](core-cs.md#memory-management-and-virtual-memory) · [Synchronisation: mutex, semaphore, race conditions](core-cs.md#synchronisation-mutex-semaphore-race-conditions) · [CPU scheduling](core-cs.md#cpu-scheduling)

[Back to the topic list](#topics)

## DBMS and SQL: model answers

*Level 2: Interview-ready*

Every backend and fintech interview asks these; Razorpay-style companies go deeper on transactions.

**Key idea**

Read the question, answer it out loud from memory, then open the model answer and compare. Mark the ones you missed and re-do them in 3 days.


**Questions and model answers**

**Q. Explain normalisation up to 3NF with an example.**

Take Student(roll, name, dept, dept\_head). 1NF: every value is atomic, no repeating groups. 2NF: no non-key column depends on part of a composite key. 3NF: no non-key column depends on another non-key column. dept\_head depends on dept, not on roll, so it's a transitive dependency; split into Student(roll, name, dept) and Dept(dept, dept\_head). This removes update anomalies: changing a head now touches one row.

**Q. What are the ACID properties?**

Atomicity: a transaction happens fully or not at all, using undo logs. Consistency: constraints hold before and after. Isolation: concurrent transactions behave as if run one after another, to the chosen isolation level. Durability: once committed, data survives crashes, using write-ahead logging. Example: a bank transfer debits one account and credits another; atomicity stops money disappearing if the system crashes in between.

**Q. Which isolation level prevents dirty reads? Explain the anomalies.**

A dirty read is reading another transaction's uncommitted data; a non-repeatable read is the same row returning different values within one transaction; a phantom read is a repeated range query returning new rows. Read Committed prevents dirty reads, Repeatable Read also prevents non-repeatable reads, and Serializable prevents phantoms. Higher isolation costs concurrency. PostgreSQL and MySQL implement these with MVCC snapshots.

**Q. How does an index speed up a query, and why B+ trees?**

Without an index the database scans every row. A B+ tree index keeps keys sorted in wide, shallow nodes sized to disk pages, so finding a key among millions takes about 3 to 4 page reads, and range queries walk the linked leaf level. Hash indexes are faster for exact matches but can't do ranges. Indexes speed reads but slow inserts and updates and use space.

**Q. Clustered vs non-clustered index?**

A clustered index determines the physical order of the rows; there's one per table, usually the primary key. A non-clustered (secondary) index is a separate structure storing the key plus a pointer or the primary key, so lookups may need a second step. A covering index includes all columns the query needs and avoids that step.

**Q. Primary key vs unique key vs foreign key?**

A primary key uniquely identifies each row and can't be null; one per table. A unique key also enforces uniqueness but allows null (one or many nulls depending on the database) and a table can have several. A foreign key references another table's key and enforces referential integrity, for example orders.user\_id must exist in users.id.

**Q. DELETE vs TRUNCATE vs DROP?**

DELETE removes chosen rows with WHERE, is logged row by row, fires triggers and can be rolled back. TRUNCATE removes all rows quickly by deallocating pages, usually can't use WHERE and resets identity counters. DROP removes the table itself along with its structure, indexes and constraints.

**Q. Write SQL for the second-highest salary per department.**

Use a window function: SELECT dept\_id, name, salary FROM (SELECT e.\*, DENSE\_RANK() OVER (PARTITION BY dept\_id ORDER BY salary DESC) AS r FROM employee e) t WHERE r = 2. DENSE\_RANK handles ties so two people sharing the top salary don't push the second-highest to rank 3. Without window functions, use a correlated subquery counting distinct higher salaries.

**Q. What is the difference between WHERE and HAVING?**

WHERE filters rows before grouping and can't use aggregates. HAVING filters groups after GROUP BY and can use aggregates, for example SELECT dept, COUNT(\*) FROM emp GROUP BY dept HAVING COUNT(\*) \> 5. The logical order is FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.

**Q. SQL vs NoSQL: when would you choose each?**

SQL databases give a fixed schema, joins and strong ACID transactions: good for payments, orders, anything relational. NoSQL stores (document, key-value, wide-column, graph) give flexible schemas and easier horizontal scaling, often with eventual consistency: good for huge write volumes, caching, feeds and logs. Many systems use both, for example PostgreSQL for orders and Redis for sessions.

**Q. How do you prevent SQL injection?**

Never build queries by concatenating user input. Use parameterised queries or prepared statements, where the query structure and the data are sent separately, so input can't change the query. Add least-privilege database accounts and input validation as extra layers.


**Learn more**

- [CMU 15-445 (free lectures)](https://15445.courses.cs.cmu.edu)
- [Use The Index, Luke](https://use-the-index-luke.com)

**Related:** [Transactions, ACID and isolation](core-cs.md#transactions-acid-and-isolation) · [Normalisation and keys](core-cs.md#normalisation-and-keys) · [Indexing and B+ trees](core-cs.md#indexing-and-b-trees) · [SQL for interviews](core-cs.md#sql-for-interviews)

[Back to the topic list](#topics)

## Computer networks: model answers

*Level 2: Interview-ready*

CN questions are short but frequent, and they connect directly to your security work.

**Key idea**

Read the question, answer it out loud from memory, then open the model answer and compare. Mark the ones you missed and re-do them in 3 days.


**Questions and model answers**

**Q. What happens when you type google.com and press Enter?**

The browser checks its caches, then resolves the name through DNS: OS cache, then a recursive resolver that asks the root, the .com TLD server and Google's authoritative server, returning an IP. The browser opens a TCP connection (three-way handshake) or QUIC, then a TLS handshake that checks Google's certificate and agrees keys. It sends an HTTP GET; the request may pass a CDN and load balancer to an application server. The response HTML is parsed, CSS, JS and images are fetched, and the page is laid out and painted.

**Q. Explain the TCP three-way handshake. Why not two?**

Client sends SYN with sequence number x; server replies SYN-ACK with its own sequence y and ack x+1; client sends ACK y+1. Three messages are needed so both sides know the other received their initial sequence number. With two, the server couldn't tell whether the client got its SYN, and an old duplicate SYN could open a ghost connection.

**Q. TCP vs UDP, and when would you use UDP?**

TCP is connection-oriented and reliable: ordered delivery, acknowledgements, retransmission, flow and congestion control. UDP sends independent datagrams with no guarantees and very little overhead. Use UDP when latency matters more than perfect delivery: video calls, online games, live streaming, DNS lookups. QUIC (HTTP/3) adds reliability on top of UDP to avoid TCP's head-of-line blocking.

**Q. Flow control vs congestion control?**

Flow control protects the receiver: the receiver advertises a window of how much it can buffer, and the sender never exceeds it. Congestion control protects the network: the sender keeps a congestion window that grows with slow start and additive increase, and shrinks sharply on packet loss (multiplicative decrease).

**Q. Explain the OSI model and where common devices sit.**

Physical (bits on the wire), data link (frames, MAC addresses, switches), network (IP packets, routing, routers), transport (TCP/UDP, ports), session, presentation and application (HTTP, DNS). TCP/IP merges them into link, internet, transport and application. Each layer adds its own header: data, then segment, packet and frame.

**Q. How does HTTPS work?**

HTTPS is HTTP over TLS. In TLS 1.3 the client and server exchange ephemeral Diffie-Hellman key shares to derive a shared secret; the server proves its identity with a certificate signed by a trusted certificate authority, which the client verifies. After the handshake, traffic is encrypted and integrity-protected with a fast symmetric cipher such as AES-GCM. Asymmetric crypto is used only to authenticate and agree keys because it's slow.

**Q. What is DNS and which record types matter?**

DNS maps names to addresses through a hierarchy of servers with caching controlled by TTLs. A maps to IPv4, AAAA to IPv6, CNAME aliases one name to another, MX gives mail servers, NS names authoritative servers, TXT holds text such as SPF records. It mostly uses UDP port 53, falling back to TCP for large responses.

**Q. What is subnetting? How many hosts in a /26?**

Subnetting splits a network by borrowing host bits for the network part. A /26 leaves 32 − 26 = 6 host bits: 2⁶ = 64 addresses, minus the network and broadcast addresses, so 62 usable hosts. Subnetting limits broadcast domains and lets you apply security rules per subnet, like public and private subnets in an AWS VPC.

**Q. What is ARP, and what is ARP spoofing?**

ARP finds the MAC address for an IP on the local network: a host broadcasts 'who has 192.168.1.1?' and the owner replies with its MAC. ARP has no authentication, so an attacker can send forged replies and become the man in the middle. Defences include dynamic ARP inspection on switches and encrypting traffic with TLS.

**Q. HTTP/1.1 vs HTTP/2 vs HTTP/3?**

HTTP/1.1 sends requests one after another per connection (browsers open several connections). HTTP/2 multiplexes many streams over one TCP connection with header compression, but a lost TCP packet still blocks all streams. HTTP/3 runs over QUIC on UDP, so streams are independent and connection setup is faster.


**Learn more**

- [Kurose and Ross](https://gaia.cs.umass.edu/kurose_ross/index.php)
- [The Illustrated TLS 1.3 Connection](https://tls13.xargs.org)

**Related:** [OSI and TCP/IP models](core-cs.md#osi-and-tcpip-models) · [TCP vs UDP and the handshake](core-cs.md#tcp-vs-udp-and-the-handshake) · [HTTP, HTTPS and TLS](core-cs.md#http-https-and-tls) · [What happens when you type a URL](core-cs.md#what-happens-when-you-type-a-url)

[Back to the topic list](#topics)

## OOP and C++: model answers

*Level 2: Interview-ready*

Every service-company round and most product rounds ask OOP; C++ depth is a plus for HFT.

**Key idea**

Read the question, answer it out loud from memory, then open the model answer and compare. Mark the ones you missed and re-do them in 3 days.


**Questions and model answers**

**Q. Explain the four pillars of OOP with examples.**

Encapsulation: keep data private and expose methods, like a BankAccount whose balance changes only through deposit and withdraw. Abstraction: show what an object does, not how, like an abstract Shape with area(). Inheritance: a Circle is a Shape and reuses its interface. Polymorphism: calling area() on a Shape reference runs Circle's or Square's version at run time through virtual functions; overloading and templates give compile-time polymorphism.

**Q. Overloading vs overriding?**

Overloading is the same function name with different parameter lists in the same scope, resolved at compile time. Overriding is a derived class redefining a base class's virtual function with the same signature, resolved at run time through the vtable. In C++, mark overrides with the override keyword so the compiler catches signature mistakes.

**Q. How does a virtual function call work in C++?**

Each class with virtual functions has a vtable, an array of pointers to its versions of those functions. Each object holds a hidden vptr to its class's vtable, set by the constructor. A virtual call loads the vptr, indexes the vtable and jumps: one extra indirection that usually prevents inlining.

**Q. Why should a base class destructor be virtual?**

If you delete a derived object through a base pointer and the destructor isn't virtual, only the base destructor runs; the derived part's resources leak and the behaviour is undefined. Any class meant to be used polymorphically should have a virtual destructor.

**Q. Abstract class vs interface?**

In C++ an abstract class has at least one pure virtual function (= 0) and can't be instantiated; it can still have data and implemented methods. An interface is the special case with only pure virtual functions and no data. Java and C# have a separate interface keyword; C++ uses abstract classes for both.

**Q. What is RAII?**

Resource Acquisition Is Initialisation: tie a resource's lifetime to an object's lifetime. The constructor acquires (memory, file, lock) and the destructor releases, so cleanup happens automatically even when an exception is thrown. unique\_ptr, lock\_guard and ifstream are RAII types; it's why modern C++ rarely needs raw new and delete.

**Q. unique\_ptr vs shared\_ptr?**

unique\_ptr has one owner, can be moved but not copied, and has no overhead over a raw pointer. shared\_ptr allows many owners through a reference count and frees the object when the count reaches zero; it costs an atomic counter and can leak through cycles, which weak\_ptr breaks. Default to unique\_ptr.

**Q. Explain SOLID briefly.**

Single responsibility: one reason to change. Open/closed: extend behaviour without editing existing code, through interfaces. Liskov substitution: a subclass must work anywhere its base does (a Square that breaks Rectangle's setters violates it). Interface segregation: small focused interfaces. Dependency inversion: depend on abstractions and inject concrete implementations.

**Q. Shallow copy vs deep copy?**

A shallow copy copies member values, so two objects end up pointing at the same heap memory, leading to double frees. A deep copy allocates new memory and copies the pointed-to data. If a class owns a raw resource, follow the rule of three/five (destructor, copy and move operations), or use RAII members like vector so the defaults are correct.

**Q. What is a static member, and what is const correctness?**

A static data member belongs to the class, not to any object, so all instances share it; a static member function has no this pointer. Const correctness means marking anything that shouldn't change as const: const references for parameters you only read, and const member functions that promise not to modify the object.


**Learn more**

- [learncpp.com](https://www.learncpp.com)
- [Refactoring.Guru](https://refactoring.guru/design-patterns)

**Related:** [OOP: the four pillars](core-cs.md#oop-the-four-pillars) · [Virtual functions and the vtable](core-cs.md#virtual-functions-and-the-vtable) · [SOLID and design patterns](core-cs.md#solid-and-design-patterns)

[Back to the topic list](#topics)

## Security and cloud: model answers

*Level 2: Interview-ready*

Your edge as a cybersecurity student: SDE interviewers remember a strong security answer.

**Key idea**

Read the question, answer it out loud from memory, then open the model answer and compare. Mark the ones you missed and re-do them in 3 days.


**Questions and model answers**

**Q. Authentication vs authorisation?**

Authentication verifies who you are (password, MFA, certificate). Authorisation decides what you may do once identified (roles, policies, ownership checks). Broken access control, the top OWASP risk, is an authorisation failure: the user is logged in but the app doesn't check they own the object they request.

**Q. Hashing vs encryption, and how should passwords be stored?**

Hashing is one-way and fixed-length, used for integrity. Encryption is reversible with a key. Passwords should be hashed with a slow, salted algorithm such as Argon2id or bcrypt: the salt defeats precomputed tables and the slowness makes brute force expensive. Never encrypt passwords or use a fast hash like MD5 or SHA-256 alone.

**Q. What is XSS and how do you prevent it?**

Cross-site scripting runs attacker-controlled JavaScript in another user's browser on your site, through reflected input, stored content or client-side DOM writes. Prevent it with context-aware output encoding, frameworks that escape by default, a Content-Security-Policy, and HttpOnly cookies so stolen scripts can't read session tokens.

**Q. What is CSRF?**

Cross-site request forgery makes a logged-in user's browser send an unwanted request, such as changing their email, from another site, because the browser attaches cookies automatically. Defences: SameSite cookies, anti-CSRF tokens tied to the session, and re-authentication for sensitive actions.

**Q. What is SSRF and why is it dangerous in the cloud?**

Server-side request forgery makes your server fetch a URL the attacker controls. They point it at internal services or the cloud metadata endpoint at 169.254.169.254 to steal temporary IAM credentials. Defend with allow-lists, blocking private address ranges after DNS resolution, IMDSv2 on AWS, and least-privilege instance roles.

**Q. How does AWS IAM decide whether a request is allowed?**

Everything starts denied. AWS evaluates all applicable policies: identity policies, resource policies, permission boundaries and organisation SCPs. An explicit Deny anywhere wins; otherwise an Allow is needed and nothing may cap it. That's why TenantWall uses explicit denies to enforce tenant isolation even if someone adds a broad allow later.

**Q. What is ABAC and why use it for multi-tenant isolation?**

Attribute-based access control grants access when attributes match, for example a principal's tenant tag equals a resource's tenant tag. One policy covers every tenant, so onboarding a new tenant needs no new policy, unlike role-per-tenant RBAC. The tags themselves must be protected so users can't re-tag themselves into another tenant.

**Q. How would you detect unauthorised access attempts in AWS?**

Enable CloudTrail, including S3 data events for sensitive buckets, and send it to CloudWatch Logs. Create a metric filter matching AccessDenied and UnauthorizedOperation error codes, put an alarm on the metric, and notify through SNS. GuardDuty adds managed threat detection. This is the monitoring layer in TenantWall.

**Q. Explain a buffer overflow and the main mitigations.**

Writing past the end of a stack buffer can overwrite the saved return address and redirect execution. Stack canaries detect the overwrite before return, NX/DEP stops executing injected code on the stack, and ASLR randomises addresses so the attacker must first leak one. Attackers respond with return-oriented programming and info leaks, so the real fix is bounds-checked code.

**Q. What is threat modelling?**

A structured way to find design-level risks before attackers do: draw the data flow and trust boundaries, then for each element ask STRIDE (spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege), and record a mitigation for each threat. It turns 'is it secure?' into a checklist you can defend in an interview.


**Learn more**

- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org)
- [AWS IAM policy evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)

**Related:** [OWASP Top 10](security.md#owasp-top-10) · [SQL injection](security.md#sql-injection) · [Cross-site scripting (XSS) and CSRF](security.md#cross-site-scripting-xss-and-csrf) · [AWS IAM and least privilege](cloud.md#aws-iam-and-least-privilege) · [Hashing, encryption and passwords](security.md#hashing-encryption-and-passwords)

[Back to the topic list](#topics)
