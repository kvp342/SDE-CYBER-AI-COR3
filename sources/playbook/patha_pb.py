"""Path A for the Playbook (run after repace.py): AI becomes a 4-week AI-security project in May, CP31 becomes
a light CP habit, two checkpoints, and Part 11 becomes the Elite HFT track opened only by the 31 Mar gate."""
import json, re, sys, datetime
dt = datetime.date; TD = datetime.timedelta
SRC, OUT = sys.argv[1], sys.argv[2]
h = open(SRC, encoding="utf-8").read()

def rep(old, new, count=1):
    global h
    n = h.count(old)
    if n != count: raise SystemExit(f"anchor count {n} != {count}: {old[:110]!r}")
    h = h.replace(old, new)
def section(sid):  # (start, end) of <section ... id="sid"> ... </section>
    s = h.index(f'<section class="sec" id="{sid}"'); e = h.index('</section>', s) + len('</section>'); return s, e

AIP = [("Build a RAG assistant over your notes", "How LLMs work, your first API call, then chunk, embed and retrieve your Core CS notes and answer with citations. Free tools: Ollama or a free API tier.", "a script that answers 10 questions from your notes, with sources"),
       ("Finish and measure it", "Better chunking and retrieval, a 20-question evaluation set, scores before and after each change.", "a repo with a README and an evaluation table"),
       ("Attack it", "OWASP Top 10 for LLM apps; direct and indirect prompt injection (hide instructions inside a note); Gandalf levels; PortSwigger's LLM labs.", "a write-up of each attack, what worked and why"),
       ("Defend it and ship", "Separate instructions from data, filter outputs, least-privilege tools, re-run every attack, record a 2-minute demo.", "a before/after attack table, a demo video and a resume line")]

# ---------- daily data: AI only in May (4 weeks, Monday to Saturday) ----------
s = h.index("\nvar D=") + 7; e = h.index("};", s) + 1; D = json.loads(h[s:e])
for v in D.values(): v.pop("ai", None)
d = dt(2027, 5, 3)
while d <= dt(2027, 5, 30):
    if d.weekday() != 6:
        n = (d - dt(2027, 5, 3)).days // 7 + 1; t, desc, proof = AIP[n - 1]
        D.setdefault(d.isoformat(), {"due": []})["ai"] = [n, t, desc, proof, "#B0B0B0"]
    d += TD(days=1)
h = h[:s] + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + h[e:]

# ---------- Today cards ----------
rep("""h='<div class="big" style="color:'+e.ai[4]+'">Week '+e.ai[0]+': '+esc(e.ai[1])+'</div>""", """h='<div class="big" style="color:'+e.ai[4]+'">Week '+e.ai[0]+' of 4: '+esc(e.ai[1])+'</div>""")
rep('g+=card("ai","AI · 2 H","#B0B0B0",h,day);', 'g+=card("ai","AI-SECURITY · 1 H","#B0B0B0",h,day);')
rep('if(awsOn(day))n.push("aws");if(day>="2026-12-14"&&day<"2027-03-22")n.push("cp");',
    'if(awsOn(day))n.push("aws");if(cpOn(day))n.push("cp");')
rep('function need(day){', 'function cpWin(day){return (day>="2027-02-08"&&day<="2027-03-21")||(day>="2027-04-08"&&day<="2027-05-30")}\n'
    'function cpOn(day){if(!cpWin(day))return false;var g=new Date(Date.UTC(+day.slice(0,4),+day.slice(5,7)-1,+day.slice(8,10))).getUTCDay();return g===2||g===4}\n'
    'function need(day){', 1)
rep('var CP_BANDS=[["2026-12-14",800],["2026-12-29",900],["2027-01-13",1000],["2027-01-28",1100],["2027-02-12",1200],["2027-02-27",1300],["2027-03-14",1400]];',
    'var CP_BANDS=[["2027-02-08",800],["2027-03-01",900],["2027-04-08",1000],["2027-04-29",1100],["2027-05-17",1200]];')
