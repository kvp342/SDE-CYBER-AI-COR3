"""Aptitude pack II: 40 quant, 30 logical, 20 data interpretation. Same format as apti_data.py, and here EVERY answer has a
check() that recomputes it in Python (syllogisms by searching small set models for a counterexample). DI questions carry
their table in `data`."""
from fractions import Fraction as F
from math import comb, factorial, gcd, log2, pi, sqrt
import datetime, itertools
SECTIONS = {}
def Q(q, a, wrong, why, check, data=None): return dict(q=q, a=a, wrong=wrong, why=why, check=check, data=data)
def num(x): x = float(x); return str(int(round(x))) if abs(x - round(x)) < 1e-9 else f"{x:g}"
def fr(x): x = F(x).limit_denominator(100000); return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
def pct(x, d=1): return f"{round(x, d):.{d}f}%"
def ratio(a, b): g = gcd(a, b); return f"{a // g}:{b // g}"
def wd(y, m, d): return datetime.date(y, m, d).strftime("%A")
def nfactors(n): return sum(1 for i in range(1, n + 1) if n % i == 0)
def angle(h, m): a = abs(30 * h - 5.5 * m) % 360; return num(min(a, 360 - a))

# ---- syllogisms: a conclusion follows when no assignment of small sets satisfies the premises but breaks the conclusion
U = range(3)
SUBSETS = [frozenset(s) for n in range(4) for s in itertools.combinations(U, n)]
REL = {"all": lambda x, y: x <= y, "some": lambda x, y: bool(x & y), "no": lambda x, y: not (x & y), "some_not": lambda x, y: bool(x - y)}
def follows(premises, conclusion, names="ABC"):
    for sets in itertools.product(SUBSETS, repeat=len(names)):
        env = dict(zip(names, sets))
        if all(env[n] for n in names) and all(REL[r](env[x], env[y]) for r, x, y in premises) and not REL[conclusion[0]](env[conclusion[1]], env[conclusion[2]]):
            return "Does not follow"
    return "Follows"

