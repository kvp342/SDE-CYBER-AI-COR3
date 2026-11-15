# CloudTrail alerting

## CloudTrail
CloudTrail records AWS API calls: who called, what action, when and from which IP address. Management events are recorded by default.

## Data events
S3 object reads and writes are data events. They must be enabled on the trail, and they cost extra, so limit them to the buckets you need.

## Metric filter and alarm
Send the trail to CloudWatch Logs and add a metric filter that counts AccessDenied and UnauthorizedOperation error codes. A CloudWatch alarm on that metric notifies an SNS topic, which sends an email.

## Delay
CloudTrail delivers events within minutes, so alerts are not instant. Measure the delay when you test.
