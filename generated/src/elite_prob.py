"""40 probability and brain-teaser questions for the elite (HFT) checkpoint. Each item: (question, answer text, worked answer, exact, sim)
where exact() returns the exact value (Fraction or float) and sim() a seeded Monte Carlo estimate (or None when exact enumeration is enough).
python3 generated/src/elite_prob.py checks every answer: exact matches the stated answer, and simulation agrees within tolerance."""
import itertools, math, random
from fractions import Fraction as F
R = random.Random(2027); N = 200_000
def mc(trial, n=N): return sum(trial() for _ in range(n)) / n
def d6(): return R.randint(1, 6)
def until(cond_seq):
    def run():
        seq = []
        while True:
            seq.append(R.random() < .5)
            if cond_seq(seq): return len(seq)
    return run
def gambler(start, target):
    x = start
    while 0 < x < target: x += 1 if R.random() < .5 else -1
    return x == target
def triangle():
    a, b = sorted((R.random(), R.random())); return max(a, b - a, 1 - b) < .5
def acute():
    t = sorted(R.random() for _ in range(3)); arcs = (t[1] - t[0], t[2] - t[1], 1 - t[2] + t[0]); return max(arcs) < .5
def fixed(n):
    p = list(range(n)); R.shuffle(p); return sum(i == x for i, x in enumerate(p))
def first_ace():
    deck = [1] * 4 + [0] * 48; R.shuffle(deck); return deck.index(1) + 1
def ants():
    d = [R.random() < .5 for _ in range(3)]; return all(d) or not any(d)
def coupon():
    seen, n = set(), 0
    while len(seen) < 6: seen.add(d6()); n += 1
    return n
def reroll():
    a = d6(); return a if a >= 4 else d6()
