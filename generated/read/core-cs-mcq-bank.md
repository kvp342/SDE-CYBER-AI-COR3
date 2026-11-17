CORE CS · OA MULTIPLE CHOICE

# 150 MCQs with answers and reasons

Online assessments often add a short MCQ round on Operating Systems, DBMS, Computer Networks, OOP and C++ output. This bank has 30 questions on each. Answers are on separate pages at the end, so you can test yourself first. Each answer has a one-line reason.

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

- All 30 C++ questions were compiled with `g++ -std=c++17 -Wall -fsanitize=address,undefined` and run; the printed output is the keyed answer. None depends on undefined behaviour.
- Page-fault counts were simulated, the fork count was run, subnet answers were computed with Python's ipaddress module, and the SQL answers (joins, COUNT, NULL comparison, second-highest salary, RANK and DENSE_RANK) were run in SQLite.
- Answer positions are shuffled: A 41, B 42, C 36, D 31.

Questions and explanations are original. For deeper reading use the Knowledge Base pages linked in each section heading and the Core CS Q&A pages.

## Operating Systems[Knowledge Base ↗](knowledge-base/core-cs.md#processes-and-threads)

**Q1.** Which scheduling algorithm can starve long processes when short ones keep arriving?

1.  **A** Round Robin
2.  **B** First In First Out with aging
3.  **C** First Come First Served
4.  **D** Shortest Job First

**Q2.** Which is NOT one of the four necessary conditions for deadlock?

1.  **A** Circular wait
2.  **B** Mutual exclusion
3.  **C** Hold and wait
4.  **D** Preemption

**Q3.** The Banker's algorithm is used for deadlock:

1.  **A** Prevention
2.  **B** Avoidance
3.  **C** Detection
4.  **D** Recovery

**Q4.** Thrashing happens when:

1.  **A** Too many I/O devices are attached
2.  **B** The CPU is faster than memory
3.  **C** Processes spend more time paging than executing
4.  **D** The cache is larger than RAM

**Q5.** Belady's anomaly (more frames, more faults) can occur with:

1.  **A** FIFO
2.  **B** Optimal
3.  **C** Any stack algorithm
4.  **D** LRU

**Q6.** Reference string 1,2,3,4,1,2,5,1,2,3,4,5 with 3 frames under FIFO gives how many page faults?

1.  **A** 12
2.  **B** 8
3.  **C** 10
4.  **D** 9

**Q7.** Same string 1,2,3,4,1,2,5,1,2,3,4,5 with 3 frames under LRU gives how many page faults?

1.  **A** 12
2.  **B** 9
3.  **C** 10
4.  **D** 8

**Q8.** During a context switch the OS saves a process's registers in its:

1.  **A** Interrupt vector
2.  **B** Process Control Block
3.  **C** TLB
4.  **D** Page table

**Q9.** Threads of the same process share:

1.  **A** Heap and code
2.  **B** Program counter
3.  **C** Registers
4.  **D** Stack

**Q10.** A semaphore initialised to 1 and used for mutual exclusion is a:

1.  **A** Condition variable
2.  **B** Counting semaphore
3.  **C** Binary semaphore
4.  **D** Monitor

**Q11.** A spinlock is the better choice when:

1.  **A** There is a single core and no preemption
2.  **B** The lock is held very briefly on a multiprocessor
3.  **C** The lock is held for a long time
4.  **D** The critical section does disk I/O

**Q12.** The TLB is a cache of:

1.  **A** Page-table entries
2.  **B** Kernel stacks
3.  **C** Disk blocks
4.  **D** File descriptors

**Q13.** 32-bit virtual addresses with 4 KB pages need how many entries in a single-level page table?

1.  **A** 2^12
2.  **B** 2^22
3.  **C** 2^32
4.  **D** 2^20

**Q14.** Internal fragmentation occurs in:

1.  **A** Paging
2.  **B** Compaction
3.  **C** Segmentation
4.  **D** Variable partitioning

**Q15.** External fragmentation can be reduced by:

1.  **A** Using FIFO replacement
2.  **B** Adding a TLB
3.  **C** Increasing the page size
4.  **D** Compaction

**Q16.** A zombie process is one that:

1.  **A** Lost its parent and was adopted by init
2.  **B** Has finished but its parent has not called wait()
3.  **C** Is blocked on I/O
4.  **D** Is swapped out to disk

**Q17.** Three fork() calls in a row (no conditions) leave how many processes in total?

1.  **A** 6
2.  **B** 8
3.  **C** 7
4.  **D** 3

**Q18.** Round Robin with a very large time quantum behaves like:

1.  **A** Multilevel queue
2.  **B** SJF
3.  **C** Priority scheduling
4.  **D** FCFS

**Q19.** Bursts 24, 3, 3 arrive at time 0 in that order. Average waiting time under FCFS?

1.  **A** 13
2.  **B** 27
3.  **C** 3
4.  **D** 17

**Q20.** The convoy effect is associated with:

1.  **A** Lottery scheduling
2.  **B** SRTF
3.  **C** FCFS
4.  **D** Round Robin

**Q21.** Peterson's solution solves the critical-section problem for how many processes?

1.  **A** Any number
2.  **B** 2
3.  **C** 3
4.  **D** 1

**Q22.** Bounded buffer of size N with semaphores empty, full, mutex. Initial values?

1.  **A** empty = 0, full = N, mutex = 1
2.  **B** empty = 1, full = 0, mutex = N
3.  **C** empty = N, full = N, mutex = 0
4.  **D** empty = N, full = 0, mutex = 1

**Q23.** Which Unix system call creates a new process?

1.  **A** fork()
2.  **B** wait()
3.  **C** kill()
4.  **D** exec()

**Q24.** After a successful execvp(), the code that follows it in the program:

1.  **A** Runs normally
2.  **B** Runs only in the child
3.  **C** Runs twice
4.  **D** Never runs

**Q25.** A page fault occurs when a process accesses a page that is:

1.  **A** Shared with another process
2.  **B** Read-only
3.  **C** In the TLB
4.  **D** Not in main memory

**Q26.** The dirty bit of a page is used to:

1.  **A** Skip writing unmodified pages back to disk
2.  **B** Mark pages for the TLB
3.  **C** Lock pages in memory
4.  **D** Detect stack overflow

**Q27.** A system call normally enters the kernel through:

1.  **A** A trap (software interrupt)
2.  **B** DMA
3.  **C** An ordinary function call
4.  **D** A page fault

**Q28.** SSTF disk scheduling can cause:

1.  **A** Starvation of far requests
2.  **B** Thrashing
3.  **C** The convoy effect
4.  **D** Belady's anomaly

**Q29.** Which is true of a mutex but not of a general semaphore?

