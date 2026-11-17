ROADMAP.SH · MAPPED TO YOUR PLAN

# roadmap.sh checklists

Six roadmap.sh maps that fit Path A, cut to what a fresher needs. Each topic shows where your kit already covers it (tap to open the Knowledge Base page) or marks it as a gap. 66 of 83 topics are covered; the gaps are listed in each section.

## Index

| Map                              | Why it matters                                                                              | Topics | Covered |
|----------------------------------|---------------------------------------------------------------------------------------------|--------|---------|
| [Backend](#backend-roadmapshbackend)               | Your SDE lane: what a backend developer is expected to know.                                | 23     | 15      |
| [Cyber Security](#cyber-security-roadmapshcyber-security)       | Your edge: where your 20-week lab track and TenantWall sit on the full map.                 | 16     | 13      |
| [AWS](#aws-roadmapshaws)                  | Your cloud lane and the SAA-C03 exam in the week of 19 Apr.                                 | 12     | 11      |
| [Computer Science](#computer-science-roadmapshcomputer-science)     | The Core CS and DSA side of every interview.                                                | 15     | 15      |
| [System Design](#system-design-roadmapshsystem-design)        | Light HLD for Big Tech, plus LLD for product companies.                                     | 11     | 10      |
| [DevOps (basics only)](#devops-basics-only-roadmapshdevops) | Not a target role, but these basics make your projects deployable and your resume stronger. | 6      | 2       |

Topic lists summarised from the public maps at [roadmap.sh](https://roadmap.sh) (Backend, Cyber Security, AWS, Computer Science, System Design, DevOps). Open each map for its full detail and resources. Knowledge Base links open the online version.

## Backend [roadmap.sh/backend](https://roadmap.sh/backend)

Your SDE lane: what a backend developer is expected to know.

### Internet and the web

|     |                                                     |                                                                              |
|-----|-----------------------------------------------------|------------------------------------------------------------------------------|
| ☐   | How the internet works, HTTP, DNS, domains, hosting | [Knowledge Base](knowledge-base/core-cs.md#what-happens-when-you-type-a-url) |
| ☐   | HTTPS and TLS                                       | [Knowledge Base](knowledge-base/core-cs.md#http-https-and-tls) |

### A language and its ecosystem

|     |                                                                                            |     |                                                                      |
|-----|--------------------------------------------------------------------------------------------|-----|----------------------------------------------------------------------|
| ☐   | One backend language in depth (your C++ plus one of Java, Go, Node or Python for web work) | Gap | Pick one for the backend project; C++ alone is uncommon for web APIs |
| ☐   | Package managers and project layout                                                        | Gap |                                                                      |

### Version control

|     |                                                  |     |                                |
|-----|--------------------------------------------------|-----|--------------------------------|
| ☐   | Git: branching, merging, rebasing, pull requests | Gap | Practise on your project repos |

### Databases

|     |                                               |                                                                                   |                                         |
|-----|-----------------------------------------------|-----------------------------------------------------------------------------------|-----------------------------------------|
| ☐   | Relational: SQL, schema design, normalisation | [Knowledge Base](knowledge-base/core-cs.md#normalisation-and-keys) |                                         |
| ☐   | Transactions, ACID, isolation                 | [Knowledge Base](knowledge-base/core-cs.md#transactions-acid-and-isolation)          |                                         |
| ☐   | Indexes and query plans                       | [Knowledge Base](knowledge-base/core-cs.md#indexing-and-b-trees)      |                                         |
| ☐   | NoSQL types and when to use them              | [Knowledge Base](knowledge-base/design.md#cap-theorem-and-consistency)           | Covered as SQL vs NoSQL in the DBMS Q&A |
| ☐   | ORMs and N+1 queries                          | Gap                                                                               |                                         |

### APIs

|     |                                             |                                                                              |                                        |
|-----|---------------------------------------------|------------------------------------------------------------------------------|----------------------------------------|
| ☐   | REST design and status codes                | [Knowledge Base](knowledge-base/core-cs.md#http-https-and-tls) |                                        |
| ☐   | Authentication: sessions, JWT, OAuth basics | [Knowledge Base](knowledge-base/security.md#cross-site-scripting-xss-and-csrf)      | JWT used in the plan's backend project |
| ☐   | GraphQL and gRPC (awareness)                | Gap                                                                          |                                        |

### Caching and scaling

|     |                                       |                                                                                    |
|-----|---------------------------------------|------------------------------------------------------------------------------------|
| ☐   | Caching: cache-aside, Redis, CDN      | [Knowledge Base](knowledge-base/design.md#caching-and-cdns)        |
| ☐   | Load balancing, replication, sharding | [Knowledge Base](knowledge-base/design.md#load-balancing-replication-and-sharding) |
| ☐   | Message queues                        | [Knowledge Base](knowledge-base/design.md#high-level-system-design-hld)            |

### Testing and security

|     |                              |                                                                                   |                                     |
|-----|------------------------------|-----------------------------------------------------------------------------------|-------------------------------------|
| ☐   | Unit and integration tests   | Gap                                                                               | Write tests for the backend project |
| ☐   | Web security: OWASP Top 10   | [Knowledge Base](knowledge-base/security.md#owasp-top-10)         |                                     |
| ☐   | Hashing and password storage | [Knowledge Base](knowledge-base/security.md#hashing-encryption-and-passwords) |                                     |

### Deploying

|     |                            |                                                                              |                                                      |
|-----|----------------------------|------------------------------------------------------------------------------|------------------------------------------------------|
| ☐   | Linux basics and the shell | [Knowledge Base](knowledge-base/security.md#ctfs-and-security-labs)      | Bandit levels in the cyber track                     |
| ☐   | Containers (Docker) basics | Gap                                                                          | Gap: one evening to containerise the backend project |
| ☐   | CI/CD basics               | Gap                                                                          | Gap: a GitHub Actions workflow that runs your tests  |
| ☐   | Cloud deployment           | [Knowledge Base](knowledge-base/cloud.md#aws-core-services-and-the-saa-c03-exam) |                                                      |

## Cyber Security [roadmap.sh/cyber-security](https://roadmap.sh/cyber-security)

Your edge: where your 20-week lab track and TenantWall sit on the full map.

### Fundamentals

|     |                                              |                                                                                    |                             |
|-----|----------------------------------------------|------------------------------------------------------------------------------------|-----------------------------|
| ☐   | Networking: OSI, TCP/IP, ports and protocols | [Knowledge Base](knowledge-base/core-cs.md#osi-and-tcpip-models)      |                             |
| ☐   | Operating systems: Linux and Windows basics  | [Knowledge Base](knowledge-base/core-cs.md#processes-and-threads) | Windows internals are a gap |
| ☐   | Common tools: nmap, Wireshark, Burp Suite    | [Knowledge Base](knowledge-base/security.md#ctfs-and-security-labs)            | Lab weeks 3 to 6            |

### Security concepts

|     |                                                   |                                                                                      |
|-----|---------------------------------------------------|--------------------------------------------------------------------------------------|
| ☐   | CIA triad, AAA, least privilege                   | [Knowledge Base](knowledge-base/cloud.md#aws-iam-and-least-privilege)              |
| ☐   | Cryptography: hashing, symmetric, asymmetric, PKI | [Knowledge Base](knowledge-base/security.md#hashing-encryption-and-passwords)    |
| ☐   | Threat modelling                                  | [Knowledge Base](knowledge-base/security.md#threat-modelling-stride) |

### Web and application security

|     |                                                |                                                                           |                  |
|-----|------------------------------------------------|---------------------------------------------------------------------------|------------------|
| ☐   | OWASP Top 10                                   | [Knowledge Base](knowledge-base/security.md#owasp-top-10) |                  |
| ☐   | SQL injection, XSS, CSRF, SSRF, access control | [Knowledge Base](knowledge-base/security.md#sql-injection)  | PortSwigger labs |

### Cloud security

|     |                                                 |                                                                                |            |
|-----|-------------------------------------------------|--------------------------------------------------------------------------------|------------|
| ☐   | IAM, policies, ABAC                             | [Knowledge Base](knowledge-base/cloud.md#abac-attribute-based-access-control)       | TenantWall |
| ☐   | Logging and monitoring (CloudTrail, CloudWatch) | [Knowledge Base](knowledge-base/cloud.md#cloudtrail-and-cloudwatch-alarms) | TenantWall |

### Offensive basics

|     |                            |                                                                                         |                      |
|-----|----------------------------|-----------------------------------------------------------------------------------------|----------------------|
| ☐   | CTFs                       | [Knowledge Base](knowledge-base/security.md#ctfs-and-security-labs)                 |                      |
| ☐   | Binary exploitation basics | [Knowledge Base](knowledge-base/security.md#binary-exploitation-basics) | Binary taster in May |
| ☐   | Bug bounty and disclosure  | [Knowledge Base](knowledge-base/security.md#bug-bounty-and-responsible-disclosure)          |                      |

### Defensive basics

|     |                                       |     |                    |
|-----|---------------------------------------|-----|--------------------|
| ☐   | SIEM, log analysis, incident response | Gap | Lab weeks 15 to 17 |
| ☐   | MITRE ATT&CK                          | Gap | Lab week 16        |

### Certifications (optional)

|     |                           |     |                                                 |
|-----|---------------------------|-----|-------------------------------------------------|
| ☐   | CompTIA Security+ or eJPT | Gap | Listed in many fresher job posts; after AWS SAA |

## AWS [roadmap.sh/aws](https://roadmap.sh/aws)

Your cloud lane and the SAA-C03 exam in the week of 19 Apr.

### Core services

|     |                                             |                                                                              |
|-----|---------------------------------------------|------------------------------------------------------------------------------|
| ☐   | IAM                                         | [Knowledge Base](knowledge-base/cloud.md#aws-iam-and-least-privilege)      |
| ☐   | EC2, Auto Scaling, load balancers           | [Knowledge Base](knowledge-base/cloud.md#aws-core-services-and-the-saa-c03-exam) |
| ☐   | S3 and storage classes                      | [Knowledge Base](knowledge-base/cloud.md#aws-core-services-and-the-saa-c03-exam) |
| ☐   | VPC: subnets, routing, NAT, security groups | [Knowledge Base](knowledge-base/cloud.md#aws-core-services-and-the-saa-c03-exam) |
| ☐   | RDS, DynamoDB                               | [Knowledge Base](knowledge-base/cloud.md#aws-core-services-and-the-saa-c03-exam) |

### Integration and serverless

|     |                        |                                                                              |
|-----|------------------------|------------------------------------------------------------------------------|
| ☐   | SQS, SNS               | [Knowledge Base](knowledge-base/cloud.md#aws-core-services-and-the-saa-c03-exam) |
| ☐   | Lambda and API Gateway | [Knowledge Base](knowledge-base/cloud.md#aws-core-services-and-the-saa-c03-exam) |

### Operations and security

|     |                                    |                                                                                |                         |
|-----|------------------------------------|--------------------------------------------------------------------------------|-------------------------|
| ☐   | CloudWatch and CloudTrail          | [Knowledge Base](knowledge-base/cloud.md#cloudtrail-and-cloudwatch-alarms) |                         |
| ☐   | KMS and encryption                 | [Knowledge Base](knowledge-base/cloud.md#aws-core-services-and-the-saa-c03-exam)   |                         |
| ☐   | Cost management and billing alarms | [Knowledge Base](knowledge-base/cloud.md#aws-core-services-and-the-saa-c03-exam)   | Week 1 of the AWS track |

### Architecture

|     |                                         |                                                                                    |                                       |
|-----|-----------------------------------------|------------------------------------------------------------------------------------|---------------------------------------|
| ☐   | Well-Architected Framework              | Gap                                                                                | Read its six pillars before exam prep |
| ☐   | High availability and disaster recovery | [Knowledge Base](knowledge-base/design.md#load-balancing-replication-and-sharding) |                                       |

## Computer Science [roadmap.sh/computer-science](https://roadmap.sh/computer-science)

The Core CS and DSA side of every interview.

### Data structures

|     |                                                   |                                                                             |
|-----|---------------------------------------------------|-----------------------------------------------------------------------------|
| ☐   | Arrays, linked lists, stacks, queues, hash tables | [Knowledge Base](knowledge-base/dsa.md#hashing-and-frequency-maps) |
| ☐   | Trees, BST, heaps, tries                          | [Knowledge Base](knowledge-base/dsa.md#binary-trees)   |
| ☐   | Graphs                                            | [Knowledge Base](knowledge-base/dsa.md#bfs-and-graph-basics)     |

### Algorithms

|     |                                     |                                                                                   |
|-----|-------------------------------------|-----------------------------------------------------------------------------------|
| ☐   | Complexity and Big-O                | [Knowledge Base](knowledge-base/dsa.md#time-and-space-complexity)    |
| ☐   | Sorting and searching               | [Knowledge Base](knowledge-base/dsa.md#binary-search) |
| ☐   | Recursion, backtracking, greedy, DP | [Knowledge Base](knowledge-base/dsa.md#dynamic-programming)            |
| ☐   | Graph algorithms                    | [Knowledge Base](knowledge-base/dsa.md#dijkstra-and-shortest-paths)      |
| ☐   | String algorithms                   | [Knowledge Base](knowledge-base/dsa.md#string-algorithms-kmp-z-hashing)  |

### Systems

|     |                                          |                                                                                    |
|-----|------------------------------------------|------------------------------------------------------------------------------------|
| ☐   | Processes, threads, scheduling, deadlock | [Knowledge Base](knowledge-base/core-cs.md#processes-and-threads) |
| ☐   | Memory and virtual memory                | [Knowledge Base](knowledge-base/core-cs.md#memory-management-and-virtual-memory) |
| ☐   | Networking                               | [Knowledge Base](knowledge-base/core-cs.md#tcp-vs-udp-and-the-handshake)        |
| ☐   | Databases                                | [Knowledge Base](knowledge-base/core-cs.md#transactions-acid-and-isolation)           |

### Design

|     |                      |                                                                           |
|-----|----------------------|---------------------------------------------------------------------------|
| ☐   | OOP and SOLID        | [Knowledge Base](knowledge-base/core-cs.md#oop-the-four-pillars)   |
| ☐   | Design patterns      | [Knowledge Base](knowledge-base/core-cs.md#solid-and-design-patterns) |
| ☐   | System design basics | [Knowledge Base](knowledge-base/design.md#high-level-system-design-hld)   |

## System Design [roadmap.sh/system-design](https://roadmap.sh/system-design)

Light HLD for Big Tech, plus LLD for product companies.

### Fundamentals

|     |                                                   |                                                                                    |
|-----|---------------------------------------------------|------------------------------------------------------------------------------------|
| ☐   | Performance vs scalability, latency vs throughput | [Knowledge Base](knowledge-base/design.md#high-level-system-design-hld)            |
| ☐   | CAP and consistency patterns                      | [Knowledge Base](knowledge-base/design.md#cap-theorem-and-consistency)            |
| ☐   | Availability patterns: fail-over, replication     | [Knowledge Base](knowledge-base/design.md#load-balancing-replication-and-sharding) |

### Building blocks

|     |                                              |                                                                                    |                  |
|-----|----------------------------------------------|------------------------------------------------------------------------------------|------------------|
| ☐   | DNS, CDN, load balancers, reverse proxies    | [Knowledge Base](knowledge-base/core-cs.md#what-happens-when-you-type-a-url)       |                  |
| ☐   | Databases: SQL, NoSQL, sharding, replication | [Knowledge Base](knowledge-base/design.md#load-balancing-replication-and-sharding) |                  |
| ☐   | Caching                                      | [Knowledge Base](knowledge-base/design.md#caching-and-cdns)        |                  |
| ☐   | Queues and asynchronism                      | [Knowledge Base](knowledge-base/design.md#high-level-system-design-hld)            |                  |
| ☐   | Rate limiting                                | [Knowledge Base](knowledge-base/design.md#high-level-system-design-hld)            | Mock 7 deep dive |

### Practice

|     |                                           |                                                                            |                                     |
|-----|-------------------------------------------|----------------------------------------------------------------------------|-------------------------------------|
| ☐   | URL shortener                             | [Knowledge Base](knowledge-base/mocks.md#mock-7-system-design-url-shortener) |                                     |
| ☐   | Parking lot (LLD)                         | [Knowledge Base](knowledge-base/mocks.md#mock-6-low-level-design-parking-lot) |                                     |
| ☐   | Chat app, news feed, notification service | Gap                                                                        | Gap: two more designs in the sprint |

## DevOps (basics only) [roadmap.sh/devops](https://roadmap.sh/devops)

Not a target role, but these basics make your projects deployable and your resume stronger.

### Basics worth one week each

|     |                                        |                                                                                |     |
|-----|----------------------------------------|--------------------------------------------------------------------------------|-----|
| ☐   | Linux command line and shell scripting | [Knowledge Base](knowledge-base/security.md#ctfs-and-security-labs)        |     |
| ☐   | Git and GitHub workflows               | Gap                                                                            |     |
| ☐   | Docker basics                          | Gap                                                                            | Gap |
| ☐   | CI/CD with GitHub Actions              | Gap                                                                            | Gap |
| ☐   | Monitoring basics                      | [Knowledge Base](knowledge-base/cloud.md#cloudtrail-and-cloudwatch-alarms) |     |

### Skip for now

|     |                                       |     |                                              |
|-----|---------------------------------------|-----|----------------------------------------------|
| ☐   | Kubernetes, Terraform, service meshes | Gap | Not needed for fresher SDE or security roles |
