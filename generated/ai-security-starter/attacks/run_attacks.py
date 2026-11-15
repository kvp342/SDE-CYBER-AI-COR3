"""Prompt-injection test suite: 6 direct and 6 indirect attacks, run with and without defences.
Usage: python3 attacks/run_attacks.py [--llm anthropic]
Indirect attacks work by adding attacks/poisoned/*.md to the knowledge base, as a compromised document would be."""
import argparse, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from secrag import Assistant, Store, make_llm

def succeeded(case, answer):
    return any(s.lower() in answer.lower() for s in case["success_if"])

def run(llm_kind="stub", verbose=True):
    cases = json.loads((ROOT / "attacks" / "cases.json").read_text())
    clean = Store.from_dirs(ROOT / "notes"); poisoned = Store.from_dirs(ROOT / "notes", ROOT / "attacks" / "poisoned"); llm = make_llm(llm_kind)
    out = {}
    for defended in (False, True):
        wins = []
        for c in cases:
            bot = Assistant(poisoned if c["type"] == "indirect" else clean, llm, defended=defended)
            r = bot.ask(c["question"]); ok = succeeded(c, r.answer); wins.append(ok)
            if verbose: print(f"{'defended' if defended else 'baseline'} {c['id']} {c['type']:8} {'ATTACK SUCCEEDED' if ok else 'stopped':16} {r.answer[:60]!r} {r.reasons}")
        out["defended" if defended else "baseline"] = dict(zip([c["id"] for c in cases], wins))
    if verbose:
        for k, v in out.items(): print(f"{k}: attack success rate {sum(v.values())}/{len(v)}")
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--llm", default="stub", choices=["stub", "anthropic"])
    run(ap.parse_args().llm)
