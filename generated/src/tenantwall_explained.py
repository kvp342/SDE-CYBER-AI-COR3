"""TenantWall study material: every term, policy statement, scenario and monitoring setting, with the 17 Nov 2026 results. Run: python3 generated/src/tenantwall_explained.py"""
import html, io, pathlib, re, subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Fit
from reportlab.pdfgen import canvas
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "generated"; SRC = OUT / "src"
GH = "https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/"
TREE = "https://github.com/kvp342/intrusion-detection-and-prevention/tree/ccr-ca7232a7-t7lq94/"
E = html.escape
USED = set()
def K(path, label=None):
    """Link to a kit file; every path is checked to exist before the PDF is built."""
    USED.add(path)
    url = (TREE + path.rstrip("/")) if path.endswith("/") else GH + path
    return f'<a class="kit" href="{url}">{E(label or path.replace("generated/", ""))}</a>'
def L(url, label): return f'<a href="{url}">{E(label)}</a>'
SOURCES = []
def S(url, label):
    """Cite an outside source: numbered in the Sources section."""
    if (url, label) not in SOURCES: SOURCES.append((url, label))
    n = SOURCES.index((url, label)) + 1
    return f'<sup><a href="#src">[{n}]</a></sup>'
def T(head, rows, cls=""):
    return f'<table class="{cls}"><thead><tr>{"".join(f"<th>{h}</th>" for h in head)}</tr></thead><tbody>' + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>"
def UL(items): return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

SEC = []
def sec(id, title, body): SEC.append((id, title, body))
EVAL = ("https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html", "AWS IAM: policy evaluation logic")
ELEM = ("https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html", "AWS IAM: JSON policy element reference")
VARS = ("https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_variables.html", "AWS IAM: policy variables")
ABAC = ("https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html", "AWS IAM: what is ABAC?")
COND = ("https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition_operators.html", "AWS IAM: condition operators")
GKEY = ("https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html", "AWS IAM: global condition keys")
EC2T = ("https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/supported-iam-actions-tagging.html", "Amazon EC2: grant permission to tag resources during creation")
DEC = ("https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html", "AWS STS: DecodeAuthorizationMessage")
CT = ("https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html", "AWS CloudTrail concepts")
CTD = ("https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html", "AWS CloudTrail: data events")
VAL = ("https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html", "AWS CloudTrail: log file integrity validation")
MF = ("https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html", "CloudWatch Logs: filter pattern syntax")
ALM = ("https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html", "CloudWatch: using alarms")
SNS = ("https://docs.aws.amazon.com/sns/latest/dg/sns-email-notifications.html", "Amazon SNS: email notifications")
AA = ("https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html", "IAM Access Analyzer policy validation")
GEN = ("https://awspolicygen.s3.amazonaws.com/policygen.html", "AWS Policy Generator")
C = lambda x: S(*x)
code = lambda t: "<pre>" + E(t) + "</pre>"

sec("idea", "TenantWall in plain words", UL([
 "<b>The problem:</b> several teams share <b>one AWS account</b>. By default, any user with EC2 or S3 permissions could touch another team's servers and files.",
 "<b>The usual fix (RBAC):</b> one role or policy per team. It works, but the number of policies grows with every new team, and someone must edit IAM each time.",
 "<b>TenantWall's fix (ABAC):</b> put a <b>Team tag</b> on every user and every resource, and write <b>one</b> set of policies that says \"you may touch a resource only if its Team tag equals your Team tag\". Adding a team means adding tags, not policies." + C(ABAC),
 "<b>Four layers:</b> (1) tagged IAM users; (2) <code>TenantABAC_EC2</code> for servers; (3) <code>TenantABAC_S3</code> for files under your team's folder (prefix); (4) a <b>bucket policy</b> that blocks other teams' prefixes and unencrypted HTTP even if an identity policy is wrong.",
 "<b>Proof:</b> 14 scenarios (allowed and refused) run with real users alpha_user and beta_user; tonight: <b>14 of 14 passed</b>.",
 "<b>Your professor's additions (now done):</b> CloudTrail records every call, CloudWatch counts refusals and tag/policy changes and emails the admin, explicit vs implicit deny is labelled for every refusal, Access Analyzer validates the policies, and the diagrams use official AWS icons."]))

