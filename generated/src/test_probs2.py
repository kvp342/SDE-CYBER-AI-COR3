"""Compile and run every Worked Solutions II entry with sanitizers. Usage: python3 generated/src/test_probs2.py"""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from t_probs2 import P
HDR = r'''#include <bits/stdc++.h>
using namespace std;
struct ListNode{int val;ListNode*next;ListNode(int x):val(x),next(nullptr){}ListNode(int x,ListNode*n):val(x),next(n){}};
struct TreeNode{int val;TreeNode*left,*right;TreeNode(int x):val(x),left(nullptr),right(nullptr){}};
ListNode* mk(vector<int> v){ListNode d(0);ListNode*t=&d;for(int x:v){t->next=new ListNode(x);t=t->next;}return d.next;}
vector<int> tov(ListNode*h){vector<int> r;while(h){r.push_back(h->val);h=h->next;}return r;}
TreeNode* tree(vector<string> v){if(v.empty()||v[0]=="null")return nullptr;TreeNode*r=new TreeNode(stoi(v[0]));queue<TreeNode*>q;q.push(r);size_t i=1;
 while(!q.empty()&&i<v.size()){auto n=q.front();q.pop();if(i<v.size()&&v[i]!="null"){n->left=new TreeNode(stoi(v[i]));q.push(n->left);}i++;
 if(i<v.size()&&v[i]!="null"){n->right=new TreeNode(stoi(v[i]));q.push(n->right);}i++;}return r;}
'''
d = tempfile.mkdtemp(); bad = 0
for p in P:
    src = f"{d}/{p['id']}.cpp"; exe = src[:-4]
    open(src, "w").write(HDR + p["code"] + "\nint main(){\n" + p["test"] + '\nputs("ok");}\n')
    c = subprocess.run(["g++", "-std=c++17", "-Wall", "-O1", "-fsanitize=address,undefined", "-fno-sanitize-recover=all", src, "-o", exe], capture_output=True, text=True)
    if c.returncode or "warning" in c.stderr: print("COMPILE", p["id"], c.stderr[:1500]); bad += 1; continue
    r = subprocess.run([exe], capture_output=True, text=True, env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0"}, timeout=60)
    if r.returncode or r.stdout.strip() != "ok": print("FAIL", p["id"], r.stdout[-500:], r.stderr[-1500:]); bad += 1
print(f"{len(P) - bad}/{len(P)} passed"); sys.exit(1 if bad else 0)