1.  **A** Only the thread that locked it may unlock it
2.  **B** It never blocks
3.  **C** It works only between processes
4.  **D** It can count more than one resource

**Q30.** Virtual memory mainly allows:

1.  **A** Sharing CPU registers between processes
2.  **B** Running programs larger than physical memory
3.  **C** Removing the need for a TLB
4.  **D** Faster disk access

## DBMS and SQL[Knowledge Base ↗](knowledge-base/core-cs.md#normalisation-and-keys)

**Q31.** Which normal form removes partial dependencies on a composite key?

1.  **A** 2NF
2.  **B** 1NF
3.  **C** 3NF
4.  **D** 4NF

**Q32.** Which normal form removes transitive dependencies?

1.  **A** 1NF
2.  **B** 5NF
3.  **C** 3NF
4.  **D** 2NF

**Q33.** A relation is in BCNF when:

1.  **A** Every attribute is atomic
2.  **B** It has no multivalued dependencies
3.  **C** Every determinant is a candidate key
4.  **D** It has no repeating groups

**Q34.** In ACID, the I stands for:

1.  **A** Isolation
2.  **B** Idempotence
3.  **C** Integrity
4.  **D** Indexing

**Q35.** Which mechanism mainly provides durability?

1.  **A** Write-ahead logging
2.  **B** Normalisation
3.  **C** Indexing
4.  **D** Locking

**Q36.** The lowest isolation level that prevents dirty reads is:

1.  **A** Read Uncommitted
2.  **B** Read Committed
3.  **C** Repeatable Read
4.  **D** Serializable

**Q37.** In the SQL standard, phantom reads are prevented only at:

1.  **A** Serializable
2.  **B** Repeatable Read
3.  **C** Read Uncommitted
4.  **D** Read Committed

**Q38.** Two-phase locking guarantees:

1.  **A** No starvation
2.  **B** Conflict serializability
3.  **C** Freedom from deadlock
4.  **D** No cascading aborts

**Q39.** A primary key must be:

1.  **A** Unique but may be NULL
2.  **B** Unique and not NULL
3.  **C** Numeric
4.  **D** Indexed as non-clustered

**Q40.** A foreign key refers to:

1.  **A** Only an indexed column of the same table
2.  **B** A primary or unique key in another (or the same) table
3.  **C** A view
4.  **D** Any column of another table

**Q41.** Which statement removes the table definition itself?

1.  **A** DELETE
2.  **B** ALTER ... CLEAR
3.  **C** DROP
4.  **D** TRUNCATE

**Q42.** Which clause filters groups after GROUP BY?

1.  **A** HAVING
2.  **B** WHERE
3.  **C** ORDER BY
4.  **D** LIMIT

**Q43.** A CROSS JOIN of a 4-row table and a 5-row table returns how many rows?

1.  **A** 20
2.  **B** 5
3.  **C** 4
4.  **D** 9

**Q44.** A has 5 rows, B has 3, and no rows match. A LEFT JOIN B returns how many rows?

1.  **A** 5
2.  **B** 15
3.  **C** 3
4.  **D** 0

**Q45.** A column holds 1, NULL, 3, NULL. COUNT(column) returns:

1.  **A** 2
2.  **B** 4
3.  **C** NULL
4.  **D** 0

**Q46.** B+ trees suit database indexes mainly because:

1.  **A** They never need rebalancing
2.  **B** They use hashing
3.  **C** High fan-out keeps them shallow and linked leaves make range scans fast
4.  **D** They store data only in internal nodes

**Q47.** How many clustered indexes can a table have?

1.  **A** Unlimited
2.  **B** Two
3.  **C** One per column
4.  **D** One

**Q48.** A view is:

1.  **A** A physical copy of a table
2.  **B** An index on several columns
3.  **C** A stored query that behaves like a virtual table
4.  **D** A backup snapshot

**Q49.** A weak entity is one that:

1.  **A** Has no attributes
2.  **B** Has only one row
3.  **C** Cannot be identified without its owner entity
4.  **D** Is never stored

**Q50.** A minimal super key is called a:

1.  **A** Composite key
2.  **B** Surrogate key
3.  **C** Foreign key
4.  **D** Candidate key

**Q51.** Which relational-algebra operator chooses columns?

1.  **A** Projection (π)
2.  **B** Selection (σ)
3.  **C** Union (∪)
4.  **D** Join (⋈)

**Q52.** A DBMS detects deadlock with a:

1.  **A** B+ tree
2.  **B** Bloom filter
3.  **C** Wait-for graph
4.  **D** Hash index

**Q53.** Which protocol avoids cascading rollbacks?

1.  **A** Basic timestamp ordering
2.  **B** Strict 2PL
3.  **C** Basic 2PL
4.  **D** Read Uncommitted

**Q54.** UNION differs from UNION ALL in that UNION:

1.  **A** Removes duplicate rows
2.  **B** Requires the same table
3.  **C** Sorts by the first column only
4.  **D** Keeps duplicates

**Q55.** In SQL, the expression NULL = NULL evaluates to:

1.  **A** An error
2.  **B** FALSE
3.  **C** UNKNOWN (NULL)
4.  **D** TRUE

**Q56.** Which query returns the second-highest salary from table e?

1.  **A** SELECT MAX(salary) FROM e WHERE salary \< (SELECT MAX(salary) FROM e)
2.  **B** SELECT salary FROM e ORDER BY salary LIMIT 2
3.  **C** SELECT MIN(salary) FROM e
4.  **D** SELECT MAX(salary) FROM e WHERE salary \> (SELECT MAX(salary) FROM e)

**Q57.** According to CAP, during a network partition a distributed store must choose between:

1.  **A** Availability and latency
2.  **B** Consistency and availability
3.  **C** Consistency and durability
4.  **D** Partition tolerance and durability

**Q58.** Sharding means:

1.  **A** Copying the whole database to replicas
2.  **B** Splitting columns into separate tables
3.  **C** Compressing old data
4.  **D** Splitting rows of a table across several servers

**Q59.** Denormalisation is done to:

1.  **A** Speed up reads at the cost of redundancy
2.  **B** Remove all redundancy
3.  **C** Enforce foreign keys
4.  **D** Reduce storage

**Q60.** Which window function ranks ties without leaving gaps?

1.  **A** ROW_NUMBER()
2.  **B** NTILE()
3.  **C** DENSE_RANK()
4.  **D** RANK()

## Computer Networks[Knowledge Base ↗](knowledge-base/core-cs.md#osi-and-tcpip-models)

**Q61.** Routing between networks happens at which OSI layer?

1.  **A** Transport
2.  **B** Data link
3.  **C** Session
4.  **D** Network

**Q62.** TCP belongs to which layer?

1.  **A** Data link
2.  **B** Transport
3.  **C** Application
4.  **D** Network

