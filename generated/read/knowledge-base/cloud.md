# Cloud

[All categories](README.md) · 5 topics

## Topics

- [AWS IAM and least privilege](#aws-iam-and-least-privilege)
- [ABAC: attribute-based access control](#abac-attribute-based-access-control)
- [CloudTrail and CloudWatch alarms](#cloudtrail-and-cloudwatch-alarms)
- [TenantWall (your research project)](#tenantwall-your-research-project)
- [AWS core services and the SAA-C03 exam](#aws-core-services-and-the-saa-c03-exam)

## AWS IAM and least privilege

*Level 1: Core*

Week 1 of your AWS track and the heart of TenantWall. The most important AWS service for security roles.

**Key idea**

Principals (users, roles) get permissions from JSON policies: Effect (Allow/Deny), Action, Resource, Condition. Roles give temporary credentials and are preferred over long-lived user keys.

Evaluation logic: everything starts as an implicit deny; an Allow grants access; an explicit Deny anywhere always wins (over any Allow). Permission boundaries and SCPs cap what can be allowed.

Tools from your professor's list: the IAM Policy Generator builds policy JSON; IAM Access Analyzer finds resources shared outside your account and validates policies; it can generate least-privilege policies from CloudTrail activity.


**Points**

- Explicit deny \> allow \> implicit deny
- Never use the root account day to day; enable MFA
- Use roles for EC2/Lambda, not access keys

```text
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Deny",
    "Action": "s3:*",
    "Resource": "*",
    "Condition": {"Bool": {"aws:SecureTransport": "false"}}
  }]
}
```

**Traps**

- Policies with "Action": "\*" and "Resource": "\*"

**Interviewers ask**

- Explain IAM policy evaluation.
- Role vs user?
- How do you achieve least privilege?

**Learn more**

- [AWS docs: policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [AWS docs: IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html)
- [flaws2.cloud](http://flaws2.cloud)

**Related:** [ABAC: attribute-based access control](#abac-attribute-based-access-control) · [TenantWall (your research project)](#tenantwall-your-research-project) · [CloudTrail and CloudWatch alarms](#cloudtrail-and-cloudwatch-alarms)

[Back to the topic list](#topics)

## ABAC: attribute-based access control

*Level 3: Advanced*

The core idea of your TenantWall paper.

**Key idea**

RBAC grants by role; ABAC grants by matching attributes. In AWS, attributes are tags on principals (aws:PrincipalTag/tenant) and on resources (aws:ResourceTag/tenant). One policy can say 'allow only when the principal's tenant tag equals the resource's tenant tag', so adding a tenant needs no new policy.

For S3, use object or bucket tags, or prefix-based conditions (s3:prefix with ${aws:PrincipalTag/tenant}). Protect the tags themselves: deny changing tenant tags (aws:TagKeys, aws:RequestTag) so a user can't re-tag into another tenant.


**Points**

- Scales better than one role per tenant
- Pair with an explicit deny on tag modification
- Test isolation with two tenant users (should get AccessDenied)

```text
"Condition": {
  "StringEquals": {
    "aws:ResourceTag/tenant": "${aws:PrincipalTag/tenant}"
  }
}
```

**Traps**

- Letting principals edit their own tags

**Interviewers ask**

- RBAC vs ABAC?
- How does TenantWall stop tenant A reading tenant B's data?

**Learn more**

- [AWS docs: What is ABAC?](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html)
- [AWS docs: ABAC tutorial](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_attribute-based-access-control.html)

**Related:** [AWS IAM and least privilege](#aws-iam-and-least-privilege) · [TenantWall (your research project)](#tenantwall-your-research-project) · [Broken access control and IDOR](security.md#broken-access-control-and-idor)

[Back to the topic list](#topics)

## CloudTrail and CloudWatch alarms

*Level 2: Interview-ready*

Your professor asked for exactly this in TenantWall: log every access attempt and alert on denied ones.

**Key idea**

CloudTrail records API calls (who, what, when, from where). Management events are on by default; S3 object-level reads and writes need data events enabled on the trail. Send the trail to CloudWatch Logs.

Create a metric filter on the log group with the pattern { ($.errorCode = "\*UnauthorizedOperation") \|\| ($.errorCode = "AccessDenied\*") }, which turns matching events into a metric. Put a CloudWatch alarm on it (e.g. ≥ 1 in 5 minutes) whose action publishes to an SNS topic with an email subscription.

Test: as tenant A, try to read tenant B's object; you should get AccessDenied, see the event in CloudTrail, the metric tick up and an email arrive.


**Points**

- Confirm the SNS email subscription or nothing arrives
- Data events cost money; limit them to TenantWall buckets
- This maps to OWASP A09 (logging and monitoring failures)

**Traps**

- Expecting S3 GetObject in CloudTrail without data events

**Interviewers ask**

- How would you detect unauthorised access attempts in AWS?

**Learn more**

- [AWS docs: CloudTrail data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html)
- [AWS docs: CloudWatch alarms for CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html)

**Related:** [TenantWall (your research project)](#tenantwall-your-research-project) · [AWS IAM and least privilege](#aws-iam-and-least-privilege)

[Back to the topic list](#topics)

## TenantWall (your research project)

*Level 3: Advanced*

Your strongest resume line: real cloud security research with a professor. It deserves a polished write-up, a diagram and a 2-minute interview story.

**Key idea**

What: multi-tenant isolation on EC2 and S3 using ABAC (tag-matched IAM policies), so tenants can't reach each other's resources.

Your professor's additions: a CloudTrail trail with S3 data events; a CloudWatch metric filter on AccessDenied/UnauthorizedOperation with an alarm and SNS email; policies built with the Policy Generator and checked with IAM Access Analyzer; a flowchart and an AWS-icon architecture diagram; explicit deny statements (confirm the exact meaning with your professor).

Plan: deadline 21 Mar 2027. Build in Dec–Jan, run isolation tests and collect evidence (screenshots, alarm emails), write in Feb–Mar.


**Points**

- Interview story: problem → design (ABAC) → how you proved isolation → what the alarm caught
- Diagram in diagrams.net with the AWS icon set
- Put the policies and test scripts on GitHub (no keys!)

**Traps**

- Committing AWS keys to GitHub
- Leaving resources running and getting billed

**Interviewers ask**

- Tell me about your project.
- How did you verify isolation?
- What would you change at 1,000 tenants?

**Learn more**

- [diagrams.net (AWS icons)](https://app.diagrams.net)
- [AWS docs: ABAC](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html)

**Related:** [ABAC: attribute-based access control](#abac-attribute-based-access-control) · [CloudTrail and CloudWatch alarms](#cloudtrail-and-cloudwatch-alarms) · [AWS IAM and least privilege](#aws-iam-and-least-privilege) · [Threat modelling (STRIDE)](security.md#threat-modelling-stride)

[Back to the topic list](#topics)

## AWS core services and the SAA-C03 exam

*Level 2: Interview-ready*

30 minutes a day from 16 Nov, exam in the week of 19 Apr 2027. Cloud skills plus a cert lift both SDE and security profiles.

**Key idea**

Compute: EC2 (instances, AMIs, security groups), Auto Scaling, Lambda. Storage: S3 (classes, versioning, lifecycle, encryption, Block Public Access), EBS, EFS. Databases: RDS (Multi-AZ for HA, read replicas for scale), DynamoDB, ElastiCache. Networking: VPC, public/private subnets, route tables, internet and NAT gateways, ALB/NLB, Route 53, CloudFront. Integration: SQS, SNS. Security: IAM, KMS, CloudTrail, GuardDuty.

Exam domains: secure architectures 30%, resilient 26%, high-performing 24%, cost-optimised 20%. 65 questions, 130 minutes, pass mark 720/1000.


**Points**

- Multi-AZ = availability; read replica = read scale
- NAT gateway lets private subnets reach the internet outbound only
- Set a billing alarm in week 1

**Traps**

- Only watching videos; do the labs
- Leaving NAT gateways running (they cost hourly)

**Interviewers ask**

- Design a highly available web app on AWS.
- Security group vs NACL?

**Learn more**

- [AWS SAA-C03 exam guide](https://aws.amazon.com/certification/certified-solutions-architect-associate/)
- [freeCodeCamp SAA course (YouTube)](https://www.youtube.com/@freecodecamp)
- [AWS Skill Builder (free tier)](https://skillbuilder.aws)

**Related:** [AWS IAM and least privilege](#aws-iam-and-least-privilege) · [Load balancing, replication and sharding](design.md#load-balancing-replication-and-sharding) · [High-level system design (HLD)](design.md#high-level-system-design-hld)

[Back to the topic list](#topics)