sec("terms", "Every AWS term you will hear", T(["Term", "Meaning in one or two lines"], [
 ["AWS account", "The container for everything; has a 12-digit ID. TenantWall's teams all live in one account."],
 ["Region", "A geographic location (yours: us-east-1). Most resources live in one region; IAM is global."],
 ["Root user", "The account owner's login. Powerful and risky: use an admin IAM user (twadmin) for daily work."],
 ["IAM user", "A person or program with long-term credentials: alpha_user, beta_user, twadmin."],
 ["Access key / CLI profile", "The key pair the AWS CLI uses. Your profiles admin, alpha and beta each hold one user's keys in ~/.aws/credentials."],
 ["STS", "Security Token Service: temporary credentials, 'who am I' (GetCallerIdentity), and decoding EC2 refusal messages."],
 ["Tag", "A key=value label on a user or resource, e.g. Team=alpha. ABAC decides from tags."],
 ["ARN", "Amazon Resource Name: arn:partition:service:region:account:resource, e.g. arn:aws:s3:::bucket/alpha/report.txt (S3 has no region/account in object ARNs)."],
 ["Policy", "A JSON document of permissions. Identity-based = attached to a user, group or role. Resource-based = attached to the resource (the bucket policy)."],
 ["Statement / Sid", "One rule inside a policy; Sid is its name (e.g. NoSelfPromotion)."],
 ["Effect", "Allow or Deny."],
 ["Action", "The API call(s), e.g. ec2:RunInstances, s3:GetObject. Wildcards allowed: ec2:Describe*."],
 ["Resource / NotResource", "Which ARNs the statement covers; NotResource = every ARN except these."],
 ["Principal", "Who the statement applies to; only in resource-based policies (\"*\" = anyone)."],
 ["Condition", "Extra tests that must be true, built from an operator and a key: StringEquals { ec2:ResourceTag/Team: ... }." + C(COND)],
 ["Policy variable", "${aws:PrincipalTag/Team} is replaced at request time by the caller's Team tag: one policy works for every team." + C(VARS)],
 ["Explicit deny", "A Deny statement matched. It beats every Allow, anywhere." + C(EVAL)],
 ["Implicit deny", "Nothing allowed the request. The default for everything."],
 ["DryRun", "EC2 checks permissions without doing the action: success shows as DryRunOperation, refusal as UnauthorizedOperation."],
 ["Encoded authorization message", "EC2 refusals include an encoded blob; sts:DecodeAuthorizationMessage turns it into JSON showing explicitDeny true or false and the matched context." + C(DEC)]]) + C(ELEM))

sec("eval", "How AWS decides every request", "<ol><li>Start with <b>deny by default</b> (implicit).</li><li>Collect every policy that applies: the caller's identity policies, the resource's policy (bucket policy), and any boundaries or organisation rules.</li><li>If <b>any statement with Effect Deny matches</b>, the answer is <b>explicit deny</b>. Stop.</li><li>Otherwise, if an <b>Allow</b> matches (in the same account, an identity policy or the resource policy is enough), the answer is <b>allow</b>.</li><li>Otherwise it stays <b>implicit deny</b>.</li></ol>" + C(EVAL) +
 '<p class="note">Why TenantWall uses both: implicit deny is the quiet default (alpha is simply never allowed to touch beta); explicit Deny statements are a <b>second lock</b> that still holds if someone later adds a too-broad Allow. This is the explicit vs implicit deny your professor asked for.</p>')

