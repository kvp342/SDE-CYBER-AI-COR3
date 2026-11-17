// Logger: levels, several sinks each with its own minimum level, a formatter, and thread safety.
#include <cassert>
#include <iostream>
#include <memory>
#include <mutex>
#include <sstream>
#include <string>
#include <thread>
#include <vector>
using namespace std;
enum class Level { Debug, Info, Warn, Error };
static const char* name(Level l) { static const char* n[] = {"DEBUG", "INFO", "WARN", "ERROR"}; return n[(int)l]; }
class Sink { public: Level min; explicit Sink(Level m) : min(m) {} virtual ~Sink() = default; virtual void write(const string& line) = 0; };
class StreamSink : public Sink { ostream& os; public: StreamSink(ostream& o, Level m) : Sink(m), os(o) {} void write(const string& l) override { os << l << '\n'; } };
class MemorySink : public Sink { public: vector<string> lines; explicit MemorySink(Level m) : Sink(m) {} void write(const string& l) override { lines.push_back(l); } };
class Logger {
    vector<shared_ptr<Sink>> sinks; mutex m; string source;
public:
    explicit Logger(string src) : source(move(src)) {}
    void add(shared_ptr<Sink> s) { lock_guard<mutex> g(m); sinks.push_back(move(s)); }
    void log(Level l, const string& msg) {
        string line = string("[") + name(l) + "] " + source + ": " + msg;   // format once, outside the per-sink loop
        lock_guard<mutex> g(m);
        for (auto& s : sinks) if (l >= s->min) s->write(line);
    }
    void debug(const string& s) { log(Level::Debug, s); } void info(const string& s) { log(Level::Info, s); }
    void warn(const string& s) { log(Level::Warn, s); } void error(const string& s) { log(Level::Error, s); }
};
int main() {
    ostringstream console; auto mem = make_shared<MemorySink>(Level::Debug);
    Logger log("payments"); log.add(make_shared<StreamSink>(console, Level::Warn)); log.add(mem);
    log.debug("cache miss"); log.info("order 42 paid"); log.warn("retrying gateway"); log.error("gateway down");
    assert(console.str() == "[WARN] payments: retrying gateway\n[ERROR] payments: gateway down\n");
    assert(mem->lines.size() == 4 && mem->lines[0] == "[DEBUG] payments: cache miss");
    auto many = make_shared<MemorySink>(Level::Info); Logger l2("api"); l2.add(many); vector<thread> ts;
    for (int t = 0; t < 8; t++) ts.emplace_back([&, t] { for (int i = 0; i < 250; i++) l2.info("t" + to_string(t)); });
    for (auto& th : ts) th.join();
    assert(many->lines.size() == 2000);                           // no lost or torn lines
    cout << "logger ok\n";
}
