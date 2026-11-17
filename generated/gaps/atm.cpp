// ATM: a state machine (Idle -> CardInserted -> Authenticated -> back to Idle), PIN attempts with card retention,
// withdrawals limited by balance and by the notes in the machine (greedy works for 100/200/500/2000 notes, checked by brute force).
#include <cassert>
#include <iostream>
#include <map>
#include <optional>
#include <string>
using namespace std;
enum class State { Idle, CardInserted, Authenticated };
struct Account { string pin; long long balance; };
class Bank { map<string, Account> acc; public:
    void open(const string& card, string pin, long long bal) { acc[card] = {move(pin), bal}; }
    bool checkPin(const string& c, const string& p) const { auto it = acc.find(c); return it != acc.end() && it->second.pin == p; }
    long long balance(const string& c) const { return acc.at(c).balance; }
    bool debit(const string& c, long long amt) { auto& a = acc.at(c); if (a.balance < amt) return false; a.balance -= amt; return true; } };
class ATM {
    Bank& bank; State st = State::Idle; string card; int tries = 0; map<int, int, greater<int>> notes;   // note -> count, largest first
public:
    explicit ATM(Bank& b) : bank(b) {}
    void load(int note, int count) { notes[note] += count; }
    State state() const { return st; }
    bool insert(const string& c) { if (st != State::Idle) return false; card = c; tries = 0; st = State::CardInserted; return true; }
    string enterPin(const string& p) {
        if (st != State::CardInserted) return "no card";
        if (bank.checkPin(card, p)) { st = State::Authenticated; return "ok"; }
        if (++tries == 3) { st = State::Idle; card.clear(); return "card retained"; }
        return "wrong pin";
    }
    optional<map<int, int, greater<int>>> plan(long long amt) const {      // greedy over available notes
        map<int, int, greater<int>> out; for (auto [n, c] : notes) { long long k = min<long long>(c, amt / n); if (k) out[n] = (int)k; amt -= k * n; }
        if (amt) return nullopt;
        return out;
    }
    string withdraw(long long amt) {
        if (st != State::Authenticated) return "not authenticated";
        if (amt <= 0 || amt % 100) return "amount must be a multiple of 100";
        auto p = plan(amt); if (!p) return "cannot dispense this amount";
        if (!bank.debit(card, amt)) return "insufficient funds";
        for (auto [n, c] : *p) notes[n] -= c;
        return "dispensed";
    }
    void eject() { st = State::Idle; card.clear(); }
};
int main() {
    Bank bank; bank.open("C1", "1234", 10000); ATM atm(bank); atm.load(500, 4); atm.load(200, 5); atm.load(100, 2);
    assert(atm.withdraw(500) == "not authenticated" && atm.insert("C1") && !atm.insert("C2"));
    assert(atm.enterPin("0000") == "wrong pin" && atm.enterPin("1234") == "ok" && atm.state() == State::Authenticated);
    assert(atm.withdraw(150) == "amount must be a multiple of 100" && atm.withdraw(2500) == "dispensed" && bank.balance("C1") == 7500);
    // 2500 used 4x500 + 2x200 + 1x100, so the machine now holds 3x200 + 1x100 = 700
    assert(atm.withdraw(800) == "cannot dispense this amount" && bank.balance("C1") == 7500);   // more than the notes in the machine
    assert(atm.withdraw(700) == "dispensed" && atm.withdraw(100) == "cannot dispense this amount" && bank.balance("C1") == 6800);
    atm.eject(); bank.open("C2", "9999", 50); atm.insert("C2");
    assert(atm.enterPin("1") == "wrong pin" && atm.enterPin("2") == "wrong pin" && atm.enterPin("3") == "card retained" && atm.state() == State::Idle);
    for (int amt = 100; amt <= 5000; amt += 100) {                    // greedy = optimal for these notes: compare with brute force
        int best = 1 << 30; for (int a = 0; a * 2000 <= amt; a++) for (int b = 0; a * 2000 + b * 500 <= amt; b++) for (int c = 0; a * 2000 + b * 500 + c * 200 <= amt; c++) { int d = amt - a * 2000 - b * 500 - c * 200; if (d % 100 == 0) best = min(best, a + b + c + d / 100); }
        int g = 0, left = amt; for (int n : {2000, 500, 200, 100}) { g += left / n; left %= n; }
        assert(g == best);
    }
    cout << "atm ok\n";
}