**Q63.** How many segments does the TCP connection setup take?

1.  **A** 4
2.  **B** 1
3.  **C** 2
4.  **D** 3

**Q64.** Which transport protocol is connectionless?

1.  **A** SCTP
2.  **B** TCP
3.  **C** QUIC over TCP
4.  **D** UDP

**Q65.** Ordinary DNS queries mostly use:

1.  **A** TCP port 25
2.  **B** UDP port 53
3.  **C** UDP port 67
4.  **D** TCP port 80

**Q66.** Which protocol gives hosts an IP address automatically?

1.  **A** DNS
2.  **B** ARP
3.  **C** DHCP
4.  **D** ICMP

**Q67.** ARP maps:

1.  **A** Ports to processes
2.  **B** IP addresses to MAC addresses
3.  **C** Host names to IP addresses
4.  **D** MAC addresses to IP addresses

**Q68.** How many usable host addresses are in a /26 subnet?

1.  **A** 64
2.  **B** 30
3.  **C** 62
4.  **D** 126

**Q69.** The subnet mask for /20 is:

1.  **A** 255.255.224.0
2.  **B** 255.255.240.0
3.  **C** 255.255.255.240
4.  **D** 255.240.0.0

**Q70.** Which address is private (RFC 1918)?

1.  **A** 172.32.0.1
2.  **B** 8.8.8.8
3.  **C** 11.0.0.1
4.  **D** 192.168.1.10

**Q71.** Broadcast address of 192.168.10.0/24?

1.  **A** 192.168.10.0
2.  **B** 192.168.255.255
3.  **C** 255.255.255.0
4.  **D** 192.168.10.255

**Q72.** Network address of 10.1.5.77/22?

1.  **A** 10.1.5.0
2.  **B** 10.1.0.0
3.  **C** 10.1.4.0
4.  **D** 10.1.5.64

**Q73.** Default port for HTTPS?

1.  **A** 443
2.  **B** 80
3.  **C** 8080
4.  **D** 22

**Q74.** ping uses which protocol?

1.  **A** UDP
2.  **B** TCP
3.  **C** ICMP
4.  **D** ARP

**Q75.** TCP flow control uses:

1.  **A** Slow start
2.  **B** The receiver's advertised window
3.  **C** Checksums
4.  **D** TTL

**Q76.** In TCP slow start the congestion window grows:

1.  **A** Only after loss
2.  **B** Exponentially per round trip
3.  **C** Not at all
4.  **D** Linearly per round trip

**Q77.** Which device works at the data link layer?

1.  **A** Repeater
2.  **B** Hub
3.  **C** Switch
4.  **D** Router

**Q78.** A MAC address is how many bits long?

1.  **A** 48
2.  **B** 128
3.  **C** 64
4.  **D** 32

**Q79.** An IPv6 address is how many bits long?

1.  **A** 128
2.  **B** 48
3.  **C** 32
4.  **D** 64

**Q80.** Which protocol guarantees in-order delivery?

1.  **A** UDP
2.  **B** ICMP
3.  **C** TCP
4.  **D** IP

**Q81.** Go-Back-N with n-bit sequence numbers allows a maximum sender window of:

1.  **A** n
2.  **B** 2^n − 1
3.  **C** 2^(n−1)
4.  **D** 2^n

**Q82.** Selective Repeat with n-bit sequence numbers allows a maximum window of:

1.  **A** 2^n − 1
2.  **B** 2^n
3.  **C** n − 1
4.  **D** 2^(n−1)

**Q83.** NAT mainly:

1.  **A** Encrypts traffic
2.  **B** Resolves host names
3.  **C** Assigns MAC addresses
4.  **D** Maps private addresses to a public address

**Q84.** In HTTPS the server proves its identity with:

1.  **A** Its MAC address
2.  **B** A certificate signed by a trusted CA
3.  **C** Its IP address
4.  **D** A cookie

**Q85.** Which HTTP method is idempotent?

1.  **A** PATCH
2.  **B** PUT
3.  **C** POST
4.  **D** CONNECT

**Q86.** HTTP 403 means:

1.  **A** The resource does not exist
2.  **B** The server understood the request but refuses to allow it
3.  **C** The server crashed
4.  **D** Authentication is missing

**Q87.** Before opening a TCP connection to a website, the browser usually must:

1.  **A** Resolve the host name with DNS
2.  **B** Send an ICMP echo
3.  **C** Open a UDP port 80
4.  **D** Run DHCP

**Q88.** Transmission time of a 1000-byte packet on a 1 Mbps link?

1.  **A** 1 ms
2.  **B** 80 ms
3.  **C** 8 ms
4.  **D** 0.8 ms

**Q89.** Wi-Fi uses which access method?

1.  **A** CSMA/CA
2.  **B** TDMA only
3.  **C** CSMA/CD
4.  **D** Token passing

**Q90.** The largest TCP port number is:

1.  **A** 32767
2.  **B** 65535
3.  **C** 1023
4.  **D** 65536

## OOP and design[Knowledge Base ↗](knowledge-base/core-cs.md#oop-the-four-pillars)

**Q91.** Encapsulation means:

1.  **A** Deriving one class from another
2.  **B** Bundling data with the methods that use it and hiding internal state
3.  **C** Converting objects to bytes
4.  **D** Having many functions with one name

**Q92.** Runtime polymorphism in C++ is achieved with:

1.  **A** Function overloading
2.  **B** Virtual functions
3.  **C** Templates
4.  **D** Macros

**Q93.** Compile-time polymorphism in C++ includes:

1.  **A** Function overloading and templates
2.  **B** Virtual functions
3.  **C** dynamic_cast
4.  **D** Abstract classes

**Q94.** An abstract class in C++ is a class with:

1.  **A** At least one pure virtual function
2.  **B** Only private members
3.  **C** Only static members
4.  **D** No constructor

**Q95.** Can you create an object of an abstract class?

1.  **A** No
2.  **B** Yes
3.  **C** Only with new\[\]
4.  **D** Only on the heap

**Q96.** Why make a base-class destructor virtual?

1.  **A** To make the class abstract
2.  **B** So deleting through a base pointer runs the derived destructor
3.  **C** To prevent copying
4.  **D** To speed up destruction

**Q97.** C++ solves the diamond problem with:

1.  **A** Friend classes
2.  **B** Templates
3.  **C** Private inheritance
4.  **D** Virtual inheritance

**Q98.** Default access of members in a C++ class is:

1.  **A** Depends on the compiler
2.  **B** protected
3.  **C** public
4.  **D** private

**Q99.** With class D : B { }; B is inherited as:

1.  **A** public
2.  **B** virtual
3.  **C** protected
4.  **D** private

**Q100.** Which cannot be virtual in C++?

