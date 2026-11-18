CLOUD SOLUTIONS ARCHITECT · 2 HOURS A DAY

# Solutions Architect 10 plan weeks, now 1 hour a day

A day-by-day plan for the Cloud Solutions Architect course (AWS SAA-C03): one fixed 2-hour routine, a topic for every day, a lab every Saturday, a review every Sunday, the rules the exam keeps testing, and checkpoints that tell you when to book the exam.

| Section                                                     |
|-------------------------------------------------------------|
| [1. What this plan is](#01-what-this-plan-is)                             |
| [2. Your dates at 1 hour a day (current routine)](#02-your-dates-at-1-hour-a-day-current-routine)  |
| [3. The 2-hour routine (every day)](#03-the-2-hour-routine-every-day)                |
| [4. Day by day, weeks 0–5](#04-day-by-day-weeks-05)                         |
| [5. Day by day, weeks 6–10](#05-day-by-day-weeks-610)                        |
| [6. Each week's exam rules (learn these by heart)](#06-each-weeks-exam-rules-learn-these-by-heart) |
| [7. Checkpoints and how to know you are ready](#07-checkpoints-and-how-to-know-you-are-ready)     |
| [Sources (6)](#-sources)                                     |

Day 1 is Wed 18 Nov 2026 (a 5-day start-up); week 1 starts Mon 23 Nov. Missed a day? Do not double up: move the rest of the table by one day and keep going.

## 01. What this plan is

- **Course assumed:** AWS Certified Solutions Architect – Associate (exam code SAA-C03). If your sir's course is a different one, keep the daily routine and swap the weekly topics for his modules.^([\[1\]](#-sources))
- **Length:** written as 10 weeks at 2 hours a day (the tables below); at your current 1 hour a day it runs to about 25 Feb 2027 (Section 2). Original 2-hour dates: Wed 18 Nov 2026 to Sun 31 Jan 2027. A 5-day start-up (W0), then weeks 1–9 (Monday to Sunday) teach the four exam domains; week 10 is practice.
- **Exam:** 65 questions (50 scored, 15 unscored), 130 minutes, pass mark 720 on a scale of 100–1000. Domains: Secure 30%, Resilient 26%, High-performing 24%, Cost-optimised 20%.^([\[2\]](#-sources))
- **Your other files:** notes and 60 practice questions are in [the SAA-C03 study pack](aws-saa-c03-study-pack.md); the hands-on labs are in [the AWS lab workbook](aws-lab-workbook.md); your own project is explained in [TenantWall explained](tenantwall-explained.md).
- **Fit with the final plan:** the final plan gives AWS 30 min/day and books the exam for the week of 19 April. Your 1 hour a day replaces that slot until about 25 February. If you then score 80% or more twice, book the exam for early March; otherwise keep 19 April.

## 02. Your dates at 1 hour a day (current routine)

Your routine is now **1 hour of cloud every day**, next to DSA and Core CS. Use the same topics and labs; each plan week simply takes two calendar weeks.

| Plan weeks                    | Dates                        | How                                                                                   |
|-------------------------------|------------------------------|---------------------------------------------------------------------------------------|
| W0–W3 + start of W4           | Thu 19 Nov 2026              | One long day (about 10 h): start-up, IAM, compute, networking, S3 basics              |
| W4: Storage                   | Fri 20 Nov – Thu 03 Dec 2026 | Each 2-hour plan day becomes two 1-hour days: day A = Learn + Do, day B = Do + Recall |
| W5: Databases                 | Fri 04 Dec – Thu 17 Dec 2026 | Each 2-hour plan day becomes two 1-hour days: day A = Learn + Do, day B = Do + Recall |
| W6: Resilience and scaling    | Fri 18 Dec – Thu 31 Dec 2026 | Each 2-hour plan day becomes two 1-hour days: day A = Learn + Do, day B = Do + Recall |
| W7: Decoupling and serverless | Fri 01 Jan – Thu 14 Jan 2027 | Each 2-hour plan day becomes two 1-hour days: day A = Learn + Do, day B = Do + Recall |
| W8: Security and monitoring   | Fri 15 Jan – Thu 28 Jan 2027 | Each 2-hour plan day becomes two 1-hour days: day A = Learn + Do, day B = Do + Recall |
| W9: Performance and cost      | Fri 29 Jan – Thu 11 Feb 2027 | Each 2-hour plan day becomes two 1-hour days: day A = Learn + Do, day B = Do + Recall |
| W10: Exam practice            | Fri 12 Feb – Thu 25 Feb 2027 | Each 2-hour plan day becomes two 1-hour days: day A = Learn + Do, day B = Do + Recall |

**Finish:** about 25 Feb 2027. **Exam:** if two full practice sets score 80%+, book it for early March, before your college exams (22 Mar – 7 Apr); otherwise book the week of 19 April. The day-by-day tables on the next pages still list the topics in order; follow them at this pace.

## 03. The 2-hour routine (every day)

| Block      | Time   | What you do                                                                                                                                                                                                     |
|------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1\. Learn  | 50 min | Your sir's lecture or the matching AWS Skill Builder module, then the AWS FAQ page for that day's service. Write one-line notes: what it is, when to choose it, one limit.^([\[3\]](#-sources)[\[4\]](#-sources)) |
| 2\. Do     | 50 min | Weekdays: build it in the console or CLI (Free Tier) or draw the architecture on paper; then 5 practice questions on the topic. Saturday: one full lab.^([\[5\]](#-sources))                                     |
| 3\. Recall | 20 min | Close the notes and write the day's topic from memory; turn every mistake into an Anki card; tick the day in the table.                                                                                         |

**Cost rule:** set the budget alert on day 1 (lab 1), and on every lab day delete what you created before you stop. NAT gateways, load balancers, RDS and unattached Elastic IPs bill by the hour.

### Weekly shape

- Mon–Fri: the five topics of the week.
- Saturday: the week's lab from the lab workbook (2 hours).
- Sunday: review, the week's three exam rules, and missed questions.

## 04. Day by day, weeks 0–5

| Date       | Week | Topic (2 hours)                                                                                                                 |
|------------|------|---------------------------------------------------------------------------------------------------------------------------------|
| Wed 18 Nov | W0   | **Start-up:** secure the account: MFA on the root user, an admin IAM user, and the budget alert (lab 1 in the AWS lab workbook) |
| Thu 19 Nov | W0   | Read the SAA-C03 exam guide: the four domains and the task statements; skim the list of in-scope services                       |
| Fri 20 Nov | W0   | Install and configure the AWS CLI with the admin profile; run aws sts get-caller-identity; Free Tier limits                     |
| Sat 21 Nov | W0   | **Lab:** nothing new to build: re-read sections 1–4 of TenantWall explained (IAM and policies)                                  |
| Sun 22 Nov | W0   | **Review:** plan the 10 weeks; put the 2-hour slot in your calendar every day                                                   |
| Mon 23 Nov | W1   | Global infrastructure: Regions, Availability Zones, edge locations; shared responsibility model; the console, CLI and SDKs      |
| Tue 24 Nov | W1   | IAM users, groups, roles; access keys vs temporary credentials; MFA; root user rules                                            |
| Wed 25 Nov | W1   | Policies: identity vs resource-based, JSON elements, evaluation logic (explicit deny \> allow \> implicit deny)                 |
| Thu 26 Nov | W1   | Organizations, SCPs, permission boundaries, IAM Identity Center, cross-account roles with STS AssumeRole                        |
| Fri 27 Nov | W1   | Re-read the IAM parts of TenantWall explained: ABAC, condition keys, policy variables, Access Analyzer                          |
| Sat 28 Nov | W1   | **Lab:** IAM: an admin group and a role for EC2 (lab 2) in the AWS lab workbook; delete everything after                        |
| Sun 29 Nov | W1   | **Review:** recall test on this week's three exam rules, redo the week's missed questions, plan next week                       |
| Mon 30 Nov | W2   | EC2 instance families, sizing, AMIs, user data, instance metadata (IMDSv2)                                                      |
| Tue 01 Dec | W2   | Purchase options: On-Demand, Savings Plans, Reserved Instances, Spot, Dedicated Hosts/Instances                                 |
| Wed 02 Dec | W2   | Block storage: EBS volume types (gp3, io2, st1, sc1), snapshots, instance store; EFS for shared files                           |
| Thu 03 Dec | W2   | Placement groups (cluster, spread, partition), ENI, Elastic IP, hibernation                                                     |
| Fri 04 Dec | W2   | Lambda basics, containers on ECS/EKS/Fargate, Elastic Beanstalk: when to choose each                                            |
| Sat 05 Dec | W2   | **Lab:** EC2 with a security group, a role and IMDSv2 (lab 5) in the AWS lab workbook; delete everything after                  |
| Sun 06 Dec | W2   | **Review:** recall test on this week's three exam rules, redo the week's missed questions, plan next week                       |
| Mon 07 Dec | W3   | VPC, CIDR, subnets, route tables, Internet Gateway; public vs private subnets                                                   |
| Tue 08 Dec | W3   | NAT gateway; security groups (stateful, allow only) vs network ACLs (stateless, allow and deny)                                 |
| Wed 09 Dec | W3   | VPC endpoints: gateway (S3, DynamoDB) vs interface (PrivateLink); VPC Flow Logs                                                 |
| Thu 10 Dec | W3   | VPC peering (not transitive), Transit Gateway, Site-to-Site VPN, Direct Connect                                                 |
| Fri 11 Dec | W3   | Route 53 basics: hosted zones, records, alias records                                                                           |
| Sat 12 Dec | W3   | **Lab:** VPC with public and private subnets (lab 4) in the AWS lab workbook; delete everything after                           |
| Sun 13 Dec | W3   | **Review:** recall test on this week's three exam rules, redo the week's missed questions, plan next week                       |
| Mon 14 Dec | W4   | S3 basics: buckets, objects, keys, prefixes, consistency, versioning, presigned URLs                                            |
| Tue 15 Dec | W4   | Storage classes (Standard, Intelligent-Tiering, Standard-IA, One Zone-IA, Glacier tiers) and lifecycle rules                    |
| Wed 16 Dec | W4   | S3 security: Block Public Access, bucket policies, encryption (SSE-S3, SSE-KMS, client-side), Object Lock                       |
| Thu 17 Dec | W4   | Replication (CRR/SRR), Transfer Acceleration, multipart upload, S3 event notifications                                          |
| Fri 18 Dec | W4   | FSx, Storage Gateway, DataSync, Snow family, AWS Backup                                                                         |
| Sat 19 Dec | W4   | **Lab:** Private S3 bucket with versioning and encryption (lab 3) in the AWS lab workbook; delete everything after              |
| Sun 20 Dec | W4   | **Review:** recall test on this week's three exam rules, redo the week's missed questions, plan next week                       |
| Mon 21 Dec | W5   | RDS engines, Multi-AZ (availability) vs read replicas (read scaling), backups and snapshots                                     |
| Tue 22 Dec | W5   | Aurora: storage model, replicas, Aurora Serverless, Global Database                                                             |
| Wed 23 Dec | W5   | DynamoDB: partition and sort keys, capacity modes, GSI/LSI, Streams, TTL, global tables                                         |
| Thu 24 Dec | W5   | ElastiCache (Redis/Memcached) and DAX: caching patterns                                                                         |
| Fri 25 Dec | W5   | Redshift, Athena and other purpose-built databases: which question words point to which                                         |
| Sat 26 Dec | W5   | **Lab:** Private RDS MySQL database (lab 7) in the AWS lab workbook; delete everything after                                    |
| Sun 27 Dec | W5   | **Review:** recall test on this week's three exam rules, redo the week's missed questions, plan next week                       |

## 05. Day by day, weeks 6–10

| Date       | Week | Topic (2 hours)                                                                                               |
|------------|------|---------------------------------------------------------------------------------------------------------------|
| Mon 28 Dec | W6   | Elastic Load Balancing: ALB (HTTP, path/host rules), NLB (TCP/UDP, static IP), GWLB                           |
| Tue 29 Dec | W6   | Auto Scaling groups: launch templates, health checks, scaling policies (target tracking, step, scheduled)     |
| Wed 30 Dec | W6   | Route 53 routing policies: simple, weighted, latency, failover, geolocation, multivalue; health checks        |
| Thu 31 Dec | W6   | Disaster recovery: backup and restore, pilot light, warm standby, multi-site active-active; RPO and RTO       |
| Fri 01 Jan | W6   | Design a three-tier web app across two AZs on paper; check each tier for a single point of failure            |
| Sat 02 Jan | W6   | **Lab:** Load balancer + Auto Scaling across two AZs (lab 6) in the AWS lab workbook; delete everything after |
| Sun 03 Jan | W6   | **Review:** recall test on this week's three exam rules, redo the week's missed questions, plan next week     |
| Mon 04 Jan | W7   | SQS: standard vs FIFO, visibility timeout, dead-letter queues, long polling                                   |
| Tue 05 Jan | W7   | SNS topics and fan-out (SNS to several SQS queues); EventBridge rules and buses                               |
| Wed 06 Jan | W7   | API Gateway + Lambda: limits, concurrency, cold starts; Step Functions for workflows                          |
| Thu 07 Jan | W7   | Streaming: Kinesis Data Streams vs Data Firehose; when SQS is enough                                          |
| Fri 08 Jan | W7   | Re-architect a monolith on paper into queue-based services; mark where each service fits                      |
| Sat 09 Jan | W7   | **Lab:** Lambda behind an HTTP API (lab 8) in the AWS lab workbook; delete everything after                   |
| Sun 10 Jan | W7   | **Review:** recall test on this week's three exam rules, redo the week's missed questions, plan next week     |
| Mon 11 Jan | W8   | KMS (keys, key policies, envelope encryption), CloudHSM, ACM certificates                                     |
| Tue 12 Jan | W8   | Secrets Manager vs Systems Manager Parameter Store; WAF, Shield, Firewall Manager                             |
| Wed 13 Jan | W8   | GuardDuty, Inspector, Macie, Security Hub, Detective: what each one finds                                     |
| Thu 14 Jan | W8   | CloudTrail (management vs data events), CloudWatch metrics, logs, alarms; AWS Config rules                    |
| Fri 15 Jan | W8   | TenantWall explained: walk through your own CloudTrail, metric filters, alarms and SNS from memory            |
| Sat 16 Jan | W8   | **Lab:** CloudTrail + root-activity alarm, KMS (labs 9–10) in the AWS lab workbook; delete everything after   |
| Sun 17 Jan | W8   | **Review:** recall test on this week's three exam rules, redo the week's missed questions, plan next week     |
| Mon 18 Jan | W9   | CloudFront (caching, origins, OAC) vs Global Accelerator; caching at every layer                              |
| Tue 19 Jan | W9   | Analytics: Athena, Glue, EMR, Kinesis, QuickSight, Lake Formation; when each fits                             |
| Wed 20 Jan | W9   | Pricing: Savings Plans vs RIs vs Spot; S3 class costs; data transfer costs; NAT gateway costs                 |
| Thu 21 Jan | W9   | Cost tools: Cost Explorer, Budgets, Cost and Usage Report, Compute Optimizer, Trusted Advisor                 |
| Fri 22 Jan | W9   | Well-Architected: the six pillars and the questions each asks                                                 |
| Sat 23 Jan | W9   | **Lab:** Teardown checklist and cost check (lab 11) in the AWS lab workbook; delete everything after          |
| Sun 24 Jan | W9   | **Review:** recall test on this week's three exam rules, redo the week's missed questions, plan next week     |
| Mon 25 Jan | W10  | Practice set 1: questions 1–30 of your SAA-C03 study pack, timed (60 min); log every miss                     |
| Tue 26 Jan | W10  | Re-read notes for each missed topic in the docs and FAQs                                                      |
| Wed 27 Jan | W10  | Practice set 2: questions 31–60 of the study pack, timed                                                      |
| Thu 28 Jan | W10  | Official sample questions and the free Skill Builder practice question set                                    |
| Fri 29 Jan | W10  | Weak-area day: redo all missed questions; rewrite the 'which service' table from memory                       |
| Sat 30 Jan | W10  | **Full mock:** 65 questions in 130 minutes (all 60 pack questions + 5 official samples)                       |
| Sun 31 Jan | W10  | **Decide:** score 80%+ twice → book the exam; else repeat weeks 8–10 practice                                 |

## 06. Each week's exam rules (learn these by heart)

| Week | Topic                     | Rules the exam keeps testing                                                                                                                                                                                                                       |
|------|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| W1   | Cloud basics and IAM      | An explicit Deny anywhere wins; SCPs and boundaries limit, they never grant. Applications on EC2 or Lambda get a role, never access keys. Cross-account access = a role in the target account + AssumeRole.                                        |
| W2   | Compute                   | Spot = cheapest, can be interrupted: only for fault-tolerant work. Instance store is lost when the instance stops; EBS persists. EBS lives in one AZ; EFS is shared across AZs.                                                                    |
| W3   | Networking                | Private subnet reaching the internet = NAT gateway in a public subnet. Private access to S3 without internet = gateway endpoint. Many VPCs + on-prem = Transit Gateway.                                                                            |
| W4   | Storage                   | Unknown or changing access pattern = Intelligent-Tiering. Write-once compliance = Object Lock (compliance mode). Huge offline transfer = Snow family; online sync = DataSync.                                                                      |
| W5   | Databases                 | Multi-AZ = failover, not read scaling; read replicas = read scaling. Microsecond DynamoDB reads = DAX. Key-value at any scale, serverless = DynamoDB.                                                                                              |
| W6   | Resilience and scaling    | Lower RTO/RPO costs more: backup-restore \< pilot light \< warm standby \< active-active. Static IP for a load balancer = NLB (or Global Accelerator). Failover between Regions = Route 53 failover routing + health checks.                       |
| W7   | Decoupling and serverless | Decouple producer and consumer = SQS. One event to many consumers = SNS fan-out or EventBridge. Exactly-once, ordered processing = SQS FIFO.                                                                                                       |
| W8   | Security and monitoring   | Automatic secret rotation = Secrets Manager. Who did what = CloudTrail; resource configuration over time = Config. Sensitive data in S3 = Macie; threat detection = GuardDuty.                                                                     |
| W9   | Performance and cost      | Static content worldwide = CloudFront; non-HTTP global performance = Global Accelerator. Query S3 data with SQL, no servers = Athena. Steady 1–3 year usage = Savings Plans or Reserved Instances.                                                 |
| W10  | Exam practice             | Read the last line of the question first: cheapest, fastest, least operational overhead or most secure. Eliminate two answers, then compare the remaining two on that last line. Managed and serverless usually wins 'least operational overhead'. |

## 07. Checkpoints and how to know you are ready

| When       | Check                                                                                       | Pass mark                         |
|------------|---------------------------------------------------------------------------------------------|-----------------------------------|
| End of W3  | Explain IAM evaluation, EC2 pricing options and a public/private VPC with no notes          | All three from memory             |
| End of W5  | Draw a three-tier app (ALB, EC2 Auto Scaling, RDS Multi-AZ, S3) and list each storage class | Under 10 minutes                  |
| End of W7  | Questions 1–34 in the study pack                                                            | 75% or more                       |
| End of W9  | Questions 35–60 in the study pack; Well-Architected pillars from memory                     | 75% or more; all 6 pillars        |
| End of W10 | Two full timed practice sets                                                                | 80% or more twice → book the exam |

### The six Well-Architected pillars

- Operational excellence
- Security
- Reliability
- Performance efficiency
- Cost optimisation
- Sustainability

^([\[6\]](#-sources))

## ··. Sources

Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.

1.  [AWS Certified Solutions Architect – Associate (exam page)](https://aws.amazon.com/certification/certified-solutions-architect-associate/)  
    https://aws.amazon.com/certification/certified-solutions-architect-associate/
2.  [SAA-C03 exam guide (PDF)](https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf)  
    https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf
3.  [AWS Skill Builder (free courses and the official practice question set)](https://skillbuilder.aws/)  
    https://skillbuilder.aws/
4.  [AWS product FAQs](https://aws.amazon.com/faqs/)  
    https://aws.amazon.com/faqs/
5.  [AWS Free Tier](https://aws.amazon.com/free/)  
    https://aws.amazon.com/free/
6.  [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)  
    https://aws.amazon.com/architecture/well-architected/
