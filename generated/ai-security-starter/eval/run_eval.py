"""Answer-quality evaluation on 20 questions. Usage (from the project folder):
    python3 eval/run_eval.py              # offline stub model
    python3 eval/run_eval.py --llm anthropic --defended
Reports retrieval hit rate (the right note in the top 3) and answer match (an expected phrase appears in the answer)."""
import argparse, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from secrag import Assistant, Store, make_llm

def run(llm_kind="stub", defended=True, verbose=True):
    qs = json.loads((ROOT / "eval" / "questions.json").read_text())
    bot = Assistant(Store.from_dirs(ROOT / "notes"), make_llm(llm_kind), defended=defended)
    hit = match = blocked = 0
    for i, item in enumerate(qs, 1):
        r = bot.ask(item["q"])
        h = item["source"] in r.sources; m = any(e.lower() in r.answer.lower() for e in item["expect"])
        hit += h; match += m; blocked += r.blocked
        if verbose: print(f"{i:2} {'hit ' if h else 'MISS'} {'ok  ' if m else 'WRONG'} {item['q'][:60]:60} -> {r.answer[:70]}")
    n = len(qs)
    if verbose: print(f"\nretrieval hit@3 {hit}/{n}, answer match {match}/{n}, blocked {blocked}/{n} (benign questions should never be blocked)")
    return dict(n=n, hit=hit, match=match, blocked=blocked)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--llm", default="stub", choices=["stub", "anthropic"]); ap.add_argument("--defended", action="store_true")
    a = ap.parse_args(); run(a.llm, a.defended)