old_cp = h[h.index('// CP31, from 14 Dec'): h.index('g+=card("cp","CP31 · 1 H","#CFCFCF",h,day);}') + len('g+=card("cp","CP31 · 1 H","#CFCFCF",h,day);}')]
h = h.replace(old_cp, """// CP habit (Path A): Tuesday and Thursday, plus a weekend round, 8 Feb to 21 Mar and 8 Apr to 30 May
  if(cpWin(day)){var wd=d.getDay();
    h=cpOn(day)?'<div class="big">'+cpBand(day)+'-rated problems</div><p>2 problems, oldest unsolved first. 30 minutes each at most, then read the editorial.</p>':
      (wd%6===0?'<div class="big">Weekend round</div><p>If a Codeforces Div 3 or Div 4 round is on, play it and upsolve one problem.</p>':'<p class="muted">Not today. The CP habit is Tuesday, Thursday and a weekend round.</p>');
    h+='<p><a href="#cp31">CP habit</a> · keeps the <a href="#p11">Elite</a> door open</p>';
    g+=card("cp","CP HABIT",'#CFCFCF',h,day);}""")

# ---------- Part 00: the big picture ----------
s, e = section("big-picture")
BIG = '''<section class="sec" id="big-picture" style="--c:#FFFFFF"><p class="eb">PART 00  |  THE BIG PICTURE</p><h2>Where this plan takes you</h2><p><b>Positioning: an SDE with cloud-security depth (Path A).</b> Main target: SDE at product companies in final placements (Aug to Dec 2027). Strong second: cloud, DevSecOps or AppSec roles, using TenantWall, AWS and the cyber track. Elite, only through the 31 March checkpoint: SDE at an HFT firm (<a href="#p11">Part 11</a>).</p><div class="tw"><table class=""><thead><tr><th>When</th><th>Main focus</th><th>Daily</th></tr></thead><tbody><tr><td>16 to 17 Nov</td><td>C++ and STL, gate test</td><td>Full days</td></tr><tr><td>18 Nov to 30 Jan</td><td><b>DSA heavy</b>: Striver 5 to 6 a day, LeetCode on the same topic · OOP, OS, DBMS, networks · cyber 30 min · AWS · TenantWall on Saturdays to 12 Dec</td><td>About 8.5 h</td></tr><tr><td>31 Jan to 7 Feb</td><td>Redo every H and F problem · <b>checkpoint 1</b> on 30 Jan</td><td>About 6 h</td></tr><tr><td>8 Feb to 21 Mar</td><td>Hard pass · <b>cyber 1 h</b> (your side track) · system design · AWS exam prep · CP habit · paper submitted · no AI yet</td><td>About 6 h</td></tr><tr><td>22 Mar to 7 Apr</td><td>Semester exams: minimum day only · <b>checkpoint 2, the HFT gate</b>, on 31 Mar</td><td>Minimum</td></tr><tr><td>8 Apr to 30 May</td><td>Hard pass 2 · AWS exam in the week of 19 Apr · cyber labs and the binary taster · <b>AI-security project</b> in May · the Elite track only if you passed the gate</td><td>About 6 to 7 h</td></tr><tr><td>Jun to Jul 2027</td><td>Placement sprint: revise Striver, timed tests, weekly mock interviews</td><td>Full days</td></tr><tr><td>Aug to Dec 2027</td><td><b>Final placements</b>, with off-campus applications alongside</td><td>—</td></tr><tr><td>Jan to Jun 2028</td><td>Final-year project; keep applying if there is no offer yet</td><td>—</td></tr></tbody></table></div><h3>Checkpoints</h3><ul class="checks"><li>17 Nov: gate test 4 of 5</li><li>12 Dec: Striver Step 6 reached · AWS weeks 1 to 4 · TenantWall changes done</li><li>20 Dec: readiness check 1</li><li>17 Jan: AWS course and its practice exam done</li><li>30 Jan: <b>checkpoint 1</b>, Striver core done and LeetCode Mediums in about 25 minutes</li><li>15 Mar: readiness check 2 · Hard pass part 1 about 70%</li><li>21 Mar: paper submitted · two AWS practice exams at 80%+</li><li>31 Mar: <b>checkpoint 2, the HFT gate</b>, Codeforces 1400+ or LeetCode contest 1800+ (<a href="#hft-gate">details</a>)</li><li>Week of 19 Apr: AWS certification</li><li>30 May: AI-security project shipped · Hard pass done</li></ul><h3>When time is short, cut in this order</h3><ol><li>The Elite HFT track, if you opened it</li><li>The CP habit</li><li>The AI-security project, down to 2 weeks</li><li>Cyber down to Sundays only</li></ol><p><b>Never cut</b> DSA, revision or Core CS. On a bad day do the minimum day, never zero.</p><aside class="note" style="--c:#8F8F8F"><b>The biggest risk</b><p>Not talent but restarts, and burnout from running too many tracks at once. That is why AI waits until May and HFT waits behind a checkpoint. Check your streak every night.</p></aside></section>'''
h = h[:s] + BIG + h[e:]

