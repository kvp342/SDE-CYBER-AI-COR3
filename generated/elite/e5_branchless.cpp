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
