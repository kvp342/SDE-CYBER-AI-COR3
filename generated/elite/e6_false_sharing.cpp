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