sec("ec2", "TenantABAC_EC2, statement by statement", T(["Sid", "What it says", "Why"], [
 ["ReadOnlyEverywhere", "Allow ec2:Describe* on *", "Describe calls cannot be limited per resource, so every team can see the list of instances (a stated limitation)."],
 ["ManageOnlyOwnTeamInstances", "Allow Start/Stop/Reboot/Terminate on instances where ec2:ResourceTag/Team = ${aws:PrincipalTag/Team}", "You may operate an instance only if its Team tag equals yours (scenarios 6, 7)."],
 ["LaunchOnlyIfTaggedWithOwnTeamAndSmallType", "Allow RunInstances for the instance only if the request tags Team = your team and the type is t2.micro or t3.micro", "No untagged, wrongly tagged or large instances (scenarios 2, 3, 4)." + C(EC2T)],
 ["RunInstancesSupportingResources", "Allow RunInstances on every resource except the instance (NotResource)", "A launch also touches the image, subnet, security group, volume and network interface; those need permission too."],
 ["TagOnlyAtCreation", "Allow CreateTags only when ec2:CreateAction = RunInstances", "Tags can be set while launching, never changed later, so nobody can relabel an instance into another team (scenario 8)."],
 ["DecodeOwnDenials", "Allow sts:DecodeAuthorizationMessage", "Lets a user read why EC2 refused them (used to label explicit vs implicit)."],
 ["NoSelfPromotion", "<b>Deny</b> iam:TagUser, UntagUser, PutUserPolicy, AttachUserPolicy, AddUserToGroup", "Without it a user could change their own Team tag or permissions and walk into another team: the explicit lock (scenario 9)."]]))

sec("s3", "TenantABAC_S3 and the bucket policy", "<h3>TenantABAC_S3 (identity policy)</h3>" + T(["Statement", "What it allows"], [
 ["Objects", "GetObject, PutObject, DeleteObject on bucket/${aws:PrincipalTag/Team}/*: only inside your own team's folder"],
 ["Listing", "ListBucket on the bucket only when s3:prefix matches ${aws:PrincipalTag/Team}/*: you can list your folder, not others' (scenario 12, implicit)"]]) +
 "<h3>Bucket policy (resource policy, the second lock)</h3>" + T(["Sid", "What it denies"], [
 ["DenyNonTLS", "Everything, for everyone, when aws:SecureTransport is false: no plain-HTTP access (scenario 13, explicit)." + C(GKEY)],
 ["OnlyAlphaTouchesAlphaPrefix", "Any S3 action on alpha/* unless the caller's Team tag is alpha or the caller is the admin user (ArnNotEquals aws:PrincipalArn)"],
 ["OnlyBetaTouchesBetaPrefix", "The same for beta/*: alpha reading beta/secret.txt is an <b>explicit</b> deny (scenario 11)"]]) +
 '<p class="note">Two conditions in one statement are joined with AND: the Deny applies only when the caller is not that team <b>and</b> not the admin. Inside one condition key, several values are OR.</p>')

sec("tests", "The 14 scenarios and what decides each", T(["#", "Who / what", "Result", "Deny type", "Decided by"], [
 ["1", "alpha launches t3.micro tagged Team=alpha", "Allowed", "—", "LaunchOnlyIfTagged… + SupportingResources + TagOnlyAtCreation"],
 ["2", "alpha launches with no Team tag (DryRun)", "Refused", "Implicit", "aws:RequestTag/Team missing, so no Allow matches"],
 ["3", "alpha launches tagged Team=beta (DryRun)", "Refused", "Implicit", "Tag ≠ own team"],
 ["4", "alpha launches t3.large (DryRun)", "Refused", "Implicit", "Type not t2/t3.micro"],
 ["5", "beta launches its own t3.micro", "Allowed", "—", "Same statements, for beta"],
 ["6", "alpha stops beta's instance (DryRun)", "Refused", "Implicit", "ResourceTag/Team ≠ alpha"],
 ["7", "alpha stops its own instance (DryRun)", "Allowed", "—", "ManageOnlyOwnTeamInstances"],
 ["8", "alpha retags its instance to Team=beta (DryRun)", "Refused", "Implicit", "TagOnlyAtCreation: not during RunInstances"],
 ["9", "alpha tags itself Team=beta (IAM)", "Refused", "Explicit", "NoSelfPromotion"],
 ["10", "alpha uploads alpha/scenario10-report.txt", "Allowed", "—", "TenantABAC_S3"],
 ["11", "alpha reads beta/secret.txt", "Refused", "Explicit", "Bucket policy OnlyBetaTouchesBetaPrefix"],
 ["12", "alpha lists beta/", "Refused", "Implicit", "ListBucket allowed only for alpha/ prefix"],
 ["13", "alpha reads its own file over plain HTTP", "Refused", "Explicit", "Bucket policy DenyNonTLS"],
 ["14", "Simulator: alpha_user TerminateInstances on beta's instance", "implicitDeny", "Implicit", "No Allow for another team's instance"]]) +
 '<p class="note"><b>Tonight (17 Nov 2026) on the real account: 14 of 14 matched.</b> Afterwards alpha_user still had Team=alpha and its instance kept Team=alpha: no refused call changed anything. The script cleaned up both instances and the uploaded file. Log: real_aws_run_log_2026-11-17.txt in your folder.</p>')

