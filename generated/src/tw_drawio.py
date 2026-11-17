"""TenantWall diagrams as draw.io files with the official AWS icon shapes (names checked against draw.io's Sidebar-AWS4.js).
Open them at app.diagrams.net (File > Open) and export as PNG. Run from the repo root: python3 generated/src/tw_drawio.py"""
import pathlib, xml.etree.ElementTree as ET
from html import escape
OUT = pathlib.Path(__file__).resolve().parents[2] / "generated" / "tenantwall" / "diagrams"; OUT.mkdir(parents=True, exist_ok=True)
VERIFIED = {"s3", "ec2", "identity_and_access_management", "cloudtrail", "cloudwatch_2", "sns", "group_aws_cloud_alt", "group_region",   # resIcon / grIcon names
            "users", "user", "permissions", "bucket_with_objects", "alarm", "logs", "email", "role"}                                     # standalone shapes
CAT = {"s3": ("#7AA116", "#60A337"), "ec2": ("#ED7100", "#F78E04"), "identity_and_access_management": ("#DD344C", "#FF5252"),
       "cloudtrail": ("#E7157B", "#FF4F8B"), "cloudwatch_2": ("#E7157B", "#FF4F8B"), "sns": ("#E7157B", "#FF4F8B")}
class D:
    def __init__(s): s.cells, s.ids = [], set()
    def _add(s, cid, xml): assert cid not in s.ids, cid; s.ids.add(cid); s.cells.append(xml)
    def service(s, cid, icon, label, x, y, parent="1", size=60):
        assert icon in VERIFIED; fill, grad = CAT[icon]
        st = (f"sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor={grad};gradientDirection=north;fillColor={fill};strokeColor=#ffffff;dashed=0;"
              f"verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{icon};")
        s._add(cid, f'<mxCell id="{cid}" value="{escape(label)}" style="{st}" vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{size}" height="{size}" as="geometry"/></mxCell>')
    def small(s, cid, icon, label, x, y, parent="1", w=46, h=46):
        assert icon in VERIFIED
        st = (f"sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#232F3D;strokeColor=none;dashed=0;verticalLabelPosition=bottom;"
              f"verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.{icon};")
        s._add(cid, f'<mxCell id="{cid}" value="{escape(label)}" style="{st}" vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    def group(s, cid, icon, label, x, y, w, h, color="#232F3E", parent="1", dashed=0):
        assert icon in VERIFIED
        st = (f"points=[[0,0],[1,0],[1,1],[0,1]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;container=1;pointerEvents=0;"
              f"collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.{icon};strokeColor={color};fillColor=none;verticalAlign=top;align=left;"
              f"spacingLeft=30;fontColor={color};dashed={dashed};")
        s._add(cid, f'<mxCell id="{cid}" value="{escape(label)}" style="{st}" vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    def box(s, cid, label, x, y, w, h, fill="#ffffff", stroke="#232F3E", shape="rounded=1", parent="1"):
        s._add(cid, f'<mxCell id="{cid}" value="{escape(label)}" style="{shape};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize=11;" vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    def edge(s, cid, a, b, label="", color="#545B64", dashed=0, parent="1"):
        assert a in s.ids and b in s.ids, (a, b)
        st = f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;strokeColor={color};strokeWidth=2;dashed={dashed};fontSize=10;fontColor={color};"
        s._add(cid, f'<mxCell id="{cid}" value="{escape(label)}" style="{st}" edge="1" parent="{parent}" source="{a}" target="{b}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    def save(s, name, title):
        xml = (f'<mxfile host="app.diagrams.net"><diagram name="{escape(title)}" id="{name}"><mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" '
               f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1000" math="0" shadow="0"><root>'
               f'<mxCell id="0"/><mxCell id="1" parent="0"/>{"".join(s.cells)}</root></mxGraphModel></diagram></mxfile>')
        ET.fromstring(xml)                                           # well-formed XML
        (OUT / f"{name}.drawio").write_text(xml); return len(s.cells)
GREEN, RED, GREY = "#1E8900", "#D13212", "#545B64"
a = D()
a.group("cloud", "group_aws_cloud_alt", "AWS account (shared by all teams)", 20, 20, 1540, 900)
a.group("region", "group_region", "Region us-east-1 (trail is multi-region)", 40, 60, 1500, 840, color="#00A4A6", parent="cloud", dashed=1)
a.small("teamA", "user", "alpha_user (tag Team=alpha)", 30, 100, "region"); a.small("teamB", "user", "beta_user (tag Team=beta)", 30, 360, "region")
a.service("iam", "identity_and_access_management", "IAM: TenantABAC_EC2 (7 statements) + TenantABAC_S3, matched on ${aws:PrincipalTag/Team}", 300, 220, "region")
a.small("deny", "permissions", "Explicit Deny: NoSelfPromotion (IAM), OnlyAlpha/OnlyBeta prefix Deny + DenyNonTLS (bucket policy)", 300, 420, "region")
a.service("s3", "s3", "Lab S3 bucket (one bucket, two prefixes)", 640, 90, "region"); a.small("pa", "bucket_with_objects", "alpha/", 800, 60, "region"); a.small("pb", "bucket_with_objects", "beta/", 800, 150, "region")
a.service("ec2", "ec2", "EC2 t2/t3.micro instances tagged Team=alpha / Team=beta", 640, 350, "region")
a.service("trail", "cloudtrail", "CloudTrail tenantwall-trail: management + S3 data events, log-file validation", 640, 600, "region")
a.small("logbucket", "bucket_with_objects", "tenantwall-logs-<account> (versioned, encrypted, private)", 400, 640, "region")
a.small("logs", "logs", "CloudWatch Logs /tenantwall/cloudtrail (30-day retention; role TenantWallCloudTrailToCWL)", 900, 610, "region")
a.service("cw", "cloudwatch_2", "Metric filters: AccessDenied, TagTampering, PolicyChange", 1080, 600, "region")
a.small("alarm", "alarm", "Alarms TenantWall-AccessDenied / -TagTampering / -PolicyChange (>=1 in 5 min)", 1250, 610, "region")
a.service("sns", "sns", "SNS topic tenantwall-alerts", 1250, 380, "region"); a.small("mail", "email", "Admin email", 1260, 200, "region")
a.edge("e1", "teamA", "iam", "requests", GREY, parent="region"); a.edge("e2", "teamB", "iam", "requests", GREY, parent="region")
a.edge("e3", "iam", "pa", "allowed: own prefix (TenantABAC_S3)", GREEN, parent="region"); a.edge("e4", "deny", "pb", "refused: beta/ (explicit deny, bucket policy)", RED, parent="region")
a.edge("e5", "iam", "ec2", "allowed: own-team instances, launch only tagged + micro", GREEN, parent="region"); a.edge("e6", "iam", "deny", "", RED, 1, parent="region")
a.edge("e7", "s3", "trail", "object reads (data events)", GREY, 1, parent="region"); a.edge("e8", "ec2", "trail", "API calls", GREY, 1, parent="region")
a.edge("e9", "trail", "logbucket", "", GREY, parent="region"); a.edge("e10", "trail", "logs", "", GREY, parent="region"); a.edge("e11", "logs", "cw", "", GREY, parent="region")
a.edge("e12", "cw", "alarm", "", GREY, parent="region"); a.edge("e13", "alarm", "sns", "", RED, parent="region"); a.edge("e14", "sns", "mail", "email alert", RED, parent="region")
n1 = a.save("tenantwall-architecture", "TenantWall architecture")
f = D(); Y = 40
f.box("s", "A team user sends an AWS request", 560, Y, 240, 50, "#E6F2F8", "#147EBA")
f.box("q1", "Does an explicit Deny match? (NoSelfPromotion, OnlyAlpha/OnlyBeta prefix, DenyNonTLS)", 520, Y + 100, 320, 110, "#FFF4E5", "#ED7100", "rhombus")
f.box("r1", "Refused: EXPLICIT deny", 940, Y + 125, 220, 60, "#FDECEA", "#D13212")
f.box("q2", "Does an Allow match with Team tag = resource's Team tag or prefix?", 520, Y + 270, 320, 110, "#FFF4E5", "#ED7100", "rhombus")
f.box("r2", "Refused: IMPLICIT deny (no Allow matched)", 940, Y + 295, 220, 60, "#FDECEA", "#D13212")
f.box("ok", "Allowed: own team's data only", 560, Y + 440, 240, 55, "#E9F5E9", "#1E8900")
f.box("log", "CloudTrail records every request (allowed and refused)", 900, Y + 450, 300, 50, "#F4F4F4", "#545B64")
f.box("cnt", "Metric filters count refusals, tag/membership changes and policy edits", 900, Y + 540, 300, 50, "#F4F4F4", "#545B64")
f.box("al", "Alarm (any refusal, tag/membership change or policy edit in 5 min) -> SNS -> email", 900, Y + 630, 300, 55, "#FDECEA", "#D13212")
f.edge("f1", "s", "q1"); f.edge("f2", "q1", "r1", "yes", RED); f.edge("f3", "q1", "q2", "no"); f.edge("f4", "q2", "r2", "no", RED); f.edge("f5", "q2", "ok", "yes", GREEN)
f.edge("f6", "r1", "log", "", GREY, 1); f.edge("f7", "r2", "log", "", GREY, 1); f.edge("f8", "ok", "log", "", GREY, 1); f.edge("f9", "log", "cnt"); f.edge("f10", "cnt", "al")
n2 = f.save("tenantwall-flowchart", "TenantWall method flowchart")
print(f"architecture: {n1} cells, flowchart: {n2} cells; XML well-formed; every icon name in the verified draw.io list")
