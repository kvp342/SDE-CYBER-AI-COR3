#!/usr/bin/env bash
# TenantWall: the professor's changes 1-4, run as your ADMIN user with the AWS CLI. Safe to re-run (each step checks what exists).
# Usage: cp tenantwall.env.example tenantwall.env; edit it; bash tenantwall_setup.sh
# Writes everything it finds to ./results/ and backs up your current policies to ./backup/ before touching anything.
set -euo pipefail
cd "$(dirname "$0")"; source ./tenantwall.env
export AWS_DEFAULT_REGION="$REGION"
mkdir -p backup results
say() { printf '\n==== %s ====\n' "$*"; }
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
ME=$(aws sts get-caller-identity --query Arn --output text)
TRAIL=tenantwall-trail; LOG_GROUP=/tenantwall/cloudtrail; ROLE=tenantwall-cloudtrail-to-logs; TOPIC=tenantwall-alerts
LOG_BUCKET="tenantwall-trail-logs-$ACCOUNT-$REGION"
say "0. Who am I: $ME in account $ACCOUNT, region $REGION"

say "0b. Backup of current policies (nothing is changed yet)"
aws s3api get-bucket-policy --bucket "$DATA_BUCKET" --query Policy --output text > backup/bucket-policy.json
for P in "$EC2_POLICY" "$S3_POLICY"; do
  ARN=$(aws iam list-policies --scope Local --query "Policies[?PolicyName=='$P'].Arn" --output text)
  VER=$(aws iam get-policy --policy-arn "$ARN" --query Policy.DefaultVersionId --output text)
  aws iam get-policy-version --policy-arn "$ARN" --version-id "$VER" --query PolicyVersion.Document --output json > "backup/$P.json"
  echo "saved backup/$P.json ($VER)"
done

say "1. Explicit vs implicit deny (IAM policy simulator; EvalDecision is allowed / explicitDeny / implicitDeny)"
USER_ARN="arn:aws:iam::$ACCOUNT:user/$USER_A"
sim() {  # $1 label, $2 action, $3 resource; includes the bucket policy as the resource policy for S3 actions
  if [[ "$2" == s3:* ]]; then
    D=$(aws iam simulate-principal-policy --policy-source-arn "$USER_ARN" --action-names "$2" --resource-arns "$3" --resource-policy file://backup/bucket-policy.json --context-entries "ContextKeyName=aws:PrincipalTag/Team,ContextKeyValues=$TEAM_A,ContextKeyType=string" --query 'EvaluationResults[0].EvalDecision' --output text)
  else
    D=$(aws iam simulate-principal-policy --policy-source-arn "$USER_ARN" --action-names "$2" --resource-arns "$3" --context-entries "ContextKeyName=aws:PrincipalTag/Team,ContextKeyValues=$TEAM_A,ContextKeyType=string" --query 'EvaluationResults[0].EvalDecision' --output text)
  fi
  printf '%-45s %-28s %s\n' "$1" "$2" "$D" | tee -a results/deny-types.txt
}
: > results/deny-types.txt
sim "Team A reads own object" s3:GetObject "arn:aws:s3:::$DATA_BUCKET/$OWN_KEY"
sim "Team A reads team B object" s3:GetObject "arn:aws:s3:::$DATA_BUCKET/$OTHER_KEY"
sim "Team A tags itself (self-promotion)" iam:TagUser "$USER_ARN"
sim "Team A creates a VPC (nothing allows it)" ec2:CreateVpc "*"

say "2. IAM Access Analyzer validation of all three policies"
val() {  # $1 file, $2 type, extra args
  aws accessanalyzer validate-policy --policy-document "file://$1" --policy-type "$2" "${@:3}" --query 'findings[].[findingType,issueCode]' --output text > "results/validate-$(basename "$1" .json).txt" || true
  printf '%-28s %s findings: %s\n' "$(basename "$1")" "$(wc -l < "results/validate-$(basename "$1" .json).txt")" "$(cut -f1 "results/validate-$(basename "$1" .json).txt" | sort | uniq -c | tr '\n' ' ')"
}
val "backup/$EC2_POLICY.json" IDENTITY_POLICY
val "backup/$S3_POLICY.json" IDENTITY_POLICY
val backup/bucket-policy.json RESOURCE_POLICY --validate-policy-resource-type AWS::S3::Bucket
echo "(ERROR or SECURITY_WARNING findings must be fixed; WARNING and SUGGESTION are advice.) The Policy Generator part is done in the browser."

say "3. CloudTrail with S3 data events for $DATA_BUCKET only"
if ! aws s3api head-bucket --bucket "$LOG_BUCKET" 2>/dev/null; then
  if [ "$REGION" = us-east-1 ]; then aws s3api create-bucket --bucket "$LOG_BUCKET"; else aws s3api create-bucket --bucket "$LOG_BUCKET" --create-bucket-configuration "LocationConstraint=$REGION"; fi
fi
aws s3api put-public-access-block --bucket "$LOG_BUCKET" --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
TRAIL_ARN="arn:aws:cloudtrail:$REGION:$ACCOUNT:trail/$TRAIL"
cat > results/log-bucket-policy.json <<JSON
{"Version": "2012-10-17", "Statement": [
 {"Sid": "AWSCloudTrailAclCheck", "Effect": "Allow", "Principal": {"Service": "cloudtrail.amazonaws.com"}, "Action": "s3:GetBucketAcl",
  "Resource": "arn:aws:s3:::$LOG_BUCKET", "Condition": {"StringEquals": {"aws:SourceArn": "$TRAIL_ARN"}}},
 {"Sid": "AWSCloudTrailWrite", "Effect": "Allow", "Principal": {"Service": "cloudtrail.amazonaws.com"}, "Action": "s3:PutObject",
  "Resource": "arn:aws:s3:::$LOG_BUCKET/AWSLogs/$ACCOUNT/*", "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control", "aws:SourceArn": "$TRAIL_ARN"}}}]}