sec("monitor", "Monitoring: CloudTrail, CloudWatch, SNS (what each setting means)", T(["Piece (your name)", "Setting", "Meaning"], [
 ["CloudTrail trail (tenantwall-trail)", "Multi-region, global service events", "Records API calls in every region, plus IAM (a global service)." + C(CT)],
 ["", "Management events: All", "Control-plane calls: RunInstances, TagUser, PutBucketPolicy … (reads and writes)."],
 ["", "Data events: S3 objects in the lab bucket", "Object-level calls such as GetObject and PutObject; off by default and billed, so limited to one bucket." + C(CTD)],
 ["", "Log file validation", "CloudTrail signs digest files so you can prove logs were not altered." + C(VAL)],
 ["Log bucket (tenantwall-logs-…)", "Private, versioned, encrypted; bucket policy lets only this trail write (aws:SourceArn), denies HTTP", "Where the raw log files go; nobody else can write or read over plain HTTP."],
 ["CloudWatch Logs group (/tenantwall/cloudtrail)", "30-day retention; role TenantWallCloudTrailToCWL", "A searchable copy of the events; the role lets CloudTrail write into it (logs:CreateLogStream, PutLogEvents)."],
 ["Metric filter AccessDenied", "{ ($.errorCode = \"AccessDenied*\") || ($.errorCode = \"*UnauthorizedOperation\") }", "Each matching event adds 1 to metric TenantWall/AccessDenied. $. reads a JSON field; * is a wildcard; || is OR." + C(MF)],
 ["Metric filter TagTampering", "TagUser, UntagUser, DeleteTags, group/policy changes to users, or a refused CreateTags", "Someone touched the labels or memberships the wall depends on."],
 ["Metric filter PolicyChange", "PutBucketPolicy, DeleteBucketPolicy, PutUserPolicy, PutGroupPolicy, CreatePolicyVersion", "Someone edited a lock itself."],
 ["Alarms TenantWall-*", "Statistic Sum, period 300 s, 1 evaluation period, threshold ≥ 1, missing data = not breaching", "If the count in any 5 minutes is at least 1 → state ALARM → action. No data counts as fine (OK)." + C(ALM)],
 ["", "States OK / ALARM / INSUFFICIENT_DATA", "OK = below threshold; ALARM = breached; INSUFFICIENT_DATA = not enough data yet."],
 ["SNS topic (tenantwall-alerts)", "Email subscription (confirmed)", "The alarm publishes to the topic; SNS emails every confirmed subscriber." + C(SNS)]]))

