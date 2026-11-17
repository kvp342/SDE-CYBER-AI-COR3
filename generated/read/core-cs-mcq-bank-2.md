CORE CS · OA MULTIPLE CHOICE · II

# 150 more MCQs with answers and reasons

A second set of 150 questions on Operating Systems, DBMS, Computer Networks, OOP and C++ output, 30 each, none repeated from the first MCQ bank. More numericals this time (SRTF and Round Robin waiting times, optimal paging, TLB access time, disk scheduling, closures and keys, subnetting, delays) plus design patterns and modern C++. Answers are on separate pages at the end, each with a one-line reason.

**How to use.** Do one section in 20 minutes (40 seconds a question), mark your answers, then check the key. Score 24 or more out of 30 before you move on; below that, read the linked Knowledge Base page and retry the section a week later. Put every wrong question into your revision tracker.

## Index

| Section                          | Questions |
|----------------------------------|-----------|
| [Operating Systems](#operating-systemsknowledge-base-)     | Q1–Q30    |
| [DBMS and SQL](#dbms-and-sqlknowledge-base-)          | Q31–Q60   |
| [Computer Networks](#computer-networksknowledge-base-)     | Q61–Q90   |
| [OOP and design](#oop-and-designknowledge-base-)        | Q91–Q120  |
| [C++ output prediction](#c-output-predictionknowledge-base-) | Q121–Q150 |

## How the answers were checked

- All 30 C++ questions were compiled with `g++ -std=c++17 -Wall -Wextra -fsanitize=address,undefined` and run; the printed output is the keyed answer, and no wrong option equals it. None depends on undefined behaviour.
- Scheduling (SRTF, Round Robin, SJF optimality), page replacement (optimal, LRU, FIFO), access time and disk scheduling were simulated in Python; candidate and super keys came from computing attribute closures; NULL and join answers were run in SQLite; subnet answers used Python's ipaddress module; three OOP answers (construction order, virtual calls in constructors, default arguments) were compiled and run. 90 checks in `generated/src/test_mcq2.py`.
- Answer positions are shuffled: A 39, B 35, C 37, D 39.

Questions and explanations are original. For deeper reading use the Knowledge Base pages linked in each section heading and the Core CS Q&A pages.

## Operating Systems[Knowledge Base ↗](knowledge-base/core-cs.md#processes-and-threads)

**Q1.** SRTF: P1 (arrives 0, burst 8), P2 (1, 4), P3 (2, 9), P4 (3, 5). Average waiting time?

1.  **A** 7.75
2.  **B** 8.25
3.  **C** 6.5
4.  **D** 6

**Q2.** Round Robin, quantum 2: P1 = 5, P2 = 3, P3 = 1, all arriving at 0 in that order. Average waiting time?

1.  **A** 4.33
2.  **B** 4
3.  **C** 3.67
4.  **D** 5

**Q3.** Optimal page replacement, 3 frames, string 7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1: how many faults?

1.  **A** 10
2.  **B** 9
3.  **C** 15
4.  **D** 12

**Q4.** TLB hit ratio 80%, TLB lookup 20 ns, memory access 100 ns, single-level page table. Effective access time?

1.  **A** 140 ns
2.  **B** 220 ns
3.  **C** 160 ns
4.  **D** 120 ns

**Q5.** 4 KB pages and 1 GB of physical memory give how many frames?

1.  **A** 1048576 (2^20)
2.  **B** 4096 (2^12)
3.  **C** 65536 (2^16)
4.  **D** 262144 (2^18)

**Q6.** 32-bit logical addresses and 1 KB pages: bits for page number and offset?

1.  **A** 24 and 8
2.  **B** 10 and 22
3.  **C** 22 and 10
4.  **D** 20 and 12

**Q7.** Disk head at 53, queue 98, 183, 37, 122, 14, 124, 65, 67. Total head movement under FCFS?

1.  **A** 382
2.  **B** 640
3.  **C** 236
4.  **D** 208

**Q8.** Same queue under SSTF?

1.  **A** 640
2.  **B** 236
3.  **C** 299
4.  **D** 208

**Q9.** Among non-preemptive algorithms, which gives the minimum average waiting time for a known set of jobs?

1.  **A** Shortest Job First
2.  **B** First Come First Served
3.  **C** Priority scheduling
4.  **D** Round Robin

**Q10.** A Round Robin time quantum that is too small mainly causes:

1.  **A** FCFS behaviour
2.  **B** Deadlock
3.  **C** Starvation of short jobs
4.  **D** Too much context-switch overhead

**Q11.** Under the many-to-one threading model, if one thread makes a blocking system call:

1.  **A** The whole process blocks
2.  **B** The kernel creates a new thread
3.  **C** Only that thread blocks
4.  **D** The call fails

**Q12.** A running process moves to the ready state when:

1.  **A** It finishes
2.  **B** Its time slice expires (timer interrupt)
3.  **C** It calls wait()
4.  **D** It requests I/O

**Q13.** Priority inversion is usually fixed by:

1.  **A** Increasing the quantum
2.  **B** Priority inheritance
3.  **C** Disabling interrupts
4.  **D** Aging

**Q14.** In the first readers–writers solution, who can starve?

1.  **A** Both equally
2.  **B** Readers
3.  **C** Writers
4.  **D** Neither

**Q15.** A standard fix for deadlock in the dining philosophers problem is:

1.  **A** Use a larger table
2.  **B** Make one philosopher pick up the right fork first
3.  **C** Give every philosopher two forks at the start
4.  **D** Let everyone pick the left fork first

**Q16.** A monitor guarantees that:

1.  **A** At most one process is active inside it at a time
2.  **B** No process ever waits
3.  **C** Busy waiting is used
4.  **D** Deadlock cannot happen anywhere

**Q17.** A system is in a safe state when:

1.  **A** Some order exists in which every process can finish
2.  **B** All resources are free
3.  **C** There are no cycles in the wait-for graph
4.  **D** No process holds any resource

**Q18.** With one instance of each resource, a cycle in the resource-allocation graph means:

1.  **A** Starvation
2.  **B** Deadlock (necessary and sufficient)
3.  **C** No deadlock
4.  **D** Possible deadlock only

**Q19.** Copy-on-write after fork() means:

1.  **A** Pages are copied to disk
2.  **B** All pages are copied at fork
3.  **C** The child cannot write memory
4.  **D** Pages are copied only when one process writes to them

**Q20.** When a parent exits before its child, the child:

1.  **A** Is adopted by init (PID 1) or a subreaper
2.  **B** Keeps the dead parent's PID as parent
3.  **C** Is killed immediately
4.  **D** Becomes a zombie

**Q21.** The fastest IPC for large data between processes on one machine is usually:

1.  **A** Shared memory
2.  **B** Message queues
3.  **C** Pipes
4.  **D** Sockets

**Q22.** An ordinary (anonymous) pipe is:

1.  **A** A one-way byte stream between related processes
2.  **B** A network socket
3.  **C** A file on disk
4.  **D** A two-way message queue

**Q23.** The working-set model tracks:

1.  **A** Pages referenced in the last Δ memory references
2.  **B** Dirty pages
3.  **C** Pages in the swap file
4.  **D** Pages loaded at start

**Q24.** Pure segmentation mainly suffers from:

1.  **A** TLB misses
2.  **B** Internal fragmentation
3.  **C** Belady's anomaly
4.  **D** External fragmentation

**Q25.** An inverted page table has one entry per:

1.  **A** Virtual page
2.  **B** TLB line
3.  **C** Process
4.  **D** Physical frame

**Q26.** Multilevel page tables mainly:

1.  **A** Remove the need for a TLB
2.  **B** Save memory for sparse address spaces
3.  **C** Prevent page faults
4.  **D** Speed up every access

**Q27.** SCAN disk scheduling is also called:

1.  **A** LOOK
2.  **B** Shortest seek first
3.  **C** Circular scheduling
4.  **D** The elevator algorithm

**Q28.** Rate-monotonic scheduling gives the highest priority to the task with:

1.  **A** The longest period
2.  **B** The longest burst
3.  **C** The shortest period
4.  **D** The earliest arrival

**Q29.** RAID 1 is:

1.  **A** Striping with double parity
2.  **B** Striping with distributed parity
3.  **C** Striping without redundancy
4.  **D** Mirroring

**Q30.** Demand paging loads a page:

1.  **A** When memory is full
2.  **B** When the process starts
3.  **C** Every time quantum
4.  **D** Only when it is first accessed

## DBMS and SQL[Knowledge Base ↗](knowledge-base/core-cs.md#normalisation-and-keys)

**Q31.** R(A, B, C, D) with A → B and B → C. The candidate key is:

1.  **A** A
2.  **B** AD
3.  **C** ABD
4.  **D** AB

**Q32.** R(A, B, C) with the single key A. How many super keys?

1.  **A** 4
2.  **B** 3
3.  **C** 1
4.  **D** 7

**Q33.** A decomposition of R into R1 and R2 is lossless when:

1.  **A** Both are in BCNF
2.  **B** R1 ∩ R2 is a key of R1 or of R2
3.  **C** R1 and R2 have no common attribute
4.  **D** Every FD stays in one table

**Q34.** Fourth normal form deals with:

1.  **A** Transitive dependencies
2.  **B** Join dependencies only
3.  **C** Multivalued dependencies
4.  **D** Partial dependencies

**Q35.** A non-repeatable read is:

1.  **A** New rows appearing in a repeated range query
2.  **B** Reading uncommitted data
3.  **C** Two writers overwriting each other
4.  **D** Reading the same row twice and getting different committed values

**Q36.** Write-ahead logging requires that:

1.  **A** No log is kept for reads
2.  **B** The log record reaches disk before the changed data page
3.  **C** Logs are written only at commit
4.  **D** Data pages are written before the log

**Q37.** A checkpoint mainly:

1.  **A** Speeds up queries
2.  **B** Locks all tables
3.  **C** Creates a backup copy
4.  **D** Shortens crash recovery

**Q38.** A schedule is conflict-serialisable exactly when:

1.  **A** It uses two-phase locking
2.  **B** Its precedence graph has no cycle
3.  **C** No transaction aborts
4.  **D** All transactions are read-only

**Q39.** In the wait–die scheme, when an older transaction requests a lock held by a younger one:

1.  **A** The older one is aborted
2.  **B** The younger one is aborted
3.  **C** The older one waits
4.  **D** Both abort

**Q40.** A hash index is good for:

1.  **A** Equality lookups
2.  **B** Prefix LIKE searches
3.  **C** ORDER BY
4.  **D** Range queries

**Q41.** An index on (a, b) helps WHERE b = 5 alone?

1.  **A** Only if b is unique
2.  **B** Yes, always
3.  **C** Usually not: only the leftmost prefix is usable
4.  **D** Only for COUNT(\*)

**Q42.** A covering index is one that:

1.  **A** Covers the whole table
2.  **B** Contains every column the query needs
3.  **C** Is clustered
4.  **D** Is on the primary key

**Q43.** A NATURAL JOIN joins on:

1.  **A** Columns you list in USING
2.  **B** All columns with the same name in both tables
3.  **C** The primary keys only
4.  **D** No columns (a cross join)

**Q44.** Values 1, 1, 2, NULL. COUNT(DISTINCT x) returns:

1.  **A** 4
2.  **B** 3
3.  **C** 1
4.  **D** 2

**Q45.** A column holds only NULLs. SUM(column) returns:

1.  **A** The row count
2.  **B** NULL
3.  **C** An error
4.  **D** 0

**Q46.** Values 2, 4, NULL. AVG(x) returns:

1.  **A** NULL
2.  **B** 2
3.  **C** 3
4.  **D** 6

**Q47.** x NOT IN (SELECT v FROM t) when t contains a NULL returns:

1.  **A** An error
2.  **B** Rows where x is NULL
3.  **C** All rows
4.  **D** No rows

**Q48.** Table A has 3 rows with k = 1; table B has 3 rows with k = 1. A JOIN B ON A.k = B.k returns:

1.  **A** 1 row
2.  **B** 6 rows
3.  **C** 3 rows
4.  **D** 9 rows

**Q49.** TRUNCATE differs from DELETE in that TRUNCATE:

1.  **A** Removes all rows without a WHERE clause and per-row logging
2.  **B** Can filter rows
3.  **C** Fires row-level triggers
4.  **D** Removes the table definition

**Q50.** A correlated subquery is one that:

1.  **A** Uses GROUP BY
2.  **B** Runs only once
3.  **C** Has no WHERE clause
4.  **D** Refers to columns of the outer query

**Q51.** A many-to-many relationship in an ER diagram becomes, in tables:

1.  **A** A separate junction table with two foreign keys
2.  **B** An index
3.  **C** One merged table
4.  **D** A foreign key on one side

**Q52.** In a one-to-many relationship, the foreign key goes in:

1.  **A** The table on the 'one' side
2.  **B** The table on the 'many' side
3.  **C** A junction table always
4.  **D** Both tables

**Q53.** Specialisation in an ER model is:

1.  **A** Top-down: splitting an entity into sub-types
2.  **B** Bottom-up: merging entities
3.  **C** Removing attributes
4.  **D** Adding a relationship

**Q54.** A trigger is:

1.  **A** Code that runs automatically on an INSERT, UPDATE or DELETE
2.  **B** A view with parameters
3.  **C** A kind of index
4.  **D** A scheduled backup

**Q55.** A main benefit of stored procedures is:

1.  **A** They replace indexes
2.  **B** They are portable across all databases
3.  **C** They make tables smaller
4.  **D** Fewer round trips and logic kept close to the data

**Q56.** Which is a document database?

1.  **A** Cassandra
2.  **B** Neo4j
3.  **C** Redis
4.  **D** MongoDB

**Q57.** Eventual consistency means:

1.  **A** Replicas converge if no new updates arrive
2.  **B** Writes are never lost
3.  **C** Every read sees the latest write
4.  **D** Data is consistent after every transaction

**Q58.** Adding many indexes to a table mainly slows down:

1.  **A** SELECT by primary key
2.  **B** INSERT, UPDATE and DELETE
3.  **C** Backups only
4.  **D** Nothing

**Q59.** Optimistic concurrency control:

1.  **A** Locks rows before reading
2.  **B** Uses only table locks
3.  **C** Checks for conflicts at commit and retries if needed
4.  **D** Never aborts

**Q60.** A materialised view:

1.  **A** Is recomputed on every read
2.  **B** Is the same as a table alias
3.  **C** Cannot be indexed
4.  **D** Stores the query result and must be refreshed

## Computer Networks[Knowledge Base ↗](knowledge-base/core-cs.md#osi-and-tcpip-models)

**Q61.** How many /24 subnets fit in a /16?

1.  **A** 256
2.  **B** 65536
3.  **C** 254
4.  **D** 16

**Q62.** Usable hosts in a /29?

1.  **A** 14
2.  **B** 8
3.  **C** 6
4.  **D** 30

**Q63.** Is 10.0.0.255 a usable host address in 10.0.0.0/23?

1.  **A** No, it is reserved
2.  **B** No, it is the network address
3.  **C** Yes
4.  **D** No, it is the broadcast address

**Q64.** The smallest single prefix covering 192.168.0.0/24 and 192.168.1.0/24:

1.  **A** 192.168.0.0/22
2.  **B** 192.168.0.0/23
3.  **C** 192.168.0.0/16
4.  **D** 192.168.1.0/23

**Q65.** Propagation delay over 2,000 km at 2 × 10^8 m/s?

1.  **A** 10 ms
2.  **B** 100 ms
3.  **C** 1 ms
4.  **D** 0.1 ms

**Q66.** Bandwidth–delay product of a 10 Mbps link with 20 ms one-way delay?

1.  **A** 50,000 bytes
2.  **B** 2,500 bytes
3.  **C** 200,000 bytes
4.  **D** 25,000 bytes

**Q67.** Stop-and-wait: transmission time 1 ms, one-way propagation 2 ms. Link utilisation?

1.  **A** 20%
2.  **B** 50%
3.  **C** 33%
4.  **D** 10%

**Q68.** Minimum TCP header size?

1.  **A** 60 bytes
2.  **B** 8 bytes
3.  **C** 20 bytes
4.  **D** 40 bytes

**Q69.** UDP header size?

1.  **A** 20 bytes
2.  **B** 16 bytes
3.  **C** 8 bytes
4.  **D** 4 bytes

**Q70.** The IP TTL field mainly:

1.  **A** Orders fragments
2.  **B** Sets the connection timeout
3.  **C** Measures bandwidth
4.  **D** Stops packets looping forever

**Q71.** Default port for SMTP?

1.  **A** 21
2.  **B** 143
3.  **C** 25
4.  **D** 110

**Q72.** Three duplicate ACKs in TCP trigger:

1.  **A** Slow start from 1 segment
2.  **B** Window scaling
3.  **C** Fast retransmit
4.  **D** Connection reset

**Q73.** Why does TCP keep a connection in TIME_WAIT?

1.  **A** To keep the port open for new data
2.  **B** To compute the RTT
3.  **C** To wait for the server to reboot
4.  **D** So the final ACK can be resent and old duplicates expire

**Q74.** Nagle's algorithm:

1.  **A** Chooses the shortest route
2.  **B** Combines small writes into fewer segments
3.  **C** Encrypts TCP data
4.  **D** Retransmits lost packets faster

**Q75.** Distance-vector routing is known for the problem of:

1.  **A** Count to infinity
2.  **B** Hidden terminals
3.  **C** Flooding storms
4.  **D** Split horizon

**Q76.** OSPF is a:

1.  **A** Distance-vector protocol
2.  **B** Link-state protocol using Dijkstra
3.  **C** Transport protocol
4.  **D** Path-vector protocol

**Q77.** BGP routes traffic:

1.  **A** Between autonomous systems
2.  **B** Between processes
3.  **C** Only over IPv6
4.  **D** Inside a LAN

**Q78.** A switch, unlike a hub:

1.  **A** Sends every frame to all ports
2.  **B** Forwards a frame only to the port of the destination MAC
3.  **C** Routes between IP networks
4.  **D** Works at the physical layer

**Q79.** A VLAN splits one switch into separate:

1.  **A** Collision domains only
2.  **B** Physical cables
3.  **C** Broadcast domains
4.  **D** IP addresses

**Q80.** CSMA/CD was used by:

1.  **A** Fibre point-to-point links
2.  **B** Classic shared Ethernet
3.  **C** Wi-Fi
4.  **D** Bluetooth

**Q81.** Minimum Ethernet frame size?

1.  **A** 46 bytes
2.  **B** 1500 bytes
3.  **C** 64 bytes
4.  **D** 18 bytes

**Q82.** To correct any single-bit error, a code needs a minimum Hamming distance of:

1.  **A** 4
2.  **B** 2
3.  **C** 1
4.  **D** 3

**Q83.** The key improvement of HTTP/2 over HTTP/1.1 is:

1.  **A** Plain-text headers
2.  **B** Using UDP
3.  **C** Multiplexing many streams over one connection
4.  **D** Removing TLS

**Q84.** HTTP 301 means:

1.  **A** Found (temporary redirect)
2.  **B** Not modified
3.  **C** Bad request
4.  **D** Moved permanently

**Q85.** HTTP cookies are mainly used to:

1.  **A** Encrypt traffic
2.  **B** Route packets
3.  **C** Compress pages
4.  **D** Keep state between stateless requests

**Q86.** The DNS record type for an IPv6 address is:

1.  **A** CNAME
2.  **B** AAAA
3.  **C** MX
4.  **D** A

**Q87.** traceroute discovers the path by:

1.  **A** Asking each router for its table
2.  **B** Opening TCP connections to each hop
3.  **C** Sending packets with increasing TTL and reading ICMP time-exceeded replies
4.  **D** Using ARP

**Q88.** The IPv4 loopback address is:

1.  **A** 192.168.0.1
2.  **B** 127.0.0.1
3.  **C** 255.255.255.255
4.  **D** 0.0.0.0

**Q89.** A TLS handshake provides:

1.  **A** Compression of HTTP
2.  **B** IP address assignment
3.  **C** Routing between networks
4.  **D** Server authentication and agreement on session keys

**Q90.** Which layer does a router work at?

1.  **A** Transport layer
2.  **B** Data link layer
3.  **C** Physical layer
4.  **D** Network layer

## OOP and design[Knowledge Base ↗](knowledge-base/core-cs.md#oop-the-four-pillars)

**Q91.** Abstraction means:

1.  **A** Bundling data with methods
2.  **B** Having many forms
3.  **C** Deriving one class from another
4.  **D** Showing what an object does while hiding how

**Q92.** A class with two direct base classes uses:

1.  **A** Multilevel inheritance
2.  **B** Hybrid composition
3.  **C** Hierarchical inheritance
4.  **D** Multiple inheritance

**Q93.** In C → B → A (C derives from B, B from A), constructors run in the order:

1.  **A** B, A, C
2.  **B** A, B, C
3.  **C** C, B, A
4.  **D** Only C

**Q94.** Two overloaded functions cannot differ only in:

1.  **A** Parameter types
2.  **B** Number of parameters
3.  **C** Return type
4.  **D** const-ness of a reference parameter

**Q95.** A pure virtual destructor:

1.  **A** Cannot exist
2.  **B** Makes the class final
3.  **C** Must still have a definition
4.  **D** Is called only for the base

**Q96.** Protected members are accessible:

1.  **A** In the class and its derived classes
2.  **B** Only in the class itself
3.  **C** Everywhere
4.  **D** Only in friend classes

**Q97.** Composition differs from aggregation in that with composition:

1.  **A** The whole owns the part's lifetime
2.  **B** There is no relationship
3.  **C** The part can belong to many wholes
4.  **D** Inheritance is used

**Q98.** Square inheriting from Rectangle with independent setWidth/setHeight is the classic violation of:

1.  **A** Single responsibility
2.  **B** Open/closed
3.  **C** Interface segregation
4.  **D** Liskov substitution

**Q99.** Single responsibility principle:

1.  **A** Each method takes one parameter
2.  **B** A class should have one method
3.  **C** A class should have one reason to change
4.  **D** A program should have one class

**Q100.** Which pattern lets you swap an algorithm at run time?

1.  **A** Facade
2.  **B** Prototype
3.  **C** Strategy
4.  **D** Singleton

**Q101.** Which pattern adds behaviour by wrapping an object in another of the same interface?

1.  **A** Decorator
2.  **B** Adapter
3.  **C** Builder
4.  **D** Proxy

**Q102.** Which pattern converts one interface into another that clients expect?

1.  **A** Decorator
2.  **B** Adapter
3.  **C** Facade
4.  **D** Command

**Q103.** Which pattern builds a complex object step by step?

1.  **A** Factory method
2.  **B** Builder
3.  **C** Prototype
4.  **D** Observer

**Q104.** Which pattern creates objects by cloning an existing one?

1.  **A** Prototype
2.  **B** Flyweight
3.  **C** Builder
4.  **D** Singleton

**Q105.** Which pattern gives one simple interface to a complex subsystem?

1.  **A** Composite
2.  **B** Mediator
3.  **C** Facade
4.  **D** Proxy

**Q106.** Which pattern controls access to an object through a stand-in?

1.  **A** Proxy
2.  **B** Decorator
3.  **C** Adapter
4.  **D** Bridge

**Q107.** Which pattern turns a request into an object, enabling undo and queues?

1.  **A** Iterator
2.  **B** Strategy
3.  **C** Command
4.  **D** State

**Q108.** std::unique_ptr:

1.  **A** Never frees memory
2.  **B** Counts references
3.  **C** Has sole ownership and can be moved but not copied
4.  **D** Can be copied freely

**Q109.** Two objects holding shared_ptrs to each other leak because of:

1.  **A** Double deletion
2.  **B** Slicing
3.  **C** A reference cycle; fix one side with weak_ptr
4.  **D** A missing virtual destructor

**Q110.** RAII means:

1.  **A** Resources are freed by a garbage collector
2.  **B** Exceptions are disabled
3.  **C** A resource is acquired in a constructor and released in the destructor
4.  **D** Every class needs an init() method

**Q111.** The rule of five adds which two to the rule of three?

1.  **A** Two comparison operators
2.  **B** swap and clone
3.  **C** Default constructor and destructor
4.  **D** Move constructor and move assignment

**Q112.** A const member function:

1.  **A** Must be static
2.  **B** Is always inline
3.  **C** Cannot be called on non-const objects
4.  **D** Cannot modify non-mutable data members

**Q113.** Calling a virtual function inside a base-class constructor calls:

1.  **A** The base-class version
2.  **B** The most-derived version
3.  **C** A pure virtual stub always
4.  **D** Nothing (it is ignored)

**Q114.** operator\<\< for printing a class is usually a non-member (often friend) because:

1.  **A** It must be virtual
2.  **B** Members cannot return references
3.  **C** Friends are faster
4.  **D** The left operand is the ostream, not your class

**Q115.** Good design aims for:

1.  **A** Low coupling and high cohesion
2.  **B** High coupling and low cohesion
3.  **C** High coupling and high cohesion
4.  **D** No classes at all

**Q116.** Dynamic binding in C++ needs:

1.  **A** A static member
2.  **B** An overloaded operator
3.  **C** A template
4.  **D** A virtual function called through a base pointer or reference

**Q117.** Templates provide:

1.  **A** Garbage collection
2.  **B** Run-time polymorphism
3.  **C** Compile-time (parametric) polymorphism
4.  **D** Multiple inheritance

**Q118.** A virtual function with a default argument, called through a base pointer to a derived object, uses:

1.  **A** The derived body and derived default
2.  **B** The derived body with the base's default argument
3.  **C** The base body and base default
4.  **D** Neither (compile error)

**Q119.** The Observer pattern is a good fit for:

1.  **A** Building objects in steps
2.  **B** Notifying many subscribers when a subject changes
3.  **C** Adapting old interfaces
4.  **D** Creating a single global instance

**Q120.** In Java a class can:

1.  **A** Not implement interfaces
2.  **B** Extend many classes
3.  **C** Extend one class and implement many interfaces
4.  **D** Implement only one interface

## C++ output prediction[Knowledge Base ↗](knowledge-base/dsa.md#c-and-the-stl)

Every program below includes \<bits/stdc++.h\> and uses namespace std (left out to save space). Compiled as C++17.

**Q121.** What does this print?

``` cpp
int main() { int x = 7; cout << (x >> 1) << (x << 1); }
```

1.  **A** 37
2.  **B** 614
3.  **C** 314
4.  **D** 3.514

**Q122.** What does this print?

``` cpp
int main() { cout << 10 % 3 * 2; }
```

1.  **A** 0
2.  **B** 5
3.  **C** 4
4.  **D** 2

**Q123.** What does this print?

``` cpp
int main() { string s = "abc"; cout << s.substr(1) << s.find('c'); }
```

1.  **A** bc2
2.  **B** c2
3.  **C** bc3
4.  **D** ab2

**Q124.** What does this print?

``` cpp
int main() { vector<int> v(3, 7); cout << v.size() << v[2]; }
```

1.  **A** 73
2.  **B** 77
3.  **C** 37
4.  **D** 30

**Q125.** What does this print?

``` cpp
int main() { vector<int> v{5, 3, 9}; sort(v.rbegin(), v.rend()); cout << v[0] << v[2]; }
```

1.  **A** 93
2.  **B** 53
3.  **C** 95
4.  **D** 39

**Q126.** What does this print?

``` cpp
int main() { int a[5] = {1, 2}; cout << a[1] << a[4]; }
```

1.  **A** 2 garbage
2.  **B** 21
3.  **C** 20
4.  **D** 12

**Q127.** What does this print?

``` cpp
int main() { pair<int, int> p{2, 3}; auto [x, y] = p; cout << x * y; }
```

1.  **A** 23
2.  **B** 6
3.  **C** 5
4.  **D** Compile error

**Q128.** What does this print?

``` cpp
int main() { map<char, int> m; for (char c : string("banana")) m[c]++; cout << m['a'] << m['n'] << m.size(); }
```

1.  **A** 323
2.  **B** 313
3.  **C** 326
4.  **D** 233

**Q129.** What does this print?

``` cpp
int main() { stack<int> s; s.push(1); s.push(2); s.pop(); cout << s.top() << s.size(); }
```

1.  **A** 21
2.  **B** 12
3.  **C** 22
4.  **D** 11

**Q130.** What does this print?

``` cpp
int main() { deque<int> d{1, 2, 3}; d.push_front(0); cout << d.front() << d.size(); }
```

1.  **A** 14
2.  **B** 03
3.  **C** 04
4.  **D** 13

**Q131.** What does this print?

``` cpp
int main() { cout << boolalpha << (3 > 2); }
```

1.  **A** true
2.  **B** 1
3.  **C** True
4.  **D** yes

**Q132.** What does this print?

``` cpp
int main() { cout << setfill('0') << setw(3) << 7; }
```

1.  **A** 700
2.  **B** 7
3.  **C** 007
4.  **D** 7

**Q133.** What does this print?

``` cpp
int main() { cout << fixed << setprecision(2) << 3.14159; }
```

1.  **A** 3.14
2.  **B** 3.142
3.  **C** 3.14159
4.  **D** 3.1

**Q134.** What does this print?

``` cpp
int main() { int i = 10; do { i++; } while (i < 5); cout << i; }
```

1.  **A** 11
2.  **B** 10
3.  **C** 6
4.  **D** 5

**Q135.** What does this print?

``` cpp
int main() { int s = 0; for (int i = 1; i <= 5; i += 2) s += i; cout << s; }
```

1.  **A** 5
2.  **B** 9
3.  **C** 6
4.  **D** 15

**Q136.** What does this print?

``` cpp
int main() { int x = 2; switch (x) { case 1: cout << "a"; [[fallthrough]]; case 2: cout << "b"; [[fallthrough]]; case 3: cout << "c"; break; default: cout << "d"; } }
```

1.  **A** b
2.  **B** bcd
3.  **C** abc
4.  **D** bc

**Q137.** What does this print?

``` cpp
struct Cnt { static int n; Cnt() { n++; } }; int Cnt::n = 0; int main() { Cnt a; vector<Cnt> v(3); cout << Cnt::n; }
```

1.  **A** 3
2.  **B** 1
3.  **C** 0
4.  **D** 4

**Q138.** What does this print?

``` cpp
struct B { virtual void f() { cout << "B"; } void g() { f(); } virtual ~B() {} }; struct D : B { void f() override { cout << "D"; } }; int main() { D d; d.g(); }
```

1.  **A** Compile error
2.  **B** BD
3.  **C** B
4.  **D** D

**Q139.** What does this print?

``` cpp
struct B { B() { f(); } virtual void f() { cout << "B"; } virtual ~B() {} }; struct D : B { void f() override { cout << "D"; } }; int main() { D d; }
```

1.  **A** D
2.  **B** B
3.  **C** Nothing
4.  **D** BD

**Q140.** What does this print?

``` cpp
struct B { virtual void f(int x = 1) { cout << x; } virtual ~B() {} }; struct D : B { void f(int x = 2) override { cout << x * 10; } }; int main() { B* p = new D; p->f(); delete p; }
```

1.  **A** 10
2.  **B** 20
3.  **C** 2
4.  **D** 1

**Q141.** What does this print?

``` cpp
void f(int) { cout << "i"; } void f(char) { cout << "c"; } int main() { f('a'); f(97); }
```

1.  **A** ic
2.  **B** ci
3.  **C** cc
4.  **D** ii

**Q142.** What does this print?

``` cpp
int main() { int a = 1, b = 2; int* p = &a; int*& r = p; r = &b; cout << *p; }
```

1.  **A** 1
2.  **B** 2
3.  **C** Address of b
4.  **D** Compile error

**Q143.** What does this print?

``` cpp
int main() { cout << (char)('a' + 25) << int('A'); }
```

1.  **A** y65
2.  **B** z97
3.  **C** z65
4.  **D** {65

**Q144.** What does this print?

``` cpp
int main() { string a = "apple", b = "banana"; cout << (a < b) << a.compare(a); }
```

1.  **A** 10
2.  **B** 01
3.  **C** 00
4.  **D** 11

**Q145.** What does this print?

``` cpp
int f(int n) { return n <= 1 ? 1 : n * f(n - 1); } int main() { cout << f(5); }
```

1.  **A** 120
2.  **B** 720
3.  **C** 15
4.  **D** 24

**Q146.** What does this print?

``` cpp
int main() { int x = 1; auto f = [x] { return x; }; x = 5; cout << f() << x; }
```

1.  **A** 55
2.  **B** 11
3.  **C** 51
4.  **D** 15

**Q147.** What does this print?

``` cpp
int main() { vector<int> v{1, 2, 3}; for (auto x : v) x *= 2; cout << v[0]; for (auto& x : v) x *= 2; cout << v[0]; }
```

1.  **A** 24
2.  **B** 11
3.  **C** 12
4.  **D** 22

**Q148.** What does this print?

``` cpp
int main() { vector<int> v{1, 2, 3, 2, 4}; v.erase(remove(v.begin(), v.end(), 2), v.end()); cout << v.size() << v[1]; }
```

1.  **A** 34
2.  **B** 33
3.  **C** 52
4.  **D** 32

**Q149.** What does this print?

``` cpp
int main() { vector<int> v{1, 3, 5, 7}; cout << lower_bound(v.begin(), v.end(), 4) - v.begin(); }
```

1.  **A** 2
2.  **B** 4
3.  **C** 1
4.  **D** 3

**Q150.** What does this print?

``` cpp
int main() { int i = 5; int j = i++; int k = ++i; cout << j << k << i; }
```

1.  **A** 567
2.  **B** 576
3.  **C** 667
4.  **D** 577

## Answer key: Operating Systems

| Q              | Ans | Option                                                | Why                                                                                        |
|----------------|-----|-------------------------------------------------------|--------------------------------------------------------------------------------------------|
| [Q1](#dbms-and-sqlknowledge-base-)  | C   | 6.5                                                   | Order P1 0–1, P2 1–5, P4 5–10, P1 10–17, P3 17–26; waits 9, 0, 15, 2 → 26 / 4.             |
| [Q2](#dbms-and-sqlknowledge-base-)  | A   | 4.33                                                  | Completions P3 5, P2 8, P1 9; waits 4, 5, 4 → 13 / 3.                                      |
| [Q3](#dbms-and-sqlknowledge-base-)  | B   | 9                                                     | Replace the page used furthest in the future; LRU gives 12 and FIFO 15 on the same string. |
| [Q4](#dbms-and-sqlknowledge-base-)  | A   | 140 ns                                                | 0.8 × (20 + 100) + 0.2 × (20 + 100 + 100) = 96 + 44.                                       |
| [Q5](#dbms-and-sqlknowledge-base-)  | D   | 262144 (2^18)                                         | 2^30 / 2^12 = 2^18.                                                                        |
| [Q6](#dbms-and-sqlknowledge-base-)  | C   | 22 and 10                                             | Offset = log2(1024) = 10; the remaining 22 bits number the pages.                          |
| [Q7](#dbms-and-sqlknowledge-base-)  | B   | 640                                                   | Sum of \|differences\| in queue order.                                                     |
| [Q8](#dbms-and-sqlknowledge-base-)  | B   | 236                                                   | Always go to the nearest request: 65, 67, 37, 14, 98, 122, 124, 183.                       |
| [Q9](#dbms-and-sqlknowledge-base-)  | A   | Shortest Job First                                    | SJF is provably optimal for average waiting time; the catch is knowing burst lengths.      |
| [Q10](#dbms-and-sqlknowledge-base-) | D   | Too much context-switch overhead                      | Each switch costs time; tiny quanta spend most of the CPU switching.                       |
| [Q11](#dbms-and-sqlknowledge-base-) | A   | The whole process blocks                              | The kernel sees one schedulable entity, so the whole process waits.                        |
| [Q12](#dbms-and-sqlknowledge-base-) | B   | Its time slice expires (timer interrupt)              | Preemption by the timer is running → ready; an I/O request is running → waiting.           |
| [Q13](#dbms-and-sqlknowledge-base-) | B   | Priority inheritance                                  | The low-priority lock holder temporarily inherits the waiting high priority.               |
| [Q14](#dbms-and-sqlknowledge-base-) | C   | Writers                                               | A steady stream of readers keeps the lock, so a writer may wait forever.                   |
| [Q15](#dbms-and-sqlknowledge-base-) | B   | Make one philosopher pick up the right fork first     | Breaking the symmetry removes the circular wait.                                           |
| [Q16](#dbms-and-sqlknowledge-base-) | A   | At most one process is active inside it at a time     | Mutual exclusion is built in; condition variables handle waiting.                          |
| [Q17](#dbms-and-sqlknowledge-base-) | A   | Some order exists in which every process can finish   | Unsafe does not mean deadlocked, but safe guarantees no deadlock.                          |
| [Q18](#dbms-and-sqlknowledge-base-) | B   | Deadlock (necessary and sufficient)                   | With multiple instances a cycle is only necessary, not sufficient.                         |
| [Q19](#dbms-and-sqlknowledge-base-) | D   | Pages are copied only when one process writes to them | Parent and child share read-only pages until a write fault.                                |
| [Q20](#dbms-and-sqlknowledge-base-) | A   | Is adopted by init (PID 1) or a subreaper             | That is an orphan; a zombie is a finished child not yet waited for.                        |
| [Q21](#dbms-and-sqlknowledge-base-) | A   | Shared memory                                         | After setup no kernel copy is needed, but you must synchronise yourself.                   |
| [Q22](#dbms-and-sqlknowledge-base-) | A   | A one-way byte stream between related processes       | Two-way needs two pipes; named pipes (FIFOs) work between unrelated processes.             |
| [Q23](#dbms-and-sqlknowledge-base-) | A   | Pages referenced in the last Δ memory references      | Giving each process its working set prevents thrashing.                                    |
| [Q24](#dbms-and-sqlknowledge-base-) | D   | External fragmentation                                | Variable-sized segments leave holes between them.                                          |
| [Q25](#dbms-and-sqlknowledge-base-) | D   | Physical frame                                        | Its size depends on RAM, not on address-space size; lookups need hashing.                  |
| [Q26](#dbms-and-sqlknowledge-base-) | B   | Save memory for sparse address spaces                 | Unused regions need no inner tables; the cost is extra memory accesses.                    |
| [Q27](#dbms-and-sqlknowledge-base-) | D   | The elevator algorithm                                | The head sweeps one way serving requests, then reverses.                                   |
| [Q28](#dbms-and-sqlknowledge-base-) | C   | The shortest period                                   | Fixed priorities by rate; EDF uses deadlines instead.                                      |
| [Q29](#dbms-and-sqlknowledge-base-) | D   | Mirroring                                             | RAID 0 stripes, RAID 5 uses distributed parity, RAID 6 double parity.                      |
| [Q30](#dbms-and-sqlknowledge-base-) | D   | Only when it is first accessed                        | The first access causes a page fault that brings it in.                                    |

Score: \_\_\_\_\_\_ / 30. Target 24 or more.

## Answer key: DBMS and SQL

| Q              | Ans | Option                                                            | Why                                                                                              |
|----------------|-----|-------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| [Q31](#computer-networksknowledge-base-) | B   | AD                                                                | A+ = {A, B, C}; D appears on no right side, so it must be in every key, and AD+ covers all four. |
| [Q32](#computer-networksknowledge-base-) | A   | 4                                                                 | Any superset of A: A, AB, AC, ABC.                                                               |
| [Q33](#computer-networksknowledge-base-) | B   | R1 ∩ R2 is a key of R1 or of R2                                   | The common attributes must functionally determine one side.                                      |
| [Q34](#computer-networksknowledge-base-) | C   | Multivalued dependencies                                          | 5NF deals with join dependencies.                                                                |
| [Q35](#computer-networksknowledge-base-) | D   | Reading the same row twice and getting different committed values | Phantoms are new rows; dirty reads are uncommitted data.                                         |
| [Q36](#computer-networksknowledge-base-) | B   | The log record reaches disk before the changed data page          | Then any change on disk can be undone or redone after a crash.                                   |
| [Q37](#computer-networksknowledge-base-) | D   | Shortens crash recovery                                           | Recovery can start from the last checkpoint instead of the start of the log.                     |
| [Q38](#computer-networksknowledge-base-) | B   | Its precedence graph has no cycle                                 | A topological order of the graph gives the equivalent serial schedule.                           |
| [Q39](#computer-networksknowledge-base-) | C   | The older one waits                                               | Older waits, younger dies; wound–wait is the reverse (the older wounds the younger).             |
| [Q40](#computer-networksknowledge-base-) | A   | Equality lookups                                                  | Hashing scatters keys, so ranges and ordering need a B+ tree.                                    |
| [Q41](#computer-networksknowledge-base-) | C   | Usually not: only the leftmost prefix is usable                   | (a, b) is sorted by a first; b alone is scattered (some engines can skip-scan).                  |
| [Q42](#computer-networksknowledge-base-) | B   | Contains every column the query needs                             | The query is answered from the index alone, without reading table rows.                          |
| [Q43](#computer-networksknowledge-base-) | B   | All columns with the same name in both tables                     | Convenient but fragile: adding a same-named column changes the join.                             |
| [Q44](#computer-networksknowledge-base-) | D   | 2                                                                 | DISTINCT removes the repeat and COUNT ignores NULL.                                              |
| [Q45](#computer-networksknowledge-base-) | B   | NULL                                                              | Aggregates ignore NULLs, and SUM over no values is NULL; use COALESCE(SUM(x), 0).                |
| [Q46](#computer-networksknowledge-base-) | C   | 3                                                                 | NULL is skipped: (2 + 4) / 2.                                                                    |
| [Q47](#computer-networksknowledge-base-) | D   | No rows                                                           | x \<\> NULL is unknown, so the NOT IN is never true. Use NOT EXISTS.                             |
| [Q48](#computer-networksknowledge-base-) | D   | 9 rows                                                            | Every A row matches every B row: 3 × 3. Duplicate keys multiply rows.                            |
| [Q49](#computer-networksknowledge-base-) | A   | Removes all rows without a WHERE clause and per-row logging       | It is usually faster; DROP removes the definition.                                               |
| [Q50](#computer-networksknowledge-base-) | D   | Refers to columns of the outer query                              | Logically it is evaluated once per outer row.                                                    |
| [Q51](#computer-networksknowledge-base-) | A   | A separate junction table with two foreign keys                   | For example enrolment(student_id, course_id).                                                    |
| [Q52](#computer-networksknowledge-base-) | B   | The table on the 'many' side                                      | Each order row points to its one customer.                                                       |
| [Q53](#computer-networksknowledge-base-) | A   | Top-down: splitting an entity into sub-types                      | Generalisation is the bottom-up opposite.                                                        |
| [Q54](#computer-networksknowledge-base-) | A   | Code that runs automatically on an INSERT, UPDATE or DELETE       | Useful for audit logs; overuse hides logic.                                                      |
| [Q55](#computer-networksknowledge-base-) | D   | Fewer round trips and logic kept close to the data                | Downsides: vendor lock-in and harder testing.                                                    |
| [Q56](#computer-networksknowledge-base-) | D   | MongoDB                                                           | Redis is key–value, Cassandra wide-column, Neo4j a graph database.                               |
| [Q57](#computer-networksknowledge-base-) | A   | Replicas converge if no new updates arrive                        | It trades read freshness for availability.                                                       |
| [Q58](#computer-networksknowledge-base-) | B   | INSERT, UPDATE and DELETE                                         | Every write must also update each index.                                                         |
| [Q59](#computer-networksknowledge-base-) | C   | Checks for conflicts at commit and retries if needed              | Good when conflicts are rare, for example with a version column.                                 |
| [Q60](#computer-networksknowledge-base-) | D   | Stores the query result and must be refreshed                     | Fast reads at the cost of staleness and refresh work.                                            |

Score: \_\_\_\_\_\_ / 30. Target 24 or more.

## Answer key: Computer Networks

| Q              | Ans | Option                                                                     | Why                                                                            |
|----------------|-----|----------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| [Q61](#oop-and-designknowledge-base-) | A   | 256                                                                        | 2^(24 − 16) = 256.                                                             |
| [Q62](#oop-and-designknowledge-base-) | C   | 6                                                                          | 2^3 − 2 (network and broadcast).                                               |
| [Q63](#oop-and-designknowledge-base-) | C   | Yes                                                                        | The /23 runs 10.0.0.0 to 10.0.1.255, so .0.255 is an ordinary host.            |
| [Q64](#oop-and-designknowledge-base-) | B   | 192.168.0.0/23                                                             | Route aggregation (supernetting) of two adjacent /24s.                         |
| [Q65](#oop-and-designknowledge-base-) | A   | 10 ms                                                                      | Distance / speed = 2 × 10^6 / 2 × 10^8 s.                                      |
| [Q66](#oop-and-designknowledge-base-) | D   | 25,000 bytes                                                               | 10^7 × 0.02 = 200,000 bits = 25,000 bytes in flight.                           |
| [Q67](#oop-and-designknowledge-base-) | A   | 20%                                                                        | Tt / (Tt + 2 Tp) = 1 / 5.                                                      |
| [Q68](#oop-and-designknowledge-base-) | C   | 20 bytes                                                                   | Up to 60 bytes with options; UDP's header is 8 bytes.                          |
| [Q69](#oop-and-designknowledge-base-) | C   | 8 bytes                                                                    | Source port, destination port, length, checksum: 2 bytes each.                 |
| [Q70](#oop-and-designknowledge-base-) | D   | Stops packets looping forever                                              | Each router decrements it and drops the packet at 0.                           |
| [Q71](#oop-and-designknowledge-base-) | C   | 25                                                                         | POP3 110, IMAP 143, FTP control 21.                                            |
| [Q72](#oop-and-designknowledge-base-) | C   | Fast retransmit                                                            | The sender resends the missing segment without waiting for a timeout.          |
| [Q73](#oop-and-designknowledge-base-) | D   | So the final ACK can be resent and old duplicates expire                   | It lasts 2 × MSL.                                                              |
| [Q74](#oop-and-designknowledge-base-) | B   | Combines small writes into fewer segments                                  | Can add latency for interactive apps (TCP_NODELAY turns it off).               |
| [Q75](#oop-and-designknowledge-base-) | A   | Count to infinity                                                          | Split horizon and poison reverse are fixes for it.                             |
| [Q76](#oop-and-designknowledge-base-) | B   | Link-state protocol using Dijkstra                                         | RIP is distance-vector; BGP is path-vector.                                    |
| [Q77](#oop-and-designknowledge-base-) | A   | Between autonomous systems                                                 | It is the routing protocol of the internet's backbone.                         |
| [Q78](#oop-and-designknowledge-base-) | B   | Forwards a frame only to the port of the destination MAC                   | It learns MAC addresses into a table.                                          |
| [Q79](#oop-and-designknowledge-base-) | C   | Broadcast domains                                                          | Traffic between VLANs needs a router (or layer-3 switch).                      |
| [Q80](#oop-and-designknowledge-base-) | B   | Classic shared Ethernet                                                    | Wi-Fi cannot detect collisions while sending, so it uses CSMA/CA.              |
| [Q81](#oop-and-designknowledge-base-) | C   | 64 bytes                                                                   | 46 bytes of payload plus 18 of header and CRC; needed for collision detection. |
| [Q82](#oop-and-designknowledge-base-) | D   | 3                                                                          | Distance d corrects ⌊(d − 1) / 2⌋ errors and detects d − 1.                    |
| [Q83](#oop-and-designknowledge-base-) | C   | Multiplexing many streams over one connection                              | Headers are also compressed (HPACK); HTTP/3 moves to QUIC over UDP.            |
| [Q84](#oop-and-designknowledge-base-) | D   | Moved permanently                                                          | 302 and 307 are temporary; 304 is not modified.                                |
| [Q85](#oop-and-designknowledge-base-) | D   | Keep state between stateless requests                                      | Session IDs, preferences, tracking.                                            |
| [Q86](#oop-and-designknowledge-base-) | B   | AAAA                                                                       | A is IPv4, MX is mail, CNAME is an alias.                                      |
| [Q87](#oop-and-designknowledge-base-) | C   | Sending packets with increasing TTL and reading ICMP time-exceeded replies | Each router that drops the packet reveals itself.                              |
| [Q88](#oop-and-designknowledge-base-) | B   | 127.0.0.1                                                                  | The whole 127.0.0.0/8 block is loopback; IPv6 uses ::1.                        |
| [Q89](#oop-and-designknowledge-base-) | D   | Server authentication and agreement on session keys                        | Data is then encrypted with symmetric keys.                                    |
| [Q90](#oop-and-designknowledge-base-) | D   | Network layer                                                              | It forwards by IP address; switches forward by MAC.                            |

Score: \_\_\_\_\_\_ / 30. Target 24 or more.

## Answer key: OOP and design

| Q               | Ans | Option                                                                 | Why                                                                                                |
|-----------------|-----|------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| [Q91](#c-output-predictionknowledge-base-)  | D   | Showing what an object does while hiding how                           | Encapsulation bundles and protects; abstraction hides complexity behind an interface.              |
| [Q92](#c-output-predictionknowledge-base-)  | D   | Multiple inheritance                                                   | Multilevel is a chain A → B → C.                                                                   |
| [Q93](#c-output-predictionknowledge-base-)  | B   | A, B, C                                                                | Bases are built first; destructors run in reverse.                                                 |
| [Q94](#c-output-predictionknowledge-base-)  | C   | Return type                                                            | The call site gives no way to choose by return type.                                               |
| [Q95](#c-output-predictionknowledge-base-)  | C   | Must still have a definition                                           | Derived destructors call it, so it needs a body.                                                   |
| [Q96](#c-output-predictionknowledge-base-)  | A   | In the class and its derived classes                                   | Private is the class only; public is everywhere.                                                   |
| [Q97](#c-output-predictionknowledge-base-)  | A   | The whole owns the part's lifetime                                     | A house and its rooms (composition) vs a team and its players (aggregation).                       |
| [Q98](#c-output-predictionknowledge-base-)  | D   | Liskov substitution                                                    | Code expecting a Rectangle breaks when width and height are forced equal.                          |
| [Q99](#c-output-predictionknowledge-base-)  | C   | A class should have one reason to change                               | Split classes that change for different reasons.                                                   |
| [Q100](#c-output-predictionknowledge-base-) | C   | Strategy                                                               | For example different payment or sorting strategies behind one interface.                          |
| [Q101](#c-output-predictionknowledge-base-) | A   | Decorator                                                              | Stackable wrappers; Java I/O streams are the classic example.                                      |
| [Q102](#c-output-predictionknowledge-base-) | B   | Adapter                                                                | A plug adapter: same job, different shape.                                                         |
| [Q103](#c-output-predictionknowledge-base-) | B   | Builder                                                                | Useful with many optional parameters.                                                              |
| [Q104](#c-output-predictionknowledge-base-) | A   | Prototype                                                              | Avoids costly construction or subclassing creators.                                                |
| [Q105](#c-output-predictionknowledge-base-) | C   | Facade                                                                 | For example one 'placeOrder' call hiding inventory, payment and shipping.                          |
| [Q106](#c-output-predictionknowledge-base-) | A   | Proxy                                                                  | Lazy loading, access checks, remote objects.                                                       |
| [Q107](#c-output-predictionknowledge-base-) | C   | Command                                                                | Each command has execute() and can store what undo needs.                                          |
| [Q108](#c-output-predictionknowledge-base-) | C   | Has sole ownership and can be moved but not copied                     | shared_ptr counts references; weak_ptr observes without owning.                                    |
| [Q109](#c-output-predictionknowledge-base-) | C   | A reference cycle; fix one side with weak_ptr                          | Neither count reaches zero.                                                                        |
| [Q110](#c-output-predictionknowledge-base-) | C   | A resource is acquired in a constructor and released in the destructor | Locks (lock_guard), files and memory are released automatically, even on exceptions.               |
| [Q111](#c-output-predictionknowledge-base-) | D   | Move constructor and move assignment                                   | Copy constructor, copy assignment and destructor were the original three.                          |
| [Q112](#c-output-predictionknowledge-base-) | D   | Cannot modify non-mutable data members                                 | Mark mutable for caches or mutexes.                                                                |
| [Q113](#c-output-predictionknowledge-base-) | A   | The base-class version                                                 | The derived part does not exist yet during the base constructor.                                   |
| [Q114](#c-output-predictionknowledge-base-) | D   | The left operand is the ostream, not your class                        | A member would need obj \<\< cout.                                                                 |
| [Q115](#c-output-predictionknowledge-base-) | A   | Low coupling and high cohesion                                         | Classes focus on one job and depend little on each other.                                          |
| [Q116](#c-output-predictionknowledge-base-) | D   | A virtual function called through a base pointer or reference          | Calling on an object by value uses its static type.                                                |
| [Q117](#c-output-predictionknowledge-base-) | C   | Compile-time (parametric) polymorphism                                 | The compiler generates code for each type used.                                                    |
| [Q118](#c-output-predictionknowledge-base-) | B   | The derived body with the base's default argument                      | Default arguments are bound statically, the body dynamically. Avoid defaults on virtual functions. |
| [Q119](#c-output-predictionknowledge-base-) | B   | Notifying many subscribers when a subject changes                      | Event listeners and pub/sub are observers.                                                         |
| [Q120](#c-output-predictionknowledge-base-) | C   | Extend one class and implement many interfaces                         | Java avoids the diamond problem by allowing only single class inheritance.                         |

Score: \_\_\_\_\_\_ / 30. Target 24 or more.

## Answer key: C++ output prediction

| Q               | Ans | Option | Why                                                                                              |
|-----------------|-----|--------|--------------------------------------------------------------------------------------------------|
| [Q121](#answer-key-operating-systems) | C   | 314    | 7 \>\> 1 is 3 (shift right halves, rounding down); 7 \<\< 1 is 14.                               |
| [Q122](#answer-key-operating-systems) | D   | 2      | % and \* have equal precedence, left to right: (10 % 3) \* 2.                                    |
| [Q123](#answer-key-operating-systems) | A   | bc2    | substr(1) starts at index 1; find returns the index 2.                                           |
| [Q124](#answer-key-operating-systems) | C   | 37     | vector(n, value) makes n copies of value.                                                        |
| [Q125](#answer-key-operating-systems) | A   | 93     | Sorting reverse iterators ascending gives descending order.                                      |
| [Q126](#answer-key-operating-systems) | C   | 20     | Missing initialisers in an aggregate are zero-initialised.                                       |
| [Q127](#answer-key-operating-systems) | B   | 6      | Structured bindings (C++17) unpack the pair.                                                     |
| [Q128](#answer-key-operating-systems) | A   | 323    | a appears 3 times, n twice, and there are 3 distinct letters.                                    |
| [Q129](#answer-key-operating-systems) | D   | 11     | pop removes the 2; 1 remains alone.                                                              |
| [Q130](#answer-key-operating-systems) | C   | 04     | push_front adds at the front.                                                                    |
| [Q131](#answer-key-operating-systems) | A   | true   | boolalpha prints bools as words.                                                                 |
| [Q132](#answer-key-operating-systems) | C   | 007    | setw pads to width 3 using the fill character on the left.                                       |
| [Q133](#answer-key-operating-systems) | A   | 3.14   | fixed with precision 2 means 2 digits after the point.                                           |
| [Q134](#answer-key-operating-systems) | A   | 11     | A do-while body runs at least once.                                                              |
| [Q135](#answer-key-operating-systems) | B   | 9      | 1 + 3 + 5.                                                                                       |
| [Q136](#answer-key-operating-systems) | D   | bc     | Without break, execution falls through to the next case until a break.                           |
| [Q137](#answer-key-operating-systems) | D   | 4      | One object plus a vector of three default-constructed elements: the constructor runs four times. |
| [Q138](#answer-key-operating-systems) | D   | D      | g is not virtual, but the f it calls is, so the call dispatches to D::f.                         |
| [Q139](#answer-key-operating-systems) | B   | B      | During B's constructor the object is still a B.                                                  |
| [Q140](#answer-key-operating-systems) | A   | 10     | D's body runs (virtual) with B's default argument (static type).                                 |
| [Q141](#answer-key-operating-systems) | B   | ci     | An exact match wins: 'a' is a char, 97 is an int.                                                |
| [Q142](#answer-key-operating-systems) | B   | 2      | r is a reference to the pointer p, so assigning r changes p.                                     |
| [Q143](#answer-key-operating-systems) | C   | z65    | 'a' + 25 is 'z'; 'A' is 65 in ASCII.                                                             |
| [Q144](#answer-key-operating-systems) | A   | 10     | Strings compare lexicographically; compare returns 0 when equal.                                 |
| [Q145](#answer-key-operating-systems) | A   | 120    | 5 × 4 × 3 × 2 × 1.                                                                               |
| [Q146](#answer-key-operating-systems) | D   | 15     | Capture by value copies x when the lambda is created.                                            |
| [Q147](#answer-key-operating-systems) | C   | 12     | auto copies each element; auto& refers to it.                                                    |
| [Q148](#answer-key-operating-systems) | B   | 33     | Erase–remove deletes every 2, leaving 1, 3, 4.                                                   |
| [Q149](#answer-key-operating-systems) | A   | 2      | lower_bound returns the first element ≥ 4, which is 5 at index 2.                                |
| [Q150](#answer-key-operating-systems) | D   | 577    | j takes 5 then i becomes 6; ++i makes 7 for k and i.                                             |

Score: \_\_\_\_\_\_ / 30. Target 24 or more.