1.  **A** A member function
2.  **B** A constructor
3.  **C** A destructor
4.  **D** An overloaded operator member

**Q101.** Why must a copy constructor take its parameter by reference?

1.  **A** For speed only
2.  **B** References cannot be null
3.  **C** Because of const rules
4.  **D** Passing by value would call the copy constructor again, recursing forever

**Q102.** The rule of three covers:

1.  **A** Destructor, copy constructor, copy assignment
2.  **B** Constructor, destructor, move
3.  **C** public, private, protected
4.  **D** new, delete, sizeof

**Q103.** A shallow copy of an object that owns a raw pointer risks:

1.  **A** A double free
2.  **B** Faster copies
3.  **C** A compile error
4.  **D** Stack overflow

**Q104.** A friend function:

1.  **A** Is inherited
2.  **B** Is a member function
3.  **C** Can access private members but is not a member
4.  **D** Must be virtual

**Q105.** A static data member is:

1.  **A** Shared by all objects of the class
2.  **B** Only visible in one file
3.  **C** Copied into each object
4.  **D** Constant

**Q106.** Inside a static member function, this is:

1.  **A** Not available
2.  **B** A const pointer
3.  **C** A null pointer
4.  **D** The first object created

**Q107.** Overriding requires that the derived function:

1.  **A** Is static
2.  **B** Has a different name
3.  **C** Has a different parameter list
4.  **D** Has the same signature as a virtual base function

**Q108.** 'Subtypes must be usable wherever the base type is' is which SOLID principle?

1.  **A** Open/closed
2.  **B** Liskov substitution
3.  **C** Dependency inversion
4.  **D** Interface segregation

**Q109.** 'Open for extension, closed for modification' is the:

1.  **A** Single responsibility principle
2.  **B** Open/closed principle
3.  **C** Dependency inversion principle
4.  **D** Liskov substitution principle

**Q110.** Dependency inversion says high-level modules should depend on:

1.  **A** Concrete classes
2.  **B** Global variables
3.  **C** Abstractions
4.  **D** The database

**Q111.** Interface segregation says:

1.  **A** Every class needs an interface
2.  **B** Use multiple inheritance always
3.  **C** Interfaces must not have methods
4.  **D** Prefer several small interfaces to one large one

**Q112.** A 'has-a' relationship is modelled by:

1.  **A** Templates
2.  **B** Overloading
3.  **C** Composition
4.  **D** Inheritance

**Q113.** Which operator cannot be overloaded in C++?

1.  **A** +
2.  **B** ::
3.  **C** \[\]
4.  **D** ()

**Q114.** The Singleton pattern ensures:

1.  **A** A class cannot be inherited
2.  **B** A class has one instance with a global access point
3.  **C** Objects are created through a factory
4.  **D** Objects are immutable

**Q115.** The Factory pattern:

1.  **A** Guarantees one instance
2.  **B** Creates objects without the caller naming the concrete class
3.  **C** Wraps an incompatible interface
4.  **D** Notifies many objects of a change

**Q116.** Which pattern notifies many objects when one object's state changes?

1.  **A** Adapter
2.  **B** Observer
3.  **C** Builder
4.  **D** Singleton

**Q117.** In a typical implementation, the vptr is stored:

1.  **A** In the stack frame
2.  **B** Once per class in the vtable
3.  **C** In each object of a class with virtual functions
4.  **D** In a global table per program

**Q118.** Object slicing happens when:

1.  **A** A class has no destructor
2.  **B** A derived object is copied into a base object by value
3.  **C** A pointer is deleted twice
4.  **D** A template is instantiated

**Q119.** The explicit keyword on a constructor:

1.  **A** Makes it public
2.  **B** Prevents implicit conversions through it
3.  **C** Makes it virtual
4.  **D** Forces inlining

**Q120.** Correct syntax for a pure virtual function:

1.  **A** virtual void f() {} = 0;
2.  **B** void f() = 0;
3.  **C** virtual void f() = 0;
4.  **D** pure virtual void f();

## C++ output prediction[Knowledge Base ↗](knowledge-base/dsa.md#c-and-the-stl)

Every program below includes \<bits/stdc++.h\> and uses namespace std (left out to save space). Compiled as C++17.

**Q121.** What does this print?

``` cpp
int main() { int a = 10, b = 3; cout << a / b << " " << a % b; }
```

1.  **A** 3 0
2.  **B** 3.33 1
3.  **C** 4 1
4.  **D** 3 1

**Q122.** What does this print?

``` cpp
int main() { cout << -7 / 2 << " " << -7 % 2; }
```

1.  **A** -4 1
2.  **B** -3 -1
3.  **C** -3 1
4.  **D** -4 -1

**Q123.** What does this print?

``` cpp
int main() { int x = 5; int &r = x; r++; cout << x; }
```

1.  **A** 6
2.  **B** 7
3.  **C** 5
4.  **D** Compile error

**Q124.** What does this print?

``` cpp
int main() { char c = 'A' + 2; cout << c; }
```

1.  **A** C
2.  **B** A2
3.  **C** 67
4.  **D** B

**Q125.** What does this print?

``` cpp
int main() { unsigned int u = 0; u--; cout << (u > 0); }
```

1.  **A** 0
2.  **B** 4294967295
3.  **C** 1
4.  **D** -1

**Q126.** What does this print?

``` cpp
int main() { int a[] = {1, 2, 3, 4, 5}; cout << *(a + 2) << a[4]; }
```

1.  **A** 3 5
2.  **B** 13
3.  **C** 35
4.  **D** 24

**Q127.** What does this print?

``` cpp
int main() { string s = "abc"; s += 'd'; cout << s.size() << s.back(); }
```

1.  **A** abcd
2.  **B** 4c
3.  **C** 4d
4.  **D** 3d

**Q128.** What does this print?

``` cpp
struct B { virtual void f() { cout << "B"; } virtual ~B() {} };
struct D : B { void f() override { cout << "D"; } };
int main() { B* p = new D; p->f(); delete p; }
```

1.  **A** D
2.  **B** B
3.  **C** BD
4.  **D** Compile error

**Q129.** What does this print?

``` cpp
struct B { void f() { cout << "B"; } };
struct D : B { void f() { cout << "D"; } };
int main() { D d; B* p = &d; p->f(); }
```

1.  **A** B
2.  **B** D
3.  **C** BD
4.  **D** Compile error

**Q130.** What does this print?

``` cpp
struct A { A() { cout << "a"; } ~A() { cout << "~a"; } };
struct B : A { B() { cout << "b"; } ~B() { cout << "~b"; } };
int main() { B x; }
```

1.  **A** ab~a~b
2.  **B** ba~b~a
3.  **C** ab~b~a
4.  **D** ab

**Q131.** What does this print?

