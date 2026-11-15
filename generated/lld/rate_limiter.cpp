// Rate limiter: token bucket and sliding-window log behind one interface, per-client state,
// an injected clock for deterministic tests, and a mutex for thread safety.
#include <cassert>
#include <deque>
#include <functional>
#include <iostream>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>
using namespace std;
using Clock = function<double()>;                                 // seconds

class RateLimiter {
public:
    virtual ~RateLimiter() = default;
    virtual bool allow(const string& client) = 0;
};

class TokenBucket : public RateLimiter {                          // allows bursts up to capacity, refills steadily
    struct Bucket { double tokens, last; };
    double capacity, ratePerSec; Clock now; unordered_map<string, Bucket> b; mutex m;
public:
    TokenBucket(double cap, double rate, Clock c) : capacity(cap), ratePerSec(rate), now(move(c)) {}
    bool allow(const string& id) override {
        lock_guard<mutex> g(m);
        double t = now();
        auto it = b.find(id);
        if (it == b.end()) it = b.emplace(id, Bucket{capacity, t}).first;
        Bucket& k = it->second;
        k.tokens = min(capacity, k.tokens + (t - k.last) * ratePerSec); k.last = t;
        if (k.tokens < 1) return false;
        k.tokens -= 1; return true;
    }
};

class SlidingWindowLog : public RateLimiter {                     // exact: at most `limit` requests in any `window` seconds
    size_t limit; double window; Clock now; unordered_map<string, deque<double>> log; mutex m;
public:
    SlidingWindowLog(size_t l, double w, Clock c) : limit(l), window(w), now(move(c)) {}
    bool allow(const string& id) override {
        lock_guard<mutex> g(m);
        double t = now(); auto& q = log[id];
        while (!q.empty() && t - q.front() >= window) q.pop_front();
        if (q.size() >= limit) return false;
        q.push_back(t); return true;
    }
};

int main() {
    double fake = 0; Clock clock = [&] { return fake; };
    TokenBucket tb(3, 1.0, clock);                                // burst of 3, then 1 per second
    assert(tb.allow("a") && tb.allow("a") && tb.allow("a") && !tb.allow("a"));
    assert(tb.allow("b"));                                        // clients are independent
    fake = 1.0; assert(tb.allow("a") && !tb.allow("a"));
    fake = 10;  int ok = 0; for (int i = 0; i < 5; i++) ok += tb.allow("a"); assert(ok == 3);   // never above capacity

    fake = 0; SlidingWindowLog sw(2, 60, clock);
    assert(sw.allow("x") && sw.allow("x") && !sw.allow("x"));
    fake = 59.9; assert(!sw.allow("x"));
    fake = 60;   assert(sw.allow("x"));                           // the first request has left the window

    double frozen = 0; TokenBucket shared(1000, 0, [&] { return frozen; });
    int granted = 0; mutex gm; vector<thread> ts;
    for (int t = 0; t < 8; t++) ts.emplace_back([&] { int mine = 0; for (int i = 0; i < 500; i++) mine += shared.allow("api"); lock_guard<mutex> g(gm); granted += mine; });
    for (auto& t : ts) t.join();
    assert(granted == 1000);                                      // 4000 attempts, exactly capacity granted
    cout << "rate limiter ok\n";
}
