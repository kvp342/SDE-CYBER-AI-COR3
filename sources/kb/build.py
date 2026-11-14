"""Build the Placement Knowledge Base page (kb.html) and aliases.json for PDF linking."""
import json, pathlib, importlib.util
D = pathlib.Path(__file__).parent
T = []
for m in ["t_method", "t_dsa", "t_probs", "t_cs", "t_qa", "t_sec", "t_elite", "t_career", "t_mocks", "t_companies"]:
    spec = importlib.util.spec_from_file_location(m, D / f"{m}.py"); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    T += mod.TOPICS
ids = [t["id"] for t in T]
assert len(ids) == len(set(ids)), "duplicate id"
for t in T:
    for r in t.get("rel", []): assert r in ids, (t["id"], r)
    t.setdefault("prac", []); t.setdefault("learn", []); t.setdefault("code", ""); t.setdefault("ask", []); t.setdefault("pit", []); t.setdefault("points", []); t.setdefault("qa", [])
data = [{k: t[k] for k in ["id", "title", "cat", "lvl", "why", "core", "points", "code", "pit", "ask", "prac", "learn", "rel", "qa"]} for t in T]
EXTRA = {"lcs": ["Longest common subsequence", "Longest common substring", "Longest palindromic subsequence", "Edit distance"],
 "dp": ["Longest increasing subsequence", "House robber", "Climbing stairs", "Coin change"],
 "knapsack": ["Unbounded knapsack", "0/1 knapsack", "Subset sum", "Partition equal subset sum", "Target sum"],
 "xss": ["Cross-site scripting", "Cross-site request forgery"], "sqli": ["SQL injection"],
 "bfs": ["Rotting oranges", "Word ladder", "Bipartite"], "dfs": ["Number of islands", "Flood fill", "Connected components"],
 "topo-sort": ["Course schedule", "Alien dictionary"], "intervals": ["Merge intervals", "Insert interval"],
 "linked-list": ["Reverse a linked list", "LRU cache"], "trees": ["Level order traversal", "Inorder traversal", "Lowest common ancestor"],
 "dsu": ["Kruskal", "Minimum spanning tree"], "dijkstra": ["Bellman-Ford", "Floyd-Warshall"],
 "deadlock": ["Banker's algorithm"], "virtual-memory": ["Page replacement", "Page fault"],
 "load-balancing": ["load balancer", "Auto Scaling"], "aws-core": ["VPC", "NAT gateway"],
 "sync": ["race condition", "critical section", "Semaphores"], "scheduling": ["Round robin", "CPU scheduling"],
 "recursion": ["N-Queens", "Permutations", "Subsets"], "heap": ["Kth largest", "Priority queue"]}
AL = {t["id"]: [t["title"]] + t.get("aka", []) + EXTRA.get(t["id"], []) for t in T}
(D / "aliases.json").write_text(json.dumps(AL, ensure_ascii=False))
html = (D / "page.html").read_text().replace("/*DATA*/[]", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
(D / "kb.html").write_text(html)
print(len(T), "topics")