# ---------- Part 03: the CP habit ----------
s, e = section("cp31")
CP = '''<section class="sec" id="cp31" style="--c:#CFCFCF"><p class="eb">PART 03  |  CP HABIT, FROM 8 FEB</p><h2>The CP habit (CP-31 sheet)</h2><p>The CP-31 sheet (search "CP-31 sheet") groups Codeforces problems by rating, about 31 per rating. On Path A it is a light habit, not a daily track: 2 problems on Tuesday and Thursday, plus a Codeforces round at the weekend. It builds the speed online tests reward, and your rating is the evidence for the 31 March checkpoint that opens the <a href="#p11">Elite</a> track.</p><div class="tw"><table class=""><thead><tr><th>Rating</th><th>Dates</th></tr></thead><tbody><tr><td><span class="mono">800</span></td><td>8 Feb to 28 Feb</td></tr><tr><td><span class="mono">900</span></td><td>1 Mar to 21 Mar</td></tr><tr><td><span class="mono">1000</span></td><td>8 Apr to 28 Apr</td></tr><tr><td><span class="mono">1100</span></td><td>29 Apr to 16 May</td></tr><tr><td><span class="mono">1200</span></td><td>17 May to 30 May</td></tr></tbody></table></div><ul class="checks"><li>Tuesday and Thursday: 2 problems, oldest unsolved first</li><li>30 minutes each at most, then read the editorial and code it yourself</li><li>Weekends: a Codeforces Div 3 or Div 4 round when one is on, then upsolve one problem</li><li>The LeetCode weekly contest stays every Sunday from November: it counts toward the checkpoint too</li></ul><aside class="note" style="--c:#CFCFCF"><b>Target</b><p>800 to 1200 by 30 May. A Codeforces rating of 1400+ or a LeetCode contest rating of 1800+ by 31 Mar opens the Elite track.</p></aside></section>'''
h = h[:s] + CP + h[e:]

# ---------- Part 10: the AI-security project ----------
s = h.index('<div class="part" id="p10"'); e = h.index('<div class="part" id="p11"')
rows = "".join(f'<tr><td><span class="mono" style="color:#B0B0B0">W{i + 1}</span><br><span class="muted">{a}</span></td><td><b>{t}</b><br>{x}</td><td>{p}</td></tr>'
               for i, ((t, x, p), a) in enumerate(zip(AIP, ["3 to 9 May", "10 to 16 May", "17 to 23 May", "24 to 30 May"])))
P10 = f'''<div class="part" id="p10" style="--c:#B0B0B0"><header class="ph"><span class="pn">10</span><div><p class="eb">PART 10  |  MAY 2027, 1 HOUR A DAY</p><h1>AI-security project</h1><p>Four weeks in May: build a RAG assistant over your notes, attack it, defend it, ship it. Your AI skill and your security edge in one project.</p></div></header><section class="sec" id="ai-hour" style="--c:#B0B0B0"><p class="eb">PART 10  |  WHY ONE PROJECT</p><h2>One project instead of a long AI course</h2><p>A two-hour daily AI track from February would have run beside the Hard pass, cyber, CP, AWS exam prep, the paper and college: too many tracks at once, which is how burnout starts. One focused project in May gives you what interviewers actually ask about (how retrieval works, how you evaluated it, how you attacked and secured it) and a demo you can show.</p><aside class="note" style="--c:#B0B0B0"><b>One hour, then stop</b><p>Start a timer, stop when it rings, write notes. Use Sunday to finish the week's proof of work.</p></aside><aside class="note" style="--c:#E8E8E8"><b>Free all the way</b><p>Local models with Ollama, free API tiers, free labs. Keep API keys in environment variables and never push them to GitHub.</p></aside><aside class="note" style="--c:#8F8F8F"><b>Only attack what you are allowed to</b><p>Practise prompt injection only on Gandalf, PortSwigger's LLM labs and the app you built yourself.</p></aside></section><section class="sec" id="ai-weeks" style="--c:#B0B0B0"><p class="eb">PART 10  |  THE 4 WEEKS</p><h2>The 4 weeks</h2><div class="tw"><table class=""><thead><tr><th>Week</th><th>Build</th><th>Proof of work</th></tr></thead><tbody>{rows}</tbody></table></div></section><section class="sec" id="ai-goal" style="--c:#B0B0B0"><p class="eb">PART 10  |  BY 30 MAY</p><h2>What you will have by 30 May</h2><ul class="checks"><li>A RAG assistant on GitHub with a README, an architecture diagram and an evaluation table</li><li>An attack write-up mapped to the OWASP Top 10 for LLM applications</li><li>A before/after table showing which defences stopped which attacks</li><li>A 2-minute demo video</li><li>A resume line: <i>Built a RAG assistant over 200 pages of notes (80% answer accuracy on a 20-question eval) and red-teamed it with 12 prompt-injection attacks, cutting successful attacks from 9 to 1 with input separation and output filtering.</i> Replace the numbers with your real ones.</li></ul><aside class="note" style="--c:#B0B0B0"><b>Interview story</b><p>Problem, design, how you measured it, how you broke it, how you fixed it. That is a complete STAR answer for SDE, security and AI interviewers alike.</p></aside></section></div>'''
h = h[:s] + P10 + h[e:]