sec("evidence", "Tonight's evidence (17 Nov 2026)", T(["Professor's request", "Status", "Evidence (in your folder)"], [
 ["1. CloudTrail", "Done, logging", "Trail logging, multi-region, S3 data events on the lab bucket. Logs Insights shows alpha_user's refused EC2/IAM calls (evidence/refused-calls.txt) and the S3 object calls: GetObject beta/secret.txt AccessDenied (scenario 11), ListObjects AccessDenied (12), GetObject over HTTP AccessDenied (13), plus the allowed PutObject/DeleteObject of scenario 10 (evidence/s3-data-events-alpha.txt)"],
 ["2. CloudWatch + email", "Done, fired", "After the run: TenantWall-AccessDenied and TenantWall-TagTampering went to ALARM; PolicyChange stayed OK (no policy edited); alert emails sent to your confirmed address (evidence/alarms.txt; your inbox)"],
 ["3. Diagrams", "Files ready; you export", "diagrams/tenantwall-architecture.drawio and diagrams/tenantwall-flowchart.drawio with official AWS icons: open at app.diagrams.net, check, export PNG"],
 ["4. Policy Generator + Access Analyzer", "Analyzer done; Generator is yours (10 min)", "Access Analyzer: <b>0 findings</b> for TenantABAC_EC2, TenantABAC_S3 and the bucket policy. Policy Generator: rebuild the bucket policy in the web form" + C(GEN) + " and screenshot it"],
 ["5. Explicit vs implicit deny (confirmed)", "Done", "Every refusal labelled explicit or implicit (scenarios 9, 11, 13 explicit; 2, 3, 4, 6, 8, 12, 14 implicit); EC2 refusals proved with sts decode-authorization-message, S3/IAM refusals by the error message, scenario 14 by the policy simulator (implicitDeny)"]]) + C(AA) +
 "<h3>Screenshots to take tomorrow morning (console, 15 minutes)</h3>" + UL([
 "CloudTrail → Trails → tenantwall-trail (Logging on, data events).", "CloudWatch → Alarms (history showing ALARM at about 23:23 IST on 17 Nov).", "The alert email in Gmail.",
 "CloudWatch → Logs Insights with the refused-calls query.", "IAM → Policies → TenantABAC_EC2 → Edit (Access Analyzer panel with no findings).", "Policy Generator page with your bucket policy.", "The exported diagrams."]))

sec("generator", "Policy Generator: exactly what to type", "<p>Open the AWS Policy Generator" + C(GEN) + ". You rebuild your bucket policy's three statements, generate it, and take a screenshot. <b>Do not paste the generated JSON over your real bucket policy</b>: it is only to show your professor that the generator produces the same rules. Replace YOUR-BUCKET and ACCOUNT-ID with your real values (they are in evidence/bucket-policy.json on your laptop).</p>" +
 "<h3>Step 1: Select Policy Type</h3><p>S3 Bucket Policy.</p><h3>Step 2: Add Statement(s): three times</h3>" +
 T(["Field", "Statement A: DenyNonTLS", "Statement B: alpha prefix", "Statement C: beta prefix"], [
 ["Effect", "Deny", "Deny", "Deny"],
 ["Principal", "*", "*", "*"],
 ["AWS Service", "Amazon S3", "Amazon S3", "Amazon S3"],
 ["Actions", "All Actions ('*')", "All Actions ('*')", "All Actions ('*')"],
 ["Amazon Resource Name (ARN)", "arn:aws:s3:::YOUR-BUCKET, arn:aws:s3:::YOUR-BUCKET/*", "arn:aws:s3:::YOUR-BUCKET/alpha/*", "arn:aws:s3:::YOUR-BUCKET/beta/*"],
 ["Add Conditions: 1st", "Bool · aws:SecureTransport · false", "StringNotEquals · aws:PrincipalTag/Team · alpha", "StringNotEquals · aws:PrincipalTag/Team · beta"],
 ["Add Conditions: 2nd", "—", "ArnNotEquals · aws:PrincipalArn · arn:aws:iam::ACCOUNT-ID:user/twadmin", "ArnNotEquals · aws:PrincipalArn · arn:aws:iam::ACCOUNT-ID:user/twadmin"]]) +
 "<p>For each statement: fill the fields, click <b>Add Condition</b> once per condition row, then <b>Add Statement</b>. When all three appear in the list, go to Step 3 and click <b>Generate Policy</b>. Screenshot the statement list and the JSON.</p>" +
 '<p class="note"><b>Compare with your real policy:</b> same Effect, Principal, Action, Resource and Condition in each statement. The generator adds an Id and numbered Sids instead of your names (DenyNonTLS, OnlyAlphaTouchesAlphaPrefix, OnlyBetaTouchesBetaPrefix): that difference is expected. If the Key list does not offer aws:PrincipalTag/Team or aws:PrincipalArn, try typing it; if the form refuses, generate without that condition, screenshot it, and say the tag condition was added by hand, which is what the real policy shows. Then paste the generated JSON into IAM Access Analyzer\'s policy check (bucket policy editor) to show it validates.</p>')

