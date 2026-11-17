// Advanced topics in one file: segment tree (range sum, point update), Fenwick tree (BIT), sieve of Eratosthenes,
// fast modular exponentiation, gcd/lcm, and modular inverse; each checked against brute force.
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
using namespace std;
struct SegTree {                                             // iterative, size n, sums
    int n; vector<long long> t;
    explicit SegTree(const vector<long long>& a) : n(a.size()), t(2 * a.size()) { for (int i = 0; i < n; i++) t[n + i] = a[i]; for (int i = n - 1; i > 0; i--) t[i] = t[2 * i] + t[2 * i + 1]; }
    void set(int i, long long v) { for (t[i += n] = v; i > 1; i >>= 1) t[i >> 1] = t[i] + t[i ^ 1]; }
    long long sum(int l, int r) const { long long s = 0; for (l += n, r += n; l < r; l >>= 1, r >>= 1) { if (l & 1) s += t[l++]; if (r & 1) s += t[--r]; } return s; }   // [l, r)
};
struct BIT {                                                 // 1-indexed internally; add and prefix sums in O(log n)
    vector<long long> f; explicit BIT(int n) : f(n + 1) {}
    void add(int i, long long d) { for (i++; i < (int)f.size(); i += i & -i) f[i] += d; }
    long long prefix(int i) const { long long s = 0; for (; i > 0; i -= i & -i) s += f[i]; return s; }   // sum of [0, i)
    long long sum(int l, int r) const { return prefix(r) - prefix(l); }
};
vector<int> sieve(int n) { vector<bool> comp(n + 1); vector<int> p; for (int i = 2; i <= n; i++) { if (comp[i]) continue; p.push_back(i); for (long long j = 1LL * i * i; j <= n; j += i) comp[j] = true; } return p; }
long long modpow(long long b, long long e, long long m) { long long r = 1 % m; b %= m; while (e) { if (e & 1) r = (__int128)r * b % m; b = (__int128)b * b % m; e >>= 1; } return r; }
long long modinv(long long a, long long p) { return modpow(a, p - 2, p); }   // p prime (Fermat)
int main() {
    mt19937 rng(7); vector<long long> a(37); for (auto& x : a) x = rng() % 100;
    SegTree st(a); BIT bit(a.size()); for (size_t i = 0; i < a.size(); i++) bit.add(i, a[i]);
    for (int it = 0; it < 2000; it++) {
        int i = rng() % a.size(); long long v = rng() % 100; st.set(i, v); bit.add(i, v - a[i]); a[i] = v;
        int l = rng() % a.size(), r = rng() % (a.size() + 1); if (l > r) swap(l, r);
        long long brute = accumulate(a.begin() + l, a.begin() + r, 0LL);
        assert(st.sum(l, r) == brute && bit.sum(l, r) == brute);
    }
    auto p = sieve(100); assert(p.size() == 25 && p.back() == 97);
    assert(sieve(1'000'000).size() == 78498);                 // known count of primes below 10^6
    const long long MOD = 1'000'000'007;
    assert(modpow(2, 10, MOD) == 1024 && modpow(3, 0, 7) == 1 && modpow(5, 3, 1) == 0);
    long long x = 1; for (int i = 0; i < 1000; i++) x = x * 7 % MOD; assert(modpow(7, 1000, MOD) == x);
    assert(modinv(3, MOD) * 3 % MOD == 1 && gcd(84, 126) == 42 && lcm(12, 18) == 36);
    cout << "data structures and maths ok\n";
}
