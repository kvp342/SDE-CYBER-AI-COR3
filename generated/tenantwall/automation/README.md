# TenantWall automation

Scripts for the professor's changes 1–4, to be run tomorrow from the student's laptop with the AWS CLI (admin profile):

- `tenantwall.env.example` → copy to `tenantwall.env` and fill in (bucket, teams, a team-A user, two object keys, policy names, alert email)
- `tenantwall_setup.sh`: backs up current policies, then: explicit/implicit deny via the IAM policy simulator, Access Analyzer validation, CloudTrail with S3 data events → CloudWatch Logs, two metric filters, SNS email, two alarms
- `tenantwall_verify.sh`: after running the tests, shows refused calls recorded by CloudTrail and the alarm states
- `tenantwall_cleanup.sh`: removes only what setup created

Status (17 Nov 2026, night): syntax checked; full dry run against a local AWS simulator (moto 5.2.5) passed: identity check, policy backups, CloudTrail trail with data events and CloudWatch Logs, both metric filters, SNS topic and subscription, both alarms; a second run changes nothing (safe to re-run); verify runs; cleanup removes only what setup created (tenant bucket, users and policies kept). The IAM policy simulator and Access Analyzer steps are not available in the simulator and run for the first time against the real account.
