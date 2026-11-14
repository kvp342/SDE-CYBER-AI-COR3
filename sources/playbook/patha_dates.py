"""Recompute every static date table in the Playbook from the new daily data (run last)."""
import json, re, sys, datetime, html as H
dt = datetime.date; TD = datetime.timedelta
SRC, OLD = sys.argv[1], sys.argv[2]
h = open(SRC, encoding="utf-8").read(); ho = open(OLD, encoding="utf-8").read()
getD = lambda x: json.loads(x[x.index("\nvar D=") + 7: x.index("};", x.index("\nvar D=")) + 1])
N, DO = getD(h), getD(ho)
d_ = dt.fromisoformat
sh = lambda d: d.strftime("%a %d %b")              # Sat 21 Nov
md = lambda d: d.strftime("%d %b")                 # 21 Nov
def runs(ds, gap=8, f=md):
    out = []
    for d in sorted(ds):
        if out and (d - out[-1][1]).days <= gap: out[-1][1] = d
        else: out.append([d, d])
    return ", ".join(f(a) if a == b else f"{f(a)} to {f(b)}" for a, b in out)
cnt = {}
def sub(name, pat, fn, flags=0, min_=1):
    global h
    h, n = re.subn(pat, fn, h, flags=flags); cnt[name] = n
    assert n >= min_, (name, n)

# LeetCode problem dates and contest dates
lcd = {}; newc = []; newp = []
for k in sorted(N):
    lc = N[k].get("lc")
    if not lc: continue
    (newc if lc["contest"] else newp).append(k)
    for p in lc["p"]: lcd.setdefault(p[0], d_(k))
oldc = [k for k in sorted(DO) if DO[k].get("lc", {}).get("contest")]
oldp = [k for k in sorted(DO) if DO[k].get("lc") and not DO[k]["lc"]["contest"]]
remap = dict(zip(oldc, newc)); remap.update(zip(oldp, newp))
sub("lc companions", r'(<li><b>#(\d+) [^<]+</b> \((?:Easy|Medium|Hard)\), )([A-Z][a-z]{2} \d{2} [A-Z][a-z]{2})(</li>)',
    lambda m: m.group(1) + (sh(lcd[int(m.group(2))]) if int(m.group(2)) in lcd else m.group(3)) + m.group(4))
def lcrow(m):
    new = remap.get(m.group(2))
    return m.group(0) if not new else f'{m.group(1)}id="lc-{new}"><td class="mono">{sh(d_(new))}</td>'
sub("lc month rows", r'(<tr class="(?:contest)?" )id="lc-(\d{4}-\d\d-\d\d)"><td class="mono">[^<]*</td>', lcrow, min_=25)

# Hard pass: problem name -> date
hd = {}
for k, v in N.items():
    if v.get("due") and not v.get("steps"):
        for x in v["due"]: hd[x[1]] = d_(k)
s = h.index('id="hard-pass"'); e = h.index('</section>', s); seg = h[s:e]
seg, n = re.subn(r'<tr><td>[A-Z][a-z]{2} \d{2} [A-Z][a-z]{2}</td><td>([^<]+)</td><td>([^<]+)</td></tr>',
                 lambda m: f'<tr><td>{sh(hd[H.unescape(m.group(2))])}</td><td>{m.group(1)}</td><td>{m.group(2)}</td></tr>' if H.unescape(m.group(2)) in hd else m.group(0), seg)
cnt["hard rows"] = n; assert n == 84, n
seg = seg.replace('PART 02B  |  4 JAN TO 28 MAR', 'PART 02B  |  8 FEB TO 19 MAY, NOT IN EXAMS')
h = h[:s] + seg + h[e:]

# Core CS: subject ranges, eyebrows and week rows
subj = {}; topic = {}
for k, v in N.items():
    c = v.get("cs")
    if not c: continue
    subj.setdefault(c[3], []).append(d_(k))
    if c[2]: topic.setdefault(c[2][0], []).append(d_(k))
def eb(m):
    ds = subj.get(m.group(1))
    return m.group(0) if not ds else f'<section class="sec" id="{m.group(1)}"{m.group(2)}><p class="eb">CORE CS  |  {runs(ds).upper()}</p>'
sub("cs eyebrows", r'<section class="sec" id="(cs-(?:oop|os|dbms|cn|sd))"([^>]*)><p class="eb">CORE CS  \|  [^<]*</p>', eb, min_=5)
sub("cs weeks", r'<tr><td>\d\d [A-Z][a-z]{2} to \d\d [A-Z][a-z]{2}</td><td><b>([^<]+)</b></td>',
    lambda m: f'<tr><td>{runs(topic[H.unescape(m.group(1))])}</td><td><b>{m.group(1)}</b></td>' if H.unescape(m.group(1)) in topic else m.group(0), min_=10)
SUBJ = {"Object-oriented programming (C++)": "cs-oop", "Operating systems": "cs-os", "DBMS and SQL": "cs-dbms", "Computer networks": "cs-cn", "System design basics": "cs-sd", "Revision and mock vivas": "cs-how"}
sub("cs summary", r'(<b>(Object-oriented programming \(C\+\+\)|Operating systems|DBMS and SQL|Computer networks|System design basics|Revision and mock vivas)</b>(?:</span>)?</td><td>)\d\d [A-Z][a-z]{2} to \d\d [A-Z][a-z]{2}(</td>)',
    lambda m: m.group(1) + runs(subj[SUBJ[m.group(2)]]) + m.group(3), min_=6)

# Cyber: lab number -> dates
lab = {}
for k, v in N.items():
    c = v.get("cy")
    if c: lab.setdefault(c[0], []).append(d_(k))
s = h.index('id="cy-weeks"'); e = h.index('</section>', s); seg = h[s:e]
seg, n = re.subn(r'(<span class="mono" style="color:#[0-9A-Fa-f]{6}">W(\d\d)</span><br><span class="muted">)[^<]*(</span>)',
                 lambda m: m.group(1) + (runs(lab[int(m.group(2))]) if int(m.group(2)) in lab else m.group(0)) + m.group(3), seg)
cnt["cyber rows"] = n; assert n == 20, n
h = h[:s] + seg + h[e:]

# AWS table: rebuild from AWS_WEEKS (exam weeks are null)
AW = json.loads(re.search(r'AWS_WEEKS=(\[.*?\]);', h).group(1)); W0 = dt(2026, 11, 16)
s = h.index('id="aws-plan"'); t0 = h.index('<tbody>', s) + 7; t1 = h.index('</tbody>', t0)
rows = "".join(f'<tr><td><span class="mono" style="color:#9E9E9E">W{i + 1:02d}</span><br><span class="muted">{md(W0 + TD(days=7 * i))} to {md(W0 + TD(days=7 * i + 6))}</span></td><td>{H.escape(t, quote=False)}</td></tr>'
               for i, t in enumerate(AW) if t)
h = h[:t0] + rows + h[t1:]; cnt["aws rows"] = sum(1 for t in AW if t)
h = h.replace("with the exam booked for April.", "with the exam in the week of 19 Apr; weeks 19 and 20 are semester exams.")
h = h.replace("You learn C++ on 5 and 6 Nov.", "You learn C++ on 16 and 17 Nov.")
open(SRC, "w", encoding="utf-8").write(h)
print(cnt)
