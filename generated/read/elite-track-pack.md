ELITE TRACK · HFT CHECKPOINT

# Elite pack probability and low-latency C++

For the checkpoint on 31 March 2027, if you take the Elite track: 40 probability and expected-value questions of the kind quant and HFT interviews ask (every answer checked by exact calculation, and 27 also by simulation), and 8 C++ exercises on the habits low-latency code depends on, each with tests and a timing harness.

**How to use.** Probability: 10 questions a week, answer on paper first, then check the working. C++: build each exercise, predict which version is faster and by how much, then run it. Compile with `g++ -std=c++17 -O2 -pthread generated/elite/e3_spsc.cpp`. See the [HFT overview](knowledge-base/elite.md#hft-roles-and-the-31-march-gate) and [low-latency C++](knowledge-base/elite.md#low-latency-c) pages.

|                                                                 |
|-----------------------------------------------------------------|
| [Probability and brain teasers: 40 questions](#probability-and-brain-teasersanswers)          |
| [Answers with working](#answers-with-working)                                 |
| [Low-latency C++: 8 exercises](#about-the-c-exercises)                         |
| [1. Data layout: array of structs vs struct of arrays](#01-data-layout-array-of-structs-vs-struct-of-arrays) |
| [2. Traversal order](#02-traversal-order)                                   |
| [3. Lock-free SPSC ring buffer](#03-lock-free-spsc-ring-buffer)                       |
| [4. Object pool with a free list](#04-object-pool-with-a-free-list)                     |
| [5. Branch-free min, abs and clamp](#05-branch-free-min-abs-and-clamp)                   |
| [6. False sharing](#06-false-sharing)                                    |
| [7. Fast integer parsing](#07-fast-integer-parsing)                             |
| [8. Array-based order book](#08-array-based-order-book)                           |

## Probability and brain teasers[Answers](#answers-with-working)

**Q1.** A fair die is rolled until a 6 appears. Expected number of rolls?

**Q2.** Expected value of the larger of two fair dice?

**Q3.** Two cards are drawn from a deck. Probability they share a suit?

**Q4.** Probability that at least two of 23 people share a birthday (365 equally likely days)?

**Q5.** Expected number of fair coin flips to see two heads in a row (HH)?

**Q6.** Expected number of flips to see head followed by tail (HT)?

**Q7.** Two players flip a fair coin in turn; the first head wins. Probability the first player wins?

**Q8.** Expected number of distinct faces in 6 rolls of a die?

**Q9.** Expected rolls to see all six faces?

**Q10.** Monty Hall: you pick a door, the host opens a goat door, you switch. Probability of winning?

**Q11.** A family has two children and at least one is a boy. Probability both are boys?

**Q12.** A stick is broken at two uniform random points. Probability the three pieces form a triangle?

**Q13.** Expected maximum of three independent Uniform(0, 1)?

**Q14.** Expected minimum of two Uniform(0, 1)?

**Q15.** Probability the sum of two dice is prime?

**Q16.** Probability of exactly 2 heads in 5 fair flips?

**Q17.** Gambler's ruin: start with ₹3, bet ₹1 on fair flips until you reach ₹10 or ₹0. Probability of reaching ₹10?

**Q18.** Expected number of fixed points of a random permutation of n items?

**Q19.** Probability a random permutation of 5 items has no fixed point?

**Q20.** Three uniform random points on a circle. Probability the triangle is acute?

**Q21.** A biased coin shows heads with probability 1/3. Expected flips to the first head?

**Q22.** A bag has 3 red and 2 blue balls; two are drawn without replacement. Probability both are red?

**Q23.** Expected fair-coin flips until both heads and tails have appeared?

**Q24.** Variance of one roll of a fair die?

**Q25.** E\[X²\] for X ~ Uniform(0, 1)?

**Q26.** Probability of at least one six in four rolls of a die?

**Q27.** Probability of at least one double six in 24 rolls of two dice?

**Q28.** Expected number of heads before the first tail (fair coin)?

**Q29.** X, Y independent Uniform(0, 1). Probability X·Y \< ½?

**Q30.** Probability that a random integer from 1 to 100 is divisible by 3 or 5?

**Q31.** Roll a die; you may reroll once and must keep the second roll. Best expected payout (face value)?

**Q32.** Ways to climb 10 stairs taking 1 or 2 steps at a time?

**Q33.** Three dice are rolled. Probability all three show different numbers?

**Q34.** Expected number of throws of two dice until a sum of 7?

**Q35.** Two dice are thrown repeatedly. Probability a sum of 7 comes before a sum of 8?

**Q36.** An even-money bet wins with probability 0.6. Kelly fraction of bankroll to stake?

**Q37.** A disease affects 1% of people. A test catches 99% of cases and has a 5% false-positive rate. Probability of disease given a positive test?

**Q38.** Three ants on the corners of a triangle each walk along a random edge. Probability no two meet?

**Q39.** A deck is shuffled. Expected position of the first ace?

**Q40.** Probability a random 5-card hand is a flush (including straight flushes)?

## Answers with working

| Q              | Answer               | Working                                                                                                        | Checked by         |
|----------------|----------------------|----------------------------------------------------------------------------------------------------------------|--------------------|
| [Q1](#answers-with-working)  | 6                    | Geometric with p = 1/6: mean 1/p.                                                                              | exact + simulation |
| [Q2](#answers-with-working)  | 161/36 ≈ 4.47        | P(max ≤ k) = (k/6)²; E = Σ k·\[(k/6)² − ((k−1)/6)²\].                                                          | exact + simulation |
| [Q3](#answers-with-working)  | 4/17                 | After the first card, 12 of the remaining 51 match its suit.                                                   | exact + simulation |
| [Q4](#answers-with-working)  | ≈ 0.507              | 1 − (365·364·…·343)/365²³.                                                                                     | exact + simulation |
| [Q5](#answers-with-working)  | 6                    | States: no progress, one H. E0 = 1 + ½E1 + ½E0, E1 = 1 + ½·0 + ½E0 → E0 = 6.                                   | exact + simulation |
| [Q6](#answers-with-working)  | 4                    | Wait for H (2 flips on average), then wait for T (2 more): 4. Unlike HH, a failed attempt keeps your progress. | exact + simulation |
| [Q7](#answers-with-working)  | 2/3                  | p = ½ + ¼p → p = 2/3.                                                                                          | exact + simulation |
| [Q8](#answers-with-working)  | 6(1 − (5/6)⁶) ≈ 3.99 | Linearity: each face appears with probability 1 − (5/6)⁶.                                                      | exact + simulation |
| [Q9](#answers-with-working)  | 14.7                 | Coupon collector: 6(1 + 1/2 + … + 1/6).                                                                        | exact + simulation |
| [Q10](#answers-with-working) | 2/3                  | Switching wins exactly when your first pick was wrong (2/3).                                                   | exact + simulation |
| [Q11](#answers-with-working) | 1/3                  | Equally likely BB, BG, GB remain; one is BB.                                                                   | exact              |
| [Q12](#answers-with-working) | 1/4                  | Every piece must be shorter than ½; the region is a quarter of the square.                                     | exact + simulation |
| [Q13](#answers-with-working) | 3/4                  | For n uniforms, E\[max\] = n/(n + 1).                                                                          | exact + simulation |
| [Q14](#answers-with-working) | 1/3                  | E\[min\] = 1/(n + 1).                                                                                          | exact + simulation |
| [Q15](#answers-with-working) | 5/12                 | Sums 2, 3, 5, 7, 11 occur 1 + 2 + 4 + 6 + 2 = 15 times of 36.                                                  | exact              |
| [Q16](#answers-with-working) | 5/16                 | C(5,2)/2⁵ = 10/32.                                                                                             | exact              |
| [Q17](#answers-with-working) | 3/10                 | A fair walk is a martingale: start/target.                                                                     | exact + simulation |
| [Q18](#answers-with-working) | 1                    | Linearity: each item is fixed with probability 1/n.                                                            | exact + simulation |
| [Q19](#answers-with-working) | 11/30                | Derangements D5 = 44; 44/120.                                                                                  | exact              |
| [Q20](#answers-with-working) | 1/4                  | Acute if and only if all three arcs are shorter than half the circle.                                          | exact + simulation |
| [Q21](#answers-with-working) | 3                    | Geometric mean 1/p.                                                                                            | exact + simulation |
| [Q22](#answers-with-working) | 3/10                 | (3/5)(2/4).                                                                                                    | exact              |
| [Q23](#answers-with-working) | 3                    | First flip, then wait for the other side (2 on average).                                                       | exact + simulation |
| [Q24](#answers-with-working) | 35/12                | E\[X²\] − E\[X\]² = 91/6 − 49/4.                                                                               | exact              |
| [Q25](#answers-with-working) | 1/3                  | ∫x² dx from 0 to 1.                                                                                            | exact + simulation |
| [Q26](#answers-with-working) | 671/1296 ≈ 0.518     | 1 − (5/6)⁴ (de Méré's first bet, slightly favourable).                                                         | exact              |
| [Q27](#answers-with-working) | ≈ 0.491              | 1 − (35/36)²⁴ (de Méré's second bet, slightly unfavourable).                                                   | exact + simulation |
| [Q28](#answers-with-working) | 1                    | Geometric count of failures: (1 − p)/p with p = ½.                                                             | exact + simulation |
| [Q29](#answers-with-working) | (1 + ln 2)/2 ≈ 0.847 | ½ + ∫ from ½ to 1 of 1/(2x) dx = ½ + ½ ln 2.                                                                   | exact + simulation |
| [Q30](#answers-with-working) | 47/100               | 33 + 20 − 6 = 47 (inclusion–exclusion).                                                                        | exact              |
| [Q31](#answers-with-working) | 4.25                 | Reroll on 1–3: ½·5 + ½·3.5.                                                                                    | exact + simulation |
| [Q32](#answers-with-working) | 89                   | Fibonacci: f(n) = f(n − 1) + f(n − 2).                                                                         | exact              |
| [Q33](#answers-with-working) | 5/9                  | 6·5·4/6³.                                                                                                      | exact              |
| [Q34](#answers-with-working) | 6                    | P(sum 7) = 1/6.                                                                                                | exact + simulation |
| [Q35](#answers-with-working) | 6/11                 | Only 7s (6 ways) and 8s (5 ways) matter.                                                                       | exact + simulation |
| [Q36](#answers-with-working) | 0.2                  | f\* = p − q = 0.6 − 0.4 for even odds.                                                                         | exact              |
| [Q37](#answers-with-working) | 1/6 ≈ 0.167          | Bayes: 0.0099 / (0.0099 + 0.0495).                                                                             | exact              |
| [Q38](#answers-with-working) | 1/4                  | Only all-clockwise or all-anticlockwise avoid collisions: 2 of 8.                                              | exact + simulation |
| [Q39](#answers-with-working) | 53/5 = 10.6          | The 4 aces split 48 other cards into 5 gaps of 48/5 on average: 48/5 + 1.                                      | exact + simulation |
| [Q40](#answers-with-working) | ≈ 0.00198            | 4·C(13, 5)/C(52, 5) = 5148/2,598,960.                                                                          | exact              |

Checks: `generated/src/elite_prob.py` recomputes every answer exactly (fractions, enumeration or closed form) and runs seeded Monte Carlo simulations for 27 of them.

## About the C++ exercises

- All eight compile with `-Wall -Wextra` and pass their checks under AddressSanitizer and UndefinedBehaviorSanitizer; the two multithreaded ones (SPSC queue, false sharing) also pass ThreadSanitizer.
- `bench.h` runs each version several times and reports the best nanoseconds per operation. Timings depend on the machine: the numbers shown came from one cloud container, so measure on your own laptop and compare the ratios, not the absolute values.
- Correctness is asserted; speed is only printed. A faster version that gives a different answer fails.

``` cpp
// Tiny timing harness: runs f several times and reports the best time in nanoseconds per operation.
#pragma once
#include <chrono>
#include <cstdio>
template <class F> double best_ns_per_op(const char* name, long ops, F f, int reps = 5) {
    double best = 1e300;
    for (int r = 0; r < reps; r++) {
        auto t0 = std::chrono::steady_clock::now(); f();
        double ns = std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now() - t0).count() / ops;
        if (ns < best) best = ns;
    }
    std::printf("  %-34s %8.3f ns/op\n", name, best); return best;
}
template <class T> inline void keep(const T& v) { asm volatile("" : : "g"(&v) : "memory"); }   // stop the optimiser deleting work
```

## 01. Data layout: array of structs vs struct of arrays

Summing one field drags whole 72-byte records through the cache in AoS; SoA reads only the field you need.

### Measured here (-O2, one cloud container)

|              |             |
|--------------|-------------|
| AoS: sum qty | 3.889 ns/op |
| SoA: sum qty | 0.326 ns/op |

### Think about

Why does SoA help vectorisation too?

### Code (`generated/elite/e1_aos_soa.cpp`)

``` cpp
// 1. Data layout: sum one field over many records. Array of structs drags unused fields through the cache; struct of arrays does not.
#include <cassert>
#include <vector>
#include <cstdint>
#include "bench.h"
struct Order { int64_t id; double price; int32_t qty; char side; char pad[43]; };   // 72 bytes, like a fat record
int main() {
    const int N = 1 << 20; std::vector<Order> aos(N); std::vector<int32_t> qty(N);
    for (int i = 0; i < N; i++) { aos[i].qty = qty[i] = i % 100; aos[i].price = i; }
    long long a = 0, b = 0;
    best_ns_per_op("AoS: sum qty", N, [&] { a = 0; for (auto& o : aos) a += o.qty; keep(a); });
    best_ns_per_op("SoA: sum qty", N, [&] { b = 0; for (int q : qty) b += q; keep(b); });
    long long expect = 0; for (int i = 0; i < N; i++) expect += i % 100;
    assert(a == b && a == expect); std::puts("e1 ok");
}
```

## 02. Traversal order

Row-major arrays read sequentially are prefetched; column order jumps a full row each step and misses the cache.

### Measured here (-O2, one cloud container)

|                        |             |
|------------------------|-------------|
| row-major traversal    | 0.229 ns/op |
| column-major traversal | 8.415 ns/op |

### Think about

What about a matrix multiply? (loop order i-k-j)

### Code (`generated/elite/e2_traversal.cpp`)

``` cpp
// 2. Traversal order: walk a row-major 2-D array row by row (sequential) versus column by column (strided, cache-hostile).
#include <cassert>
#include <vector>
#include "bench.h"
int main() {
    const int R = 2048, C = 2048; std::vector<int> a(R * C); for (int i = 0; i < R * C; i++) a[i] = i & 7;
    long long s1 = 0, s2 = 0;
    best_ns_per_op("row-major traversal", (long)R * C, [&] { s1 = 0; for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) s1 += a[r * C + c]; keep(s1); });
    best_ns_per_op("column-major traversal", (long)R * C, [&] { s2 = 0; for (int c = 0; c < C; c++) for (int r = 0; r < R; r++) s2 += a[r * C + c]; keep(s2); });
    assert(s1 == s2); std::puts("e2 ok");
}
```

## 03. Lock-free SPSC ring buffer

One producer, one consumer, acquire/release on head and tail, power-of-two capacity, head and tail on separate cache lines.

### Measured here (-O2, one cloud container)

|                           |              |
|---------------------------|--------------|
| SPSC transfer (2 threads) | 10.145 ns/op |

### Think about

Why is relaxed enough for a thread's own index? What changes for multiple producers?

### Code (`generated/elite/e3_spsc.cpp`)

``` cpp
// 3. Lock-free single-producer single-consumer ring buffer. One writer owns `tail`, one reader owns `head`;
// acquire/release ordering publishes each slot. Capacity is a power of two so wrap-around is a mask.
#include <array>
#include <atomic>
#include <cassert>
#include <cstddef>
#include <optional>
#include <thread>
#include "bench.h"
template <class T, size_t N> class Spsc {
    static_assert((N & (N - 1)) == 0, "capacity must be a power of two");
    std::array<T, N> buf;
    alignas(64) std::atomic<size_t> head{0};   // read position, written by the consumer only
    alignas(64) std::atomic<size_t> tail{0};   // write position, written by the producer only (separate cache line: no false sharing)
public:
    bool push(const T& v) {
        size_t t = tail.load(std::memory_order_relaxed);
        if (t - head.load(std::memory_order_acquire) == N) return false;     // full
        buf[t & (N - 1)] = v; tail.store(t + 1, std::memory_order_release); return true;
    }
    std::optional<T> pop() {
        size_t h = head.load(std::memory_order_relaxed);
        if (h == tail.load(std::memory_order_acquire)) return std::nullopt;   // empty
        T v = buf[h & (N - 1)]; head.store(h + 1, std::memory_order_release); return v;
    }
};
int main() {
    Spsc<int, 4> small; assert(small.push(1) && small.push(2) && small.push(3) && small.push(4) && !small.push(5));
    assert(*small.pop() == 1); assert(small.push(5)); for (int e : {2, 3, 4, 5}) assert(*small.pop() == e); assert(!small.pop());
    static Spsc<long, 1024> q; const long M = 2'000'000; bool ordered = true;
    best_ns_per_op("SPSC transfer (2 threads)", M, [&] {
        std::thread prod([&] { for (long i = 0; i < M; i++) while (!q.push(i)) {} });
        long expect = 0; while (expect < M) if (auto v = q.pop()) { ordered &= (*v == expect); expect++; }
        prod.join();
    }, 3);
    assert(ordered); std::puts("e3 ok");
}
```

## 04. Object pool with a free list

Preallocate and recycle objects: no allocator call and no fragmentation on the hot path.

### Measured here (-O2, one cloud container)

|                   |             |
|-------------------|-------------|
| new/delete        | 9.304 ns/op |
| pool make/destroy | 1.516 ns/op |

### Think about

How would you make it thread-safe? Per-thread pools.

### Code (`generated/elite/e4_pool.cpp`)

``` cpp
// 4. Object pool: preallocate objects and recycle them through a free list instead of calling new/delete on the hot path.
#include <cassert>
#include <cstddef>
#include <new>
#include <vector>
#include "bench.h"
struct Msg { long id; double px; int qty; };
template <class T> class Pool {
    union Slot { Slot* next; alignas(T) unsigned char obj[sizeof(T)]; };
    std::vector<Slot> slots; Slot* free_ = nullptr;
public:
    explicit Pool(size_t n) : slots(n) { for (auto& s : slots) { s.next = free_; free_ = &s; } }
    template <class... A> T* make(A&&... a) { if (!free_) return nullptr; Slot* s = free_; free_ = s->next; return new (s->obj) T{a...}; }
    void destroy(T* p) { p->~T(); Slot* s = reinterpret_cast<Slot*>(p); s->next = free_; free_ = s; }
};
int main() {
    Pool<Msg> pool(2); Msg* a = pool.make(1L, 1.0, 1); Msg* b = pool.make(2L, 2.0, 2);
    assert(a && b && a != b && !pool.make(3L, 3.0, 3)); pool.destroy(a); Msg* c = pool.make(4L, 4.0, 4); assert(c == a && c->id == 4); pool.destroy(b); pool.destroy(c);
    const long N = 1'000'000; Pool<Msg> big(64); long sum = 0;
    best_ns_per_op("new/delete", N, [&] { for (long i = 0; i < N; i++) { Msg* m = new Msg{i, 1.0, 1}; sum += m->qty; keep(m); delete m; } });
    best_ns_per_op("pool make/destroy", N, [&] { for (long i = 0; i < N; i++) { Msg* m = big.make(i, 1.0, 1); sum += m->qty; keep(m); big.destroy(m); } });
    assert(sum == 10 * N); std::puts("e4 ok");
}
```

## 05. Branch-free min, abs and clamp

Sign-mask tricks replace unpredictable branches; check against std:: and read the assembly, because compilers often do this already.

### Measured here (-O2, one cloud container)

|                         |             |
|-------------------------|-------------|
| branchy clamp (if/else) | 3.365 ns/op |
| branch-free clamp       | 0.923 ns/op |

### Think about

When does a branch beat branch-free code? (predictable data)

### Code (`generated/elite/e5_branchless.cpp`)

``` cpp
// 5. Branch-free arithmetic: min, abs and clamp without if-statements, checked against std on every value pattern.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <random>
#include <vector>
#include "bench.h"
inline int32_t bmin(int32_t a, int32_t b) { int32_t d = a - b; return b + (d & (d >> 31)); }        // valid when a - b does not overflow
inline int32_t babs(int32_t x) { int32_t m = x >> 31; return (x ^ m) - m; }                           // valid for x != INT32_MIN
inline int32_t bclamp(int32_t x, int32_t lo, int32_t hi) { return bmin(hi, lo - bmin(lo - x, 0)); }  // max(lo, x) as lo - min(lo - x, 0)
int main() {
    std::mt19937 g(7); std::uniform_int_distribution<int32_t> u(-1'000'000, 1'000'000);
    std::vector<int32_t> v(1 << 20); for (auto& x : v) x = u(g);
    for (size_t i = 0; i + 1 < v.size(); i++) { assert(bmin(v[i], v[i + 1]) == std::min(v[i], v[i + 1])); assert(babs(v[i]) == std::abs(v[i])); assert(bclamp(v[i], -500, 500) == std::clamp(v[i], -500, 500)); }
    long long s1 = 0, s2 = 0;
    best_ns_per_op("branchy clamp (if/else)", (long)v.size(), [&] { s1 = 0; for (int32_t x : v) { if (x < -500) s1 += -500; else if (x > 500) s1 += 500; else s1 += x; } keep(s1); });
    best_ns_per_op("branch-free clamp", (long)v.size(), [&] { s2 = 0; for (int32_t x : v) s2 += bclamp(x, -500, 500); keep(s2); });
    assert(s1 == s2); std::puts("e5 ok  (the compiler may already emit branch-free code for the if/else version; compare with -O2 and read the assembly)");
}
```

## 06. False sharing

Two threads writing different variables on one cache line still fight over the line; alignas(64) separates them.

### Measured here (-O2, one cloud container)

|                             |              |
|-----------------------------|--------------|
| counters on one cache line  | 22.907 ns/op |
| counters padded to 64 bytes | 2.395 ns/op  |

### Think about

How do you find false sharing in a real program? (perf c2c)

### Code (`generated/elite/e6_false_sharing.cpp`)

``` cpp
// 6. False sharing: two threads increment their own counters. If both counters sit on one cache line, the line ping-pongs between cores.
#include <atomic>
#include <cassert>
#include <thread>
#include "bench.h"
struct Shared { std::atomic<long> a{0}, b{0}; };                                   // same 64-byte line
struct Padded { alignas(64) std::atomic<long> a{0}; alignas(64) std::atomic<long> b{0}; };  // separate lines
template <class S> void run(S& s, long n) {
    std::thread t1([&] { for (long i = 0; i < n; i++) s.a.fetch_add(1, std::memory_order_relaxed); });
    std::thread t2([&] { for (long i = 0; i < n; i++) s.b.fetch_add(1, std::memory_order_relaxed); });
    t1.join(); t2.join();
}
int main() {
    static_assert(sizeof(Padded) >= 128); const long N = 20'000'000; Shared s; Padded p;
    best_ns_per_op("counters on one cache line", 2 * N, [&] { run(s, N); }, 3);
    best_ns_per_op("counters padded to 64 bytes", 2 * N, [&] { run(p, N); }, 3);
    assert(s.a == 3 * N && s.b == 3 * N && p.a == 3 * N && p.b == 3 * N); std::puts("e6 ok");
}
```

## 07. Fast integer parsing

A tight loop over chars avoids locale handling and virtual calls in streams; feed handlers parse like this.

### Measured here (-O2, one cloud container)

|                     |              |
|---------------------|--------------|
| stringstream \>\>   | 33.409 ns/op |
| hand-written parser | 5.271 ns/op  |

### Think about

How would you parse fixed-point prices without doubles?

### Code (`generated/elite/e7_parse.cpp`)

``` cpp
// 7. Fast parsing: read signed integers from a text buffer with a hand-written loop instead of stringstream.
#include <cassert>
#include <sstream>
#include <string>
#include <vector>
#include "bench.h"
inline const char* parse_int(const char* p, long& out) {
    while (*p == ' ' || *p == '\n') p++;
    bool neg = *p == '-'; if (neg) p++;
    long v = 0; while (*p >= '0' && *p <= '9') v = v * 10 + (*p++ - '0');
    out = neg ? -v : v; return p;
}
int main() {
    std::string text; long expect = 0; const int N = 500'000;
    for (int i = 0; i < N; i++) { long x = (i % 2 ? -1 : 1) * (long)i * 37; text += std::to_string(x) + (i % 10 == 9 ? "\n" : " "); expect += x; }
    long s1 = 0, s2 = 0;
    best_ns_per_op("stringstream >>", N, [&] { std::istringstream in(text); long x; s1 = 0; while (in >> x) s1 += x; keep(s1); }, 3);
    best_ns_per_op("hand-written parser", N, [&] { const char* p = text.c_str(); long x; s2 = 0; for (int i = 0; i < N; i++) { p = parse_int(p, x); s2 += x; } keep(s2); }, 3);
    long y; parse_int("  -42 7", y); assert(y == -42);
    assert(s1 == expect && s2 == expect); std::puts("e7 ok");
}
```

## 08. Array-based order book

Integer ticks in a known band index an array: O(1) add and cancel; the best price moves by a short scan only when a level empties. Checked against a std::map reference on 200,000 random operations.

### Measured here (-O2, one cloud container)

|                       |              |
|-----------------------|--------------|
| std::map add + best   | 59.960 ns/op |
| array book add + best | 1.243 ns/op  |

### Think about

What if the price band is unbounded? (hash map of levels plus a heap)

### Code (`generated/elite/e8_book.cpp`)

``` cpp
// 8. Price-level order book: prices are integer ticks in a known band, so each side is an array indexed by tick.
// Add and cancel are O(1); the best price moves with a short scan only when its level empties.
#include <cassert>
#include <cstdint>
#include <map>
#include <random>
#include <vector>
#include "bench.h"
class Book {
    int lo; std::vector<int64_t> bids, asks; int bestBid = -1, bestAsk = -1;   // indices into the arrays; -1 = empty
public:
    Book(int loTick, int hiTick) : lo(loTick), bids(hiTick - loTick + 1), asks(hiTick - loTick + 1) {}
    void add(bool buy, int tick, int64_t qty) {
        int i = tick - lo; auto& side = buy ? bids : asks; side[i] += qty;
        if (buy && (bestBid < 0 || i > bestBid)) bestBid = i;
        if (!buy && (bestAsk < 0 || i < bestAsk)) bestAsk = i;
    }
    void cancel(bool buy, int tick, int64_t qty) {
        int i = tick - lo; auto& side = buy ? bids : asks; side[i] -= qty; assert(side[i] >= 0);
        if (buy && i == bestBid) while (bestBid >= 0 && bids[bestBid] == 0) bestBid--;
        if (!buy && i == bestAsk) { while (bestAsk >= 0 && bestAsk < (int)asks.size() && asks[bestAsk] == 0) bestAsk++; if (bestAsk == (int)asks.size()) bestAsk = -1; }
    }
    int bestBidTick() const { return bestBid < 0 ? -1 : bestBid + lo; }
    int bestAskTick() const { return bestAsk < 0 ? -1 : bestAsk + lo; }
};
int main() {
    Book b(1000, 2000); b.add(true, 1500, 10); b.add(true, 1490, 5); b.add(false, 1510, 7); b.add(false, 1505, 3);
    assert(b.bestBidTick() == 1500 && b.bestAskTick() == 1505); b.cancel(true, 1500, 10); assert(b.bestBidTick() == 1490);
    b.cancel(false, 1505, 3); assert(b.bestAskTick() == 1510); b.cancel(false, 1510, 7); assert(b.bestAskTick() == -1);
    // Randomised check against a std::map reference
    std::mt19937 g(1); Book bk(0, 999); std::map<int, int64_t> rb, ra;
    for (int s = 0; s < 200000; s++) {
        bool buy = g() & 1; int t = buy ? 300 + g() % 200 : 500 + g() % 200; auto& ref = buy ? rb : ra;
        if (ref.count(t) && (g() & 1)) { int64_t q = ref[t]; bk.cancel(buy, t, q); ref.erase(t); } else { bk.add(buy, t, 1); ref[t] += 1; }
        assert(bk.bestBidTick() == (rb.empty() ? -1 : rb.rbegin()->first)); assert(bk.bestAskTick() == (ra.empty() ? -1 : ra.begin()->first));
    }
    const long N = 2'000'000; Book hot(0, 9999); std::map<int, int64_t> m; std::vector<int> ticks(N); for (auto& t : ticks) t = 4000 + g() % 2000;
    best_ns_per_op("std::map add + best", N, [&] { for (int t : ticks) { m[t] += 1; keep(m.rbegin()->first); } }, 3);
    best_ns_per_op("array book add + best", N, [&] { for (int t : ticks) { hot.add(true, t, 1); keep(hot.bestBidTick()); } }, 3);
    std::puts("e8 ok");
}
```