Q = [
 ("A fair die is rolled until a 6 appears. Expected number of rolls?", "6", "Geometric with p = 1/6: mean 1/p.", lambda: F(6), lambda: mc(lambda: next(i for i in itertools.count(1) if d6() == 6))),
 ("Expected value of the larger of two fair dice?", "161/36 ≈ 4.47", "P(max ≤ k) = (k/6)²; E = Σ k·[(k/6)² − ((k−1)/6)²].", lambda: F(sum(max(a, b) for a in range(1, 7) for b in range(1, 7)), 36), lambda: mc(lambda: max(d6(), d6()))),
 ("Two cards are drawn from a deck. Probability they share a suit?", "4/17", "After the first card, 12 of the remaining 51 match its suit.", lambda: F(12, 51), lambda: mc(lambda: (lambda c: c[0] // 13 == c[1] // 13)(R.sample(range(52), 2)))),
 ("Probability that at least two of 23 people share a birthday (365 equally likely days)?", "≈ 0.507", "1 − (365·364·…·343)/365²³.", lambda: 1 - math.prod((365 - i) / 365 for i in range(23)), lambda: mc(lambda: len({R.randrange(365) for _ in range(23)}) < 23, 50_000)),
 ("Expected number of fair coin flips to see two heads in a row (HH)?", "6", "States: no progress, one H. E0 = 1 + ½E1 + ½E0, E1 = 1 + ½·0 + ½E0 → E0 = 6.", lambda: F(6), lambda: mc(until(lambda s: s[-2:] == [True, True]))),
 ("Expected number of flips to see head followed by tail (HT)?", "4", "Wait for H (2 flips on average), then wait for T (2 more): 4. Unlike HH, a failed attempt keeps your progress.", lambda: F(4), lambda: mc(until(lambda s: s[-2:] == [True, False]))),
 ("Two players flip a fair coin in turn; the first head wins. Probability the first player wins?", "2/3", "p = ½ + ¼p → p = 2/3.", lambda: F(2, 3), lambda: mc(lambda: next(i for i in itertools.count() if R.random() < .5) % 2 == 0)),
 ("Expected number of distinct faces in 6 rolls of a die?", "6(1 − (5/6)⁶) ≈ 3.99", "Linearity: each face appears with probability 1 − (5/6)⁶.", lambda: 6 * (1 - (5 / 6) ** 6), lambda: mc(lambda: len({d6() for _ in range(6)}))),
 ("Expected rolls to see all six faces?", "14.7", "Coupon collector: 6(1 + 1/2 + … + 1/6).", lambda: 6 * sum(F(1, k) for k in range(1, 7)), lambda: mc(coupon)),
 ("Monty Hall: you pick a door, the host opens a goat door, you switch. Probability of winning?", "2/3", "Switching wins exactly when your first pick was wrong (2/3).", lambda: F(2, 3), lambda: mc(lambda: R.randrange(3) != R.randrange(3))),
 ("A family has two children and at least one is a boy. Probability both are boys?", "1/3", "Equally likely BB, BG, GB remain; one is BB.", lambda: F(sum(1 for k in itertools.product("BG", repeat=2) if k == ("B", "B")), sum(1 for k in itertools.product("BG", repeat=2) if "B" in k)), None),
 ("A stick is broken at two uniform random points. Probability the three pieces form a triangle?", "1/4", "Every piece must be shorter than ½; the region is a quarter of the square.", lambda: F(1, 4), lambda: mc(triangle)),
 ("Expected maximum of three independent Uniform(0, 1)?", "3/4", "For n uniforms, E[max] = n/(n + 1).", lambda: F(3, 4), lambda: mc(lambda: max(R.random() for _ in range(3)))),
 ("Expected minimum of two Uniform(0, 1)?", "1/3", "E[min] = 1/(n + 1).", lambda: F(1, 3), lambda: mc(lambda: min(R.random(), R.random()))),
 ("Probability the sum of two dice is prime?", "5/12", "Sums 2, 3, 5, 7, 11 occur 1 + 2 + 4 + 6 + 2 = 15 times of 36.", lambda: F(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b in (2, 3, 5, 7, 11)), 36), None),
 ("Probability of exactly 2 heads in 5 fair flips?", "5/16", "C(5,2)/2⁵ = 10/32.", lambda: F(math.comb(5, 2), 32), None),
 ("Gambler's ruin: start with ₹3, bet ₹1 on fair flips until you reach ₹10 or ₹0. Probability of reaching ₹10?", "3/10", "A fair walk is a martingale: start/target.", lambda: F(3, 10), lambda: mc(lambda: gambler(3, 10), 50_000)),
 ("Expected number of fixed points of a random permutation of n items?", "1", "Linearity: each item is fixed with probability 1/n.", lambda: F(1), lambda: mc(lambda: fixed(10), 50_000)),
 ("Probability a random permutation of 5 items has no fixed point?", "11/30", "Derangements D5 = 44; 44/120.", lambda: F(sum(1 for p in itertools.permutations(range(5)) if all(i != x for i, x in enumerate(p))), 120), None),
 ("Three uniform random points on a circle. Probability the triangle is acute?", "1/4", "Acute if and only if all three arcs are shorter than half the circle.", lambda: F(1, 4), lambda: mc(acute)),
 ("A biased coin shows heads with probability 1/3. Expected flips to the first head?", "3", "Geometric mean 1/p.", lambda: F(3), lambda: mc(lambda: next(i for i in itertools.count(1) if R.random() < 1 / 3))),
 ("A bag has 3 red and 2 blue balls; two are drawn without replacement. Probability both are red?", "3/10", "(3/5)(2/4).", lambda: F(3, 5) * F(2, 4), None),
 ("Expected fair-coin flips until both heads and tails have appeared?", "3", "First flip, then wait for the other side (2 on average).", lambda: F(3), lambda: mc(until(lambda s: len(set(s)) == 2))),
 ("Variance of one roll of a fair die?", "35/12", "E[X²] − E[X]² = 91/6 − 49/4.", lambda: F(sum(k * k for k in range(1, 7)), 6) - F(7, 2) ** 2, None),
 ("E[X²] for X ~ Uniform(0, 1)?", "1/3", "∫x² dx from 0 to 1.", lambda: F(1, 3), lambda: mc(lambda: R.random() ** 2)),
 ("Probability of at least one six in four rolls of a die?", "671/1296 ≈ 0.518", "1 − (5/6)⁴ (de Méré's first bet, slightly favourable).", lambda: 1 - F(5, 6) ** 4, None),
 ("Probability of at least one double six in 24 rolls of two dice?", "≈ 0.491", "1 − (35/36)²⁴ (de Méré's second bet, slightly unfavourable).", lambda: 1 - (35 / 36) ** 24, lambda: mc(lambda: any(d6() == 6 and d6() == 6 for _ in range(24)), 50_000)),
 ("Expected number of heads before the first tail (fair coin)?", "1", "Geometric count of failures: (1 − p)/p with p = ½.", lambda: F(1), lambda: mc(lambda: next(i for i in itertools.count() if R.random() < .5))),
 ("X, Y independent Uniform(0, 1). Probability X·Y < ½?", "(1 + ln 2)/2 ≈ 0.847", "½ + ∫ from ½ to 1 of 1/(2x) dx = ½ + ½ ln 2.", lambda: (1 + math.log(2)) / 2, lambda: mc(lambda: R.random() * R.random() < .5)),
 ("Probability that a random integer from 1 to 100 is divisible by 3 or 5?", "47/100", "33 + 20 − 6 = 47 (inclusion–exclusion).", lambda: F(sum(1 for k in range(1, 101) if k % 3 == 0 or k % 5 == 0), 100), None),
 ("Roll a die; you may reroll once and must keep the second roll. Best expected payout (face value)?", "4.25", "Reroll on 1–3: ½·5 + ½·3.5.", lambda: F(4 + 5 + 6, 6) + F(3, 6) * F(7, 2), lambda: mc(reroll)),
 ("Ways to climb 10 stairs taking 1 or 2 steps at a time?", "89", "Fibonacci: f(n) = f(n − 1) + f(n − 2).", lambda: F(sum(1 for m in range(1, 11) for k in itertools.product((1, 2), repeat=m) if sum(k) == 10)), None),
 ("Three dice are rolled. Probability all three show different numbers?", "5/9", "6·5·4/6³.", lambda: F(6 * 5 * 4, 216), None),
 ("Expected number of throws of two dice until a sum of 7?", "6", "P(sum 7) = 1/6.", lambda: F(6), lambda: mc(lambda: next(i for i in itertools.count(1) if d6() + d6() == 7))),
 ("Two dice are thrown repeatedly. Probability a sum of 7 comes before a sum of 8?", "6/11", "Only 7s (6 ways) and 8s (5 ways) matter.", lambda: F(6, 11), lambda: mc(lambda: next(s for s in iter(lambda: d6() + d6(), None) if s in (7, 8)) == 7)),
 ("An even-money bet wins with probability 0.6. Kelly fraction of bankroll to stake?", "0.2", "f* = p − q = 0.6 − 0.4 for even odds.", lambda: 0.6 - 0.4, None),
 ("A disease affects 1% of people. A test catches 99% of cases and has a 5% false-positive rate. Probability of disease given a positive test?", "1/6 ≈ 0.167", "Bayes: 0.0099 / (0.0099 + 0.0495).", lambda: F(99, 10000) / (F(99, 10000) + F(495, 10000)), None),
 ("Three ants on the corners of a triangle each walk along a random edge. Probability no two meet?", "1/4", "Only all-clockwise or all-anticlockwise avoid collisions: 2 of 8.", lambda: F(2, 8), lambda: mc(ants)),
 ("A deck is shuffled. Expected position of the first ace?", "53/5 = 10.6", "The 4 aces split 48 other cards into 5 gaps of 48/5 on average: 48/5 + 1.", lambda: F(53, 5), lambda: mc(first_ace, 100_000)),
 ("Probability a random 5-card hand is a flush (including straight flushes)?", "≈ 0.00198", "4·C(13, 5)/C(52, 5) = 5148/2,598,960.", lambda: F(4 * math.comb(13, 5), math.comb(52, 5)), None),
]
def parse(ans):
    a = ans.split("≈")[-1].strip().split(" ")[0] if "≈" in ans else ans.split(" ")[0].split("=")[-1].strip()
    if "/" in a: n, d = a.split("/"); return float(F(int(n), int(d)))
    return float(a.replace(",", ""))
def check(verbose=True):
    bad = 0; sims = 0
    for i, (q, ans, why, ex, sim) in enumerate(Q, 1):
        e = float(ex()); stated = parse(ans)
        tol = 0.0005 if "≈" in ans else 1e-9 * max(1, abs(e))
        ok = abs(e - stated) <= max(tol, 0.005 * abs(e) if "≈" in ans else tol)
        if sim:
            sims += 1; s = sim(); ok_s = abs(s - e) <= max(0.02 * abs(e), 0.01)
        else: s, ok_s = None, True
        if not (ok and ok_s): bad += 1; print("FAIL", i, q[:50], "stated", stated, "exact", e, "sim", s)
    if verbose: print(f"{len(Q)} questions, {sims} simulated, failures: {bad}")
    return bad == 0
if __name__ == "__main__":
    assert len(Q) == 40
    raise SystemExit(0 if check() else 1)
