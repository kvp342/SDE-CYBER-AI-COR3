"""Check OA packs III: 24 unique problems with no overlap against every earlier problem, 90-minute sets, real Saturday dates
outside the exam break, valid Knowledge Base ids, and every reference solution compiled and tested under ASan/UBSan.
Usage: python3 generated/src/test_oa3.py"""
import datetime, os, re, subprocess, sys, tempfile
H = os.path.dirname(__file__); sys.path[:0] = [H, os.path.join(H, "../../sources/kb")]
from oa_data3 import SETS
import oa_data, oa_data2, t_probs, t_probs2, t_probs3
slug = lambda q: q["prac"][0][1].rstrip("/").rsplit("/", 1)[1]
used = {p["slug"] for s in oa_data.SETS + oa_data2.SETS for p in s["probs"]} | {slug(q) for q in t_probs.P + t_probs2.P} | {q["slug"] for q in t_probs3.P}
assert len(used) == 171, len(used)
allp = [p for s in SETS for p in s["probs"]]
assert len(SETS) == 8 and len(allp) == 24 and len({p["slug"] for p in allp}) == 24, "duplicate problem"
assert not used & {p["slug"] for p in allp}, used & {p["slug"] for p in allp}
for s in SETS:
    assert sum(p["mins"] for p in s["probs"]) == 90, s["title"]
    d = datetime.datetime.strptime(s["date"], "Sat %d %b %Y").date(); assert d.weekday() == 5, s["date"]
    assert not (datetime.date(2027, 3, 22) <= d <= datetime.date(2027, 4, 7)), s["date"]
kb_ids = set(re.findall(r'page\("([\w-]+)"', "".join(open(os.path.join(H, "../../sources/kb", f)).read() for f in os.listdir(os.path.join(H, "../../sources/kb")) if f.endswith(".py"))))
kb_ids |= {t["id"] for f in ("t_dsa", "t_cs", "t_method") for t in __import__(f).TOPICS}
missing = {p["kb"] for p in allp} - kb_ids; assert not missing, f"unknown Knowledge Base ids: {missing}"
HDR = r'''#include <bits/stdc++.h>
using namespace std;
struct TreeNode{int val;TreeNode*left,*right;TreeNode(int x):val(x),left(nullptr),right(nullptr){}};
TreeNode* tree(vector<string> v){if(v.empty()||v[0]=="null")return nullptr;TreeNode*r=new TreeNode(stoi(v[0]));queue<TreeNode*>q;q.push(r);size_t i=1;
 while(!q.empty()&&i<v.size()){auto n=q.front();q.pop();if(i<v.size()&&v[i]!="null"){n->left=new TreeNode(stoi(v[i]));q.push(n->left);}i++;
 if(i<v.size()&&v[i]!="null"){n->right=new TreeNode(stoi(v[i]));q.push(n->right);}i++;}return r;}
'''
d = tempfile.mkdtemp(); bad = 0
for p in allp:
    src = f"{d}/{p['slug']}.cpp"
    open(src, "w").write(HDR + p["code"] + "\nint main(){\n" + p["test"] + '\nputs("ok");}\n')
    c = subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-O1", "-fsanitize=address,undefined", "-fno-sanitize-recover=all", src, "-o", src[:-4]], capture_output=True, text=True)
    if c.returncode or "warning" in c.stderr: print("COMPILE", p["slug"], c.stderr[:1500]); bad += 1; continue
    r = subprocess.run([src[:-4]], capture_output=True, text=True, env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0"}, timeout=60)
    if r.returncode or r.stdout.strip() != "ok": print("FAIL", p["slug"], r.stdout[-300:], r.stderr[-1200:]); bad += 1
print(f"{len(allp) - bad}/{len(allp)} passed; no overlap with the 171 earlier problems; 8 sets of 90 minutes on Saturdays"); sys.exit(1 if bad else 0)
