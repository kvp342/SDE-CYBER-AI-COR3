#!/usr/bin/env bash
# After running your tests: show the refused calls CloudTrail recorded, and the alarm states. Usage: bash tenantwall_verify.sh
set -euo pipefail
cd "$(dirname "$0")"; source ./tenantwall.env; export AWS_DEFAULT_REGION="$REGION"
LOG_GROUP=/tenantwall/cloudtrail
START=$(( $(date +%s) - 3600 )); END=$(date +%s)
Q=$(aws logs start-query --log-group-name "$LOG_GROUP" --start-time "$START" --end-time "$END" --query-string 'fields @timestamp, eventName, errorCode, userIdentity.arn, requestParameters.key | filter errorCode like /AccessDenied|UnauthorizedOperation/ | sort @timestamp desc | limit 20' --query queryId --output text)
for i in 1 2 3 4 5 6 7 8 9 10; do
  S=$(aws logs get-query-results --query-id "$Q" --query status --output text)
  [ "$S" = Complete ] && break; sleep 3
done
echo "==== Refused calls in the last hour (from CloudTrail via CloudWatch Logs) ===="
aws logs get-query-results --query-id "$Q" --query 'results[*][?field!=`@ptr`].value' --output text | tee results/refused-calls.txt
echo "==== Alarms ===="
aws cloudwatch describe-alarms --alarm-names tenantwall-access-denied tenantwall-tag-tampering --query 'MetricAlarms[].[AlarmName,StateValue,StateReason]' --output table | tee results/alarms.txt