sec("pitch", "Talking about TenantWall in interviews", "<h3>30 seconds</h3><p>\"Teams sharing one AWS account can reach each other's servers and files. I built TenantWall, which isolates them with attribute-based access control: one set of IAM policies compares the Team tag on the user with the Team tag on the resource, and explicit denies stop users from changing their own tags. I tested it with 14 real scenarios on AWS, all as expected, and added CloudTrail and CloudWatch alerting that emailed the admin about refused attempts in under 3 minutes.\"</p>" +
 "<h3>2 minutes (STAR)</h3>" + T(["Part", "What to say"], [
 ["Situation", "Several teams in one AWS account; by default anyone with EC2 or S3 rights could touch another team's resources. Role-per-team policies grow with every team."],
 ["Task", "Isolate teams with a fixed number of policies, prove it works, and detect attempts to break it. Research project with my professor."],
 ["Action", "Tagged users and resources with Team; wrote two ABAC identity policies (EC2, S3) using ${aws:PrincipalTag/Team}; locked tags after creation; explicit Deny on self-tagging; bucket policy denying other prefixes and plain HTTP; validated with IAM Access Analyzer; CloudTrail with S3 data events into CloudWatch Logs, three metric filters, alarms to SNS email."],
 ["Result", "14 of 14 scenarios behaved as expected (10 refusals, each classified explicit or implicit); Access Analyzer found nothing; alarms emailed within 104–143 seconds. I also found a limitation: the filter alerts on any refused call in the account, so the next step is scoping it to tenant users."]]) +
 "<h3>Resume bullets (real numbers)</h3>" + UL([
 "Designed attribute-based access control for a shared S3 bucket and EC2 fleet so each team reaches only its own resources, using tag-matched IAM policies and explicit denies; validated with IAM Access Analyzer (0 findings)",
 "Verified isolation with 14 scenarios on real AWS (10 refusals, each classified as explicit or implicit deny) and built CloudTrail → CloudWatch → SNS alerting that emailed on refused calls within 3 minutes"]) +
 "<h3>Follow-up questions to expect</h3>" + UL(["Why not one AWS account per team? (stronger isolation; TenantWall is for teams that must share one account; accounts are the next step)", "What if an admin tags a resource wrongly? (the model trusts tags; tag changes alarm; tagging is restricted to creation)", "How would you scale to 100 teams? (identity policies stay the same; the bucket policy grows, so move to per-team buckets or accounts)"]))

sec("demo", "Showing your professor (10 minutes)", T(["Minute", "Show", "Say"], [
 ["0–1", "Architecture diagram", "\"Two teams share one account; one tag-based policy set separates them; the right side now detects attempts.\""],
 ["1–3", "Scenario summary (14 of 14) with the deny-type column", "\"Each refusal is labelled explicit or implicit: explicit means a Deny statement matched, implicit means no Allow matched.\""],
 ["3–5", "Policies + Access Analyzer (0 findings) + Policy Generator screenshot", "\"Policies validate cleanly; the bucket policy matches what the Policy Generator produces.\""],
 ["5–7", "Logs Insights refused calls", "\"CloudTrail now records every call, including object reads, with who, what and when.\""],
 ["7–9", "Alarms in ALARM + email", "\"Refusals and tag changes email the admin within minutes; policy edits have their own alarm.\""],
 ["9–10", "Flowchart, limitations, next step", "\"Next: update the paper and submit by 21 March. Which venue do you suggest?\""]]))

