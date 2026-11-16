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
