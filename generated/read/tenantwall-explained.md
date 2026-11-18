TENANTWALL · STUDY MATERIAL

# TenantWall explained every term, policy and alarm

Everything about your project in one place: the idea, every AWS term, how AWS decides each request, your three policies statement by statement, what decides each of the 14 scenarios, what every monitoring setting means, tonight's real results for your professor's five requests, a 10-minute demo, and the questions he may ask.

| Section                                                                         |
|---------------------------------------------------------------------------------|
| [1. TenantWall in plain words](#01-tenantwall-in-plain-words)                                         |
| [2. Every AWS term you will hear](#02-every-aws-term-you-will-hear)                                      |
| [3. How AWS decides every request](#03-how-aws-decides-every-request)                                     |
| [4. TenantABAC_EC2, statement by statement](#04-tenantabac_ec2-statement-by-statement)                            |
| [5. TenantABAC_S3 and the bucket policy](#05-tenantabac_s3-and-the-bucket-policy)                               |
| [6. The 14 scenarios and what decides each](#06-the-14-scenarios-and-what-decides-each)                            |
| [7. Monitoring: CloudTrail, CloudWatch, SNS (what each setting means)](#07-monitoring-cloudtrail-cloudwatch-sns-what-each-setting-means) |
| [8. Tonight's evidence (17 Nov 2026)](#08-tonights-evidence-17-nov-2026)                                 |
| [9. Policy Generator: exactly what to type](#09-policy-generator-exactly-what-to-type)                           |
| [10. Talking about TenantWall in interviews](#10-talking-about-tenantwall-in-interviews)                          |
| [11. Showing your professor (10 minutes)](#11-showing-your-professor-10-minutes)                             |
| [12. Questions he may ask, with answers](#12-questions-he-may-ask-with-answers)                              |
| [Sources (16)](#-sources)                                                        |

Based on your real setup (account in us-east-1, users alpha_user, beta_user, twadmin; policies TenantABAC_EC2 and TenantABAC_S3; the lab bucket policy) and on the run of 17 Nov 2026: 14 of 14 scenarios, two alarms fired, Access Analyzer 0 findings.

## 01. TenantWall in plain words

- **The problem:** several teams share **one AWS account**. By default, any user with EC2 or S3 permissions could touch another team's servers and files.
- **The usual fix (RBAC):** one role or policy per team. It works, but the number of policies grows with every new team, and someone must edit IAM each time.
- **TenantWall's fix (ABAC):** put a **Team tag** on every user and every resource, and write **one** set of policies that says "you may touch a resource only if its Team tag equals your Team tag". Adding a team means adding tags, not policies.^([\[1\]](#-sources))
- **Four layers:** (1) tagged IAM users; (2) `TenantABAC_EC2` for servers; (3) `TenantABAC_S3` for files under your team's folder (prefix); (4) a **bucket policy** that blocks other teams' prefixes and unencrypted HTTP even if an identity policy is wrong.
- **Proof:** 14 scenarios (allowed and refused) run with real users alpha_user and beta_user; tonight: **14 of 14 passed**.
- **Your professor's additions (now done):** CloudTrail records every call, CloudWatch counts refusals and tag/policy changes and emails the admin, explicit vs implicit deny is labelled for every refusal, Access Analyzer validates the policies, and the diagrams use official AWS icons.

## 02. Every AWS term you will hear

| Term                          | Meaning in one or two lines                                                                                                                                             |
|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AWS account                   | The container for everything; has a 12-digit ID. TenantWall's teams all live in one account.                                                                            |
| Region                        | A geographic location (yours: us-east-1). Most resources live in one region; IAM is global.                                                                             |
| Root user                     | The account owner's login. Powerful and risky: use an admin IAM user (twadmin) for daily work.                                                                          |
| IAM user                      | A person or program with long-term credentials: alpha_user, beta_user, twadmin.                                                                                         |
| Access key / CLI profile      | The key pair the AWS CLI uses. Your profiles admin, alpha and beta each hold one user's keys in ~/.aws/credentials.                                                     |
| STS                           | Security Token Service: temporary credentials, 'who am I' (GetCallerIdentity), and decoding EC2 refusal messages.                                                       |
| Tag                           | A key=value label on a user or resource, e.g. Team=alpha. ABAC decides from tags.                                                                                       |
| ARN                           | Amazon Resource Name: arn:partition:service:region:account:resource, e.g. arn:aws:s3:::bucket/alpha/report.txt (S3 has no region/account in object ARNs).               |
| Policy                        | A JSON document of permissions. Identity-based = attached to a user, group or role. Resource-based = attached to the resource (the bucket policy).                      |
| Statement / Sid               | One rule inside a policy; Sid is its name (e.g. NoSelfPromotion).                                                                                                       |
| Effect                        | Allow or Deny.                                                                                                                                                          |
| Action                        | The API call(s), e.g. ec2:RunInstances, s3:GetObject. Wildcards allowed: ec2:Describe\*.                                                                                |
| Resource / NotResource        | Which ARNs the statement covers; NotResource = every ARN except these.                                                                                                  |
| Principal                     | Who the statement applies to; only in resource-based policies ("\*" = anyone).                                                                                          |
| Condition                     | Extra tests that must be true, built from an operator and a key: StringEquals { ec2:ResourceTag/Team: ... }.^([\[2\]](#-sources))                                        |
| Policy variable               | \${aws:PrincipalTag/Team} is replaced at request time by the caller's Team tag: one policy works for every team.^([\[3\]](#-sources))                                    |
| Explicit deny                 | A Deny statement matched. It beats every Allow, anywhere.^([\[4\]](#-sources))                                                                                           |
| Implicit deny                 | Nothing allowed the request. The default for everything.                                                                                                                |
| DryRun                        | EC2 checks permissions without doing the action: success shows as DryRunOperation, refusal as UnauthorizedOperation.                                                    |
| Encoded authorization message | EC2 refusals include an encoded blob; sts:DecodeAuthorizationMessage turns it into JSON showing explicitDeny true or false and the matched context.^([\[5\]](#-sources)) |

^([\[6\]](#-sources))

## 03. How AWS decides every request

1.  Start with **deny by default** (implicit).
2.  Collect every policy that applies: the caller's identity policies, the resource's policy (bucket policy), and any boundaries or organisation rules.
3.  If **any statement with Effect Deny matches**, the answer is **explicit deny**. Stop.
4.  Otherwise, if an **Allow** matches (in the same account, an identity policy or the resource policy is enough), the answer is **allow**.
5.  Otherwise it stays **implicit deny**.

^([\[4\]](#-sources))

Why TenantWall uses both: implicit deny is the quiet default (alpha is simply never allowed to touch beta); explicit Deny statements are a **second lock** that still holds if someone later adds a too-broad Allow. This is the explicit vs implicit deny your professor asked for.

## 04. TenantABAC_EC2, statement by statement

| Sid                                       | What it says                                                                                                       | Why                                                                                                                          |
|-------------------------------------------|--------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| ReadOnlyEverywhere                        | Allow ec2:Describe\* on \*                                                                                         | Describe calls cannot be limited per resource, so every team can see the list of instances (a stated limitation).            |
| ManageOnlyOwnTeamInstances                | Allow Start/Stop/Reboot/Terminate on instances where ec2:ResourceTag/Team = \${aws:PrincipalTag/Team}              | You may operate an instance only if its Team tag equals yours (scenarios 6, 7).                                              |
| LaunchOnlyIfTaggedWithOwnTeamAndSmallType | Allow RunInstances for the instance only if the request tags Team = your team and the type is t2.micro or t3.micro | No untagged, wrongly tagged or large instances (scenarios 2, 3, 4).^([\[7\]](#-sources))                                      |
| RunInstancesSupportingResources           | Allow RunInstances on every resource except the instance (NotResource)                                             | A launch also touches the image, subnet, security group, volume and network interface; those need permission too.            |
| TagOnlyAtCreation                         | Allow CreateTags only when ec2:CreateAction = RunInstances                                                         | Tags can be set while launching, never changed later, so nobody can relabel an instance into another team (scenario 8).      |
| DecodeOwnDenials                          | Allow sts:DecodeAuthorizationMessage                                                                               | Lets a user read why EC2 refused them (used to label explicit vs implicit).                                                  |
| NoSelfPromotion                           | **Deny** iam:TagUser, UntagUser, PutUserPolicy, AttachUserPolicy, AddUserToGroup                                   | Without it a user could change their own Team tag or permissions and walk into another team: the explicit lock (scenario 9). |

## 05. TenantABAC_S3 and the bucket policy

### TenantABAC_S3 (identity policy)

| Statement | What it allows                                                                                                                                   |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| Objects   | GetObject, PutObject, DeleteObject on bucket/\${aws:PrincipalTag/Team}/\*: only inside your own team's folder                                    |
| Listing   | ListBucket on the bucket only when s3:prefix matches \${aws:PrincipalTag/Team}/\*: you can list your folder, not others' (scenario 12, implicit) |

### Bucket policy (resource policy, the second lock)

| Sid                         | What it denies                                                                                                                  |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| DenyNonTLS                  | Everything, for everyone, when aws:SecureTransport is false: no plain-HTTP access (scenario 13, explicit).^([\[8\]](#-sources))  |
| OnlyAlphaTouchesAlphaPrefix | Any S3 action on alpha/\* unless the caller's Team tag is alpha or the caller is the admin user (ArnNotEquals aws:PrincipalArn) |
| OnlyBetaTouchesBetaPrefix   | The same for beta/\*: alpha reading beta/secret.txt is an **explicit** deny (scenario 11)                                       |

Two conditions in one statement are joined with AND: the Deny applies only when the caller is not that team **and** not the admin. Inside one condition key, several values are OR.

## 06. The 14 scenarios and what decides each

| \#  | Who / what                                                  | Result       | Deny type | Decided by                                                    |
|-----|-------------------------------------------------------------|--------------|-----------|---------------------------------------------------------------|
| 1   | alpha launches t3.micro tagged Team=alpha                   | Allowed      | —         | LaunchOnlyIfTagged… + SupportingResources + TagOnlyAtCreation |
| 2   | alpha launches with no Team tag (DryRun)                    | Refused      | Implicit  | aws:RequestTag/Team missing, so no Allow matches              |
| 3   | alpha launches tagged Team=beta (DryRun)                    | Refused      | Implicit  | Tag ≠ own team                                                |
| 4   | alpha launches t3.large (DryRun)                            | Refused      | Implicit  | Type not t2/t3.micro                                          |
| 5   | beta launches its own t3.micro                              | Allowed      | —         | Same statements, for beta                                     |
| 6   | alpha stops beta's instance (DryRun)                        | Refused      | Implicit  | ResourceTag/Team ≠ alpha                                      |
| 7   | alpha stops its own instance (DryRun)                       | Allowed      | —         | ManageOnlyOwnTeamInstances                                    |
| 8   | alpha retags its instance to Team=beta (DryRun)             | Refused      | Implicit  | TagOnlyAtCreation: not during RunInstances                    |
| 9   | alpha tags itself Team=beta (IAM)                           | Refused      | Explicit  | NoSelfPromotion                                               |
| 10  | alpha uploads alpha/scenario10-report.txt                   | Allowed      | —         | TenantABAC_S3                                                 |
| 11  | alpha reads beta/secret.txt                                 | Refused      | Explicit  | Bucket policy OnlyBetaTouchesBetaPrefix                       |
| 12  | alpha lists beta/                                           | Refused      | Implicit  | ListBucket allowed only for alpha/ prefix                     |
| 13  | alpha reads its own file over plain HTTP                    | Refused      | Explicit  | Bucket policy DenyNonTLS                                      |
| 14  | Simulator: alpha_user TerminateInstances on beta's instance | implicitDeny | Implicit  | No Allow for another team's instance                          |

**Tonight (17 Nov 2026) on the real account: 14 of 14 matched.** Afterwards alpha_user still had Team=alpha and its instance kept Team=alpha: no refused call changed anything. The script cleaned up both instances and the uploaded file. Log: real_aws_run_log_2026-11-17.txt in your folder.

## 07. Monitoring: CloudTrail, CloudWatch, SNS (what each setting means)

| Piece (your name)                              | Setting                                                                                              | Meaning                                                                                                                                  |
|------------------------------------------------|------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| CloudTrail trail (tenantwall-trail)            | Multi-region, global service events                                                                  | Records API calls in every region, plus IAM (a global service).^([\[9\]](#-sources))                                                      |
|                                                | Management events: All                                                                               | Control-plane calls: RunInstances, TagUser, PutBucketPolicy … (reads and writes).                                                        |
|                                                | Data events: S3 objects in the lab bucket                                                            | Object-level calls such as GetObject and PutObject; off by default and billed, so limited to one bucket.^([\[10\]](#-sources))            |
|                                                | Log file validation                                                                                  | CloudTrail signs digest files so you can prove logs were not altered.^([\[11\]](#-sources))                                               |
| Log bucket (tenantwall-logs-…)                 | Private, versioned, encrypted; bucket policy lets only this trail write (aws:SourceArn), denies HTTP | Where the raw log files go; nobody else can write or read over plain HTTP.                                                               |
| CloudWatch Logs group (/tenantwall/cloudtrail) | 30-day retention; role TenantWallCloudTrailToCWL                                                     | A searchable copy of the events; the role lets CloudTrail write into it (logs:CreateLogStream, PutLogEvents).                            |
| Metric filter AccessDenied                     | { (\$.errorCode = "AccessDenied\*") \|\| (\$.errorCode = "\*UnauthorizedOperation") }                | Each matching event adds 1 to metric TenantWall/AccessDenied. \$. reads a JSON field; \* is a wildcard; \|\| is OR.^([\[12\]](#-sources)) |
| Metric filter TagTampering                     | TagUser, UntagUser, DeleteTags, group/policy changes to users, or a refused CreateTags               | Someone touched the labels or memberships the wall depends on.                                                                           |
| Metric filter PolicyChange                     | PutBucketPolicy, DeleteBucketPolicy, PutUserPolicy, PutGroupPolicy, CreatePolicyVersion              | Someone edited a lock itself.                                                                                                            |
| Alarms TenantWall-\*                           | Statistic Sum, period 300 s, 1 evaluation period, threshold ≥ 1, missing data = not breaching        | If the count in any 5 minutes is at least 1 → state ALARM → action. No data counts as fine (OK).^([\[13\]](#-sources))                    |
|                                                | States OK / ALARM / INSUFFICIENT_DATA                                                                | OK = below threshold; ALARM = breached; INSUFFICIENT_DATA = not enough data yet.                                                         |
| SNS topic (tenantwall-alerts)                  | Email subscription (confirmed)                                                                       | The alarm publishes to the topic; SNS emails every confirmed subscriber.^([\[14\]](#-sources))                                            |

## 08. Tonight's evidence (17 Nov 2026)

| Professor's request                       | Status                                     | Evidence (in your folder)                                                                                                                                                                                                                                                                                                                                                                          |
|-------------------------------------------|--------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1\. CloudTrail                            | Done, logging                              | Trail logging, multi-region, S3 data events on the lab bucket. Logs Insights shows alpha_user's refused EC2/IAM calls (evidence/refused-calls.txt) and the S3 object calls: GetObject beta/secret.txt AccessDenied (scenario 11), ListObjects AccessDenied (12), GetObject over HTTP AccessDenied (13), plus the allowed PutObject/DeleteObject of scenario 10 (evidence/s3-data-events-alpha.txt) |
| 2\. CloudWatch + email                    | Done, fired                                | After the run: TenantWall-AccessDenied and TenantWall-TagTampering went to ALARM; PolicyChange stayed OK (no policy edited); alert emails sent to your confirmed address (evidence/alarms.txt; your inbox)                                                                                                                                                                                         |
| 3\. Diagrams                              | Files ready; you export                    | diagrams/tenantwall-architecture.drawio and diagrams/tenantwall-flowchart.drawio with official AWS icons: open at app.diagrams.net, check, export PNG                                                                                                                                                                                                                                              |
| 4\. Policy Generator + Access Analyzer    | Analyzer done; Generator is yours (10 min) | Access Analyzer: **0 findings** for TenantABAC_EC2, TenantABAC_S3 and the bucket policy. Policy Generator: rebuild the bucket policy in the web form^([\[15\]](#-sources)) and screenshot it                                                                                                                                                                                                        |
| 5\. Explicit vs implicit deny (confirmed) | Done                                       | Every refusal labelled explicit or implicit (scenarios 9, 11, 13 explicit; 2, 3, 4, 6, 8, 12, 14 implicit); EC2 refusals proved with sts decode-authorization-message, S3/IAM refusals by the error message, scenario 14 by the policy simulator (implicitDeny)                                                                                                                                    |

^([\[16\]](#-sources))

### Screenshots to take tomorrow morning (console, 15 minutes)

- CloudTrail → Trails → tenantwall-trail (Logging on, data events).
- CloudWatch → Alarms (history showing ALARM at about 23:23 IST on 17 Nov).
- The alert email in Gmail.
- CloudWatch → Logs Insights with the refused-calls query.
- IAM → Policies → TenantABAC_EC2 → Edit (Access Analyzer panel with no findings).
- Policy Generator page with your bucket policy.
- The exported diagrams.

## 09. Policy Generator: exactly what to type

Open the AWS Policy Generator^([\[15\]](#-sources)). You rebuild your bucket policy's three statements, generate it, and take a screenshot. **Do not paste the generated JSON over your real bucket policy**: it is only to show your professor that the generator produces the same rules. Replace YOUR-BUCKET and ACCOUNT-ID with your real values (they are in evidence/bucket-policy.json on your laptop).

### Step 1: Select Policy Type

S3 Bucket Policy.

### Step 2: Add Statement(s): three times

| Field                      | Statement A: DenyNonTLS                               | Statement B: alpha prefix                                              | Statement C: beta prefix                                               |
|----------------------------|-------------------------------------------------------|------------------------------------------------------------------------|------------------------------------------------------------------------|
| Effect                     | Deny                                                  | Deny                                                                   | Deny                                                                   |
| Principal                  | \*                                                    | \*                                                                     | \*                                                                     |
| Actions                    | tick All Actions ("\*")                               | tick All Actions ("\*")                                                | tick All Actions ("\*")                                                |
| Amazon Resource Name (ARN) | arn:aws:s3:::YOUR-BUCKET, arn:aws:s3:::YOUR-BUCKET/\* | arn:aws:s3:::YOUR-BUCKET/alpha/\*                                      | arn:aws:s3:::YOUR-BUCKET/beta/\*                                       |
| Add Conditions: 1st        | Bool · aws:SecureTransport · false                    | StringNotEquals · aws:PrincipalTag/\${TagKey} · alpha                  | StringNotEquals · aws:PrincipalTag/\${TagKey} · beta                   |
| Add Conditions: 2nd        | —                                                     | ArnNotEquals · aws:PrincipalArn · arn:aws:iam::ACCOUNT-ID:user/twadmin | ArnNotEquals · aws:PrincipalArn · arn:aws:iam::ACCOUNT-ID:user/twadmin |

For each statement: fill the fields, click **Add Condition** once per condition row, then **Add Statement**. When all three appear in the list, go to Step 3 and click **Generate Policy**. In the JSON window that opens, replace each `${TagKey}` with `Team` (the window is editable), then screenshot the statement list and the JSON.

**Compare with your real policy:** same Effect, Principal, Action, Resource and Condition in each statement. The generator adds an Id and numbered Sids instead of your names (DenyNonTLS, OnlyAlphaTouchesAlphaPrefix, OnlyBetaTouchesBetaPrefix): that difference is expected. Done on 18 Nov 2026: with these values the generator produced exactly your three statements (apart from the Sids), and IAM Access Analyzer reported no findings for it (evidence/policy-generator-output.json and policy-generator-access-analyzer.txt on your laptop). Then paste the generated JSON into IAM Access Analyzer's policy check (bucket policy editor) to show it validates.

## 10. Talking about TenantWall in interviews

### 30 seconds

"Teams sharing one AWS account can reach each other's servers and files. I built TenantWall, which isolates them with attribute-based access control: one set of IAM policies compares the Team tag on the user with the Team tag on the resource, and explicit denies stop users from changing their own tags. I tested it with 14 real scenarios on AWS, all as expected, and added CloudTrail and CloudWatch alerting that emailed the admin about refused attempts in under 3 minutes."

### 2 minutes (STAR)

| Part      | What to say                                                                                                                                                                                                                                                                                                                                                           |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Situation | Several teams in one AWS account; by default anyone with EC2 or S3 rights could touch another team's resources. Role-per-team policies grow with every team.                                                                                                                                                                                                          |
| Task      | Isolate teams with a fixed number of policies, prove it works, and detect attempts to break it. Research project with my professor.                                                                                                                                                                                                                                   |
| Action    | Tagged users and resources with Team; wrote two ABAC identity policies (EC2, S3) using \${aws:PrincipalTag/Team}; locked tags after creation; explicit Deny on self-tagging; bucket policy denying other prefixes and plain HTTP; validated with IAM Access Analyzer; CloudTrail with S3 data events into CloudWatch Logs, three metric filters, alarms to SNS email. |
| Result    | 14 of 14 scenarios behaved as expected (10 refusals, each classified explicit or implicit); Access Analyzer found nothing; alarms emailed within 104–143 seconds. I also found a limitation: the filter alerts on any refused call in the account, so the next step is scoping it to tenant users.                                                                    |

### Resume bullets (real numbers)

- Designed attribute-based access control for a shared S3 bucket and EC2 fleet so each team reaches only its own resources, using tag-matched IAM policies and explicit denies; validated with IAM Access Analyzer (0 findings)
- Verified isolation with 14 scenarios on real AWS (10 refusals, each classified as explicit or implicit deny) and built CloudTrail → CloudWatch → SNS alerting that emailed on refused calls within 3 minutes

### Follow-up questions to expect

- Why not one AWS account per team? (stronger isolation; TenantWall is for teams that must share one account; accounts are the next step)
- What if an admin tags a resource wrongly? (the model trusts tags; tag changes alarm; tagging is restricted to creation)
- How would you scale to 100 teams? (identity policies stay the same; the bucket policy grows, so move to per-team buckets or accounts)

## 11. Showing your professor (10 minutes)

| Minute | Show                                                                  | Say                                                                                                                        |
|--------|-----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| 0–1    | Architecture diagram                                                  | "Two teams share one account; one tag-based policy set separates them; the right side now detects attempts."               |
| 1–3    | Scenario summary (14 of 14) with the deny-type column                 | "Each refusal is labelled explicit or implicit: explicit means a Deny statement matched, implicit means no Allow matched." |
| 3–5    | Policies + Access Analyzer (0 findings) + Policy Generator screenshot | "Policies validate cleanly; the bucket policy matches what the Policy Generator produces."                                 |
| 5–7    | Logs Insights refused calls                                           | "CloudTrail now records every call, including object reads, with who, what and when."                                      |
| 7–9    | Alarms in ALARM + email                                               | "Refusals and tag changes email the admin within minutes; policy edits have their own alarm."                              |
| 9–10   | Flowchart, limitations, next step                                     | "Next: update the paper and submit by 21 March. Which venue do you suggest?"                                               |

## 12. Questions he may ask, with answers

| Question                                                      | Answer                                                                                                                                                                     |
|---------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Why ABAC instead of a role per team?                          | Policy count stays fixed (2 identity policies) for any number of teams; only the bucket policy grows by one statement per team.                                            |
| What stops a user changing their own Team tag?                | NoSelfPromotion: an explicit Deny on TagUser/UntagUser and on changing their own policies or groups.                                                                       |
| What stops relabelling an instance later?                     | TagOnlyAtCreation: CreateTags is allowed only as part of RunInstances.                                                                                                     |
| Explicit vs implicit deny?                                    | Explicit = a Deny statement matched and beats all Allows; implicit = nothing allowed it. We label each refusal using the error message or the decoded EC2 message.         |
| Why a bucket policy if identity policies already restrict S3? | Defence in depth: if an identity policy is wrong or broadened, the bucket's explicit Deny still protects each team's prefix and blocks HTTP.                               |
| Why can every team see all instances?                         | ec2:Describe\* does not support resource-level permissions; it is listed as a limitation.                                                                                  |
| What are CloudTrail data events?                              | Object-level S3 calls like GetObject; management events alone would miss reads of other teams' files.                                                                      |
| How fast do alerts arrive?                                    | Minutes: CloudTrail delivers to CloudWatch Logs, the filter counts, the alarm evaluates every 5 minutes, SNS emails.                                                       |
| Can logs be tampered with?                                    | Log-file validation lets you prove integrity; the log bucket allows writes only from this trail and denies HTTP.                                                           |
| What did Access Analyzer report?                              | No errors, security warnings, warnings or suggestions for any of the three policies.                                                                                       |
| What if tagging is wrong?                                     | The model trusts correct tags at creation; that is why tags are locked after creation and changes alarm.                                                                   |
| Cost?                                                         | Management events in the first trail are free; S3 data events and CloudWatch Logs are billed per volume, so data events are limited to one bucket.                         |
| Why t2/t3.micro only?                                         | Cost control per team, enforced with the ec2:InstanceType condition (scenario 4).                                                                                          |
| What is \${aws:PrincipalTag/Team}?                            | A policy variable replaced at request time by the caller's Team tag.                                                                                                       |
| Limitations?                                                  | Shared Describe visibility, shared network and quotas, listing guarded on one side, EBS volumes not covered, bucket policy size limit, trust in tagging, small evaluation. |

## ··. Sources

Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.

1.  [AWS IAM: what is ABAC?](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html)  
    https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html
2.  [AWS IAM: condition operators](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition_operators.html)  
    https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition_operators.html
3.  [AWS IAM: policy variables](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_variables.html)  
    https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_variables.html
4.  [AWS IAM: policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)  
    https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html
5.  [AWS STS: DecodeAuthorizationMessage](https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html)  
    https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html
6.  [AWS IAM: JSON policy element reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html)  
    https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html
7.  [Amazon EC2: grant permission to tag resources during creation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/supported-iam-actions-tagging.html)  
    https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/supported-iam-actions-tagging.html
8.  [AWS IAM: global condition keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html)  
    https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html
9.  [AWS CloudTrail concepts](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html)  
    https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html
10. [AWS CloudTrail: data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html)  
    https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html
11. [AWS CloudTrail: log file integrity validation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html)  
    https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html
12. [CloudWatch Logs: filter pattern syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html)  
    https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html
13. [CloudWatch: using alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)  
    https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html
14. [Amazon SNS: email notifications](https://docs.aws.amazon.com/sns/latest/dg/sns-email-notifications.html)  
    https://docs.aws.amazon.com/sns/latest/dg/sns-email-notifications.html
15. [AWS Policy Generator](https://awspolicygen.s3.amazonaws.com/policygen.html)  
    https://awspolicygen.s3.amazonaws.com/policygen.html
16. [IAM Access Analyzer policy validation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html)  
    https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html
