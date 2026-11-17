"""Check every AWS CLI line in the lab workbook against the AWS service models shipped in botocore:
the service exists, the operation exists, every --option is a real input parameter (or a documented CLI-only option),
and every required parameter is given. Usage: <python with botocore> generated/src/test_awslab.py"""
import os, shlex, sys
import botocore.session
from botocore import xform_name
sys.path.insert(0, os.path.dirname(__file__)); from awslab_data import LABS
S = botocore.session.get_session()
GLOBAL = {"--region", "--query", "--output", "--profile", "--no-cli-pager", "--cli-input-json"}
CUSTOM = {("lambda", "create-function"): {"--zip-file"}, ("ec2", "authorize-security-group-ingress"): {"--protocol", "--port", "--cidr", "--source-group"},
          ("sns", "subscribe"): {"--notification-endpoint"},
          ("ec2", "run-instances"): {"--count"}}                          # the CLI replaces MinCount/MaxCount with --count   # the CLI renames Endpoint to --notification-endpoint                       # CLI customisations not in the API model
CUSTOM_REMOVE = {("lambda", "create-function"): {"--code"}, ("sns", "subscribe"): {"--endpoint"}, ("ec2", "run-instances"): {"--min-count", "--max-count"}}                    # --zip-file supplies Code
HIGH_LEVEL = {("s3", "cp"), ("s3", "ls"), ("s3", "mb"), ("s3", "rb")}           # aws s3 commands are CLI-only
POSITIONAL = {("lambda", "invoke"): 1}                                         # outfile argument
n = 0
for L in LABS:
    lines = L["cli"] + [c for c in L["cleanup"] if c.startswith("aws ")]
    assert L["cli"], L["id"]
    for line in lines:
        t = shlex.split(line); assert t[0] == "aws", line
        svc, op = t[1], t[2]; n += 1
        if (svc, op) in HIGH_LEVEL: continue
        model = S.get_service_model({"s3api": "s3"}.get(svc, svc))       # the CLI calls the S3 API "s3api"
        ops = {xform_name(o, "-"): o for o in model.operation_names}
        assert op in ops, f"{svc} {op}: no such operation"
        shape = model.operation_model(ops[op]).input_shape
        members = {("--" + xform_name(m, "-")): s for m, s in (shape.members.items() if shape else [])}
        given, pos, i = set(), 0, 3
        while i < len(t):
            a = t[i]
            if not a.startswith("--"): pos += 1; i += 1; continue
            if a in GLOBAL or a in CUSTOM.get((svc, op), set()): given.add(a); i += 2 if a not in {"--no-cli-pager"} else 1; continue
            if a in members:
                given.add(a)
                if members[a].type_name == "boolean" and (i + 1 == len(t) or t[i + 1].startswith("--")): i += 1
                elif members[a].type_name == "list":                         # lists take one or more space-separated values
                    i += 1
                    while i < len(t) and not t[i].startswith("--"): i += 1
                else: i += 2
                continue
            if a.startswith("--no-") and ("--" + a[5:]) in members and members["--" + a[5:]].type_name == "boolean": given.add("--" + a[5:]); i += 1; continue
            raise AssertionError(f"{line}\n  unknown option {a}")
        assert pos == POSITIONAL.get((svc, op), 0), f"{line}: unexpected positional arguments"
        req = {"--" + xform_name(r, "-") for r in (shape.required_members if shape else [])} - CUSTOM_REMOVE.get((svc, op), set())
        if (svc, op) == ("lambda", "invoke"): req -= set()
        missing = req - given
        assert not missing, f"{line}\n  missing required {missing}"
print(f"{n} CLI commands in {len(LABS)} labs checked against botocore service models")