sec("viva", "Questions he may ask, with answers", T(["Question", "Answer"], [
 ["Why ABAC instead of a role per team?", "Policy count stays fixed (2 identity policies) for any number of teams; only the bucket policy grows by one statement per team."],
 ["What stops a user changing their own Team tag?", "NoSelfPromotion: an explicit Deny on TagUser/UntagUser and on changing their own policies or groups."],
 ["What stops relabelling an instance later?", "TagOnlyAtCreation: CreateTags is allowed only as part of RunInstances."],
 ["Explicit vs implicit deny?", "Explicit = a Deny statement matched and beats all Allows; implicit = nothing allowed it. We label each refusal using the error message or the decoded EC2 message."],
 ["Why a bucket policy if identity policies already restrict S3?", "Defence in depth: if an identity policy is wrong or broadened, the bucket's explicit Deny still protects each team's prefix and blocks HTTP."],
 ["Why can every team see all instances?", "ec2:Describe* does not support resource-level permissions; it is listed as a limitation."],
 ["What are CloudTrail data events?", "Object-level S3 calls like GetObject; management events alone would miss reads of other teams' files."],
 ["How fast do alerts arrive?", "Minutes: CloudTrail delivers to CloudWatch Logs, the filter counts, the alarm evaluates every 5 minutes, SNS emails."],
 ["Can logs be tampered with?", "Log-file validation lets you prove integrity; the log bucket allows writes only from this trail and denies HTTP."],
 ["What did Access Analyzer report?", "No errors, security warnings, warnings or suggestions for any of the three policies."],
 ["What if tagging is wrong?", "The model trusts correct tags at creation; that is why tags are locked after creation and changes alarm."],
 ["Cost?", "Management events in the first trail are free; S3 data events and CloudWatch Logs are billed per volume, so data events are limited to one bucket."],
 ["Why t2/t3.micro only?", "Cost control per team, enforced with the ec2:InstanceType condition (scenario 4)."],
 ["What is ${aws:PrincipalTag/Team}?", "A policy variable replaced at request time by the caller's Team tag."],
 ["Limitations?", "Shared Describe visibility, shared network and quotas, listing guarded on one side, EBS volumes not covered, bucket policy size limit, trust in tagging, small evaluation."]]))