# ---------- Part 11: Elite, the HFT track ----------
rep('<p class="eb">PART 11  |  LATER: APRIL TO JULY 2027</p><h1>HFT track: maths and probability</h1><p>For a chance at high-frequency trading firms. Not now: it starts after this plan ends, and nothing here appears on Today.</p></div></header>',
    '<p class="eb">PART 11  |  ELITE · OPENS ONLY IF YOU PASS THE 31 MAR CHECKPOINT</p><h1>Elite: the HFT track</h1><p>The only place HFT appears in your plan. It opens on 8 Apr only if you pass the 31 March checkpoint, and nothing here appears on Today.</p></div></header>'
    '<section class="sec" id="hft-gate" style="--c:#8C8C8C"><p class="eb">ELITE  |  THE GATE</p><h2>Two checkpoints decide it</h2><div class="tw"><table class=""><thead><tr><th>Checkpoint</th><th>Date</th><th>Pass if</th><th>Then</th></tr></thead><tbody>'
    '<tr><td>1</td><td><span class="mono">30 Jan</span></td><td>Striver core done on time; LeetCode Mediums in about 25 minutes</td><td>Keep the CP habit from 8 Feb. Missed it? Finish Striver first; the gate stays at 31 Mar.</td></tr>'
    '<tr><td>2, the gate</td><td><span class="mono">31 Mar</span></td><td>Codeforces rating 1400+ <b>or</b> LeetCode contest rating 1800+</td><td><b>Pass:</b> open this track on 8 Apr. <b>Miss:</b> stay on Path A and leave HFT until placements. The contest practice still makes every online test easier.</td></tr></tbody></table></div>'
    '<h3>What changes if you open it</h3><ul class="checks"><li>Add 1 to 1.5 hours a day of the 16-week plan below, 8 Apr to 25 Jul</li><li>The CP habit becomes daily: 2 problems a day and a Codeforces Div 2 round every week, aiming for 1600+ by July</li><li>Cyber drops to 3 days a week; keep the binary taster, it pairs with low-latency C++</li><li>The AI-security project shrinks to 2 weeks: build, then attack</li><li>Never cut the Hard pass, Core CS, the AWS exam or mock interviews</li></ul></section>')
rep('<p class="eb">PART 11  |  WHY AND WHICH ROLE</p>', '<p class="eb">ELITE  |  WHY AND WHICH ROLE</p>')
rep('<p class="eb">HFT  |  16 WEEKS, 1 TO 1.5 HOURS A DAY</p>', '<p class="eb">ELITE  |  16 WEEKS, 1 TO 1.5 HOURS A DAY, ONLY IF THE GATE IS OPEN</p>')
rep('<p class="eb">HFT  |  TOPIC CHECKLIST</p>', '<p class="eb">ELITE  |  TOPIC CHECKLIST</p>')
rep('<h3>Before April: keep the doors open</h3><ul class="checks"><li>Keep CP31 going and play Codeforces Div 2 rounds; aim for a 1600+ rating by the summer</li>',
    '<h3>Before April: keep the door open</h3><ul class="checks"><li>Keep the CP habit and the Sunday LeetCode contest; they are the evidence for the gate</li>')

