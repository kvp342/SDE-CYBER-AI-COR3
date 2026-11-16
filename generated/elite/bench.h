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
