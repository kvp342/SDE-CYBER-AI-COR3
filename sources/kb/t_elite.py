"""Elite category: everything HFT, opened only by the 31 Mar checkpoint."""
TOPICS = [
dict(id="hft-overview", title="HFT roles and the 31 March gate", cat="Elite", lvl=4,
 aka=["HFT track", "The HFT track", "Elite: the HFT track", "HFT gate", "the HFT gate", "Checkpoint 2"],
 why="You said you're willing to go for HFT. This page is the honest version: what these firms test, how few freshers they hire, and the checkpoint that decides whether the hours are worth spending.",
 core=["High-frequency trading firms (for example Tower Research, Graviton, Quadeye, Optiver) hire freshers into three roles: software engineers who build low-latency trading systems in C++, quant traders, and quant researchers. For a CSE student the software-engineer role is the best fit.",
       "Their online tests are much harder than product-company OAs: hard competitive programming under time pressure, C++ depth (memory, move semantics, templates), OS and networks, and for trader roles fast probability and mental maths. Most fresher hires come from campus drives at top colleges or from strong Codeforces and ICPC profiles.",
       "Your plan is Path A (SDE with security and cloud depth). The HFT track opens only if you pass checkpoint 2 on 31 March 2027: a Codeforces rating of 1400+ or a LeetCode contest rating of 1800+. If you pass, you add 1 to 1.5 hours a day from 8 April to 25 July; cyber drops to 3 days a week and the AI-security project shrinks to 2 weeks. If you miss it, you stay on Path A; the contest practice still makes every online test easier."],
 points=["Checkpoint 1 (30 Jan): Striver core done, LeetCode Mediums in about 25 minutes", "Checkpoint 2, the gate (31 Mar): CF 1400+ or LC contest 1800+", "16 weeks: counting and probability → expected value → interview puzzles → timed practice and low-latency C++", "Daily while open: 10 minutes of Zetamac, a Codeforces Div 2 round each week", "Aim for CF 1600+ by July if the track is open"],
 pit=["Starting HFT preparation before DSA basics are solid", "Running HFT on top of every other track (that is the burnout zone)", "Treating a missed gate as failure: Path A is the plan"],
 ask=["Why do you want to work at a trading firm?", "What happens in memory when you push_back into a full vector?", "Expected number of coin flips to get two heads in a row?"],
 prac=[("Codeforces", "https://codeforces.com"), ("Zetamac", "https://arithmetic.zetamac.com"), ("Brainstellar", "https://www.brainstellar.com")],
 learn=[("Harvard Stat 110", "https://projects.iq.harvard.edu/stat110"), ("CSES problem set", "https://cses.fi/problemset/")], rel=["probability", "low-latency-cpp", "cp"]),

dict(id="low-latency-cpp", title="Low-latency C++", cat="Elite", lvl=4,
 aka=["low-latency C++", "Low-latency C++"],
 why="The skill that makes you a fit for HFT software-engineer roles, and a strong C++ answer in any systems interview.",
 core=["Latency-critical code avoids work on the hot path: no heap allocation (pre-allocate and reuse), no system calls, no locks where a single-producer single-consumer queue will do, and no virtual dispatch in tight loops (templates or CRTP resolve calls at compile time).",
       "Memory layout dominates speed. Contiguous arrays beat linked structures because CPUs fetch 64-byte cache lines and prefetch sequential access. Keep hot data small and together; separate data written by different threads onto different cache lines to avoid false sharing.",
       "Move semantics let you transfer ownership of buffers instead of copying them. Reserve vectors up front, pass large objects by const reference, and return by value (copy elision).",
       "Measure, don't guess: microbenchmarks with many repetitions, percentiles (p50, p99) rather than averages, and a profiler such as perf."],
 points=["Cache line = 64 bytes; false sharing = two threads writing the same line", "std::atomic with acquire/release ordering for a lock-free SPSC queue", "Branch prediction: predictable branches are cheap, random ones cost ~15–20 cycles", "Avoid std::endl in hot loops (it flushes)", "constexpr and templates move work to compile time"],
 code="""// Single-producer single-consumer ring buffer: no locks, no allocation after construction.
template <typename T, size_t N>                 // N must be a power of two
class SpscQueue {
    static_assert((N & (N - 1)) == 0, "N must be a power of two");
    T buf[N];
    alignas(64) std::atomic<size_t> head{0};    // written only by the consumer
    alignas(64) std::atomic<size_t> tail{0};    // written only by the producer
public:
    bool push(const T& v) {
        size_t t = tail.load(std::memory_order_relaxed);
        if (t - head.load(std::memory_order_acquire) == N) return false;    // full
        buf[t & (N - 1)] = v;
        tail.store(t + 1, std::memory_order_release);
        return true;
    }
    bool pop(T& out) {
        size_t h = head.load(std::memory_order_relaxed);
        if (h == tail.load(std::memory_order_acquire)) return false;        // empty
        out = buf[h & (N - 1)];
        head.store(h + 1, std::memory_order_release);
        return true;
    }
};""",
 pit=["Optimising before measuring", "Putting head and tail on the same cache line (false sharing)", "Using memory_order_relaxed everywhere and hoping"],
 ask=["What is false sharing and how do you avoid it?", "Why is a vector usually faster than a linked list even for inserts?", "Explain acquire and release memory ordering."],
 prac=[], learn=[("cppreference: std::atomic", "https://en.cppreference.com/w/cpp/atomic/atomic"), ("What every programmer should know about memory (Drepper)", "https://people.freebsd.org/~lstewart/articles/cpumemory.pdf")],
 rel=["vtable", "cpp-stl", "hft-overview"]),
]
