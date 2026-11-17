AWS · SOLUTIONS ARCHITECT ASSOCIATE · SAA-C03

# SAA-C03 study pack

Notes for the four exam domains, a service-for-need table, 60 original practice questions in the exam's scenario style with explained answers, and a two-week final revision plan for 5–18 April 2027, before your exam in the week of 19 April.

## Index

|                                                                       |
|-----------------------------------------------------------------------|
| [Exam facts and how to use this pack](#exam-facts-and-how-to-use-this-pack)                        |
| [Notes: Design secure architectures (30%)](#design-secure-architectures-30-of-the-examknowledge-base-)                   |
| [Notes: Design resilient architectures (26%)](#design-resilient-architectures-26-of-the-examknowledge-base-)                |
| [Notes: Design high-performing architectures (24%)](#design-high-performing-architectures-24-of-the-examknowledge-base-)          |
| [Notes: Design cost-optimised architectures (20%)](#design-cost-optimised-architectures-20-of-the-examknowledge-base-)           |
| [Which service for which need](#which-service-for-which-need)                               |
| [Questions: Design secure architectures (Q1–Q18)](#questions-design-secure-architecturesanswer-key)           |
| [Questions: Design resilient architectures (Q19–Q34)](#questions-design-resilient-architecturesanswer-key)       |
| [Questions: Design high-performing architectures (Q35–Q48)](#questions-design-high-performing-architecturesanswer-key) |
| [Questions: Design cost-optimised architectures (Q49–Q60)](#questions-design-cost-optimised-architecturesanswer-key)  |
| [Answer keys](#answer-key-design-secure-architectures)                                               |
| [Final revision plan, 5–18 Apr 2027](#final-revision-plan-518-apr-2027)                        |

Sources: the official [exam page](https://aws.amazon.com/certification/certified-solutions-architect-associate/) and [exam guide](https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf) (domains, weights, format), the [Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) and the [AWS service FAQs](https://aws.amazon.com/faqs/). Notes and questions are original summaries, not copied exam content. AWS changes services and prices often: check the exam guide for the current version before you book.

## Exam facts and how to use this pack

|               |                                                                    |
|---------------|--------------------------------------------------------------------|
| Questions     | 65 (50 scored, 15 unscored), multiple choice and multiple response |
| Time          | 130 minutes                                                        |
| Passing score | 720 on a scaled 100–1000 range                                     |
| Domains       | Secure 30%, Resilient 26%, High-performing 24%, Cost-optimised 20% |

From the official exam guide. Unscored questions are not marked; you cannot tell which they are, so answer everything. There is no penalty for guessing.

### How to use

1.  Learn the services hands-on first (your plan's AWS track and the [Knowledge Base AWS pages](knowledge-base/cloud.md#aws-core-services-and-the-saa-c03-exam)). This pack is for the final revision.
2.  Read one domain's notes, then do that domain's questions without looking at the key. Aim for 80%.
3.  For every miss, write one line: what clue in the question should have pointed to the right service.
4.  Follow the revision plan on the last page. Take full practice exams from [AWS Skill Builder](https://skillbuilder.aws/) (it has a free official practice question set) and the sample questions on the exam page.

### Reading scenario questions

- Find the constraint words: **most cost-effective**, **least operational overhead**, **highly available**, **lowest latency**, **without code changes**. They decide between two answers that both work.
- Managed and serverless usually wins "least operational overhead". Multi-AZ wins "highly available". Caching and edge services win "lowest latency".
- Eliminate options that are insecure (keys in code, public buckets, root user) or do not exist (security groups on S3, deny rules in security groups).

## Design secure architectures 30% of the exam[Knowledge Base ↗](knowledge-base/cloud.md#aws-iam-and-least-privilege)

- IAM: users, groups, roles, policies. Prefer roles with temporary credentials (STS) to long-lived access keys. Never use the root user for daily work; enable MFA on it.
- Policy evaluation: an explicit Deny anywhere wins; otherwise access needs an Allow; the default is deny. SCPs in AWS Organizations set the maximum permissions for member accounts.
- Cross-account access: an IAM role whose trust policy names the other account, assumed through STS.
- Network: security groups are stateful and allow-only, attached to ENIs; network ACLs are stateless, have allow and deny rules, and apply to subnets.
- Private subnets reach the internet through a NAT gateway in a public subnet. Gateway endpoints (S3, DynamoDB) and interface endpoints (PrivateLink) keep traffic inside AWS.
- Encryption at rest: KMS keys (AWS managed or customer managed); SSE-S3, SSE-KMS, client-side. In transit: TLS, ACM certificates on ALB and CloudFront.
- Secrets Manager stores and rotates secrets; Systems Manager Parameter Store holds configuration and SecureString values.
- Edge protection: AWS WAF (layer 7 rules such as SQL injection and XSS), Shield Standard (automatic DDoS protection), Shield Advanced (paid, with response team).
- Detection: GuardDuty (threat detection from logs), Inspector (vulnerability scanning), Macie (sensitive data in S3), Security Hub (findings in one place), CloudTrail (API audit), Config (resource configuration history and rules).
- S3 security: Block Public Access, bucket policies, Object Lock (WORM), origin access control for CloudFront, presigned URLs for temporary access.
- Identity for app users: Cognito user pools (sign-up and sign-in, social login) and identity pools (temporary AWS credentials).

[Practice questions for this domain →](#questions-design-secure-architecturesanswer-key)

## Design resilient architectures 26% of the exam[Knowledge Base ↗](knowledge-base/cloud.md#aws-core-services-and-the-saa-c03-exam)

- Spread across Availability Zones: Auto Scaling groups over several AZs behind an Elastic Load Balancer.
- Decouple with SQS (buffer, at-least-once; FIFO for ordering and exactly-once processing), SNS (pub/sub fan-out), EventBridge (event routing).
- RDS Multi-AZ gives synchronous standby and automatic failover; read replicas scale reads (asynchronous). Aurora keeps six copies of data across three AZs.
- DynamoDB global tables give multi-Region, multi-active replication; S3 Cross-Region Replication needs versioning on both buckets.
- Route 53 routing policies: simple, weighted, latency, failover (with health checks), geolocation, geoproximity, multivalue.
- Disaster recovery, cheapest to most expensive: backup and restore, pilot light, warm standby, multi-site active-active. Lower RTO and RPO cost more.
- Stateless tiers: keep sessions in ElastiCache or DynamoDB so instances can be replaced at any time.
- Storage durability: EBS is in one AZ (use snapshots); instance store is lost when the instance stops; EFS is regional and multi-AZ; S3 is designed for eleven nines of durability.
- Step Functions orchestrate multi-step workflows with retries; dead-letter queues catch messages that keep failing.

[Practice questions for this domain →](#questions-design-resilient-architecturesanswer-key)

## Design high-performing architectures 24% of the exam[Knowledge Base ↗](knowledge-base/design.md#caching-and-cdns)

- Caching: CloudFront at the edge, ElastiCache (Redis or Memcached) for databases, DAX for DynamoDB.
- Global performance: CloudFront for HTTP content, Global Accelerator for TCP/UDP with static anycast IPs, Route 53 latency routing.
- EBS types: gp3 general purpose SSD; io2 provisioned IOPS for demanding databases; st1 throughput HDD for big sequential data; sc1 cold HDD for infrequent access.
- EC2 placement groups: cluster (low latency, one AZ), spread (separate hardware), partition (large distributed systems).
- Databases by need: RDS and Aurora (relational), DynamoDB (key-value, any scale), Redshift (data warehouse), OpenSearch (search), Neptune (graph).
- Analytics: Athena (SQL on S3, serverless), Kinesis Data Streams (real-time ingestion, replay), Data Firehose (load streams into S3, Redshift, OpenSearch), Glue (ETL and data catalogue), EMR (Hadoop and Spark).
- S3 performance: multipart upload for large objects, Transfer Acceleration for distant clients, spread work across prefixes.
- Serverless: Lambda scales automatically; provisioned concurrency removes cold starts; API Gateway fronts APIs.

[Practice questions for this domain →](#questions-design-high-performing-architecturesanswer-key)

## Design cost-optimised architectures 20% of the exam[Knowledge Base ↗](knowledge-base/cloud.md#aws-core-services-and-the-saa-c03-exam)

- EC2 pricing: On-Demand (flexible), Savings Plans and Reserved Instances (1 or 3 years, steady use), Spot (up to large discounts, can be interrupted), Dedicated Hosts (licensing, compliance).
- S3 storage classes: Standard, Intelligent-Tiering (unknown patterns), Standard-IA and One Zone-IA, Glacier Instant Retrieval (quarterly access, milliseconds), Glacier Flexible Retrieval (minutes to hours), Glacier Deep Archive (cheapest, hours).
- Lifecycle rules move or expire objects automatically.
- Cost tools: Cost Explorer (analyse), AWS Budgets (alerts), Cost and Usage Report (detail), Compute Optimizer and Trusted Advisor (right-sizing and checks), cost allocation tags.
- Data transfer: inbound from the internet is free; outbound to the internet, between Regions and between AZs is charged. Gateway endpoints for S3 and DynamoDB avoid NAT gateway processing charges.
- Serverless and managed services (Lambda, Fargate, Aurora Serverless) avoid paying for idle capacity.
- Stop or schedule non-production resources outside working hours.

[Practice questions for this domain →](#questions-design-cost-optimised-architecturesanswer-key)

## Which service for which need

| Need                                            | Service                                                |
|-------------------------------------------------|--------------------------------------------------------|
| Give an EC2 app access to S3 without keys       | IAM role (instance profile)                            |
| Limit what member accounts can do               | SCPs in AWS Organizations                              |
| Block one IP at the subnet level                | Network ACL deny rule                                  |
| Private subnet needs outbound internet          | NAT gateway                                            |
| Reach S3 privately from a VPC                   | Gateway VPC endpoint                                   |
| Rotate database passwords                       | Secrets Manager                                        |
| Block SQL injection and XSS                     | AWS WAF                                                |
| Detect threats from logs                        | GuardDuty                                              |
| Find personal data in S3                        | Macie                                                  |
| Scan EC2 and containers for CVEs                | Inspector                                              |
| Audit API calls                                 | CloudTrail                                             |
| Track configuration changes and compliance      | AWS Config                                             |
| App sign-up and social login                    | Cognito                                                |
| Write-once storage for logs                     | S3 Object Lock                                         |
| Decouple producers and consumers                | SQS                                                    |
| Fan out one message to many                     | SNS (with SQS subscribers)                             |
| Automatic database failover                     | RDS Multi-AZ                                           |
| Scale relational reads                          | Read replicas or Aurora replicas                       |
| Multi-Region active-active NoSQL                | DynamoDB global tables                                 |
| Shared Linux file system                        | EFS                                                    |
| Shared Windows file system                      | FSx for Windows File Server                            |
| Workflow with retries                           | Step Functions                                         |
| Edge caching for websites                       | CloudFront                                             |
| Static IPs and fast global failover for TCP/UDP | Global Accelerator                                     |
| Cache database queries                          | ElastiCache                                            |
| Microsecond DynamoDB reads                      | DAX                                                    |
| SQL over files in S3                            | Athena                                                 |
| Real-time stream with replay                    | Kinesis Data Streams                                   |
| Data warehouse                                  | Redshift                                               |
| Containers without managing servers             | Fargate (ECS or EKS)                                   |
| Interruptible batch at lowest cost              | Spot Instances                                         |
| Steady 24/7 compute for years                   | Savings Plans or Reserved Instances                    |
| Unknown access pattern storage                  | S3 Intelligent-Tiering                                 |
| Cheapest long-term archive                      | S3 Glacier Deep Archive                                |
| Spend alerts                                    | AWS Budgets                                            |
| Hybrid private link to on-premises              | Site-to-Site VPN (quick) or Direct Connect (dedicated) |

Cover the right column and test yourself.

## Questions: Design secure architectures[Answer key](#answer-key-design-secure-architectures)

**Q1.** An application on EC2 must read objects from an S3 bucket. What is the most secure way to give it credentials?

1.  **A** Bake access keys into the AMI
2.  **B** Use the root user's access keys
3.  **C** Attach an IAM role to the instance through an instance profile
4.  **D** Store an IAM user's access keys in environment variables

**Q2.** Compliance requires that CloudTrail log files in S3 cannot be deleted or changed by anyone, including administrators, for one year. What meets this?

1.  **A** Enable versioning only
2.  **B** S3 Object Lock in compliance mode with a one-year retention period
3.  **C** A lifecycle rule that moves logs to Glacier
4.  **D** A bucket policy that denies DeleteObject

**Q3.** A company with many AWS accounts must stop every account from launching resources outside one Region. What is the simplest central control?

1.  **A** An IAM policy in each account
2.  **B** Security groups that block other Regions
3.  **C** An AWS Config rule
4.  **D** A service control policy in AWS Organizations that denies other Regions

**Q4.** EC2 instances in a private subnet must download patches from the internet but must not accept inbound connections from it. What should be added?

1.  **A** A public IP on each instance
2.  **B** A VPC peering connection
3.  **C** A route from the private subnet to the internet gateway
4.  **D** A NAT gateway in a public subnet and a route to it from the private subnet

**Q5.** Instances in a private subnet upload large amounts of data to S3 and NAT gateway charges are high. What reduces cost while keeping traffic private?

1.  **A** An interface endpoint for EC2
2.  **B** A larger NAT gateway
3.  **C** AWS Direct Connect
4.  **D** A gateway VPC endpoint for S3

**Q6.** A single malicious IP address must be blocked from reaching any instance in a subnet. What should be used?

1.  **A** A Route 53 routing policy
2.  **B** AWS Shield Standard
3.  **C** A deny rule in the security group
4.  **D** A deny rule in the subnet's network ACL

**Q7.** Data in S3 must be encrypted at rest with a key whose use is logged and whose rotation the company controls. Which option fits?

1.  **A** No encryption, but a strict bucket policy
2.  **B** SSE-KMS with a customer managed key
3.  **C** SSE-S3
4.  **D** Client-side encryption with a key stored in the code

**Q8.** An application needs database credentials that rotate automatically without code changes. Which service?

1.  **A** AWS Secrets Manager
2.  **B** Systems Manager Parameter Store String parameters
3.  **C** An encrypted file in S3
4.  **D** Environment variables on the instance

**Q9.** A public web application behind an Application Load Balancer must be protected from SQL injection and cross-site scripting. What should be used?

1.  **A** Amazon GuardDuty
2.  **B** Security group rules
3.  **C** AWS WAF attached to the load balancer
4.  **D** AWS Shield Standard

**Q10.** The security team wants alerts when an EC2 instance talks to known malicious IP addresses. Which service?

1.  **A** AWS Trusted Advisor
2.  **B** Amazon Inspector
3.  **C** Amazon GuardDuty
4.  **D** Amazon Macie

**Q11.** A company must find buckets that contain personal data such as ID numbers. Which service?

1.  **A** Amazon GuardDuty
2.  **B** Amazon Macie
3.  **C** AWS Config
4.  **D** Amazon Inspector

**Q12.** A mobile app needs customer sign-up, sign-in and login with social identity providers. What should be used?

1.  **A** AWS Directory Service
2.  **B** An IAM user per customer
3.  **C** IAM groups
4.  **D** Amazon Cognito user pools

**Q13.** A partner company's AWS account needs temporary access to one S3 bucket. What is the recommended approach?

1.  **A** Create an IAM role that the partner account can assume
2.  **B** Share an IAM user's access keys
3.  **C** Make the bucket public
4.  **D** Give them the root credentials

**Q14.** A static site in S3 must be reachable only through CloudFront, not directly. What should be configured?

1.  **A** Origin access control with a bucket policy that allows only the distribution
2.  **B** A security group on the bucket
3.  **C** A network ACL on the bucket
4.  **D** S3 Transfer Acceleration

**Q15.** Administrators must use MFA before they can stop production EC2 instances. How can this be enforced?

1.  **A** A security group rule
2.  **B** An S3 bucket policy
3.  **C** An IAM policy condition on aws:MultiFactorAuthPresent
4.  **D** A CloudWatch alarm

**Q16.** The team needs to know who modified a security group yesterday. Where should they look?

1.  **A** CloudWatch metrics
2.  **B** VPC Flow Logs
3.  **C** AWS CloudTrail
4.  **D** AWS Trusted Advisor

**Q17.** All new EBS volumes in a Region must be encrypted without relying on each engineer. What should be done?

1.  **A** Encrypt snapshots only
2.  **B** Use instance store volumes
3.  **C** Ask engineers to tick the encryption box
4.  **D** Enable EBS encryption by default for the Region

**Q18.** A user's identity policy allows s3:\* and the bucket policy explicitly denies s3:DeleteObject for that user. Can the user delete objects?

1.  **A** Yes, the identity policy allows it
2.  **B** Yes, because s3:\* includes delete
3.  **C** No, the explicit deny wins
4.  **D** Only if MFA is used

## Questions: Design resilient architectures[Answer key](#answer-key-design-resilient-architectures)

**Q19.** A web tier must keep running if one Availability Zone fails. What design meets this?

1.  **A** An Auto Scaling group across at least two AZs behind an Application Load Balancer
2.  **B** A cluster placement group
3.  **C** Several instances in one AZ
4.  **D** One large instance with a bigger EBS volume

**Q20.** An RDS MySQL database must fail over automatically to another AZ with no data loss. What should be enabled?

1.  **A** A read replica in the same AZ
2.  **B** Automated backups only
3.  **C** Multi-AZ deployment
4.  **D** A larger instance class

**Q21.** An order service sometimes sends bursts faster than the processing service can handle, and orders must not be lost. What should be placed between them?

1.  **A** An SNS topic with no subscribers
2.  **B** An Amazon SQS queue
3.  **C** Direct synchronous HTTP calls
4.  **D** A bigger EC2 instance for processing

**Q22.** One event must be delivered to three independent processing services, each at its own pace. What design fits?

1.  **A** One SQS queue polled by all three services
2.  **B** An SNS topic with an SQS queue subscribed for each service
3.  **C** A single Lambda function calling all three
4.  **D** Three cron jobs

**Q23.** A small company needs a disaster recovery plan at the lowest cost and can accept an RTO of 24 hours. Which strategy?

1.  **A** Warm standby
2.  **B** Pilot light
3.  **C** Multi-site active-active
4.  **D** Backup and restore

**Q24.** A company keeps a scaled-down but fully working copy of production always running in a second Region and scales it up during a disaster. What is this strategy?

1.  **A** Backup and restore
2.  **B** Warm standby
3.  **C** Multi-site active-active
4.  **D** Pilot light

**Q25.** Traffic must go to a secondary Region only when health checks on the primary fail. Which Route 53 routing policy?

1.  **A** Weighted routing
2.  **B** Simple routing
3.  **C** Geolocation routing
4.  **D** Failover routing

**Q26.** An application needs a NoSQL table that accepts writes in two Regions at once. Which feature?

1.  **A** DynamoDB Streams alone
2.  **B** ElastiCache Global Datastore only
3.  **C** DynamoDB global tables
4.  **D** RDS read replicas

**Q27.** Objects in an S3 bucket must be copied automatically to a bucket in another Region. What must be enabled on both buckets?

1.  **A** Static website hosting
2.  **B** Requester Pays
3.  **C** Versioning
4.  **D** Transfer Acceleration

**Q28.** Users are logged out whenever Auto Scaling removes an instance. What fixes this?

1.  **A** Enable sticky sessions only
2.  **B** Store sessions on the instance store
3.  **C** Use larger instances
4.  **D** Store session data in ElastiCache or DynamoDB

**Q29.** A Lambda function processes messages from SQS and some messages always fail. They must be kept for analysis without blocking the queue. What should be configured?

1.  **A** Deleting failed messages in code
2.  **B** A longer Lambda timeout only
3.  **C** A dead-letter queue with a redrive policy
4.  **D** A FIFO queue

**Q30.** How does Amazon Aurora store data for durability?

1.  **A** One copy plus nightly backups
2.  **B** Six copies across three Availability Zones
3.  **C** Three copies across three Regions
4.  **D** Two copies in one AZ

**Q31.** Which storage loses its data when the EC2 instance is stopped?

1.  **A** Amazon EFS
2.  **B** Amazon S3
3.  **C** Instance store
4.  **D** EBS gp3 volume

**Q32.** Many Linux EC2 instances in several AZs need the same shared file system. Which service?

1.  **A** Instance store
2.  **B** S3 Glacier Flexible Retrieval
3.  **C** One EBS gp3 volume
4.  **D** Amazon EFS

**Q33.** An Auto Scaling group should replace instances that the load balancer reports as unhealthy. What should be set?

1.  **A** The ASG health check type to ELB
2.  **B** A CloudTrail trail
3.  **C** Sticky sessions
4.  **D** A larger health check grace period only

**Q34.** A multi-step order workflow across several Lambda functions needs retries, branching and visible state. Which service?

1.  **A** A cron job on EC2
2.  **B** AWS Step Functions
3.  **C** AWS CloudFormation
4.  **D** An SQS FIFO queue alone

## Questions: Design high-performing architectures[Answer key](#answer-key-design-high-performing-architectures)

**Q35.** Users worldwide load images and videos slowly from an S3 bucket in one Region. What improves latency most?

1.  **A** EBS io2 volumes
2.  **B** A larger S3 bucket
3.  **C** S3 Standard-IA
4.  **D** Amazon CloudFront in front of the bucket

**Q36.** Reporting queries slow down an RDS MySQL primary that also serves the application. What helps most?

1.  **A** Use the Multi-AZ standby for reads
2.  **B** Send reports to a read replica
3.  **C** Add storage to the primary
4.  **D** Switch to an st1 volume

**Q37.** A read-heavy DynamoDB application needs microsecond read latency with minimal code changes. What should be added?

1.  **A** A read replica
2.  **B** S3 Transfer Acceleration
3.  **C** DynamoDB Accelerator (DAX)
4.  **D** ElastiCache for Memcached

**Q38.** Users on other continents upload 5 GB files to S3 and uploads are slow. What helps most?

1.  **A** Cross-Region Replication
2.  **B** S3 Glacier
3.  **C** S3 Transfer Acceleration with multipart upload
4.  **D** A bigger EC2 instance

**Q39.** A tightly coupled HPC application needs the lowest network latency between instances. Which placement group?

1.  **A** Partition
2.  **B** Spread
3.  **C** No placement group
4.  **D** Cluster

**Q40.** A database needs the highest sustained IOPS from block storage. Which EBS type?

1.  **A** Cold HDD (sc1)
2.  **B** Provisioned IOPS SSD (io2)
3.  **C** Magnetic (standard)
4.  **D** Throughput optimised HDD (st1)

**Q41.** Analysts want to run SQL on CSV and Parquet files in S3 without managing servers. Which service?

1.  **A** AWS Batch
2.  **B** Amazon ElastiCache
3.  **C** Amazon RDS
4.  **D** Amazon Athena

**Q42.** A clickstream must be ingested in real time and read by several consumers that may need to replay data. Which service?

1.  **A** Amazon SNS
2.  **B** Amazon SQS standard queue
3.  **C** AWS Glue
4.  **D** Amazon Kinesis Data Streams

**Q43.** A company needs a data warehouse for complex analytical queries on terabytes of structured data. Which service?

1.  **A** Amazon EFS
2.  **B** Amazon Redshift
3.  **C** Amazon ElastiCache
4.  **D** Amazon DynamoDB

**Q44.** An API has unpredictable spiky traffic and the team does not want to manage servers. What fits best?

1.  **A** Amazon API Gateway with AWS Lambda
2.  **B** EC2 instances sized for the peak
3.  **C** One large EC2 instance
4.  **D** Amazon Lightsail

**Q45.** A global multiplayer game over UDP needs static IP addresses and fast failover between Regions. Which service?

1.  **A** Amazon CloudFront
2.  **B** An Application Load Balancer
3.  **C** AWS Global Accelerator
4.  **D** Route 53 simple routing

**Q46.** An application needs a key-value database with single-digit millisecond latency at any scale. Which service?

1.  **A** Amazon Athena
2.  **B** Amazon Redshift
3.  **C** Amazon S3 Glacier
4.  **D** Amazon DynamoDB

**Q47.** A latency-sensitive Lambda function suffers from cold starts at peak hours. What helps?

1.  **A** Provisioned concurrency
2.  **B** A larger deployment package
3.  **C** A longer timeout
4.  **D** Running it in a different Region

**Q48.** A popular product page runs the same expensive database query thousands of times a minute. What reduces database load most?

1.  **A** Cache the result in Amazon ElastiCache
2.  **B** Add a Multi-AZ standby
3.  **C** Move the database to an st1 volume
4.  **D** Enable CloudTrail

## Questions: Design cost-optimised architectures[Answer key](#answer-key-design-cost-optimised-architectures)

**Q49.** A web application runs steadily 24/7 and will for the next three years. Which purchase option costs least?

1.  **A** Spot Instances
2.  **B** On-Demand Instances
3.  **C** 3-year Savings Plan or Reserved Instances
4.  **D** Dedicated Hosts

**Q50.** Nightly image-processing jobs can be stopped and restarted without harm. Which option costs least?

1.  **A** Spot Instances
2.  **B** 3-year Reserved Instances
3.  **C** Dedicated Instances
4.  **D** On-Demand Instances

**Q51.** Data in S3 has an unknown and changing access pattern. Which storage class lowers cost automatically?

1.  **A** S3 Glacier Deep Archive
2.  **B** S3 Intelligent-Tiering
3.  **C** S3 One Zone-IA
4.  **D** S3 Standard

**Q52.** Records must be kept for 10 years, are almost never read, and a 12-hour retrieval time is acceptable. Which class is cheapest?

1.  **A** S3 Glacier Deep Archive
2.  **B** S3 Intelligent-Tiering
3.  **C** S3 Standard-IA
4.  **D** S3 Glacier Instant Retrieval

**Q53.** Data is read about once a quarter but must be available in milliseconds when needed. Which class is the best fit?

1.  **A** S3 Glacier Deep Archive
2.  **B** S3 Glacier Instant Retrieval
3.  **C** S3 Glacier Flexible Retrieval
4.  **D** S3 Standard

**Q54.** Log objects should move to a cheaper class after 30 days and be deleted after a year, automatically. What should be used?

1.  **A** S3 Versioning
2.  **B** A cron job on EC2
3.  **C** Cross-Region Replication
4.  **D** An S3 Lifecycle configuration

**Q55.** Finance wants an email when the monthly bill is forecast to exceed a set amount. Which tool?

1.  **A** AWS CloudTrail
2.  **B** Cost Explorer only
3.  **C** AWS Budgets
4.  **D** VPC Flow Logs

**Q56.** Development EC2 instances are idle at night and on weekends. What is the simplest saving?

1.  **A** Buy 3-year Reserved Instances for them
2.  **B** Add more instances
3.  **C** Stop them on a schedule (for example EventBridge with a Lambda function or Instance Scheduler)
4.  **D** Move them to Dedicated Hosts

**Q57.** The team wants recommendations to resize over-provisioned EC2 instances based on actual usage. Which service?

1.  **A** AWS CloudTrail
2.  **B** AWS Compute Optimizer
3.  **C** AWS Shield
4.  **D** Amazon Inspector

**Q58.** Which data transfer is generally free?

1.  **A** Data transferred between AZs
2.  **B** Data transferred into AWS from the internet
3.  **C** Data transferred between Regions
4.  **D** Data transferred out to the internet

**Q59.** Small container jobs run a few times a day, and the EC2 cluster sits idle most of the time. What reduces cost and management?

1.  **A** Keep the cluster and add Reserved Instances
2.  **B** Buy larger EC2 instances
3.  **C** Run them on AWS Fargate
4.  **D** Run them on Dedicated Hosts

**Q60.** Which change cuts NAT gateway data charges for heavy traffic from private subnets to DynamoDB?

1.  **A** A gateway VPC endpoint for DynamoDB
2.  **B** A larger instance type
3.  **C** An internet gateway for the private subnet
4.  **D** A second NAT gateway

## Answer key: Design secure architectures

| Q               | Ans | Answer                                                                       | Why                                                                                                            |
|-----------------|-----|------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| [Q1](#questions-design-resilient-architecturesanswer-key)  | C   | Attach an IAM role to the instance through an instance profile               | Roles give temporary credentials that rotate automatically; nothing long-lived is stored on the instance.      |
| [Q2](#questions-design-resilient-architecturesanswer-key)  | B   | S3 Object Lock in compliance mode with a one-year retention period           | Compliance mode cannot be shortened or removed by any user; a bucket policy can be edited by an administrator. |
| [Q3](#questions-design-resilient-architecturesanswer-key)  | D   | A service control policy in AWS Organizations that denies other Regions      | SCPs set the maximum permissions for all accounts in an organisational unit.                                   |
| [Q4](#questions-design-resilient-architecturesanswer-key)  | D   | A NAT gateway in a public subnet and a route to it from the private subnet   | NAT allows outbound-initiated traffic only.                                                                    |
| [Q5](#questions-design-resilient-architecturesanswer-key)  | D   | A gateway VPC endpoint for S3                                                | Gateway endpoints for S3 have no hourly or data processing charge and keep traffic on the AWS network.         |
| [Q6](#questions-design-resilient-architecturesanswer-key)  | D   | A deny rule in the subnet's network ACL                                      | Security groups have allow rules only; network ACLs support explicit deny.                                     |
| [Q7](#questions-design-resilient-architecturesanswer-key)  | B   | SSE-KMS with a customer managed key                                          | KMS key use appears in CloudTrail and customer managed keys have company-controlled policies and rotation.     |
| [Q8](#questions-design-resilient-architecturesanswer-key)  | A   | AWS Secrets Manager                                                          | Secrets Manager has built-in rotation, including for RDS.                                                      |
| [Q9](#questions-design-resilient-architecturesanswer-key)  | C   | AWS WAF attached to the load balancer                                        | WAF inspects HTTP requests with managed rule groups for these attacks.                                         |
| [Q10](#questions-design-resilient-architecturesanswer-key) | C   | Amazon GuardDuty                                                             | GuardDuty analyses VPC Flow Logs, DNS logs and CloudTrail for threats.                                         |
| [Q11](#questions-design-resilient-architecturesanswer-key) | B   | Amazon Macie                                                                 | Macie uses pattern matching and machine learning to find sensitive data in S3.                                 |
| [Q12](#questions-design-resilient-architecturesanswer-key) | D   | Amazon Cognito user pools                                                    | IAM users are for people and systems that manage AWS, not app customers.                                       |
| [Q13](#questions-design-resilient-architecturesanswer-key) | A   | Create an IAM role that the partner account can assume                       | Cross-account roles give temporary credentials and can be revoked at any time.                                 |
| [Q14](#questions-design-resilient-architecturesanswer-key) | A   | Origin access control with a bucket policy that allows only the distribution | S3 has no security groups; OAC plus a bucket policy restricts access to CloudFront.                            |
| [Q15](#questions-design-resilient-architecturesanswer-key) | C   | An IAM policy condition on aws:MultiFactorAuthPresent                        | The condition key checks that the request was authenticated with MFA.                                          |
| [Q16](#questions-design-resilient-architecturesanswer-key) | C   | AWS CloudTrail                                                               | CloudTrail records API calls with the identity, time and source.                                               |
| [Q17](#questions-design-resilient-architecturesanswer-key) | D   | Enable EBS encryption by default for the Region                              | Encryption by default applies to every new volume and snapshot copy in that Region.                            |
| [Q18](#questions-design-resilient-architecturesanswer-key) | C   | No, the explicit deny wins                                                   | In policy evaluation, any explicit deny overrides allows.                                                      |

Score: \_\_\_\_\_\_ / 18

## Answer key: Design resilient architectures

| Q               | Ans | Answer                                                                            | Why                                                                                                                |
|-----------------|-----|-----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| [Q19](#questions-design-high-performing-architecturesanswer-key) | A   | An Auto Scaling group across at least two AZs behind an Application Load Balancer | Spreading across AZs removes the single point of failure.                                                          |
| [Q20](#questions-design-high-performing-architecturesanswer-key) | C   | Multi-AZ deployment                                                               | Multi-AZ keeps a synchronous standby and fails over automatically.                                                 |
| [Q21](#questions-design-high-performing-architecturesanswer-key) | B   | An Amazon SQS queue                                                               | The queue buffers messages until consumers catch up.                                                               |
| [Q22](#questions-design-high-performing-architecturesanswer-key) | B   | An SNS topic with an SQS queue subscribed for each service                        | SNS fans out; each queue buffers for its own consumer.                                                             |
| [Q23](#questions-design-high-performing-architecturesanswer-key) | D   | Backup and restore                                                                | Restoring from backups is cheapest and slowest.                                                                    |
| [Q24](#questions-design-high-performing-architecturesanswer-key) | B   | Warm standby                                                                      | Pilot light keeps only core pieces such as the database running; warm standby runs the whole stack at small scale. |
| [Q25](#questions-design-high-performing-architecturesanswer-key) | D   | Failover routing                                                                  | Failover routing uses health checks to switch to the secondary record.                                             |
| [Q26](#questions-design-high-performing-architecturesanswer-key) | C   | DynamoDB global tables                                                            | Global tables replicate across Regions with multi-active writes.                                                   |
| [Q27](#questions-design-high-performing-architecturesanswer-key) | C   | Versioning                                                                        | Cross-Region Replication requires versioning on source and destination.                                            |
| [Q28](#questions-design-high-performing-architecturesanswer-key) | D   | Store session data in ElastiCache or DynamoDB                                     | External session storage makes the web tier stateless.                                                             |
| [Q29](#questions-design-high-performing-architecturesanswer-key) | C   | A dead-letter queue with a redrive policy                                         | After the maximum receives, messages move to the DLQ.                                                              |
| [Q30](#questions-design-high-performing-architecturesanswer-key) | B   | Six copies across three Availability Zones                                        | Aurora's storage layer replicates six ways across three AZs.                                                       |
| [Q31](#questions-design-high-performing-architecturesanswer-key) | C   | Instance store                                                                    | Instance store is physically attached to the host and is temporary.                                                |
| [Q32](#questions-design-high-performing-architecturesanswer-key) | D   | Amazon EFS                                                                        | EFS is a regional NFS file system usable across AZs.                                                               |
| [Q33](#questions-design-high-performing-architecturesanswer-key) | A   | The ASG health check type to ELB                                                  | By default the ASG uses EC2 status checks only.                                                                    |
| [Q34](#questions-design-high-performing-architecturesanswer-key) | B   | AWS Step Functions                                                                | Step Functions is a managed state machine with built-in retries.                                                   |

Score: \_\_\_\_\_\_ / 16

## Answer key: Design high-performing architectures

| Q               | Ans | Answer                                         | Why                                                                                                             |
|-----------------|-----|------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| [Q35](#questions-design-cost-optimised-architecturesanswer-key) | D   | Amazon CloudFront in front of the bucket       | Edge locations cache content close to users.                                                                    |
| [Q36](#questions-design-cost-optimised-architecturesanswer-key) | B   | Send reports to a read replica                 | Read replicas take read load; a classic Multi-AZ standby does not serve reads.                                  |
| [Q37](#questions-design-cost-optimised-architecturesanswer-key) | C   | DynamoDB Accelerator (DAX)                     | DAX is an in-memory cache built for DynamoDB's API.                                                             |
| [Q38](#questions-design-cost-optimised-architecturesanswer-key) | C   | S3 Transfer Acceleration with multipart upload | Uploads enter at the nearest edge location and travel on the AWS backbone; multipart uploads parts in parallel. |
| [Q39](#questions-design-cost-optimised-architecturesanswer-key) | D   | Cluster                                        | Cluster packs instances close together in one AZ.                                                               |
| [Q40](#questions-design-cost-optimised-architecturesanswer-key) | B   | Provisioned IOPS SSD (io2)                     | io2 is designed for I/O-intensive databases.                                                                    |
| [Q41](#questions-design-cost-optimised-architecturesanswer-key) | D   | Amazon Athena                                  | Athena is serverless and charges per data scanned.                                                              |
| [Q42](#questions-design-cost-optimised-architecturesanswer-key) | D   | Amazon Kinesis Data Streams                    | Streams keep records for a retention period and support many consumers.                                         |
| [Q43](#questions-design-cost-optimised-architecturesanswer-key) | B   | Amazon Redshift                                | Redshift is columnar and built for analytics.                                                                   |
| [Q44](#questions-design-cost-optimised-architecturesanswer-key) | A   | Amazon API Gateway with AWS Lambda             | Both scale automatically and charge per request.                                                                |
| [Q45](#questions-design-cost-optimised-architecturesanswer-key) | C   | AWS Global Accelerator                         | Global Accelerator gives anycast static IPs and supports TCP and UDP.                                           |
| [Q46](#questions-design-cost-optimised-architecturesanswer-key) | D   | Amazon DynamoDB                                | DynamoDB is a managed key-value and document store.                                                             |
| [Q47](#questions-design-cost-optimised-architecturesanswer-key) | A   | Provisioned concurrency                        | Provisioned concurrency keeps environments initialised.                                                         |
| [Q48](#questions-design-cost-optimised-architecturesanswer-key) | A   | Cache the result in Amazon ElastiCache         | A cache serves repeated reads from memory.                                                                      |

Score: \_\_\_\_\_\_ / 14

## Answer key: Design cost-optimised architectures

| Q               | Ans | Answer                                                                                         | Why                                                                                  |
|-----------------|-----|------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| [Q49](#answer-key-design-secure-architectures) | C   | 3-year Savings Plan or Reserved Instances                                                      | Long commitments give the biggest discounts for steady use; Spot can be interrupted. |
| [Q50](#answer-key-design-secure-architectures) | A   | Spot Instances                                                                                 | Spot uses spare capacity at a large discount; interruptions are acceptable here.     |
| [Q51](#answer-key-design-secure-architectures) | B   | S3 Intelligent-Tiering                                                                         | It moves objects between tiers based on access.                                      |
| [Q52](#answer-key-design-secure-architectures) | A   | S3 Glacier Deep Archive                                                                        | Deep Archive is the lowest-cost class, with retrieval in hours.                      |
| [Q53](#answer-key-design-secure-architectures) | B   | S3 Glacier Instant Retrieval                                                                   | Instant Retrieval suits rarely accessed data that still needs immediate access.      |
| [Q54](#answer-key-design-secure-architectures) | D   | An S3 Lifecycle configuration                                                                  | Lifecycle rules handle transitions and expiration.                                   |
| [Q55](#answer-key-design-secure-architectures) | C   | AWS Budgets                                                                                    | Budgets sends alerts on actual or forecast spend.                                    |
| [Q56](#answer-key-design-secure-architectures) | C   | Stop them on a schedule (for example EventBridge with a Lambda function or Instance Scheduler) | Stopped instances do not incur compute charges (EBS storage still does).             |
| [Q57](#answer-key-design-secure-architectures) | B   | AWS Compute Optimizer                                                                          | It analyses utilisation metrics and suggests instance types.                         |
| [Q58](#answer-key-design-secure-architectures) | B   | Data transferred into AWS from the internet                                                    | Inbound transfer is free; outbound, inter-Region and cross-AZ transfer are charged.  |
| [Q59](#answer-key-design-secure-architectures) | C   | Run them on AWS Fargate                                                                        | Fargate charges for the resources a task uses while it runs.                         |
| [Q60](#answer-key-design-secure-architectures) | A   | A gateway VPC endpoint for DynamoDB                                                            | DynamoDB, like S3, supports free gateway endpoints.                                  |

Score: \_\_\_\_\_\_ / 12

## Final revision plan, 5–18 Apr 2027

Your semester exams run until 7 April, so the first three days are light. Exam in the week of 19 April.

|     | Day        | Focus              | Do                                                                                                                                                        |
|-----|------------|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| ☐   | Mon 5 Apr  | Light (exam week)  | 30 min: re-read the Secure notes page and the service table.                                                                                              |
| ☐   | Tue 6 Apr  | Light (exam week)  | 30 min: re-read the Resilient notes page.                                                                                                                 |
| ☐   | Wed 7 Apr  | Light (exam week)  | 30 min: re-read the High-performing and Cost notes pages.                                                                                                 |
| ☐   | Thu 8 Apr  | Secure, part 1     | IAM, policy evaluation, Organizations and SCPs, STS. Do practice questions 1–9 here. Read the IAM FAQs.                                                   |
| ☐   | Fri 9 Apr  | Secure, part 2     | VPC security, KMS, Secrets Manager, WAF, GuardDuty, Macie. Questions 10–18. Build a VPC with public and private subnets in the free tier, then delete it. |
| ☐   | Sat 10 Apr | Resilient          | Multi-AZ, Auto Scaling, ELB, SQS and SNS, Route 53, DR strategies. Questions 19–34.                                                                       |
| ☐   | Sun 11 Apr | Mock 1             | Take the official sample questions and the free AWS Skill Builder practice question set under exam timing. Log every miss.                                |
| ☐   | Mon 12 Apr | High-performing    | Caching, CloudFront vs Global Accelerator, EBS types, databases, analytics. Questions 35–48.                                                              |
| ☐   | Tue 13 Apr | Cost-optimised     | Pricing models, S3 classes, lifecycle, data transfer, Budgets. Questions 49–60.                                                                           |
| ☐   | Wed 14 Apr | Weak areas         | Redo every question you got wrong. Re-read those topics in the AWS docs and FAQs.                                                                         |
| ☐   | Thu 15 Apr | Well-Architected   | Read the six pillars of the Well-Architected Framework. Redo the service table from memory.                                                               |
| ☐   | Fri 16 Apr | Mock 2             | All 60 questions in this pack, mixed, in 120 minutes (or a full 65-question practice exam if you have one). Aim for 80% or more.                          |
| ☐   | Sat 17 Apr | Review             | Review mock 2 explanations; final pass over this pack's notes pages.                                                                                      |
| ☐   | Sun 18 Apr | Rest and logistics | Light review only. Check the exam booking, ID and test-centre or online-proctoring requirements.                                                          |

### Free resources

- [Official exam page](https://aws.amazon.com/certification/certified-solutions-architect-associate/): exam guide and sample questions.
- [AWS Skill Builder](https://skillbuilder.aws/): free exam-prep course and official practice question set.
- [Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/): the six pillars.
- [AWS FAQs](https://aws.amazon.com/faqs/) for IAM, VPC, S3, EC2, RDS, DynamoDB: many exam details come from these.
- Free tier: build a VPC, an ALB with an Auto Scaling group, and an S3 static site; delete everything after and set an AWS Budgets alert first.
