#!/usr/bin/env bash
# Remove everything tenantwall_setup.sh created (run only AFTER you have shown the professor and saved screenshots).
# It does NOT touch your tenant bucket, users, or your TenantABAC policies.
set -uo pipefail
cd "$(dirname "$0")"; source ./tenantwall.env; export AWS_DEFAULT_REGION="$REGION"
ACCOUNT=$(aws sts get-caller-identity --query Account --output text); LOG_BUCKET="tenantwall-trail-logs-$ACCOUNT-$REGION"
aws cloudwatch delete-alarms --alarm-names tenantwall-access-denied tenantwall-tag-tampering
aws logs delete-metric-filter --log-group-name /tenantwall/cloudtrail --filter-name tenantwall-access-denied
aws logs delete-metric-filter --log-group-name /tenantwall/cloudtrail --filter-name tenantwall-tag-tampering
TOPIC_ARN=$(aws sns list-topics --query "Topics[?ends_with(TopicArn, ':tenantwall-alerts')].TopicArn" --output text)
[ -n "$TOPIC_ARN" ] && aws sns delete-topic --topic-arn "$TOPIC_ARN"
aws cloudtrail stop-logging --name tenantwall-trail; aws cloudtrail delete-trail --name tenantwall-trail
aws logs delete-log-group --log-group-name /tenantwall/cloudtrail
aws iam delete-role-policy --role-name tenantwall-cloudtrail-to-logs --policy-name tenantwall-cloudtrail-to-logs
aws iam delete-role --role-name tenantwall-cloudtrail-to-logs
aws s3 rm "s3://$LOG_BUCKET" --recursive && aws s3api delete-bucket --bucket "$LOG_BUCKET"
echo "Cleanup done. Your tenant bucket, users and TenantABAC policies were not touched."