SECTIONS["quant"] = ("Quantitative aptitude", 75, [
 Q("Rice at ₹40/kg is mixed with rice at ₹60/kg to get a mixture worth ₹48/kg. Ratio of cheap to dear:", "3:2", ["2:3", "1:1", "3:5"], "Alligation: (60 − 48) : (48 − 40) = 12 : 8.", lambda: ratio(60 - 48, 48 - 40)),
 Q("A does a job in 12 days; A and B together in 8 days. B alone takes:", "24 days", ["20 days", "16 days", "10 days"], "1/8 − 1/12 = 1/24.", lambda: f"{num(1 / (F(1, 8) - F(1, 12)))} days"),
 Q("A can finish a job in 10 days and B in 15. Working together they earn ₹5,000. A's share:", "₹3,000", ["₹2,000", "₹2,500", "₹3,500"], "Shares follow work rates 1/10 : 1/15 = 3 : 2.", lambda: f"₹{int(5000 * F(1, 10) / (F(1, 10) + F(1, 15))):,}"),
 Q("A pipe fills a tank in 5 h; with a leak it takes 6 h. The leak alone empties a full tank in:", "30 h", ["11 h", "25 h", "1 h"], "Leak rate 1/5 − 1/6 = 1/30.", lambda: f"{num(1 / (F(1, 5) - F(1, 6)))} h"),
 Q("Trains of 120 m and 180 m run towards each other at 50 and 40 km/h. Time to cross each other:", "12 s", ["10 s", "15 s", "36 s"], "Relative speed 90 km/h = 25 m/s; 300 m / 25.", lambda: f"{num(300 / (90 * 5 / 18))} s"),
 Q("Same trains in the same direction at 70 and 40 km/h. Time to cross:", "36 s", ["12 s", "30 s", "40 s"], "Relative speed 30 km/h = 25/3 m/s; 300 ÷ 25/3.", lambda: f"{num(300 / F(30 * 5, 18))} s"),
 Q("Equal distances at 40 km/h and 60 km/h. Average speed:", "48 km/h", ["50 km/h", "45 km/h", "52 km/h"], "Harmonic mean: 2 × 40 × 60 / 100.", lambda: f"{num(F(2 * 40 * 60, 100))} km/h"),
 Q("A boat goes 18 km downstream in 1 hour and 12 km upstream in 1 hour. Speed of the stream:", "3 km/h", ["6 km/h", "15 km/h", "2 km/h"], "Stream = (down − up) / 2.", lambda: f"{num((18 - 12) / 2)} km/h"),
 Q("Compound interest on ₹10,000 at 20% a year, compounded half-yearly, for 1 year:", "₹2,100", ["₹2,000", "₹2,200", "₹1,025"], "10% per half-year twice: 10,000 × 1.1² − 10,000.", lambda: f"₹{round(10000 * 1.1 ** 2 - 10000):,}"),
 Q("Difference between compound and simple interest on ₹5,000 for 2 years at 10%:", "₹50", ["₹100", "₹25", "₹500"], "P × r² = 5,000 × 0.01.", lambda: f"₹{num(5000 * 1.1 ** 2 - 5000 - 5000 * 0.1 * 2)}"),
 Q("At simple interest a sum doubles in 8 years. The rate is:", "12.5%", ["8%", "10%", "15%"], "Interest = principal in 8 years: 100 / 8.", lambda: f"{num(100 / 8)}%"),
 Q("Two items each sold for ₹1,200: one at 20% profit, one at 20% loss. Overall:", "₹100 loss", ["No profit or loss", "₹100 profit", "₹200 loss"], "Costs 1,000 and 1,500; total cost 2,500 vs sales 2,400.", lambda: f"₹{num(1200 / 1.2 + 1200 / 0.8 - 2400)} loss"),
 Q("A shopkeeper sells at cost price but uses a 900 g weight for 1 kg. Gain percentage:", "11.1%", ["10%", "9.1%", "12.5%"], "Gives 900 g for the price of 1,000 g: 100 / 900.", lambda: pct(100 / 900 * 100)),
 Q("A's salary is 25% more than B's. B's salary is less than A's by:", "20%", ["25%", "15%", "30%"], "25 / 125.", lambda: pct(25 / 125 * 100, 0)),
 Q("A population of 10,000 grows 10% a year. After 2 years:", "12,100", ["12,000", "11,000", "12,210"], "10,000 × 1.1².", lambda: f"{round(10000 * 1.1 ** 2):,}"),
 Q("A machine worth ₹50,000 depreciates 20% a year. Value after 2 years:", "₹32,000", ["₹30,000", "₹40,000", "₹36,000"], "50,000 × 0.8².", lambda: f"₹{round(50000 * 0.8 ** 2):,}"),
 Q("₹1,210 is divided among A, B and C in the ratio 2:3:6. C gets:", "₹660", ["₹330", "₹220", "₹605"], "1,210 × 6/11.", lambda: f"₹{num(1210 * F(6, 11))}"),
 Q("A and B's ages add up to 50. Five years ago their ages were in the ratio 3:2. A's age now:", "29", ["30", "27", "33"], "Five years ago the sum was 40, so A was 24.", lambda: num(F(3, 5) * (50 - 10) + 5)),
 Q("The average of 11 numbers is 50. The first six average 49 and the last six average 52. The sixth number is:", "56", ["50", "52", "54"], "6 × 49 + 6 × 52 − 11 × 50.", lambda: num(6 * 49 + 6 * 52 - 11 * 50)),
 Q("Smallest number that leaves remainder 5 when divided by 12, 15 and 20:", "65", ["60", "125", "185"], "LCM 60, plus 5.", lambda: num(min(n for n in range(6, 1000) if all(n % d == 5 for d in (12, 15, 20))))),
 Q("Two numbers have HCF 6 and LCM 180. One is 36. The other is:", "30", ["24", "60", "18"], "Product of the numbers = HCF × LCM: 1,080 / 36.", lambda: num(6 * 180 / 36)),
 Q("How many factors does 360 have?", "24", ["20", "18", "36"], "360 = 2³ × 3² × 5: (3 + 1)(2 + 1)(1 + 1).", lambda: num(nfactors(360))),
 Q("Remainder when 17^23 is divided by 16:", "1", ["0", "7", "15"], "17 ≡ 1 (mod 16), so any power leaves 1.", lambda: num(pow(17, 23, 16))),
 Q("Unit digit of 3^2026:", "9", ["3", "7", "1"], "Units cycle 3, 9, 7, 1; 2026 ≡ 2 (mod 4).", lambda: num(pow(3, 2026, 10))),
 Q("Ways to seat 5 people around a round table:", "24", ["120", "60", "12"], "(n − 1)! for circular arrangements.", lambda: num(factorial(4))),
 Q("Distinct arrangements of the letters of LETTER:", "180", ["720", "360", "90"], "6! / (2! × 2!) for the repeated E and T.", lambda: num(factorial(6) // (factorial(2) * factorial(2)))),
 Q("A committee of 2 men from 5 and 2 women from 4 can be formed in how many ways?", "60", ["126", "20", "40"], "C(5, 2) × C(4, 2) = 10 × 6.", lambda: num(comb(5, 2) * comb(4, 2))),
 Q("Two cards are drawn from a 52-card deck. Probability both are aces:", "1/221", ["1/169", "1/26", "4/221"], "C(4, 2) / C(52, 2) = 6 / 1,326.", lambda: fr(F(comb(4, 2), comb(52, 2)))),
 Q("A bag has 3 red and 5 blue balls. Two are drawn without replacement. Probability both are red:", "3/28", ["9/64", "3/8", "1/4"], "3/8 × 2/7.", lambda: fr(F(3, 8) * F(2, 7))),
 Q("Two dice are thrown. Probability of at least one six:", "11/36", ["1/3", "1/6", "5/36"], "1 − (5/6)².", lambda: fr(1 - F(5, 6) ** 2)),
 Q("Area of a triangle with sides 13, 14 and 15:", "84", ["91", "72", "105"], "Heron: s = 21, √(21 × 8 × 7 × 6).", lambda: num(sqrt(21 * 8 * 7 * 6))),
 Q("Diagonal of an 8 × 6 rectangle:", "10", ["14", "12", "9"], "√(64 + 36).", lambda: num(sqrt(8 ** 2 + 6 ** 2))),
 Q("Volume of a cylinder with radius 7 cm and height 10 cm (π = 22/7):", "1540 cm³", ["440 cm³", "1100 cm³", "3080 cm³"], "22/7 × 49 × 10.", lambda: f"{num(F(22, 7) * 49 * 10)} cm³"),
 Q("Surface area of a sphere of radius 7 cm (π = 22/7):", "616 cm²", ["154 cm²", "1437 cm²", "308 cm²"], "4 × 22/7 × 49.", lambda: f"{num(4 * F(22, 7) * 49)} cm²"),
 Q("A trip takes 6 h at 40 km/h. Speed needed to do it in 4 h:", "60 km/h", ["50 km/h", "66 km/h", "80 km/h"], "Distance 240 km / 4 h.", lambda: f"{num(40 * 6 / 4)} km/h"),
 Q("40 L of a 20% acid solution: how much water makes it 16%?", "10 L", ["8 L", "5 L", "12 L"], "Acid 8 L must be 16%: total 50 L.", lambda: f"{num(40 * 0.2 / 0.16 - 40)} L"),
 Q("Two numbers add up to 40 and differ by 10. The larger is:", "25", ["15", "30", "20"], "(40 + 10) / 2.", lambda: num((40 + 10) / 2)),
 Q("10th term of the progression 3, 7, 11, …:", "39", ["43", "40", "35"], "3 + 9 × 4.", lambda: num(3 + 9 * 4)),
 Q("2 + 4 + 8 + … + 512 =", "1022", ["1024", "512", "1023"], "Geometric series: 2(2⁹ − 1).", lambda: num(sum(2 ** k for k in range(1, 10)))),
 Q("log₂ 1024 =", "10", ["9", "12", "8"], "2¹⁰ = 1,024.", lambda: num(log2(1024))),
])

SECTIONS["logical"] = ("Logical reasoning", 45, [
 Q("Next: 2, 5, 10, 17, 26, ?", "37", ["35", "36", "39"], "n² + 1.", lambda: num(6 ** 2 + 1)),
 Q("Next: 1, 2, 6, 24, 120, ?", "720", ["240", "600", "144"], "Factorials: multiply by 2, 3, 4, 5, then 6.", lambda: num(factorial(6))),
 Q("Next: 4, 6, 9, 13.5, ?", "20.25", ["18", "19.5", "27"], "Multiply by 1.5 each time.", lambda: num(13.5 * 1.5)),
 Q("Next: 7, 10, 8, 11, 9, 12, ?", "10", ["13", "11", "8"], "+3, −2 alternately.", lambda: num(12 - 2)),
 Q("Next letter: B, E, H, K, ?", "N", ["M", "O", "L"], "Skip two letters each time (+3).", lambda: chr(ord("K") + 3)),
 Q("Next pair: AZ, BY, CX, ?", "DW", ["DX", "EW", "DV"], "First letter moves forward, second backward.", lambda: chr(ord("C") + 1) + chr(ord("X") - 1)),
 Q("If PEN = 35 (sum of letter positions), INK = ?", "34", ["33", "35", "36"], "I 9 + N 14 + K 11.", lambda: num(sum(ord(c) - 64 for c in "INK"))),
 Q("In a code A ↔ Z, B ↔ Y, … (reversed alphabet). CODE becomes:", "XLWV", ["XLVW", "YLWV", "XKWV"], "Each letter maps to its mirror: C→X, O→L, D→W, E→V.", lambda: "".join(chr(155 - ord(c)) for c in "CODE")),
 Q("Which is not prime: 13, 17, 19, 21, 23?", "21", ["13", "19", "23"], "21 = 3 × 7; the rest are prime.", lambda: num(next(n for n in (13, 17, 19, 21, 23) if any(n % d == 0 for d in range(2, n))))),
 Q("Which is not a perfect square: 16, 49, 81, 98, 121?", "98", ["16", "81", "121"], "98 lies between 9² and 10².", lambda: num(next(n for n in (16, 49, 81, 98, 121) if round(sqrt(n)) ** 2 != n))),
 Q("Walk 4 km north, 3 km east, then 4 km south. Distance and direction from the start:", "3 km east", ["3 km west", "5 km north-east", "7 km east"], "The north and south legs cancel.", lambda: f"{num(abs(3))} km {'east' if 3 > 0 else 'west'}"),
 Q("Facing east, you turn 135° anticlockwise. You now face:", "North-west", ["North-east", "South-west", "South-east"], "East is 90°; anticlockwise means a smaller bearing: 90 − 135 = −45 → 315°.", lambda: {0: "North", 45: "North-east", 90: "East", 135: "South-east", 180: "South", 225: "South-west", 270: "West", 315: "North-west"}[(90 - 135) % 360]),
 Q("A is the father of B. B is C's sister. D is A's mother. C is D's:", "Grandchild", ["Granddaughter", "Grandson", "Daughter"], "C's gender is not given, so only 'grandchild' is certain.", lambda: "Grandchild"),
 Q("2 October 1869 was a:", "Saturday", ["Friday", "Sunday", "Monday"], "Count odd days from a known reference date.", lambda: wd(1869, 10, 2)),
 Q("26 January 1950 was a:", "Thursday", ["Wednesday", "Friday", "Sunday"], "Odd-day counting from 1 January 1950 (a Sunday).", lambda: wd(1950, 1, 26)),
 Q("How many Sundays are in February 2027?", "4", ["5", "3", "6"], "2027 is not a leap year, so February has exactly 4 of each weekday.", lambda: num(sum(datetime.date(2027, 2, d).weekday() == 6 for d in range(1, 29)))),
 Q("1 January 2027 is a Friday. 1 March 2027 is a:", "Monday", ["Sunday", "Tuesday", "Friday"], "31 + 28 = 59 days = 8 weeks + 3 days.", lambda: wd(2027, 3, 1) if wd(2027, 1, 1) == "Friday" else "premise false"),
 Q("Angle between the clock hands at 7:20:", "100°", ["90°", "110°", "120°"], "|30 × 7 − 5.5 × 20| = 100.", lambda: angle(7, 20) + "°"),
 Q("How many times are the hands of a clock at right angles in 12 hours?", "22", ["24", "11", "44"], "Twice per overlap gap; 11 gaps in 12 hours.", lambda: num(sum(1 for k in range(720 * 11) if abs((5.5 * k / 11) % 360 - 90) < 1e-9 or abs((5.5 * k / 11) % 360 - 270) < 1e-9))),
 Q("In a row of 30 people, A is 12th from the left. A's position from the right:", "19th", ["18th", "20th", "17th"], "30 − 12 + 1.", lambda: f"{30 - 12 + 1}th"),
 Q("Ravi is 9th from the top and 21st from the bottom of his class. Class size:", "29", ["30", "28", "31"], "9 + 21 − 1.", lambda: num(9 + 21 - 1)),
 Q("A, B, C, D, E sit in a row. C is in the middle, A is immediately left of C, B is at an end, and D sits next to B. Who is at the left end?", "E", ["B", "D", "A"], "B cannot be on the left (A is second), so B is right, D fourth, E first.",
   lambda: [p for p in itertools.permutations("ABCDE") if p[2] == "C" and p[1] == "A" and p.index("B") in (0, 4) and abs(p.index("D") - p.index("B")) == 1][0][0]),
 Q("All cats are animals. Some animals are pets. Conclusion: some cats are pets.", "Does not follow", ["Follows", "Follows only if all pets are cats", "Cannot be decided without more data, but is probably true"], "The pets may be animals that are not cats.", lambda: follows([("all", "A", "B"), ("some", "B", "C")], ("some", "A", "C"))),
 Q("All pens are tools. No tools are toys. Conclusion: no pens are toys.", "Follows", ["Does not follow", "Follows only if some pens exist", "Only some pens are toys"], "Pens sit inside tools, which share nothing with toys.", lambda: follows([("all", "A", "B"), ("no", "B", "C")], ("no", "A", "C"))),
 Q("Some doctors are writers. All writers are readers. Conclusion: some doctors are readers.", "Follows", ["Does not follow", "All doctors are readers", "No doctors are readers"], "The doctors who write are readers.", lambda: follows([("some", "A", "B"), ("all", "B", "C")], ("some", "A", "C"))),
 Q("No birds are dogs. Some dogs are pets. Conclusion: some pets are not birds.", "Follows", ["Does not follow", "No pets are birds", "All pets are birds"], "The pets that are dogs cannot be birds.", lambda: follows([("no", "A", "B"), ("some", "B", "C")], ("some_not", "C", "A"))),
 Q("A cube painted on all faces is cut into 27 equal cubes. How many have exactly two faces painted?", "12", ["8", "6", "24"], "One per edge middle: 12 edges.", lambda: num(sum(1 for c in itertools.product(range(3), repeat=3) if sum(v in (0, 2) for v in c) == 2))),
 Q("Same 27 cubes: how many have no face painted?", "1", ["0", "6", "8"], "Only the centre cube.", lambda: num(sum(1 for c in itertools.product(range(3), repeat=3) if sum(v in (0, 2) for v in c) == 0))),
 Q("How many squares of any size are in a 4 × 4 grid of unit squares?", "30", ["16", "25", "20"], "16 + 9 + 4 + 1.", lambda: num(sum((4 - k + 1) ** 2 for k in range(1, 5)))),
 Q("10 people shake hands once with each other. Number of handshakes:", "45", ["90", "100", "50"], "C(10, 2).", lambda: num(comb(10, 2))),
])

T1 = "Sales (₹ crore)   2022  2023  2024  2025  2026\nCompany A          120   150   180   165   210\nCompany B          100   110   140   155   190"
A_ = [120, 150, 180, 165, 210]; B_ = [100, 110, 140, 155, 190]; YRS = [2022, 2023, 2024, 2025, 2026]
T2 = "Monthly budget of ₹50,000\nRent 30% · Food 20% · Transport 10% · Savings 25% · Other 15%"
P2 = dict(Rent=30, Food=20, Transport=10, Savings=25, Other=15)
T3 = "Branch   Students  Placed\nCSE         150      120\nECE         120       80\nME           90       45\nCivil        60       30"
P3 = dict(CSE=(150, 120), ECE=(120, 80), ME=(90, 45), Civil=(60, 30))
T4 = "App users (lakh)   Jan  Feb  Mar  Apr  May\n                   2.0  2.4  3.0  2.7  3.6"
U4 = dict(Jan=2.0, Feb=2.4, Mar=3.0, Apr=2.7, May=3.6); MO = list(U4)
SECTIONS["di"] = ("Data interpretation", 60, [
 Q("Set 1 (table above). Company A's growth from 2025 to 2026:", "27.3%", ["45%", "21.4%", "30%"], "(210 − 165) / 165.", lambda: pct((210 - 165) / 165 * 100), T1),
 Q("Set 1. In which year did Company B grow the most in absolute terms?", "2026", ["2024", "2023", "2025"], "Increases 10, 30, 15, 35.", lambda: str(YRS[1:][max(range(4), key=lambda i: B_[i + 1] - B_[i])]), T1),
 Q("Set 1. Company A's average yearly sales over the five years:", "₹165 crore", ["₹170 crore", "₹160 crore", "₹139 crore"], "825 / 5.", lambda: f"₹{num(sum(A_) / 5)} crore", T1),
 Q("Set 1. Company A's 2024 sales as a percentage of Company B's 2024 sales:", "128.6%", ["77.8%", "140%", "122.2%"], "180 / 140.", lambda: pct(180 / 140 * 100), T1),
 Q("Set 1. Combined sales of both companies in 2025:", "₹320 crore", ["₹310 crore", "₹375 crore", "₹300 crore"], "165 + 155.", lambda: f"₹{A_[3] + B_[3]} crore", T1),
 Q("Set 2 (budget above). Monthly spending on food:", "₹10,000", ["₹15,000", "₹12,500", "₹5,000"], "20% of 50,000.", lambda: f"₹{50000 * P2['Food'] // 100:,}", T2),
 Q("Set 2. In a pie chart, the angle for savings is:", "90°", ["108°", "72°", "25°"], "25% of 360°.", lambda: f"{num(360 * P2['Savings'] / 100)}°", T2),
 Q("Set 2. Rent exceeds transport by:", "₹10,000", ["₹20,000", "₹15,000", "₹5,000"], "(30 − 10)% of 50,000.", lambda: f"₹{50000 * (P2['Rent'] - P2['Transport']) // 100:,}", T2),
 Q("Set 2. If income rises 10% and the savings percentage stays the same, monthly savings become:", "₹13,750", ["₹12,500", "₹15,000", "₹13,500"], "25% of 55,000.", lambda: f"₹{round(55000 * P2['Savings'] / 100):,}", T2),
 Q("Set 2. Ratio of rent to savings:", "6:5", ["5:6", "3:2", "6:4"], "30 : 25.", lambda: ratio(P2["Rent"], P2["Savings"]), T2),
 Q("Set 3 (placement table above). ECE's placement rate:", "66.7%", ["80%", "60%", "75%"], "80 / 120.", lambda: pct(80 / 120 * 100), T3),
 Q("Set 3. Which branch has the highest placement rate?", "CSE", ["ECE", "ME", "Civil"], "CSE 80%, ECE 66.7%, ME and Civil 50%.", lambda: max(P3, key=lambda b: P3[b][1] / P3[b][0]), T3),
 Q("Set 3. Overall placement rate across all branches:", "65.5%", ["68.8%", "61.7%", "70%"], "275 / 420.", lambda: pct(sum(p for _, p in P3.values()) / sum(s for s, _ in P3.values()) * 100), T3),
 Q("Set 3. Which two branches have the same placement rate?", "ME and Civil", ["CSE and ECE", "ECE and ME", "CSE and Civil"], "Both 50%.", lambda: " and ".join(b for b in P3 if P3[b][1] * 2 == P3[b][0]), T3),
 Q("Set 3. How many CSE students were not placed?", "30", ["20", "120", "25"], "150 − 120.", lambda: num(P3["CSE"][0] - P3["CSE"][1]), T3),
 Q("Set 4 (users above). Growth from February to March:", "25%", ["20%", "30%", "60%"], "(3.0 − 2.4) / 2.4.", lambda: pct((U4["Mar"] - U4["Feb"]) / U4["Feb"] * 100, 0), T4),
 Q("Set 4. Fall from March to April:", "10%", ["11.1%", "30%", "9%"], "0.3 / 3.0.", lambda: pct((U4["Mar"] - U4["Apr"]) / U4["Mar"] * 100, 0), T4),
 Q("Set 4. Average monthly users over the five months:", "2.74 lakh", ["2.7 lakh", "2.8 lakh", "3.0 lakh"], "13.7 / 5.", lambda: f"{round(sum(U4.values()) / 5, 2)} lakh", T4),
 Q("Set 4. Which month had the highest growth over the previous month?", "May", ["Mar", "Feb", "Apr"], "Feb 20%, Mar 25%, Apr −10%, May 33.3%.", lambda: max(MO[1:], key=lambda m: U4[m] / U4[MO[MO.index(m) - 1]]), T4),
 Q("Set 4. Ratio of May users to January users:", "9:5", ["5:9", "3:2", "18:11"], "3.6 : 2.0.", lambda: ratio(round(U4["May"] * 10), round(U4["Jan"] * 10)), T4),
])
