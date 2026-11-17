AWS SAA-C03 · HANDS-ON

# 10 AWS labs plus a teardown checklist

Build what the exam asks about: IAM roles, S3, a VPC, EC2, a load balancer with Auto Scaling, RDS, Lambda, CloudTrail alarms and KMS. Each lab has the goal, console steps, the same thing in the AWS CLI, how to check it worked, cleanup, and what the exam expects you to know. All 70 CLI commands were checked against the AWS service models and passed the AWS CLI's own argument parser.

| Lab                                                                          | Exam domain                                      |
|------------------------------------------------------------------------------|--------------------------------------------------|
| [Lab 1. Budget alert first (do this before anything else)](#01-budget-alert-first-do-this-before-anything-else)          | Cost-optimised architectures                     |
| [Lab 2. IAM: an admin group and a role for EC2](#02-iam-an-admin-group-and-a-role-for-ec2)                     | Secure architectures                             |
| [Lab 3. S3: private bucket, versioning and encryption](#03-s3-private-bucket-versioning-and-encryption)             | Secure and resilient architectures               |
| [Lab 4. VPC: public and private subnets](#04-vpc-public-and-private-subnets)                           | Resilient architectures                          |
| [Lab 5. EC2: an instance with a security group, a role and IMDSv2](#05-ec2-an-instance-with-a-security-group-a-role-and-imdsv2) | Secure architectures                             |
| [Lab 6. Load balancer and Auto Scaling across two AZs](#06-load-balancer-and-auto-scaling-across-two-azs)             | Resilient and high-performing architectures      |
| [Lab 7. RDS: a private MySQL database](#07-rds-a-private-mysql-database)                             | Resilient architectures                          |
| [Lab 8. Serverless: Lambda behind an HTTP API](#08-serverless-lambda-behind-an-http-api)                     | High-performing and cost-optimised architectures |
| [Lab 9. CloudTrail and an alarm on root-user activity](#09-cloudtrail-and-an-alarm-on-root-user-activity)             | Secure architectures                             |
| [Lab 10. KMS: encrypt, decrypt and envelope encryption](#10-kms-encrypt-decrypt-and-envelope-encryption)            | Secure architectures                             |
| [Lab 11. Teardown checklist and cost check](#11-teardown-checklist-and-cost-check)                        | Cost-optimised architectures                     |

**Before you start.** Do Lab 1 first: a budget alert and MFA on the root user. Accounts created on or after 15 July 2025 are on AWS's credit-based Free plan (up to 200 USD of credits for 6 months), not the old 12-month free tier, so every lab says what it may cost and how to delete it ([AWS announcement](https://aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan)). Region: ap-south-1 (Mumbai). Words like \$VPC_ID are placeholders: copy the ID from the previous command's output. Never paste access keys into code or chat; use roles and `aws configure sso` or a named profile.

## 01. Budget alert first (do this before anything else)

Cost-optimised architectures · about 15 minutes

**Cost:** No charge for this lab.

**Goal.** Get an email before you spend money by mistake, and turn on MFA for the root user.

### Console

1.  Root user: Security credentials → assign an MFA device. Then stop using root for daily work.
2.  Billing and Cost Management → Budgets → Create budget → Use a template → Monthly cost budget; amount 1 USD; your email.
3.  Billing preferences: turn on Free Tier usage alerts.

### CLI

``` bash
aws budgets create-budget --account-id $ACCOUNT_ID --budget file://budget.json --notifications-with-subscribers file://notify.jsonaws budgets describe-budgets --account-id $ACCOUNT_ID
```

### Check it worked

describe-budgets lists the budget; the console shows it with your email as a subscriber.

### Clean up

- Keep the budget for as long as the account exists.

### For the exam

- Budgets alert on actual or forecast cost; Cost Explorer analyses past spend.
- MFA on root and no root access keys are the first two items of every AWS security checklist.

**Official guide:** [AWS Budgets user guide](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)

## 02. IAM: an admin group and a role for EC2

Secure architectures · about 30 minutes

**Cost:** No charge: IAM is free.

**Goal.** Work as an IAM identity instead of root, and create a role that EC2 can assume to read S3 without access keys.

### Console

1.  IAM → User groups → Create group Admins with the AdministratorAccess policy. Create your own user in it (or use IAM Identity Center).
2.  IAM → Roles → Create role → Trusted entity AWS service, use case EC2 → policy AmazonS3ReadOnlyAccess → name ec2-s3-read.
3.  Open the role's Trust relationships tab and read the policy: the principal is ec2.amazonaws.com.

### CLI

``` bash
aws iam create-group --group-name Adminsaws iam attach-group-policy --group-name Admins --policy-arn arn:aws:iam::aws:policy/AdministratorAccessaws iam create-role --role-name ec2-s3-read --assume-role-policy-document file://trust-ec2.jsonaws iam attach-role-policy --role-name ec2-s3-read --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccessaws iam create-instance-profile --instance-profile-name ec2-s3-readaws iam add-role-to-instance-profile --instance-profile-name ec2-s3-read --role-name ec2-s3-readaws sts get-caller-identity
```

### Check it worked

get-caller-identity shows your IAM user ARN, not root. In Lab 5 the instance reads S3 with no keys stored on it.

### Clean up

- Keep the group and role for the later labs; delete the role and instance profile at the end (Lab 11 checklist).

### For the exam

- Roles give temporary credentials; an instance profile is how EC2 carries a role.
- Policy evaluation: default deny, explicit deny wins, otherwise an allow is needed.

**Official guide:** [IAM roles for Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)

## 03. S3: private bucket, versioning and encryption

Secure and resilient architectures · about 30 minutes

**Cost:** A few MB of storage and requests: well under a cent; delete the bucket at the end.

**Goal.** Create a bucket that can never be public, keeps old versions, and encrypts by default; then recover a deleted file.

### Console

1.  S3 → Create bucket in ap-south-1 with a globally unique name; keep Block all public access on.
2.  Properties → Bucket versioning → Enable. Default encryption is SSE-S3 already; note it.
3.  Upload notes.txt, upload a changed copy, delete it, then turn on Show versions and restore by deleting the delete marker.

### CLI

``` bash
aws s3api create-bucket --bucket $BUCKET --region ap-south-1 --create-bucket-configuration LocationConstraint=ap-south-1aws s3api put-public-access-block --bucket $BUCKET --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=trueaws s3api put-bucket-versioning --bucket $BUCKET --versioning-configuration Status=Enabledaws s3 cp notes.txt s3://$BUCKET/notes.txtaws s3api list-object-versions --bucket $BUCKET --prefix notes.txtaws s3api delete-object --bucket $BUCKET --key notes.txt --version-id $DELETE_MARKER_ID
```

### Check it worked

list-object-versions shows two versions and a delete marker; after deleting the marker, the file is back.

### Clean up

- Delete every object version and delete marker (Empty in the console does this), then delete the bucket.
- Note: aws s3 rb --force does not remove old versions from a versioned bucket; empty it in the console first.

### For the exam

- Versioning plus MFA Delete or Object Lock protects against deletion and ransomware.
- Block Public Access overrides bucket policies and ACLs that would make data public.

**Official guide:** [S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)

## 04. VPC: public and private subnets

Resilient architectures · about 40 minutes

**Cost:** No charge for a VPC, subnets, route tables or an internet gateway. Do not create a NAT gateway: it is billed by the hour.

**Goal.** Build a VPC across two Availability Zones with public subnets (route to the internet) and a private subnet (no route).

### Console

1.  VPC → Create VPC → VPC only, 10.0.0.0/16, name lab-vpc.
2.  Create subnets: public-a 10.0.1.0/24 (ap-south-1a), public-b 10.0.2.0/24 (ap-south-1b), private-a 10.0.11.0/24 (ap-south-1a).
3.  Create an internet gateway, attach it, and add a route table with 0.0.0.0/0 → IGW; associate it with both public subnets. Turn on auto-assign public IPv4 for them.

### CLI

``` bash
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=lab-vpc}]'aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone ap-south-1aaws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 --availability-zone ap-south-1baws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.11.0/24 --availability-zone ap-south-1aaws ec2 create-internet-gatewayaws ec2 attach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_IDaws ec2 create-route-table --vpc-id $VPC_IDaws ec2 create-route --route-table-id $RTB_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_IDaws ec2 associate-route-table --route-table-id $RTB_ID --subnet-id $PUBLIC_Aaws ec2 modify-subnet-attribute --subnet-id $PUBLIC_A --map-public-ip-on-launch
```

### Check it worked

The public route table has 0.0.0.0/0 → igw-…; the private subnet uses the main route table with only the local route.

### Clean up

- Keep the VPC for Labs 5–7; delete it last (deleting the VPC in the console removes its subnets, route tables and the attached gateway).

### For the exam

- A subnet is public only because of its route to an internet gateway.
- Private instances reach the internet through a NAT gateway (paid) or not at all; VPC endpoints reach S3 and DynamoDB privately.

**Official guide:** [How Amazon VPC works](https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html)

## 05. EC2: an instance with a security group, a role and IMDSv2

Secure architectures · about 40 minutes

**Cost:** One t3.micro (or t2.micro where free-tier eligible) for an hour: covered by free-tier hours or credits. Terminate it the same day.

**Goal.** Launch a web server that only you can SSH into, that reads S3 through its role, and that requires IMDSv2.

### Console

1.  Security group web-sg in lab-vpc: inbound SSH 22 from My IP only, HTTP 80 from anywhere.
2.  Launch Amazon Linux 2023, t3.micro, subnet public-a, web-sg, IAM instance profile ec2-s3-read, Advanced → Metadata version: V2 only (token required).
3.  User data: install and start a web server (dnf install -y httpd; systemctl enable --now httpd).

### CLI

``` bash
aws ec2 create-security-group --group-name web-sg --description web-lab --vpc-id $VPC_IDaws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 22 --cidr $MY_IP/32aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0aws ec2 run-instances --image-id resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 --instance-type t3.micro --count 1 --subnet-id $PUBLIC_A --security-group-ids $SG_ID --iam-instance-profile Name=ec2-s3-read --metadata-options HttpTokens=required --user-data file://web.shaws ec2 describe-instances --instance-ids $INSTANCE_ID --query Reservations[].Instances[].PublicIpAddress
```

### Check it worked

The public IP serves the web page. On the instance, aws s3 ls s3://\$BUCKET works with no keys, and curl http://169.254.169.254/latest/meta-data/ without a token returns 401.

### Clean up

- `aws ec2 terminate-instances --instance-ids $INSTANCE_ID`
- Delete web-sg after the instance is gone.

### For the exam

- Security groups are stateful and allow-only; NACLs are stateless with numbered allow and deny rules.
- IMDSv2 blocks most SSRF attempts to steal instance credentials.

**Official guide:** [Use IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)

## 06. Load balancer and Auto Scaling across two AZs

Resilient and high-performing architectures · about 60 minutes

**Cost:** An Application Load Balancer and instances are billed by the hour (free-tier hours or credits may cover a short lab). Finish and delete in one sitting.

**Goal.** Put two web servers behind an ALB in two Availability Zones and watch Auto Scaling replace one you terminate.

### Console

1.  EC2 → Launch templates → create web-lt from the Lab 5 settings (AMI, t3.micro, web-sg, user data, IMDSv2).
2.  Target group web-tg (HTTP 80, health check /). Application Load Balancer web-alb, internet-facing, subnets public-a and public-b, listener HTTP 80 → web-tg.
3.  Auto Scaling group web-asg from web-lt, subnets public-a and public-b, attach to web-tg, desired 2, min 1, max 2.

### CLI

``` bash
aws ec2 create-launch-template --launch-template-name web-lt --launch-template-data file://lt.jsonaws elbv2 create-target-group --name web-tg --protocol HTTP --port 80 --vpc-id $VPC_ID --health-check-path /aws elbv2 create-load-balancer --name web-alb --subnets $PUBLIC_A $PUBLIC_B --security-groups $SG_IDaws elbv2 create-listener --load-balancer-arn $ALB_ARN --protocol HTTP --port 80 --default-actions Type=forward,TargetGroupArn=$TG_ARNaws autoscaling create-auto-scaling-group --auto-scaling-group-name web-asg --launch-template 'LaunchTemplateName=web-lt,Version=$Latest' --min-size 1 --max-size 2 --desired-capacity 2 --vpc-zone-identifier $PUBLIC_A,$PUBLIC_B --target-group-arns $TG_ARNaws elbv2 describe-target-health --target-group-arn $TG_ARN
```

### Check it worked

Both targets are healthy; refreshing the ALB's DNS name alternates between instances. Terminate one: within minutes the group launches a replacement.

### Clean up

- `aws autoscaling delete-auto-scaling-group --auto-scaling-group-name web-asg --force-delete`
- `aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN`
- `aws elbv2 delete-target-group --target-group-arn $TG_ARN`
- `aws ec2 delete-launch-template --launch-template-name web-lt`

### For the exam

- ALB = layer 7 (paths, hosts, HTTP); NLB = layer 4 (TCP/UDP, static IPs, very high throughput).
- Multi-AZ plus Auto Scaling is the default answer for 'highly available web tier'.

**Official guide:** [Elastic Load Balancing with Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/autoscaling-load-balancer.html)

## 07. RDS: a private MySQL database

Resilient architectures · about 45 minutes

**Cost:** A db.t4g.micro (or db.t3.micro) single-AZ instance with 20 GB: free-tier hours or credits may cover it. Delete it the same day.

**Goal.** Run MySQL in the private subnet, reachable only from the web security group, with the password kept in Secrets Manager.

### Console

1.  Create a second private subnet in ap-south-1b (10.0.12.0/24): a DB subnet group needs two AZs.
2.  Security group db-sg: inbound MySQL 3306 only from web-sg (choose the group, not an IP).
3.  RDS → Create database → MySQL, Free tier template, db.t4g.micro, not publicly accessible, subnet group with both private subnets, db-sg, Manage master credentials in Secrets Manager.

### CLI

``` bash
aws rds create-db-subnet-group --db-subnet-group-name lab-db --db-subnet-group-description lab --subnet-ids $PRIVATE_A $PRIVATE_Baws rds create-db-instance --db-instance-identifier lab-mysql --engine mysql --db-instance-class db.t4g.micro --allocated-storage 20 --master-username admin --manage-master-user-password --no-publicly-accessible --db-subnet-group-name lab-db --vpc-security-group-ids $DB_SG_IDaws rds describe-db-instances --db-instance-identifier lab-mysql --query DBInstances[].Endpoint
```

### Check it worked

From the Lab 5 instance (in web-sg), mysql -h \<endpoint\> -u admin -p connects; from your laptop it times out.

### Clean up

- `aws rds delete-db-instance --db-instance-identifier lab-mysql --skip-final-snapshot --delete-automated-backups`
- Then delete the DB subnet group and db-sg.

### For the exam

- Multi-AZ = synchronous standby for failover; read replicas = asynchronous copies for read scaling.
- Reference a security group as the source to allow 'only the app tier'.

**Official guide:** [Amazon RDS user guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)

## 08. Serverless: Lambda behind an HTTP API

High-performing and cost-optimised architectures · about 30 minutes

**Cost:** No charge for a few hundred requests (Lambda and API Gateway include free monthly requests).

**Goal.** Deploy a Python function and call it from a public URL with no servers to manage.

### Console

1.  Lambda → Create function hello, Python 3.12, new execution role with basic Lambda permissions. Code: return a JSON greeting.
2.  Add trigger → API Gateway → HTTP API, security Open. Copy the API endpoint.
3.  Monitor tab: open the CloudWatch log group and find your invocation.

### CLI

``` bash
aws lambda create-function --function-name hello --runtime python3.12 --role $LAMBDA_ROLE_ARN --handler app.handler --zip-file fileb://function.zipaws apigatewayv2 create-api --name hello-api --protocol-type HTTP --target $FUNCTION_ARNaws lambda add-permission --function-name hello --statement-id apigw --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn $API_EXECUTE_ARNaws lambda invoke --function-name hello out.json
```

### Check it worked

curl on the API endpoint returns the JSON; the log group shows one START/END/REPORT block per call.

### Clean up

- `aws apigatewayv2 delete-api --api-id $API_ID`
- `aws lambda delete-function --function-name hello`
- Delete the log group /aws/lambda/hello and the execution role.

### For the exam

- Lambda: up to 15 minutes per invocation, pay per request and duration.
- HTTP APIs are cheaper and simpler than REST APIs; REST APIs add features such as usage plans and request validation.

**Official guide:** [Lambda with API Gateway](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html)

## 09. CloudTrail and an alarm on root-user activity

Secure architectures · about 45 minutes

**Cost:** The first trail's management events are free; the CloudWatch Logs, alarm and SNS email for a lab stay well within free amounts.

**Goal.** Record every API call in the account and get an email whenever the root user is used (the same idea TenantWall uses).

### Console

1.  CloudTrail → Create trail lab-trail (multi-region), new S3 bucket, send to CloudWatch Logs (new log group and role).
2.  SNS → topic security-alerts → email subscription → confirm the email.
3.  CloudWatch → Log group → Metric filter with the root-usage pattern below → alarm when Sum ≥ 1 in 5 minutes → notify security-alerts.

### CLI

``` bash
aws cloudtrail create-trail --name lab-trail --s3-bucket-name $TRAIL_BUCKET --is-multi-region-trail --cloud-watch-logs-log-group-arn $LOG_GROUP_ARN --cloud-watch-logs-role-arn $TRAIL_ROLE_ARNaws cloudtrail start-logging --name lab-trailaws sns create-topic --name security-alertsaws sns subscribe --topic-arn $TOPIC_ARN --protocol email --notification-endpoint $EMAILaws logs put-metric-filter --log-group-name $LOG_GROUP --filter-name root-usage --filter-pattern file://root-pattern.txt --metric-transformations metricName=RootUsage,metricNamespace=Security,metricValue=1aws cloudwatch put-metric-alarm --alarm-name root-usage --metric-name RootUsage --namespace Security --statistic Sum --period 300 --threshold 1 --comparison-operator GreaterThanOrEqualToThreshold --evaluation-periods 1 --alarm-actions $TOPIC_ARN
```

### Check it worked

Sign in as root once: within about 5–15 minutes the alarm goes to ALARM and you get the email. Filter pattern: { \$.userIdentity.type = "Root" && \$.userIdentity.invokedBy NOT EXISTS && \$.eventType != "AwsServiceEvent" }

### Clean up

- Keep the trail if you like (management events in one trail are free); otherwise stop logging and delete the trail, alarm, metric filter, log group, topic and bucket.

### For the exam

- CloudTrail = who did what (API audit); CloudWatch = metrics, logs and alarms; Config = resource configuration history and rules.
- GuardDuty analyses CloudTrail, VPC Flow Logs and DNS logs for threats.

**Official guide:** [CloudWatch alarms for CloudTrail events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudwatch-alarms-for-cloudtrail.html)

## 10. KMS: encrypt, decrypt and envelope encryption

Secure architectures · about 30 minutes

**Cost:** A customer managed key has a small monthly fee, prorated by the hour, plus per-request charges after a free amount. Schedule deletion the same day.

**Goal.** Create a key, encrypt a file with it, and generate a data key the way envelope encryption works.

### Console

1.  KMS → Create key → Symmetric, encrypt and decrypt, alias lab-key; key administrator and user = your IAM user.
2.  Read the key policy: it decides who can use the key, in addition to IAM policies.
3.  Use the CLI lines below, then schedule deletion with a 7-day waiting period.

### CLI

``` bash
aws kms create-key --description lab-keyaws kms create-alias --alias-name alias/lab-key --target-key-id $KEY_IDaws kms encrypt --key-id alias/lab-key --plaintext fileb://secret.txt --query CiphertextBlob --output textaws kms decrypt --ciphertext-blob fileb://secret.enc --query Plaintext --output textaws kms generate-data-key --key-id alias/lab-key --key-spec AES_256aws kms schedule-key-deletion --key-id $KEY_ID --pending-window-in-days 7
```

### Check it worked

Decrypting gives back the original (Base64-decode the output). generate-data-key returns the same data key twice: in plain text and encrypted under lab-key.

### Clean up

- schedule-key-deletion (above) with 7 days; the alias is deleted with the key. The key cannot be used while deletion is pending.

### For the exam

- KMS encrypts at most 4 KB directly; bigger data uses envelope encryption with a data key.
- SSE-KMS on S3 gives audit trails of key use in CloudTrail; SSE-S3 does not.

**Official guide:** [AWS KMS concepts](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html)

## 11. Teardown checklist and cost check

Cost-optimised architectures · about 20 minutes

**Cost:** No charge.

**Goal.** Make sure nothing is left running, then check the bill.

### Console

1.  Run through the list: Auto Scaling groups, load balancers, target groups, instances, RDS databases, NAT gateways (should be none), Elastic IPs, EBS volumes and snapshots, KMS keys, S3 buckets, CloudWatch log groups, Lambda functions, APIs.
2.  Delete lab-vpc last; then delete the ec2-s3-read role and instance profile.
3.  Billing → Bills: check the month; Cost Explorer: group by service. Anything not near zero tells you what you missed.

### CLI

``` bash
aws ec2 describe-instances --filters Name=instance-state-name,Values=running --query Reservations[].Instances[].InstanceIdaws elbv2 describe-load-balancers --query LoadBalancers[].LoadBalancerNameaws rds describe-db-instances --query DBInstances[].DBInstanceIdentifieraws ec2 describe-addressesaws ec2 describe-volumes --filters Name=status,Values=availableaws iam remove-role-from-instance-profile --instance-profile-name ec2-s3-read --role-name ec2-s3-readaws iam delete-instance-profile --instance-profile-name ec2-s3-read
```

### Check it worked

Every describe command returns an empty list, and the next day's bill shows no new charges.

### Clean up

- Repeat this checklist after every lab session, not only at the end.

### For the exam

- Unattached Elastic IPs and EBS volumes keep costing money after an instance is gone.
- Tag everything (Project=lab) so Cost Explorer and the Tag Editor find it.

**Official guide:** [Avoiding unexpected charges](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/checklistforunwantedcharges.html)