``` cpp
struct B { virtual string n() { return "B"; } virtual ~B() {} };
struct D : B { string n() override { return "D"; } };
void show(B b) { cout << b.n(); }
int main() { D d; show(d); }
```

1.  **A** D
2.  **B** B
3.  **C** BD
4.  **D** Undefined

**Q132.** What does this print?

``` cpp
int f() { static int c = 0; return ++c; }
int main() { cout << f() << f() << f(); }
```

1.  **A** 111
2.  **B** Unspecified
3.  **C** 321
4.  **D** 123

**Q133.** What does this print?

``` cpp
int main() { int i = 0; for (; i < 5; i++); cout << i; }
```

1.  **A** 4
2.  **B** 5
3.  **C** 0
4.  **D** 01234

**Q134.** What does this print?

``` cpp
int main() { cout << (7 & 3) << (7 | 8) << (5 ^ 1); }
```

1.  **A** 7154
2.  **B** 31512
3.  **C** 3155
4.  **D** 3154

**Q135.** What does this print?

``` cpp
int main() { cout << (1 << 10); }
```

1.  **A** 11
2.  **B** 20
3.  **C** 1024
4.  **D** 100

**Q136.** What does this print?

``` cpp
int main() { vector<int> v{1, 2, 3}; v.push_back(4); v.erase(v.begin() + 1); for (int x : v) cout << x; }
```

1.  **A** 234
2.  **B** 1234
3.  **C** 134
4.  **D** 124

**Q137.** What does this print?

``` cpp
int main() { map<string, int> m; m["b"] = 2; m["a"] = 1; m["c"]; for (auto& [k, v] : m) cout << k << v; }
```

1.  **A** b2a1c0
2.  **B** a1b2c0
3.  **C** a1b2c
4.  **D** a1b2

**Q138.** What does this print?

``` cpp
int main() { set<int> s{3, 1, 3, 2}; cout << s.size() << *s.begin(); }
```

1.  **A** 33
2.  **B** 31
3.  **C** 41
4.  **D** 43

**Q139.** What does this print?

``` cpp
int main() { int a = 5; int* p = &a; *p += 2; cout << a; }
```

1.  **A** Address of a
2.  **B** 2
3.  **C** 5
4.  **D** 7

**Q140.** What does this print?

``` cpp
int main() { cout << 5 / 2.0; }
```

1.  **A** 2.50
2.  **B** 3
3.  **C** 2
4.  **D** 2.5

**Q141.** What does this print?

``` cpp
int main() { cout << (int)3.99 << (int)-3.99; }
```

1.  **A** 3-3
2.  **B** 4-3
3.  **C** 4-4
4.  **D** 3-4

**Q142.** What does this print?

``` cpp
int main() { bool b = (0.1 + 0.2 == 0.3); cout << b; }
```

1.  **A** 0
2.  **B** Compile error
3.  **C** 1
4.  **D** true

**Q143.** What does this print?

``` cpp
int main() { string s = "hello"; reverse(s.begin(), s.end()); cout << s.substr(1, 3); }
```

1.  **A** lle
2.  **B** llo
3.  **C** oll
4.  **D** ell

**Q144.** What does this print?

``` cpp
int main() { int x = 10; auto f = [x]() mutable { return ++x; }; f(); cout << f() << x; }
```

1.  **A** 1210
2.  **B** 1212
3.  **C** 1112
4.  **D** 1110

**Q145.** What does this print?

``` cpp
int main() { int x = 10; auto g = [&x] { x++; }; g(); g(); cout << x; }
```

1.  **A** Compile error
2.  **B** 10
3.  **C** 12
4.  **D** 11

**Q146.** What does this print?

``` cpp
void f(int) { cout << "int"; }
void f(double) { cout << "double"; }
int main() { f('a'); }
```

1.  **A** char
2.  **B** double
3.  **C** int
4.  **D** Ambiguous call error

**Q147.** What does this print?

``` cpp
int main() { priority_queue<int> pq; pq.push(3); pq.push(1); pq.push(4); cout << pq.top(); pq.pop(); cout << pq.top(); }
```

1.  **A** 34
2.  **B** 41
3.  **C** 43
4.  **D** 13

**Q148.** What does this print?

``` cpp
int main() { int i = 0; if (i++ || i++) cout << i; }
```

1.  **A** 1
2.  **B** Nothing
3.  **C** 2
4.  **D** 0

**Q149.** What does this print?

``` cpp
struct A { A() { cout << "c"; } A(const A&) { cout << "k"; } A& operator=(const A&) { return *this; } };
int main() { A a; A b = a; A c; c = b; }
```

1.  **A** ckck
2.  **B** ckcc
3.  **C** ckc
4.  **D** ccc

**Q150.** What does this print?

``` cpp
int main() { cout << sizeof(char) << " " << sizeof("ab"); }
```

1.  **A** 1 2
2.  **B** 1 3
3.  **C** 0 3
4.  **D** 2 3

## Answer key: Operating Systems

