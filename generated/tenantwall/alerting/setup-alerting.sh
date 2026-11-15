#!/usr/bin/env bash
# TenantWall audit and alerting setup with the AWS CLI (v2).
# Replace the placeholders below before running. Uses your configured AWS CLI profile; never put keys in this file.
# Order: log bucket -> trail with S3 data events -> CloudWatch Logs delivery -> metric filter -> SNS topic -> alarm.
# Cost note: S3 data events and CloudWatch Logs are billed; keep data events limited to the TenantWall bucket and delete everything after the experiment.
set -euo pipefail
REGION=ap-south-1
ACCOUNT=111122223333                      # your 12-digit account id
DATA_BUCKET=tenantwall-data-EXAMPLE       # bucket that holds tenant prefixes
LOG_BUCKET=tenantwall-trail-logs-EXAMPLE  # bucket that receives CloudTrail files
TRAIL=tenantwall-trail
LOG_GROUP=/tenantwall/cloudtrail
TRAIL_ROLE=tenantwall-cloudtrail-to-logs  # role CloudTrail assumes to write to CloudWatch Logs (create it first; see the AWS guide linked in the PDF)
ALERT_EMAIL=you@example.com               # replace with the address that should get alerts

# 1. Bucket for trail files, with the CloudTrail bucket policy (edit the placeholders inside the JSON first)
aws s3api create-bucket --bucket "$LOG_BUCKET" --region "$REGION" --create-bucket-configuration LocationConstraint="$REGION"
aws s3api put-bucket-policy --bucket "$LOG_BUCKET" --policy file://../policies/cloudtrail-bucket-policy.json

# 2. Log group, trail, and S3 data events for the TenantWall bucket only
aws logs create-log-group --log-group-name "$LOG_GROUP" --region "$REGION"
aws cloudtrail create-trail --name "$TRAIL" --s3-bucket-name "$LOG_BUCKET" --region "$REGION" \
  --cloud-watch-logs-log-group-arn "arn:aws:logs:$REGION:$ACCOUNT:log-group:$LOG_GROUP:*" \
  --cloud-watch-logs-role-arn "arn:aws:iam::$ACCOUNT:role/$TRAIL_ROLE"
aws cloudtrail put-event-selectors --trail-name "$TRAIL" --region "$REGION" --event-selectors file://../policies/data-event-selectors.json
aws cloudtrail start-logging --name "$TRAIL" --region "$REGION"

# 3. Metric filter: count AccessDenied and UnauthorizedOperation errors
aws logs put-metric-filter --region "$REGION" --log-group-name "$LOG_GROUP" \
  --filter-name tenantwall-access-denied \
  --filter-pattern '{ ($.errorCode = "*UnauthorizedOperation") || ($.errorCode = "AccessDenied*") }' \
  --metric-transformations metricName=AccessDeniedCount,metricNamespace=TenantWall,metricValue=1,defaultValue=0

# 4. SNS topic with an email subscription (confirm the email AWS sends, or nothing arrives)
TOPIC_ARN=$(aws sns create-topic --name tenantwall-alerts --region "$REGION" --query TopicArn --output text)
aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol email --notification-endpoint "$ALERT_EMAIL" --region "$REGION"

# 5. Alarm: one or more denied calls in a 5-minute period
aws cloudwatch put-metric-alarm --region "$REGION" --alarm-name tenantwall-access-denied \
  --namespace TenantWall --metric-name AccessDeniedCount --statistic Sum --period 300 \
  --evaluation-periods 1 --threshold 1 --comparison-operator GreaterThanOrEqualToThreshold \
  --treat-missing-data notBreaching --alarm-actions "$TOPIC_ARN"

echo "Done. Test: as tenant A, try to read an object under tenant-b/ and wait up to about 15 minutes for the email."
