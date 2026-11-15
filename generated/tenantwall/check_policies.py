"""Offline checks for the TenantWall policy files: JSON syntax, IAM policy structure, and a simplified evaluation of the
isolation rules for two tenants. This is a teaching model of IAM evaluation (explicit deny > allow > implicit deny) covering only
the condition operators used here; confirm in your account with IAM Access Analyzer (validate-policy) and the IAM policy simulator.
Run: python3 generated/tenantwall/check_policies.py"""
import json, pathlib, fnmatch, sys
D = pathlib.Path(__file__).parent / "policies"
OPS = {"StringEquals", "StringNotEquals", "StringLike", "Bool", "ForAnyValue:StringEquals"}
bad = 0
def ok(c, m):
    global bad
    print(("ok   " if c else "FAIL ") + m); bad += (not c)
def as_list(x): return x if isinstance(x, list) else [x]
pols = {}
for f in sorted(D.glob("*.json")):
    j = json.loads(f.read_text()); pols[f.name] = j
    if isinstance(j, list): ok(all("DataResources" in s for s in j), f"{f.name}: event selectors"); continue
    ok(j.get("Version") == "2012-10-17" and isinstance(j.get("Statement"), list), f"{f.name}: version and statement list")
    for s in j["Statement"]:
        good = s.get("Effect") in ("Allow", "Deny") and ("Action" in s) and (("Resource" in s) ^ ("NotResource" in s)) \
            and all(":" in a for a in as_list(s["Action"])) and set(s.get("Condition", {})) <= OPS and len(s.get("Sid", "")) > 0
        ok(good, f"{f.name}: {s.get('Sid')} structure")
def sub(v, ctx): return v.replace("${aws:PrincipalTag/tenant}", ctx["tenant"])
def cond_ok(c, ctx):
    for op, kv in c.items():
        for k, want in kv.items():
            want = [sub(w, ctx) for w in as_list(want)]; have = ctx.get(k)
            if op == "StringEquals" and have not in want: return False
            if op == "StringNotEquals" and have in want: return False
            if op == "StringLike" and not any(fnmatch.fnmatchcase(have or "", w) for w in want): return False
            if op == "Bool" and str(have).lower() not in [w.lower() for w in want]: return False
            if op == "ForAnyValue:StringEquals" and not set(have or []) & set(want): return False
    return True
def applies(s, action, res, ctx):
    if not any(fnmatch.fnmatchcase(action, a) for a in as_list(s["Action"])): return False
    if "Resource" in s: m = any(fnmatch.fnmatchcase(res, sub(r, ctx)) for r in as_list(s["Resource"]))
    else: m = not any(fnmatch.fnmatchcase(res, sub(r, ctx)) for r in as_list(s["NotResource"]))
    return m and cond_ok(s.get("Condition", {}), ctx)
def decide(action, res, ctx):
    st = pols["tenant-abac-identity.json"]["Statement"] + pols["tenant-explicit-deny.json"]["Statement"]
    if any(s["Effect"] == "Deny" and applies(s, action, res, ctx) for s in st): return "Deny (explicit)"
    if any(s["Effect"] == "Allow" and applies(s, action, res, ctx) for s in st): return "Allow"
    return "Deny (implicit)"
B = "arn:aws:s3:::tenantwall-data-EXAMPLE"; I = "arn:aws:ec2:ap-south-1:111122223333:instance/i-0abc"
A = {"tenant": "tenant-a"}
CASES = [
 ("A reads own object", "s3:GetObject", f"{B}/tenant-a/report.csv", {}, "Allow"),
 ("A reads B's object", "s3:GetObject", f"{B}/tenant-b/report.csv", {}, "Deny (explicit)"),
 ("A writes into B's prefix", "s3:PutObject", f"{B}/tenant-b/x.txt", {}, "Deny (explicit)"),
 ("A lists own prefix", "s3:ListBucket", B, {"s3:prefix": "tenant-a/2026/"}, "Allow"),
 ("A lists B's prefix", "s3:ListBucket", B, {"s3:prefix": "tenant-b/"}, "Deny (implicit)"),
 ("A starts own instance", "ec2:StartInstances", I, {"aws:ResourceTag/tenant": "tenant-a"}, "Allow"),
 ("A stops B's instance", "ec2:StopInstances", I, {"aws:ResourceTag/tenant": "tenant-b"}, "Deny (explicit)"),
 ("A terminates own instance (not granted)", "ec2:TerminateInstances", I, {"aws:ResourceTag/tenant": "tenant-a"}, "Deny (implicit)"),
 ("A re-tags an instance to tenant-b", "ec2:CreateTags", I, {"aws:TagKeys": ["tenant"]}, "Deny (explicit)"),
 ("A changes own principal tag", "iam:TagRole", "arn:aws:iam::111122223333:role/tenant-a", {"aws:TagKeys": ["tenant"]}, "Deny (explicit)"),
 ("A tags an object", "s3:PutObjectTagging", f"{B}/tenant-a/report.csv", {}, "Deny (explicit)"),
]
for name, act, res, extra, want in CASES:
    got = decide(act, res, {**A, **extra}); ok(got == want, f"{name}: {got}")
bp = pols["bucket-policy-secure-transport.json"]["Statement"][0]
ok(cond_ok(bp["Condition"], {"tenant": "", "aws:SecureTransport": False}) and not cond_ok(bp["Condition"], {"tenant": "", "aws:SecureTransport": True}), "bucket policy denies HTTP, not HTTPS")
print(f"\n{bad} failures"); sys.exit(1 if bad else 0)
