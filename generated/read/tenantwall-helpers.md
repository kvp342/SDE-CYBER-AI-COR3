TENANTWALL · HELPERS FOR THE PAPER

# TenantWall diagrams, policies, alerting

Ready-to-adapt material for the requests on the project: an architecture diagram and a method flowchart, sample IAM policies (ABAC allow, explicit denies, deny insecure transport), the CloudTrail and CloudWatch alerting setup, a test plan and a checklist for the audit and alerting section. All account ids, bucket names and emails are placeholders.

**Files.** Everything is in `generated/tenantwall/`: `architecture.svg/.png`, `flowchart.svg/.png`, `policies/*.json`, `alerting/setup-alerting.sh`, `alerting/alarm-settings.json` and `check_policies.py`. See also the [TenantWall](knowledge-base/cloud.md#tenantwall-your-research-project), [ABAC](knowledge-base/cloud.md#abac-attribute-based-access-control) and [CloudTrail](knowledge-base/cloud.md#cloudtrail-and-cloudwatch-alarms) Knowledge Base pages.

|                                                                  |
|------------------------------------------------------------------|
| [Architecture diagram](#architecture-diagram)                                  |
| [Method flowchart](#method-flowchart)                                      |
| [IAM and bucket policies](#iam-and-bucket-policies)                               |
| [Audit and alerting setup](#audit-and-alerting-setup)                              |
| [Isolation test plan](#isolation-test-plan)                                  |
| [Checklist for the paper's audit and alerting section](#checklist-for-the-audit-and-alerting-section) |
| [Sources](#sources)                                              |

Confirm details such as the exact meaning of "explicit deny" with your professor. Redraw the diagram with the official AWS icon set in diagrams.net for the paper; the layout here is the content to copy.

## Architecture diagram

Two tenant roles share one bucket and one fleet. IAM evaluates every request against tag-matched allows and explicit denies. Every call, allowed or denied, reaches CloudTrail; denied calls become a metric, an alarm and an email.

## Method flowchart

Order of evaluation follows the AWS policy evaluation logic: an explicit deny wins; otherwise a matching allow is needed; otherwise the request is implicitly denied.

## IAM and bucket policies

Replace 111122223333, the bucket names and the Region. Before using them, run IAM Access Analyzer policy validation on each file and test with the IAM policy simulator. `check_policies.py` checks the JSON structure offline and simulates the isolation cases with a simplified evaluator (all 29 checks pass).

### tenant-abac-identity.json

Identity policy attached to every tenant role. Grants access only where the object prefix or the instance's tenant tag equals the caller's own tenant tag. One policy serves all tenants: adding a tenant means adding a tagged role, not a new policy.

``` text
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListOnlyOwnTenantPrefix",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::tenantwall-data-EXAMPLE",
      "Condition": { "StringLike": { "s3:prefix": ["${aws:PrincipalTag/tenant}/*"] } }
    },
    {
      "Sid": "ReadWriteOwnTenantObjects",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::tenantwall-data-EXAMPLE/${aws:PrincipalTag/tenant}/*"
    },
    {
      "Sid": "DescribeInstancesHasNoResourceLevelControl",
      "Effect": "Allow",
      "Action": "ec2:DescribeInstances",
      "Resource": "*"
    },
    {
      "Sid": "OperateOwnTenantInstances",
      "Effect": "Allow",
      "Action": ["ec2:StartInstances", "ec2:StopInstances", "ec2:RebootInstances"],
      "Resource": "arn:aws:ec2:ap-south-1:111122223333:instance/*",
      "Condition": { "StringEquals": { "aws:ResourceTag/tenant": "${aws:PrincipalTag/tenant}" } }
    }
  ]
}
```

### tenant-explicit-deny.json

Explicit denies that hold even if someone later attaches a broad allow: other tenants' objects and instances, changing the tenant tag on instances or principals, and object or bucket tagging.

``` text
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyOtherTenantsObjects",
      "Effect": "Deny",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "NotResource": "arn:aws:s3:::tenantwall-data-EXAMPLE/${aws:PrincipalTag/tenant}/*"
    },
    {
      "Sid": "DenyOtherTenantsInstances",
      "Effect": "Deny",
      "Action": ["ec2:StartInstances", "ec2:StopInstances", "ec2:RebootInstances", "ec2:TerminateInstances"],
      "Resource": "arn:aws:ec2:ap-south-1:111122223333:instance/*",
      "Condition": { "StringNotEquals": { "aws:ResourceTag/tenant": "${aws:PrincipalTag/tenant}" } }
    },
    {
      "Sid": "DenyChangingTenantTagOnInstances",
      "Effect": "Deny",
      "Action": ["ec2:CreateTags", "ec2:DeleteTags"],
      "Resource": "*",
      "Condition": { "ForAnyValue:StringEquals": { "aws:TagKeys": ["tenant"] } }
    },
    {
      "Sid": "DenyChangingTenantTagOnPrincipals",
      "Effect": "Deny",
      "Action": ["iam:TagUser", "iam:UntagUser", "iam:TagRole", "iam:UntagRole"],
      "Resource": "*",
      "Condition": { "ForAnyValue:StringEquals": { "aws:TagKeys": ["tenant"] } }
    },
    {
      "Sid": "DenyObjectAndBucketTagging",
      "Effect": "Deny",
      "Action": ["s3:PutObjectTagging", "s3:DeleteObjectTagging", "s3:PutBucketTagging"],
      "Resource": "*"
    }
  ]
}
```

### bucket-policy-secure-transport.json

Bucket policy on the data bucket that refuses any request not made over TLS.

``` text
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyInsecureTransport",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::tenantwall-data-EXAMPLE", "arn:aws:s3:::tenantwall-data-EXAMPLE/*"],
      "Condition": { "Bool": { "aws:SecureTransport": "false" } }
    }
  ]
}
```

### cloudtrail-bucket-policy.json

Bucket policy that lets CloudTrail write log files to the log bucket, limited to this trail by aws:SourceArn.

``` text
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSCloudTrailAclCheck",
      "Effect": "Allow",
      "Principal": { "Service": "cloudtrail.amazonaws.com" },
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::tenantwall-trail-logs-EXAMPLE",
      "Condition": { "StringEquals": { "aws:SourceArn": "arn:aws:cloudtrail:ap-south-1:111122223333:trail/tenantwall-trail" } }
    },
    {
      "Sid": "AWSCloudTrailWrite",
      "Effect": "Allow",
      "Principal": { "Service": "cloudtrail.amazonaws.com" },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::tenantwall-trail-logs-EXAMPLE/AWSLogs/111122223333/*",
      "Condition": { "StringEquals": { "s3:x-amz-acl": "bucket-owner-full-control", "aws:SourceArn": "arn:aws:cloudtrail:ap-south-1:111122223333:trail/tenantwall-trail" } }
    }
  ]
}
```

### data-event-selectors.json

Event selectors that add S3 object-level (data) events for the TenantWall bucket only, so GetObject and PutObject calls are logged without paying for every bucket.

``` text
[
  {
    "ReadWriteType": "All",
    "IncludeManagementEvents": true,
    "DataResources": [ { "Type": "AWS::S3::Object", "Values": ["arn:aws:s3:::tenantwall-data-EXAMPLE/"] } ]
  }
]
```

**Design notes.** ec2:DescribeInstances does not support resource-level permissions, so tenants can see instance metadata of others; if that matters for the paper, say so as a limitation or filter by tag in the application. S3 isolation uses tenant prefixes because object-tag conditions apply only to some actions; prefixes are simpler to reason about.

## Audit and alerting setup

1.  Create a log bucket and give CloudTrail permission to write to it (`cloudtrail-bucket-policy.json`).
2.  Create a trail with management events plus S3 data events for the TenantWall bucket only (`data-event-selectors.json`), delivering to a CloudWatch Logs group.
3.  Add a metric filter that counts AccessDenied and UnauthorizedOperation errors.
4.  Create an SNS topic with an email subscription and confirm the subscription email.
5.  Create an alarm on the metric that notifies the topic.

`alerting/setup-alerting.sh` does these steps with the AWS CLI once you fill in the placeholders. It never stores credentials; it uses your CLI profile.

|                    |                                                                                       |
|--------------------|---------------------------------------------------------------------------------------|
| LogGroup           | /tenantwall/cloudtrail                                                                |
| FilterName         | tenantwall-access-denied                                                              |
| FilterPattern      | { (\$.errorCode = "\*UnauthorizedOperation") \|\| (\$.errorCode = "AccessDenied\*") } |
| MetricNamespace    | TenantWall                                                                            |
| MetricName         | AccessDeniedCount                                                                     |
| MetricValue        | 1                                                                                     |
| DefaultValue       | 0                                                                                     |
| AlarmName          | tenantwall-access-denied                                                              |
| Statistic          | Sum                                                                                   |
| PeriodSeconds      | 300                                                                                   |
| EvaluationPeriods  | 1                                                                                     |
| Threshold          | 1                                                                                     |
| ComparisonOperator | GreaterThanOrEqualToThreshold                                                         |
| TreatMissingData   | notBreaching                                                                          |
| Action             | SNS topic tenantwall-alerts (email subscription)                                      |

CloudTrail usually delivers events within minutes, so the email arrives minutes after the denied call, not instantly. Measure it for the paper.

## Isolation test plan

| \#  | Test (run as the tenant A role)          | Expected                | Evidence to capture                      |
|-----|------------------------------------------|-------------------------|------------------------------------------|
| 1   | Tenant A reads own object                | Allow                   | Object returned                          |
| 2   | Tenant A reads tenant B's object         | AccessDenied (explicit) | CLI error, CloudTrail event, alarm email |
| 3   | Tenant A writes into tenant-b/           | AccessDenied (explicit) | Same as above                            |
| 4   | Tenant A lists tenant-b/ prefix          | AccessDenied (implicit) | CLI error, CloudTrail event              |
| 5   | Tenant A stops tenant B's instance       | UnauthorizedOperation   | CloudTrail event, alarm email            |
| 6   | Tenant A re-tags an instance to tenant-b | UnauthorizedOperation   | Tag unchanged                            |
| 7   | Tenant A changes its own tenant tag      | AccessDenied            | Tag unchanged                            |
| 8   | Plain HTTP request to the bucket         | AccessDenied            | Request refused                          |
| 9   | No denied calls for 5 minutes            | Alarm returns to OK     | Alarm history                            |

Repeat tests 2 and 5 several times and record the time from the call to the email. Then clean up: delete the trail, alarm, topic, log group, buckets and instances.

## Checklist for the audit and alerting section

|     |                                                                                                                                                                                                           |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ☐   | State the threat model: a tenant (or a stolen tenant credential) trying to read, change or re-tag another tenant's resources.                                                                             |
| ☐   | Show the trail configuration: multi-Region or single-Region, management events, S3 data events limited to the TenantWall bucket, log file validation on.                                                  |
| ☐   | Explain where logs go and how long they are kept (S3 log bucket retention, CloudWatch Logs retention period).                                                                                             |
| ☐   | Give the exact metric filter pattern and why it covers both S3 (AccessDenied) and EC2 (UnauthorizedOperation) errors.                                                                                     |
| ☐   | Give the alarm settings: statistic, period, threshold, evaluation periods, missing-data treatment, SNS action. Justify the threshold (one denied call is already suspicious in a tenant-isolated design). |
| ☐   | Report measured detection latency: time from the denied call to the email, over several trials (CloudTrail delivery adds minutes; say so).                                                                |
| ☐   | Include evidence: CLI output of each denied test, the CloudTrail event JSON (redact the account id), the metric graph and the alarm email screenshot.                                                     |
| ☐   | Discuss false positives (for example a misconfigured script) and how to tune: per-tenant dimensions, higher threshold, or an EventBridge rule for specific events.                                        |
| ☐   | Discuss limits: tags as a trust anchor, eventual consistency of IAM changes, CloudTrail delivery delay, cost of data events.                                                                              |
| ☐   | Name the checks used on the policies: IAM Access Analyzer policy validation and the IAM policy simulator, plus the offline check script in the repository.                                                |
| ☐   | Map the design to standards in one line each: least privilege, defence in depth (explicit deny plus bucket policy), and OWASP A09 logging and monitoring.                                                 |
| ☐   | List cleanup steps so readers do not leave billable resources running.                                                                                                                                    |

## Sources

- [ABAC in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html) https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html
- [Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html
- [CloudTrail data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html) https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html
- [Sending CloudTrail events to CloudWatch Logs](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/send-cloudtrail-events-to-cloudwatch-logs.html) https://docs.aws.amazon.com/awscloudtrail/latest/userguide/send-cloudtrail-events-to-cloudwatch-logs.html
- [CloudWatch alarms for CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html) https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html
- [Metric filter pattern syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html) https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html
- [S3 bucket policy for CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-s3-bucket-policy-for-cloudtrail.html) https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-s3-bucket-policy-for-cloudtrail.html
- [Access Analyzer policy validation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html) https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html
- [Testing policies with the IAM policy simulator](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html) https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html
- [S3 security best practices (secure transport)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html) https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html
- [AWS architecture icons (for the final diagram)](https://aws.amazon.com/architecture/icons/) https://aws.amazon.com/architecture/icons/

Policies and settings follow the AWS documentation above; the metric filter pattern is the one AWS documents for unauthorised API calls.