JSON
aws s3api put-bucket-policy --bucket "$LOG_BUCKET" --policy file://results/log-bucket-policy.json
aws logs create-log-group --log-group-name "$LOG_GROUP" 2>/dev/null || echo "log group exists"
LOG_GROUP_ARN=$(aws logs describe-log-groups --log-group-name-prefix "$LOG_GROUP" --query "logGroups[?logGroupName=='$LOG_GROUP'].arn" --output text)
cat > results/trust.json <<'JSON'
{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "cloudtrail.amazonaws.com"}, "Action": "sts:AssumeRole"}]}
JSON
cat > results/to-logs.json <<JSON
{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
  "Resource": "arn:aws:logs:$REGION:$ACCOUNT:log-group:$LOG_GROUP:log-stream:*"}]}
JSON
aws iam get-role --role-name "$ROLE" >/dev/null 2>&1 || aws iam create-role --role-name "$ROLE" --assume-role-policy-document file://results/trust.json >/dev/null
aws iam put-role-policy --role-name "$ROLE" --policy-name tenantwall-cloudtrail-to-logs --policy-document file://results/to-logs.json
ROLE_ARN="arn:aws:iam::$ACCOUNT:role/$ROLE"
for TRY in 1 2 3 4 5 6; do                      # a new IAM role can take a few seconds to be usable
  if aws cloudtrail describe-trails --trail-name-list "$TRAIL" --query 'trailList[0].Name' --output text 2>/dev/null | grep -q "$TRAIL"; then
    aws cloudtrail update-trail --name "$TRAIL" --s3-bucket-name "$LOG_BUCKET" --cloud-watch-logs-log-group-arn "$LOG_GROUP_ARN" --cloud-watch-logs-role-arn "$ROLE_ARN" >/dev/null && break
  else
    aws cloudtrail create-trail --name "$TRAIL" --s3-bucket-name "$LOG_BUCKET" --cloud-watch-logs-log-group-arn "$LOG_GROUP_ARN" --cloud-watch-logs-role-arn "$ROLE_ARN" >/dev/null && break
  fi
  echo "role not ready yet, retry $TRY in 10 s"; sleep 10
done
cat > results/event-selectors.json <<JSON
[{"ReadWriteType": "All", "IncludeManagementEvents": true, "DataResources": [{"Type": "AWS::S3::Object", "Values": ["arn:aws:s3:::$DATA_BUCKET/"]}]}]
JSON
aws cloudtrail put-event-selectors --trail-name "$TRAIL" --event-selectors file://results/event-selectors.json >/dev/null
aws cloudtrail start-logging --name "$TRAIL"
aws cloudtrail get-trail-status --name "$TRAIL" --query '{Logging: IsLogging, LatestDelivery: LatestDeliveryTime}' --output table

say "4. CloudWatch: two metric filters, an SNS email topic and two alarms"
aws logs put-metric-filter --log-group-name "$LOG_GROUP" --filter-name tenantwall-access-denied --filter-pattern '{ ($.errorCode = "*UnauthorizedOperation") || ($.errorCode = "AccessDenied*") }' --metric-transformations metricName=AccessDeniedCount,metricNamespace=TenantWall,metricValue=1,defaultValue=0
aws logs put-metric-filter --log-group-name "$LOG_GROUP" --filter-name tenantwall-tag-tampering --filter-pattern '{ ($.eventName = "CreateTags") || ($.eventName = "DeleteTags") || ($.eventName = "TagUser") || ($.eventName = "UntagUser") }' --metric-transformations metricName=TagChangeCount,metricNamespace=TenantWall,metricValue=1,defaultValue=0
TOPIC_ARN=$(aws sns create-topic --name "$TOPIC" --query TopicArn --output text)
if ! aws sns list-subscriptions-by-topic --topic-arn "$TOPIC_ARN" --query 'Subscriptions[].Endpoint' --output text | grep -q "$ALERT_EMAIL"; then
  aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol email --notification-endpoint "$ALERT_EMAIL" >/dev/null
  echo ">>> Open $ALERT_EMAIL and click 'Confirm subscription' in the AWS email, or no alarm email will arrive. <<<"
fi
aws cloudwatch put-metric-alarm --alarm-name tenantwall-access-denied --namespace TenantWall --metric-name AccessDeniedCount --statistic Sum --period 300 --evaluation-periods 1 --threshold 3 --comparison-operator GreaterThanOrEqualToThreshold --treat-missing-data notBreaching --alarm-actions "$TOPIC_ARN"
aws cloudwatch put-metric-alarm --alarm-name tenantwall-tag-tampering --namespace TenantWall --metric-name TagChangeCount --statistic Sum --period 300 --evaluation-periods 1 --threshold 1 --comparison-operator GreaterThanOrEqualToThreshold --treat-missing-data notBreaching --alarm-actions "$TOPIC_ARN"
aws cloudwatch describe-alarms --alarm-names tenantwall-access-denied tenantwall-tag-tampering --query 'MetricAlarms[].[AlarmName,StateValue,Threshold]' --output table

say "Done. Next: run python3 tenantwall_tests.py (refused calls happen), wait ~10 minutes, then: bash tenantwall_verify.sh"
