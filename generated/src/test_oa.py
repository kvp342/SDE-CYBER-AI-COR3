"""Compile and test every OA reference solution. Usage: python3 generated/src/test_oa.py"""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__)); from oa_data import SETS
d = tempfile.mkdtemp(); bad = 0; allp = [p for s in SETS for p in s["probs"]]
assert len(allp) == 24 and len({p["slug"] for p in allp}) == 24, "duplicate problem"
for p in allp:
    src = f"{d}/{p['slug']}.cpp"
    open(src, "w").write("#include <bits/stdc++.h>\nusing namespace std;\n" + p["code"] + "\nint main(){\n" + p["test"] + '\nputs("ok");}\n')
    c = subprocess.run(["g++", "-std=c++17", "-Wall", "-O1", "-fsanitize=address,undefined", "-fno-sanitize-recover=all", src, "-o", src[:-4]], capture_output=True, text=True)
    if c.returncode or "warning" in c.stderr: print("COMPILE", p["slug"], c.stderr[:1200]); bad += 1; continue
    r = subprocess.run([src[:-4]], capture_output=True, text=True, env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0"}, timeout=60)
    if r.returncode or r.stdout.strip() != "ok": print("FAIL", p["slug"], r.stderr[-1200:]); bad += 1
print(f"{len(allp) - bad}/{len(allp)} passed"); sys.exit(1 if bad else 0)