# ---------- index cards and the sidebar ----------
rep('<b>AI track</b><ul><li>The AI hour</li><li>The 12-week plan</li><li>What you will have by March</li></ul>', '<b>AI-security project</b><ul><li>Why one project</li><li>The 4 weeks</li><li>What you will have by 30 May</li></ul>')
rep('<b>HFT track (later)</b><ul><li>What HFT firms test</li><li>The 16-week plan</li><li>Topics to cover</li></ul>', '<b>Elite: HFT track</b><ul><li>The gate</li><li>What HFT firms test</li><li>The 16-week plan</li><li>Topics to cover</li></ul>')
rep('<span class="mono">10</span> AI track</summary><ol><li><a href="#ai-hour">The AI hour</a></li><li><a href="#ai-weeks">The 12-week plan</a></li><li><a href="#ai-goal">What you will have by March</a></li></ol>',
    '<span class="mono">10</span> AI-security project</summary><ol><li><a href="#ai-hour">Why one project</a></li><li><a href="#ai-weeks">The 4 weeks</a></li><li><a href="#ai-goal">What you will have by 30 May</a></li></ol>', 2)
rep('<span class="mono">11</span> HFT track (later)</summary><ol><li><a href="#hft-why">What HFT firms test</a></li>',
    '<span class="mono">11</span> Elite: HFT track</summary><ol><li><a href="#hft-gate">The gate</a></li><li><a href="#hft-why">What HFT firms test</a></li>', 2)
rep('CP31 from mid-December, a two-hour AI track from January, a later maths and probability track for HFT roles,',
    'a light CP habit from February, a 4-week AI-security project in May, an Elite HFT track opened only by a checkpoint,')

# ---------- step headers: dates from the new schedule, and a link to each step's concept page ----------
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT"
TRK = "https://docs.google.com/spreadsheets/d/1JhZAMJmKocsnES-4Rhn-gSnhuJA9XoSHccqPZWZwREY/edit"
STEPKB = {1: "cpp-stl", 2: "complexity", 3: "two-pointers", 4: "binary-search", 5: "hashing", 6: "linked-list", 7: "recursion", 8: "bit-manipulation",
          9: "stack-queue", 10: "sliding-window", 11: "heap", 12: "greedy", 13: "trees", 14: "bst", 15: "bfs", 16: "dp", 17: "trie", 18: "string-algos"}
ss = h.index("\nvar D=") + 7; ee = h.index("};", ss) + 1; DN = json.loads(h[ss:ee])
span = {}
for k, v in DN.items():
    for x in v.get("due", []):
        if x[2] != "H": span.setdefault(x[0], []).append(k)
fmt = lambda k: dt.fromisoformat(k).strftime("%d %b").upper().lstrip("0")
def eyebrow(m):
    n = int(m.group(1)); ks = sorted(span.get(n, []))
    return m.group(0) if not ks else f'<p class="eb">STEP {m.group(1)}  |  {fmt(ks[0])}{" TO " + fmt(ks[-1]) if ks[-1] != ks[0] else ""}  |'
h, cnt = re.subn(r'<p class="eb">STEP (\d\d)  \|  ([^|<]+?)  \|', eyebrow, h)
assert cnt >= 18, cnt
def kbl(m):
    n = int(m.group(1))
    return m.group(0) + f'<p class="muted">Concepts first: <a href="{KB}#{STEPKB[n]}" target="_blank" rel="noopener">Knowledge Base page</a> · worked solutions in its Problems section.</p>'
h, cnt2 = re.subn(r'(?<=<section class="sec" id="step-)(\d+)("[^>]*>(?:(?!</h2>).)*?</h2>)', lambda m: m.group(1) + m.group(2) + f'<p class="muted">Concepts first: <a href="{KB}#{STEPKB[int(m.group(1))]}" target="_blank" rel="noopener">Knowledge Base page</a> · worked solutions in its Problems section.</p>', h, flags=re.S)
assert cnt2 == 18, cnt2
rep('<a class="sl" href="#index">Index</a>', f'<a class="sl" href="#index">Index</a><a class="sl" href="{KB}" target="_blank" rel="noopener">Knowledge Base ↗</a><a class="sl" href="{TRK}" target="_blank" rel="noopener">Revision tracker ↗</a>')
rep('<a href="#logs">Logs</a></nav>', f'<a href="#logs">Logs</a><a href="{KB}" target="_blank" rel="noopener">Knowledge</a></nav>')

h = h.replace('Five tracks, one route', 'Every track, one route')
open(OUT, "w", encoding="utf-8").write(h)
print("playbook Path A written", len(h))
