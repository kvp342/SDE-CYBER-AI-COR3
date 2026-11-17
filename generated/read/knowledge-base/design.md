# Design

[All categories](README.md) · 5 topics

## Topics

- [Low-level design (LLD)](#low-level-design-lld)
- [High-level system design (HLD)](#high-level-system-design-hld)
- [Caching and CDNs](#caching-and-cdns)
- [Load balancing, replication and sharding](#load-balancing-replication-and-sharding)
- [CAP theorem and consistency](#cap-theorem-and-consistency)

## Low-level design (LLD)

*Level 1: Core*

Freshers at product companies get LLD more often than HLD. Flipkart, Swiggy, Atlassian and others run a machine-coding or LLD round.

**Key idea**

Process: clarify requirements and scope (5 min) → list entities (nouns) and behaviours (verbs) → define classes, fields and relationships → key interfaces → walk through one flow → discuss extensions, concurrency and patterns used.

Practise: parking lot, library management, Splitwise, elevator, snake and ladder, BookMyShow, rate limiter, LRU cache, vending machine.


**Points**

- Draw a class diagram first
- Use enums for states and types
- Mention thread safety where shared state exists
- Machine-coding rounds want runnable, clean code in 60–90 min

**Traps**

- Starting to code before agreeing on requirements
- God classes that do everything

**Interviewers ask**

- Design a parking lot.
- Design Splitwise.
- Design an elevator system.

**Learn more**

- [awesome-low-level-design](https://github.com/ashishps1/awesome-low-level-design)
- [Refactoring.Guru](https://refactoring.guru/design-patterns)

**Related:** [SOLID and design patterns](core-cs.md#solid-and-design-patterns) · [OOP: the four pillars](core-cs.md#oop-the-four-pillars) · [High-level system design (HLD)](#high-level-system-design-hld)

[Back to the topic list](#topics)

## High-level system design (HLD)

*Level 2: Interview-ready*

Big Tech asks light HLD even for new grads; a clear design discussion lifts you above candidates who only grind DSA. Your AWS SAA prep covers half of it.

**Key idea**

Framework: requirements (functional + non-functional: scale, latency, availability) → back-of-envelope numbers (QPS, storage) → API → data model → high-level diagram → deep dive on the bottleneck → trade-offs.

Building blocks: load balancer, stateless app servers, cache (Redis), CDN, SQL vs NoSQL, replication, sharding, message queues (SQS/Kafka), object storage (S3), rate limiter, search index.

Starter designs: URL shortener, pastebin, rate limiter, chat app, news feed, notification service.


**Points**

- 1 day ≈ 10⁵ seconds; 1M requests/day ≈ 12 QPS
- Read-heavy → cache + replicas; write-heavy → sharding + queues
- State the trade-off you chose and why

**Traps**

- Jumping to microservices for a simple system
- No numbers

**Interviewers ask**

- Design a URL shortener.
- How would you scale it to 100× traffic?

**Learn more**

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [roadmap.sh system design](https://roadmap.sh/system-design)
- [ByteByteGo blog (free posts)](https://blog.bytebytego.com)

**Related:** [Caching and CDNs](#caching-and-cdns) · [CAP theorem and consistency](#cap-theorem-and-consistency) · [Load balancing, replication and sharding](#load-balancing-replication-and-sharding) · [Low-level design (LLD)](#low-level-design-lld)

[Back to the topic list](#topics)

## Caching and CDNs

*Level 2: Interview-ready*

The first scaling answer in any design question, and it links to LRU (a DSA favourite).

**Key idea**

A cache keeps hot data in fast storage. Patterns: cache-aside (app reads cache, falls back to DB and fills cache), write-through (write cache and DB together), write-back (write cache, flush later).

Eviction: LRU, LFU, TTL. Invalidation is the hard part: set TTLs, delete on write, version keys.

A CDN caches static (and some dynamic) content at edge locations close to users (CloudFront on AWS).


**Points**

- Cache stampede: many misses at once; use locking or early refresh
- Hit ratio is the metric
- LRU = hash map + doubly linked list

**Traps**

- Caching data that must be strongly consistent without a plan

**Interviewers ask**

- How would you add caching to this system?
- How do you keep the cache consistent?

**Learn more**

- [System Design Primer: cache](https://github.com/donnemartin/system-design-primer#cache)

**Related:** [High-level system design (HLD)](#high-level-system-design-hld) · [Linked lists](dsa.md#linked-lists)

[Back to the topic list](#topics)

## Load balancing, replication and sharding

*Level 2: Interview-ready*

Core scaling vocabulary for HLD rounds and AWS SAA.

**Key idea**

A load balancer spreads requests across servers (round robin, least connections, consistent hashing) and removes unhealthy ones via health checks. L4 balances by IP/port, L7 by HTTP content.

Replication copies data to more nodes for read scaling and availability (leader-follower; replication lag means followers can be stale). Sharding splits data across nodes by a key for write scaling; choose a key that spreads load evenly and avoids cross-shard queries.

Consistent hashing keeps most keys in place when nodes join or leave.


**Points**

- AWS: ALB (L7), NLB (L4), Auto Scaling groups, RDS read replicas, DynamoDB partitions
- Hot shard problem: celebrity users

**Traps**

- Sharding before trying caching and replicas

**Interviewers ask**

- How would you shard a users table?
- What is consistent hashing?

**Learn more**

- [System Design Primer](https://github.com/donnemartin/system-design-primer)

**Related:** [High-level system design (HLD)](#high-level-system-design-hld) · [CAP theorem and consistency](#cap-theorem-and-consistency) · [AWS core services and the SAA-C03 exam](cloud.md#aws-core-services-and-the-saa-c03-exam)

[Back to the topic list](#topics)

## CAP theorem and consistency

*Level 3: Advanced*

An L3 depth question that shows you understand distributed trade-offs.

**Key idea**

During a network partition, a distributed store must choose between consistency (every read sees the latest write) and availability (every request gets a response). PACELC adds: Else, when there's no partition, choose between latency and consistency.

Consistency models range from strong (linearisable) to eventual. Banking ledgers lean to consistency; social feeds lean to availability.


**Points**

- Quorums: R + W \> N gives read-your-writes
- Idempotency keys make retries safe (payments)

**Traps**

- Saying a system can 'pick two' outside partitions

**Interviewers ask**

- Explain CAP with an example.
- How do you make a payment API safe to retry?

**Learn more**

- [Designing Data-Intensive Applications (book)](https://dataintensive.net)

**Related:** [High-level system design (HLD)](#high-level-system-design-hld) · [Transactions, ACID and isolation](core-cs.md#transactions-acid-and-isolation)

[Back to the topic list](#topics)
