TENANTWALL · ONE-DAY RUNBOOK

# Your professor's five changes done in one day

Everything to finish TenantWall's requested changes tomorrow and show them: (1) explicit vs implicit deny, (2) Policy Generator and Access Analyzer, (3) CloudTrail with S3 data events, (4) CloudWatch alarms with email, (5) an AWS-style architecture diagram and a method flowchart. Then the paper changes, a 10-minute demo script, the screenshots to take, and fixes for what usually goes wrong.

| Section                                                                 |
|-------------------------------------------------------------------------|
| [1. Tomorrow at a glance](#01-tomorrow-at-a-glance)                                      |
| [2. Before you start (20 minutes)](#02-before-you-start-20-minutes)                             |
| [3. Step 1: explicit vs implicit deny (45 minutes)](#03-step-1-explicit-vs-implicit-deny-45-minutes)            |
| [4. Step 2: Policy Generator and Access Analyzer (45 minutes)](#04-step-2-policy-generator-and-access-analyzer-45-minutes) |
| [5. Step 3: CloudTrail with S3 data events (45 minutes)](#05-step-3-cloudtrail-with-s3-data-events-45-minutes)       |
| [6. Step 4: CloudWatch alarms and email (60 minutes)](#06-step-4-cloudwatch-alarms-and-email-60-minutes)          |
| [7. Step 5: architecture diagram and flowchart (60 minutes)](#07-step-5-architecture-diagram-and-flowchart-60-minutes)  |
| [8. Step 6: update the paper (40 minutes)](#08-step-6-update-the-paper-40-minutes)                    |
| [9. Showing it to your professor (10 minutes)](#09-showing-it-to-your-professor-10-minutes)                |
| [10. If something goes wrong, costs and cleanup](#10-if-something-goes-wrong-costs-and-cleanup)              |
| [Sources (10)](#-sources)                                                |

Work in the order of the sections; each step produces evidence the next one uses. Files: `generated/tenantwall/runbook/` (CLI commands, filter patterns, Logs Insights query).

## 01. Tomorrow at a glance

Your professor's five requests, done in one day in an order where each step feeds the next. Times are working time; take the breaks.

| Time      | Step                                                  | Done when                                                               |
|-----------|-------------------------------------------------------|-------------------------------------------------------------------------|
| 0:00–0:20 | Before you start (Section 2)                          | Signed in as your admin IAM user, right region, budget alert on         |
| 0:20–1:05 | **1. Explicit vs implicit deny** (Section 3)          | Simulator screenshots for both kinds; test table has a deny-type column |
| 1:05–1:50 | **2. Policy Generator + Access Analyzer** (Section 4) | Bucket policy regenerated; all three policies validate with no errors   |
| 1:50–2:35 | **3. CloudTrail with S3 data events** (Section 5)     | Trail logging; refused GetObject visible in CloudWatch Logs             |
| Break     |                                                       |                                                                         |
| 2:50–3:50 | **4. CloudWatch alarms + email** (Section 6)          | Both alarms fired and the emails arrived                                |
| 3:50–4:50 | **5. Architecture diagram + flowchart** (Section 7)   | Two diagrams exported as PNG                                            |
| 4:50–5:30 | Update the paper (Section 8)                          | New subsections and test-table column written                           |
| 5:30–6:00 | Rehearse the demo (Section 9)                         | You can show everything in 10 minutes                                   |

**Names used here are your real ones:** tag key `Team`, policies `TenantABAC_EC2` and `TenantABAC_S3`, the bucket policy with `DenyNonTLS` and one prefix Deny per team, and `tenantwall_tests.py` (14 tests). The sample JSON in [generated/tenantwall/policies/](https://github.com/kvp342/intrusion-detection-and-prevention/tree/ccr-ca7232a7-t7lq94/generated/tenantwall/policies) uses a lowercase `tenant` placeholder: do not paste those over your working policies.

## 02. Before you start (20 minutes)

- **Sign in as your admin IAM user**, not the root user. Check the region at the top right is the one your TenantWall resources are in.
- **Budget alert:** if you have none, Billing → Budgets → Create budget → monthly cost budget, 1 USD, your email. Data events and logs cost a little; this catches surprises.
- **Re-run your tests first:** `python3 tenantwall_tests.py` should still show 14 of 14 passing. If not, fix that before adding anything.
- **Make a screenshots folder** and name files as in Section 9 (S1, S2 …) so the paper and the demo use the same evidence.
- **Write down:** account ID, region, bucket name, one user from team A (call it USER_A) and one from team B, an object key under team B's prefix, and your email for alerts.
- **Optional, for the CLI appendix:** AWS CLI v2 configured with your admin profile (`aws sts get-caller-identity` shows your admin user).

## 03. Step 1: explicit vs implicit deny (45 minutes)

**The idea in one line:** an *explicit deny* is a Deny statement that matches the request; it wins over every Allow. An *implicit deny* is the default when no Allow matches at all. Both refuse the request, but for different reasons, and the paper should show which one stopped each attack.^([\[1\]](#-sources))

### Show both kinds in the IAM policy simulator

1.  IAM → Policy simulator (or open the simulator from the user's page). Choose **USER_A**.
2.  **Explicit deny:** service S3, action `GetObject`, resource `arn:aws:s3:::BUCKET/TEAM_B/…` with the bucket policy included. Expect *denied*, matched by your per-team prefix Deny. Screenshot **S1**.
3.  **Explicit deny (identity side):** IAM `TagUser` on USER_A itself: matched by `NoSelfPromotion`. Screenshot **S2**.
4.  **Implicit deny:** an action none of your policies allows, for example EC2 `CreateVpc`. Expect *denied* with no matching statement. Screenshot **S3**.

^([\[2\]](#-sources))

### Confirm from a real refusal

When an EC2 call is refused, the error carries an encoded message. Decode it as admin: `aws sts decode-authorization-message --encoded-message …`. The decoded JSON says whether the request was allowed, whether it was an `explicitDeny`, and which statements matched.^([\[3\]](#-sources)) Screenshot **S4**.

### Add a column to your test table

| Test                           | Expected | Result  | Deny type | Stopped by                |
|--------------------------------|----------|---------|-----------|---------------------------|
| Team A reads team B's object   | Refused  | Refused | Explicit  | Bucket policy prefix Deny |
| Team A tags itself into team B | Refused  | Refused | Explicit  | NoSelfPromotion           |
| Team A creates a VPC           | Refused  | Refused | Implicit  | No Allow matched          |
| Team A reads own object        | Allowed  | Allowed | —         | TenantABAC_S3 Allow       |

Fill the real rows from your 14 tests; the four above are examples of each kind. **Ask your professor** (Section 9) whether "something explicit" meant exactly this, as your notes say to confirm.

## 04. Step 2: Policy Generator and Access Analyzer (45 minutes)

1.  Open the **AWS Policy Generator**^([\[4\]](#-sources)). Type: *S3 Bucket Policy*.
2.  Add the `DenyNonTLS` statement: Effect Deny, Principal `*`, Actions *All Actions*, ARN of the bucket and `bucket/*`, condition *Bool* `aws:SecureTransport` = `false`.
3.  Add one statement per team: Effect Deny, the object actions, ARN `bucket/TEAM_X/*`, and the condition that excludes that team and your admin ARN, exactly as in your current bucket policy.
4.  Generate the JSON. Compare it with your current bucket policy line by line; the generator may order keys differently but the meaning must be the same. Screenshot the generator page **S5**.
5.  S3 → bucket → Permissions → Bucket policy → Edit → paste. The editor runs **IAM Access Analyzer policy checks** automatically^([\[5\]](#-sources)): fix any *errors* and *security warnings*, then save. Screenshot the clean checks **S6**.
6.  Open `TenantABAC_EC2` and `TenantABAC_S3` in IAM → Policies → Edit (JSON) and read the Access Analyzer findings panel for each. Screenshot **S7**. Do not save changes you do not understand.
7.  Re-run `tenantwall_tests.py`: still 14 of 14.

Sentence for the paper: "The bucket policy was produced with the AWS Policy Generator and, with both identity policies, validated by IAM Access Analyzer, which reported no errors or security warnings."

## 05. Step 3: CloudTrail with S3 data events (45 minutes)

Event history only keeps management events. Object reads such as `GetObject` are **data events**, which are recorded only by a trail that asks for them.^([\[6\]](#-sources))

1.  CloudTrail → Trails → **Create trail**. Name `tenantwall-trail`. Storage: a **new** S3 bucket for logs (separate from the tenant bucket).
2.  **CloudWatch Logs: Enabled**, new log group `/tenantwall/cloudtrail`, **new IAM role** (the console creates the role CloudTrail needs to write logs).^([\[7\]](#-sources))
3.  Events: Management events on (Read and Write). **Data events on**: S3, limited to **your tenant bucket only** (not all buckets: that costs more and adds noise).
4.  Create. Check the trail shows *Logging: On*. Screenshot the trail settings **S8**.
5.  Wait 5 minutes, then re-run `tenantwall_tests.py` so refused calls happen while the trail records.
6.  CloudWatch → Logs Insights → log group `/tenantwall/cloudtrail` → paste the query below → Run. You should see the refused `GetObject` with USER_A's ARN, team B's key and `AccessDenied`. Screenshot **S9**.^([\[8\]](#-sources))

``` text
fields @timestamp, eventName, errorCode, userIdentity.arn, requestParameters.bucketName, requestParameters.key
| filter errorCode like /AccessDenied|UnauthorizedOperation/
| sort @timestamp desc
| limit 20
```

Records reach CloudWatch Logs after a delay, often a few minutes. If nothing shows after 15 minutes, see Section 10.

## 06. Step 4: CloudWatch alarms and email (60 minutes)

1.  **SNS:** SNS → Topics → Create topic (Standard) `tenantwall-alerts` → Create subscription → Email → your address. **Open the email and click Confirm subscription**, or no alert will ever arrive.
2.  **Metric filter 1 (refused calls):** CloudWatch → Log groups → `/tenantwall/cloudtrail` → Metric filters → Create. Pattern below. Namespace `TenantWall`, metric `AccessDeniedCount`, value 1, default 0.^([\[9\]](#-sources))
3.  **Metric filter 2 (tag tampering):** same log group, second pattern below, metric `TagChangeCount`.
4.  **Alarm 1:** on `AccessDeniedCount`, statistic Sum, period 5 minutes, **≥ 3** (your professor's threshold), missing data = not breaching, action: notify `tenantwall-alerts`.
5.  **Alarm 2:** on `TagChangeCount`, Sum over 5 minutes, **≥ 1**, same topic.
6.  **Trigger them:** as USER_A, try three or more refused reads of team B's objects; then, as admin, add and remove a test tag on a spare instance. Wait up to about 15 minutes.
7.  Screenshot both alarms in *In alarm* state **S10** and the two emails **S11**.

### Filter patterns (checked syntax; also in the runbook folder)

``` text
Refused calls:
{ ($.errorCode = "*UnauthorizedOperation") || ($.errorCode = "AccessDenied*") }

Tag tampering:
{ ($.eventName = "CreateTags") || ($.eventName = "DeleteTags") || ($.eventName = "TagUser") || ($.eventName = "UntagUser") }
```

Sentence for the paper: TenantWall now **prevents** cross-team access (policies) and **detects** attempts (CloudTrail → CloudWatch metric filter → alarm → email within minutes).

## 07. Step 5: architecture diagram and flowchart (60 minutes)

- Open [draw.io (diagrams.net)](https://app.diagrams.net) → More Shapes → enable the **AWS** shape library (it contains the official AWS architecture icons^([\[10\]](#-sources))).
- **Architecture diagram:** the AWS account as a big box; inside it IAM (users tagged Team=A / Team=B, the Tenants group, the two identity policies), the S3 bucket with team prefixes and its bucket policy, EC2 instances tagged by team, and the new path CloudTrail → S3 log bucket and CloudWatch Logs → metric filters → alarms → SNS → email. Draw allowed paths in green, refused ones in red.
- **Method flowchart:** request → does an explicit Deny match? (yes → refused, explicit) → does an Allow match with Team equal to the resource's team or prefix? (no → refused, implicit; yes → allowed) → in every case CloudTrail records it → refused calls counted → alarm.
- Use [architecture.png](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/tenantwall/architecture.png) and [flowchart.png](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/tenantwall/flowchart.png) as a starting sketch, but redraw them with the official icons, since that is what your professor asked for.
- Export both as PNG at 300 DPI (File → Export as → PNG → zoom 300%) and save the .drawio files too: **S12**, **S13**.

## 08. Step 6: update the paper (40 minutes)

| Where                     | Add                                                                                                                                                                             |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Abstract and introduction | TenantWall now prevents and detects: one sentence on CloudTrail data events and CloudWatch alarms.                                                                              |
| Design                    | The architecture diagram (S12); a paragraph on explicit versus implicit deny with the evaluation-logic citation.                                                                |
| Implementation            | Policy Generator and Access Analyzer validation (S5–S7); the trail settings (S8); the two metric filters and alarms.                                                            |
| Evaluation                | The test table with the new deny-type column; the refused GetObject record (S9); alarm and email evidence (S10–S11) with the measured delay from the refused call to the email. |
| Method                    | The flowchart (S13).                                                                                                                                                            |
| Limitations               | Alerts arrive after a delay of minutes; data events add cost; per-team prefix Deny statements grow the bucket policy.                                                           |

The paper outline ([tenantwall-paper-outline.pdf](tenantwall-paper-outline.md)) and the LaTeX skeleton ([main.tex](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/tenantwall/paper/main.tex)) already have places for these.

## 09. Showing it to your professor (10 minutes)

| Minute | Show                                                          | Say                                                                                                                |
|--------|---------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| 0–1    | Architecture diagram (S12)                                    | "Teams share one account; one tag-based policy set isolates them, and the new path on the right detects attempts." |
| 1–3    | Test table with the deny-type column; simulator S1–S3         | "Each refusal is now labelled explicit or implicit. Is this what you meant by 'something explicit'?"               |
| 3–4    | Policy Generator S5 and Access Analyzer S6–S7                 | "The bucket policy came from the Policy Generator and all policies validate with no errors."                       |
| 4–6    | Run one refused read live; show the Logs Insights result (S9) | "The trail records object reads, so the refused GetObject is visible with who, what and when."                     |
| 6–8    | Alarm in ALARM state and the email (S10–S11)                  | "Three refusals in five minutes, or any tag change, email the admin within minutes."                               |
| 8–10   | Flowchart (S13); next steps                                   | "Next: paper update by 12 Dec, then choose a venue and submit before 21 March. Which venue would you suggest?"     |

### Evidence checklist

| \#  | Screenshot                                      |
|-----|-------------------------------------------------|
| S1  | Simulator: explicit deny, bucket policy         |
| S2  | Simulator: explicit deny, NoSelfPromotion       |
| S3  | Simulator: implicit deny                        |
| S4  | Decoded EC2 authorization message               |
| S5  | Policy Generator                                |
| S6  | Bucket policy with clean Access Analyzer checks |
| S7  | Identity policies' Access Analyzer findings     |
| S8  | Trail settings (data events, CloudWatch Logs)   |
| S9  | Logs Insights: refused GetObject                |
| S10 | Both alarms in ALARM                            |
| S11 | Alert emails                                    |
| S12 | Architecture diagram (official icons)           |
| S13 | Method flowchart                                |

If live AWS is slow in his office, show the screenshots: they are the same evidence. Keep the trail and alarms running until after the meeting.

## 10. If something goes wrong, costs and cleanup

| Problem                              | Fix                                                                                                                            |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| No alert email                       | Did you confirm the SNS subscription? Check the alarm's History tab and that its action points at the topic.                   |
| Nothing in CloudWatch Logs           | Trail must show Logging: On with CloudWatch Logs enabled; same region; wait 10–15 minutes; check the trail's role was created. |
| No GetObject records                 | Data events must be on for your tenant bucket (and the right bucket ARN); management events alone never show object reads.     |
| Alarm never leaves INSUFFICIENT_DATA | No matching records yet: trigger refused calls again; default value 0 on the metric filter helps.                              |
| Access Analyzer errors after pasting | Do not save; compare with your old policy. Keep the old JSON in a text file before editing.                                    |
| Tests start failing                  | Undo the last policy change from your saved copy, re-run the tests, then change one statement at a time.                       |

- **Cost:** the first copy of management events is free; S3 data events, CloudWatch Logs storage and alarms are billed in small amounts. For a demo week this is usually a few rupees, and the budget alert covers you.
- **After the paper evidence is captured:** stop logging or delete the trail, delete the alarms, metric filters, log group, SNS topic and the trail's log bucket (empty it first). Keep the screenshots and the .drawio files.
- **CLI versions** of every step are in [runbook/cli_commands.txt](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/tenantwall/runbook/cli_commands.txt) (18 commands, checked against the AWS service models and the AWS CLI's own parser).

## ··. Sources

Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.

1.  [AWS IAM: policy evaluation logic (explicit vs implicit deny)](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)  
    https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html
2.  [AWS IAM: testing policies with the IAM policy simulator](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html)  
    https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html
3.  [AWS STS: DecodeAuthorizationMessage](https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html)  
    https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html
4.  [AWS Policy Generator](https://awspolicygen.s3.amazonaws.com/policygen.html)  
    https://awspolicygen.s3.amazonaws.com/policygen.html
5.  [IAM Access Analyzer policy validation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html)  
    https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html
6.  [AWS CloudTrail: logging data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html)  
    https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html
7.  [AWS CloudTrail: sending events to CloudWatch Logs](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/send-cloudtrail-events-to-cloudwatch-logs.html)  
    https://docs.aws.amazon.com/awscloudtrail/latest/userguide/send-cloudtrail-events-to-cloudwatch-logs.html
8.  [CloudWatch Logs Insights query syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)  
    https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html
9.  [AWS CloudTrail: CloudWatch alarms for CloudTrail events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html)  
    https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html
10. [AWS Architecture Icons (official)](https://aws.amazon.com/architecture/icons/)  
    https://aws.amazon.com/architecture/icons/
