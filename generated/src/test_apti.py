"""Check the aptitude pack: counts, distinct options, and every computable answer recomputed in Python."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent)); from apti_data import SECTIONS
bad = 0; computed = 0
for key, (title, secs, qs) in SECTIONS.items():
    for i, q in enumerate(qs, 1):
        opts = [q["a"]] + q["wrong"]
        if len(set(opts)) != 4: print("DUP OPTIONS", key, i, opts); bad += 1
        if q["check"]:
            computed += 1
            got = q["check"]()
            if got != q["a"]: print("MISMATCH", key, i, q["q"][:60], "| key:", q["a"], "| computed:", got); bad += 1
print({k: len(v[2]) for k, v in SECTIONS.items()}, "computed checks:", computed, "failures:", bad); sys.exit(1 if bad else 0)