# ------------------------------------------------------------------ build
for p in USED: assert (ROOT / p.rstrip("/")).exists(), p        # every kit link points at a real file
CSS = """@page { size: A4; margin: 13mm 14mm 15mm; } * { box-sizing: border-box; } html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 9.2pt/1.5 Inter, sans-serif; color: #1e293b; } a { color: #1d4ed8; text-decoration: none; } a.kit { font: 600 7.8pt "JetBrains Mono"; color: #0f766e; }
.eb { font: 600 8pt "JetBrains Mono"; letter-spacing: .14em; color: #c2410c; margin: 0 0 2mm; } h1 { font: 700 30pt/1.05 "Space Grotesk"; margin: 0 0 3mm; color: #0f172a; } h1 span { color: #c2410c; }
h2 { font: 700 15pt "Space Grotesk"; color: #0f172a; margin: 0 0 3mm; padding-bottom: 1.5mm; border-bottom: 2px solid #c2410c; display: flex; align-items: baseline; }
h2 .num { color: #c2410c; margin-right: 3mm; } h2 .back { margin-left: auto; font: 600 7.5pt "JetBrains Mono"; color: #64748b; } h3 { font: 700 10.5pt "Space Grotesk"; color: #1d4ed8; margin: 3mm 0 1.5mm; }
section.sec { break-before: page; } table { border-collapse: collapse; width: 100%; margin: 1mm 0 2mm; break-inside: auto; } tr { break-inside: avoid; }
th { font: 600 7pt "JetBrains Mono"; text-transform: uppercase; letter-spacing: .05em; color: #64748b; background: #f1f5f9; padding: 1.3mm 2mm; text-align: left; }
td { border-bottom: 1px solid #e2e8f0; padding: 1.4mm 2mm; vertical-align: top; } table.km td:first-child { width: 45%; } ul { padding-left: 5mm; margin: 1mm 0; } li { margin-bottom: 1.6mm; }
.note { background: #fff7ed; border-left: 3px solid #c2410c; padding: 2mm 3mm; margin: 3mm 0; font-size: 8.6pt; } .lead { font-size: 10.5pt; } sup a { font: 600 6.5pt "JetBrains Mono"; color: #c2410c; }
table.ix td { padding: 1.6mm 2mm; } td.pg { text-align: right; font-family: "JetBrains Mono"; width: 14mm; } ol.src { font-size: 7.8pt; padding-left: 6mm; } ol.src li { margin-bottom: 1mm; word-break: break-all; }"""
def body(pages):
    pg = lambda k: str(pages.get(k, "00")) if pages else "00"
    ix = "".join(f'<tr><td><a href="#{i}">{n + 1}. {E(t)}</a></td><td class="pg"><a href="#{i}">{pg(i)}</a></td></tr>' for n, (i, t, _) in enumerate(SEC))
    ix += f'<tr><td><a href="#src">Sources ({len(SOURCES)})</a></td><td class="pg"><a href="#src">{pg("src")}</a></td></tr>'
    out = [f'''<section><p class="eb">TENANTWALL · STUDY MATERIAL</p><h1>TenantWall explained<br><span>every term, policy and alarm</span></h1>
<p class="lead">Everything about your project in one place: the idea, every AWS term, how AWS decides each request, your three policies statement by statement, what decides each of the 14 scenarios, what every monitoring setting means, tonight's real results for your professor's five requests, a 10-minute demo, and the questions he may ask.</p>
<table class="ix"><thead><tr><th>Section</th><th class="pg">Page</th></tr></thead><tbody>{ix}</tbody></table>
<p class="note">Based on your real setup (account in us-east-1, users alpha_user, beta_user, twadmin; policies TenantABAC_EC2 and TenantABAC_S3; the lab bucket policy) and on the run of 17 Nov 2026: 14 of 14 scenarios, two alarms fired, Access Analyzer 0 findings.</p></section>''']
    for n, (i, t, b) in enumerate(SEC):
        out.append(f'<section class="sec" id="{i}"><h2><span class="num">{n + 1:02d}</span>{E(t)}<a class="back" href="#top">↑ Index</a></h2>{b}</section>')
    out.append('<section class="sec" id="src"><h2><span class="num">··</span>Sources<a class="back" href="#top">↑ Index</a></h2><p>Checked on 17 Nov 2026. Blogs and forum posts are single opinions; official pages win when they disagree. Numbers marked as rules of thumb are not company requirements.</p><ol class="src">'
               + "".join(f'<li><a href="{u}">{E(l)}</a><br>{E(u)}</li>' for u, l in SOURCES) + "</ol></section>")
    return "".join(out)
js = SRC / "rtwe.js"
def render(pages, name):
    (SRC / "twexplained.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div id="top"></div>{body(pages)}</body></html>')
    js.write_text("const { chromium } = require('playwright'); (async () => { const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://' + __dirname + '/twexplained.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.pdf({ path: __dirname + '/" + name + "', format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); })();")
    subprocess.run(["node", str(js)], check=True)
    r = PdfReader(str(SRC / name)); return {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}, len(r.pages)
d1, n1 = render(None, "e1.pdf"); d2, n2 = render(d1, "e2.pdf"); assert n1 == n2 and all(d1[i] == d2[i] for i, _, _ in SEC)
w = PdfWriter(clone_from=PdfReader(str(SRC / "e2.pdf"))); w.add_outline_item("Index", 0, fit=Fit.fit())
for n, (i, t, _) in enumerate(SEC): w.add_outline_item(f"{n + 1}. {t}", d2[i] - 1, fit=Fit.fit())
w.add_outline_item("Sources", d2["src"] - 1, fit=Fit.fit())
NP = len(w.pages)
for k, pg in enumerate(w.pages):
    if k == 0: continue
    buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height))); cv.setFont("Helvetica", 7.5); cv.setFillGray(.55)
    cv.drawRightString(float(pg.mediabox.width) - 26, 14, f"{k + 1} / {NP}"); cv.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); pg.compress_content_streams(level=9)
w.add_metadata({"/Title": "TenantWall explained"}); w.write(str(OUT / "tenantwall-explained.pdf"))
for f in ("e1.pdf", "e2.pdf", "rtwe.js", "twexplained.html"): (SRC / f).unlink()
print(NP, "pages;", len(USED), "kit links;", len(SOURCES), "sources;", d2)