| Q              | Ans | Option                                            | Why                                                                         |
|----------------|-----|---------------------------------------------------|-----------------------------------------------------------------------------|
| [Q1](#dbms-and-sqlknowledge-base-)  | D   | Shortest Job First                                | Short jobs always go first, so a long job can wait forever; aging fixes it. |
| [Q2](#dbms-and-sqlknowledge-base-)  | D   | Preemption                                        | The condition is no preemption; allowing preemption breaks deadlock.        |
| [Q3](#dbms-and-sqlknowledge-base-)  | B   | Avoidance                                         | It grants a request only if the system stays in a safe state.               |
| [Q4](#dbms-and-sqlknowledge-base-)  | C   | Processes spend more time paging than executing   | Too few frames per process causes constant page faults.                     |
| [Q5](#dbms-and-sqlknowledge-base-)  | A   | FIFO                                              | LRU and Optimal are stack algorithms and never show it.                     |
| [Q6](#dbms-and-sqlknowledge-base-)  | D   | 9                                                 | With 4 frames it gives 10: the textbook Belady example.                     |
| [Q7](#dbms-and-sqlknowledge-base-)  | C   | 10                                                | Simulate: only the references 1, 2 after 5 hit.                             |
| [Q8](#dbms-and-sqlknowledge-base-)  | B   | Process Control Block                             | The PCB holds registers, state, PC and scheduling information.              |
| [Q9](#dbms-and-sqlknowledge-base-)  | A   | Heap and code                                     | Each thread has its own stack, registers and PC.                            |
| [Q10](#dbms-and-sqlknowledge-base-) | C   | Binary semaphore                                  | Values 0 and 1 only; acts like a lock.                                      |
| [Q11](#dbms-and-sqlknowledge-base-) | B   | The lock is held very briefly on a multiprocessor | Busy-waiting is cheaper than sleeping only for very short waits.            |
| [Q12](#dbms-and-sqlknowledge-base-) | A   | Page-table entries                                | It speeds up virtual-to-physical address translation.                       |
| [Q13](#dbms-and-sqlknowledge-base-) | D   | 2^20                                              | 32 − 12 offset bits leaves 20 bits of page number.                          |
| [Q14](#dbms-and-sqlknowledge-base-) | A   | Paging                                            | The last page of a process is partly unused.                                |
| [Q15](#dbms-and-sqlknowledge-base-) | D   | Compaction                                        | Compaction moves allocations together to merge free holes.                  |
| [Q16](#dbms-and-sqlknowledge-base-) | B   | Has finished but its parent has not called wait() | Its exit status waits in the process table until reaped.                    |
| [Q17](#dbms-and-sqlknowledge-base-) | B   | 8                                                 | Each fork doubles the count: 2^3.                                           |
| [Q18](#dbms-and-sqlknowledge-base-) | D   | FCFS                                              | No process is ever preempted.                                               |
| [Q19](#dbms-and-sqlknowledge-base-) | D   | 17                                                | (0 + 24 + 27) / 3 = 17. Under SJF it would be 3.                            |
| [Q20](#dbms-and-sqlknowledge-base-) | C   | FCFS                                              | Short jobs queue behind one long CPU-bound job.                             |
| [Q21](#dbms-and-sqlknowledge-base-) | B   | 2                                                 | It uses a turn variable and two flags.                                      |
| [Q22](#dbms-and-sqlknowledge-base-) | D   | empty = N, full = 0, mutex = 1                    | All slots start empty and the lock starts free.                             |
| [Q23](#dbms-and-sqlknowledge-base-) | A   | fork()                                            | exec() replaces the current image; it does not create a process.            |
| [Q24](#dbms-and-sqlknowledge-base-) | D   | Never runs                                        | The process image is replaced; exec returns only on failure.                |
| [Q25](#dbms-and-sqlknowledge-base-) | D   | Not in main memory                                | The OS then loads it from disk (demand paging).                             |
| [Q26](#dbms-and-sqlknowledge-base-) | A   | Skip writing unmodified pages back to disk        | Only modified pages must be written back on eviction.                       |
| [Q27](#dbms-and-sqlknowledge-base-) | A   | A trap (software interrupt)                       | The trap switches the CPU to kernel mode.                                   |
| [Q28](#dbms-and-sqlknowledge-base-) | A   | Starvation of far requests                        | Requests near the head keep winning.                                        |
| [Q29](#dbms-and-sqlknowledge-base-) | A   | Only the thread that locked it may unlock it      | A mutex has an owner; a semaphore does not.                                 |
| [Q30](#dbms-and-sqlknowledge-base-) | B   | Running programs larger than physical memory      | Only the needed pages are kept in RAM.                                      |

Score: \_\_\_\_\_\_ / 30. Target 24 or more.

## Answer key: DBMS and SQL

| Q              | Ans | Option                                                                  | Why                                                                  |
|----------------|-----|-------------------------------------------------------------------------|----------------------------------------------------------------------|
| [Q31](#computer-networksknowledge-base-) | A   | 2NF                                                                     | 2NF: every non-key attribute depends on the whole key.               |
| [Q32](#computer-networksknowledge-base-) | C   | 3NF                                                                     | 3NF: non-key attributes depend only on keys.                         |
| [Q33](#computer-networksknowledge-base-) | C   | Every determinant is a candidate key                                    | Stricter than 3NF.                                                   |
| [Q34](#computer-networksknowledge-base-) | A   | Isolation                                                               | Concurrent transactions do not see each other's partial work.        |
| [Q35](#computer-networksknowledge-base-) | A   | Write-ahead logging                                                     | The log is flushed before commit so changes survive a crash.         |
| [Q36](#computer-networksknowledge-base-) | B   | Read Committed                                                          | Read Uncommitted allows dirty reads.                                 |
| [Q37](#computer-networksknowledge-base-) | A   | Serializable                                                            | Repeatable Read still allows phantoms in the standard.               |
| [Q38](#computer-networksknowledge-base-) | B   | Conflict serializability                                                | 2PL can still deadlock; strict 2PL also avoids cascades.             |
| [Q39](#computer-networksknowledge-base-) | B   | Unique and not NULL                                                     | It identifies each row.                                              |
| [Q40](#computer-networksknowledge-base-) | B   | A primary or unique key in another (or the same) table                  | It enforces referential integrity.                                   |
| [Q41](#computer-networksknowledge-base-) | C   | DROP                                                                    | DELETE and TRUNCATE remove rows only.                                |
| [Q42](#computer-networksknowledge-base-) | A   | HAVING                                                                  | WHERE filters rows before grouping.                                  |
| [Q43](#computer-networksknowledge-base-) | A   | 20                                                                      | Every pair: 4 × 5.                                                   |
| [Q44](#computer-networksknowledge-base-) | A   | 5                                                                       | All left rows are kept, with NULLs for B.                            |
| [Q45](#computer-networksknowledge-base-) | A   | 2                                                                       | COUNT(column) skips NULLs; COUNT(\*) would return 4.                 |
| [Q46](#computer-networksknowledge-base-) | C   | High fan-out keeps them shallow and linked leaves make range scans fast | Fewer disk reads per lookup.                                         |
| [Q47](#computer-networksknowledge-base-) | D   | One                                                                     | It defines the physical order of rows.                               |
| [Q48](#computer-networksknowledge-base-) | C   | A stored query that behaves like a virtual table                        | Materialised views are the exception that store results.             |
| [Q49](#computer-networksknowledge-base-) | C   | Cannot be identified without its owner entity                           | It has a partial key plus the owner's key.                           |
| [Q50](#computer-networksknowledge-base-) | D   | Candidate key                                                           | Remove any attribute and it stops being unique.                      |
| [Q51](#computer-networksknowledge-base-) | A   | Projection (π)                                                          | Selection chooses rows.                                              |
| [Q52](#computer-networksknowledge-base-) | C   | Wait-for graph                                                          | A cycle in the graph means deadlock.                                 |
| [Q53](#computer-networksknowledge-base-) | B   | Strict 2PL                                                              | Write locks are held until commit, so nobody reads uncommitted data. |
| [Q54](#computer-networksknowledge-base-) | A   | Removes duplicate rows                                                  | UNION ALL is faster because it skips duplicate removal.              |
| [Q55](#computer-networksknowledge-base-) | C   | UNKNOWN (NULL)                                                          | Use IS NULL to test for NULL.                                        |
| [Q56](#computer-networksknowledge-base-) | A   | SELECT MAX(salary) FROM e WHERE salary \< (SELECT MAX(salary) FROM e)   | The largest value below the maximum.                                 |
| [Q57](#computer-networksknowledge-base-) | B   | Consistency and availability                                            | Partitions cannot be ruled out, so C or A gives way.                 |
| [Q58](#computer-networksknowledge-base-) | D   | Splitting rows of a table across several servers                        | Horizontal partitioning across machines.                             |
| [Q59](#computer-networksknowledge-base-) | A   | Speed up reads at the cost of redundancy                                | Fewer joins at query time.                                           |
| [Q60](#computer-networksknowledge-base-) | C   | DENSE_RANK()                                                            | RANK gives 1, 1, 3; DENSE_RANK gives 1, 1, 2.                        |

Score: \_\_\_\_\_\_ / 30. Target 24 or more.

## Answer key: Computer Networks

| Q              | Ans | Option                                                    | Why                                                       |
|----------------|-----|-----------------------------------------------------------|-----------------------------------------------------------|
| [Q61](#oop-and-designknowledge-base-) | D   | Network                                                   | Layer 3: IP addresses and routers.                        |
| [Q62](#oop-and-designknowledge-base-) | B   | Transport                                                 | Layer 4, end to end.                                      |
| [Q63](#oop-and-designknowledge-base-) | D   | 3                                                         | SYN, SYN-ACK, ACK.                                        |
| [Q64](#oop-and-designknowledge-base-) | D   | UDP                                                       | UDP sends datagrams with no handshake.                    |
| [Q65](#oop-and-designknowledge-base-) | B   | UDP port 53                                               | TCP 53 is used for large answers and zone transfers.      |
| [Q66](#oop-and-designknowledge-base-) | C   | DHCP                                                      | Discover, Offer, Request, Acknowledge.                    |
| [Q67](#oop-and-designknowledge-base-) | B   | IP addresses to MAC addresses                             | Used on the local link.                                   |
| [Q68](#oop-and-designknowledge-base-) | C   | 62                                                        | 2^6 − 2 (network and broadcast).                          |
| [Q69](#oop-and-designknowledge-base-) | B   | 255.255.240.0                                             | 20 ones: 8 + 8 + 4.                                       |
| [Q70](#oop-and-designknowledge-base-) | D   | 192.168.1.10                                              | Private 172 range is 172.16–172.31 only.                  |
| [Q71](#oop-and-designknowledge-base-) | D   | 192.168.10.255                                            | All host bits set to 1.                                   |
| [Q72](#oop-and-designknowledge-base-) | C   | 10.1.4.0                                                  | /22 blocks start at multiples of 4 in the third octet.    |
| [Q73](#oop-and-designknowledge-base-) | A   | 443                                                       | HTTP uses 80.                                             |
| [Q74](#oop-and-designknowledge-base-) | C   | ICMP                                                      | Echo request and echo reply.                              |
| [Q75](#oop-and-designknowledge-base-) | B   | The receiver's advertised window                          | The sender never exceeds what the receiver can buffer.    |
| [Q76](#oop-and-designknowledge-base-) | B   | Exponentially per round trip                              | It doubles every RTT until the threshold.                 |
| [Q77](#oop-and-designknowledge-base-) | C   | Switch                                                    | It forwards by MAC address.                               |
| [Q78](#oop-and-designknowledge-base-) | A   | 48                                                        | Six bytes, written in hex.                                |
| [Q79](#oop-and-designknowledge-base-) | A   | 128                                                       | IPv4 is 32.                                               |
| [Q80](#oop-and-designknowledge-base-) | C   | TCP                                                       | Sequence numbers and retransmission.                      |
| [Q81](#oop-and-designknowledge-base-) | B   | 2^n − 1                                                   | One number must stay free to tell new frames from old.    |
| [Q82](#oop-and-designknowledge-base-) | D   | 2^(n−1)                                                   | Sender and receiver windows must not overlap.             |
| [Q83](#oop-and-designknowledge-base-) | D   | Maps private addresses to a public address                | Many hosts share one public IP.                           |
| [Q84](#oop-and-designknowledge-base-) | B   | A certificate signed by a trusted CA                      | The browser checks the certificate chain.                 |
| [Q85](#oop-and-designknowledge-base-) | B   | PUT                                                       | Repeating PUT leaves the same state.                      |
| [Q86](#oop-and-designknowledge-base-) | B   | The server understood the request but refuses to allow it | 401 is for missing or bad authentication.                 |
| [Q87](#oop-and-designknowledge-base-) | A   | Resolve the host name with DNS                            | It needs the server's IP address.                         |
| [Q88](#oop-and-designknowledge-base-) | C   | 8 ms                                                      | 8000 bits / 10^6 bits per second.                         |
| [Q89](#oop-and-designknowledge-base-) | A   | CSMA/CA                                                   | Wireless stations cannot detect collisions while sending. |
| [Q90](#oop-and-designknowledge-base-) | B   | 65535                                                     | Ports are 16-bit fields.                                  |

Score: \_\_\_\_\_\_ / 30. Target 24 or more.

## Answer key: OOP and design

| Q               | Ans | Option                                                                    | Why                                                   |
|-----------------|-----|---------------------------------------------------------------------------|-------------------------------------------------------|
| [Q91](#c-output-predictionknowledge-base-)  | B   | Bundling data with the methods that use it and hiding internal state      | Access specifiers enforce it.                         |
| [Q92](#c-output-predictionknowledge-base-)  | B   | Virtual functions                                                         | Calls resolve through the vtable.                     |
| [Q93](#c-output-predictionknowledge-base-)  | A   | Function overloading and templates                                        | Resolved by the compiler.                             |
| [Q94](#c-output-predictionknowledge-base-)  | A   | At least one pure virtual function                                        | Declared as virtual f() = 0.                          |
| [Q95](#c-output-predictionknowledge-base-)  | A   | No                                                                        | You can have pointers or references to it.            |
| [Q96](#c-output-predictionknowledge-base-)  | B   | So deleting through a base pointer runs the derived destructor            | Otherwise behaviour is undefined.                     |
| [Q97](#c-output-predictionknowledge-base-)  | D   | Virtual inheritance                                                       | One shared base subobject.                            |
| [Q98](#c-output-predictionknowledge-base-)  | D   | private                                                                   | In a struct it is public.                             |
| [Q99](#c-output-predictionknowledge-base-)  | D   | private                                                                   | struct would default to public.                       |
| [Q100](#c-output-predictionknowledge-base-) | B   | A constructor                                                             | The object does not have a vptr yet.                  |
| [Q101](#c-output-predictionknowledge-base-) | D   | Passing by value would call the copy constructor again, recursing forever | Compilers reject by-value copy constructors.          |
| [Q102](#c-output-predictionknowledge-base-) | A   | Destructor, copy constructor, copy assignment                             | If you need one, you usually need all three.          |
| [Q103](#c-output-predictionknowledge-base-) | A   | A double free                                                             | Both objects delete the same memory.                  |
| [Q104](#c-output-predictionknowledge-base-) | C   | Can access private members but is not a member                            | Friendship is granted, not inherited.                 |
| [Q105](#c-output-predictionknowledge-base-) | A   | Shared by all objects of the class                                        | Defined once.                                         |
| [Q106](#c-output-predictionknowledge-base-) | A   | Not available                                                             | It is not tied to any object.                         |
| [Q107](#c-output-predictionknowledge-base-) | D   | Has the same signature as a virtual base function                         | Use override so the compiler checks.                  |
| [Q108](#c-output-predictionknowledge-base-) | B   | Liskov substitution                                                       | The L in SOLID.                                       |
| [Q109](#c-output-predictionknowledge-base-) | B   | Open/closed principle                                                     | Add new behaviour without editing tested code.        |
| [Q110](#c-output-predictionknowledge-base-) | C   | Abstractions                                                              | Both sides depend on interfaces.                      |
| [Q111](#c-output-predictionknowledge-base-) | D   | Prefer several small interfaces to one large one                          | Clients should not depend on methods they do not use. |
| [Q112](#c-output-predictionknowledge-base-) | C   | Composition                                                               | Inheritance models 'is-a'.                            |
| [Q113](#c-output-predictionknowledge-base-) | B   | ::                                                                        | Also . .\* ?: and sizeof.                             |
| [Q114](#c-output-predictionknowledge-base-) | B   | A class has one instance with a global access point                       | Often criticised for hidden global state.             |
| [Q115](#c-output-predictionknowledge-base-) | B   | Creates objects without the caller naming the concrete class              | Callers depend on an interface.                       |
| [Q116](#c-output-predictionknowledge-base-) | B   | Observer                                                                  | Publish and subscribe.                                |
| [Q117](#c-output-predictionknowledge-base-) | C   | In each object of a class with virtual functions                          | Each object points to its class's vtable.             |
| [Q118](#c-output-predictionknowledge-base-) | B   | A derived object is copied into a base object by value                    | The derived part is cut off.                          |
| [Q119](#c-output-predictionknowledge-base-) | B   | Prevents implicit conversions through it                                  | Stops surprises like f(42) building an object.        |
| [Q120](#c-output-predictionknowledge-base-) | C   | virtual void f() = 0;                                                     | The = 0 marks it pure.                                |

Score: \_\_\_\_\_\_ / 30. Target 24 or more.

## Answer key: C++ output prediction

| Q               | Ans | Option | Why                                                                                          |
|-----------------|-----|--------|----------------------------------------------------------------------------------------------|
| [Q121](#answer-key-operating-systems) | D   | 3 1    | Integer division truncates; 10 % 3 = 1.                                                      |
| [Q122](#answer-key-operating-systems) | B   | -3 -1  | Since C++11 division truncates toward zero and the remainder takes the sign of the dividend. |
| [Q123](#answer-key-operating-systems) | A   | 6      | r is another name for x.                                                                     |
| [Q124](#answer-key-operating-systems) | A   | C      | 'A' + 2 is 67, stored in a char, printed as a character.                                     |
| [Q125](#answer-key-operating-systems) | C   | 1      | Unsigned 0 − 1 wraps to the maximum value, which is \> 0.                                    |
| [Q126](#answer-key-operating-systems) | C   | 35     | \*(a + 2) is a\[2\] = 3; a\[4\] = 5.                                                         |
| [Q127](#answer-key-operating-systems) | C   | 4d     | Appending a char adds one to the size.                                                       |
| [Q128](#answer-key-operating-systems) | A   | D      | f is virtual, so the call uses the object's dynamic type.                                    |
| [Q129](#answer-key-operating-systems) | A   | B      | Without virtual, the static type B picks the function.                                       |
| [Q130](#answer-key-operating-systems) | C   | ab~b~a | Base is built first and destroyed last.                                                      |
| [Q131](#answer-key-operating-systems) | B   | B      | Passing by value slices D into a B.                                                          |
| [Q132](#answer-key-operating-systems) | D   | 123    | Since C++17 the operands of \<\< are evaluated left to right; the static keeps its value.    |
| [Q133](#answer-key-operating-systems) | B   | 5      | The loop body is the empty statement after the semicolon.                                    |
| [Q134](#answer-key-operating-systems) | D   | 3154   | 7 & 3 = 3, 7 \| 8 = 15, 5 ^ 1 = 4.                                                           |
| [Q135](#answer-key-operating-systems) | C   | 1024   | 1 shifted left 10 times is 2^10.                                                             |
| [Q136](#answer-key-operating-systems) | C   | 134    | erase(begin() + 1) removes the 2.                                                            |
| [Q137](#answer-key-operating-systems) | B   | a1b2c0 | map is sorted by key; m\["c"\] inserts a value-initialised 0.                                |
| [Q138](#answer-key-operating-systems) | B   | 31     | set keeps unique sorted values {1, 2, 3}.                                                    |
| [Q139](#answer-key-operating-systems) | D   | 7      | p points to a, so \*p += 2 changes a.                                                        |
| [Q140](#answer-key-operating-systems) | D   | 2.5    | One operand is double, so the division is floating point.                                    |
| [Q141](#answer-key-operating-systems) | A   | 3-3    | Casting to int truncates toward zero.                                                        |
| [Q142](#answer-key-operating-systems) | A   | 0      | 0.1 + 0.2 is not exactly 0.3 in binary floating point.                                       |
| [Q143](#answer-key-operating-systems) | A   | lle    | Reversed string is "olleh"; substr(1, 3) takes 3 chars from index 1.                         |
| [Q144](#answer-key-operating-systems) | A   | 1210   | A mutable lambda changes its own copy of x; the outer x stays 10.                            |
| [Q145](#answer-key-operating-systems) | C   | 12     | Captured by reference, so each call changes x.                                               |
| [Q146](#answer-key-operating-systems) | C   | int    | char to int is a promotion, which beats conversion to double.                                |
| [Q147](#answer-key-operating-systems) | C   | 43     | priority_queue is a max-heap by default.                                                     |
| [Q148](#answer-key-operating-systems) | C   | 2      | The first i++ yields 0 (false), the second yields 1 (true); i is now 2.                      |
| [Q149](#answer-key-operating-systems) | C   | ckc    | A b = a copies (k); c = b is assignment, not construction.                                   |
| [Q150](#answer-key-operating-systems) | B   | 1 3    | sizeof(char) is 1 by definition; the string "ab" has 3 bytes including '\0'.                 |

Score: \_\_\_\_\_\_ / 30. Target 24 or more.
