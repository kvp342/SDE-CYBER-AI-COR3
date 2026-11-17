# TenantWall automation (draft: finish and test on 18 Nov 2026)

Scripts for the professor's changes 1–4, to be run tomorrow from the student's laptop with the AWS CLI (admin profile):

- `tenantwall.env.example` → copy to `tenantwall.env` and fill in (bucket, teams, a team-A user, two object keys, policy names, alert email)
- `tenantwall_setup.sh`: backs up current policies, then: explicit/implicit deny via the IAM policy simulator, Access Analyzer validation, CloudTrail with S3 data events → CloudWatch Logs, two metric filters, SNS email, two alarms
- `tenantwall_verify.sh`: after running the tests, shows refused calls recorded by CloudTrail and the alarm states
- `tenantwall_cleanup.sh`: removes only what setup created

Status: syntax checked; a dry run against a local AWS simulator passed the identity check and policy backups. The simulator, Access Analyzer, CloudTrail and CloudWatch steps are still to be tested tomorrow before use.
