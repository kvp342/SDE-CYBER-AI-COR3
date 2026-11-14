"""Path A for the Roadmap: AI becomes a 4-week AI-security project in May, CP-31 becomes a light CP habit,
two checkpoints, and every HFT item moves into one Elite section (opened only by the 31 Mar checkpoint)."""
import json, re, sys, datetime
dt = datetime.date; TD = datetime.timedelta
SRC, OUT = sys.argv[1], sys.argv[2]
h = open(SRC, encoding="utf-8").read()
KB = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT"

def rep(old, new, count=1):
    global h
    n = h.count(old)
    if n != count: raise SystemExit(f"anchor count {n} != {count}: {old[:100]!r}")
    h = h.replace(old, new)

AIP = [  # the 4-week AI-security project, 1 hour a day
 ("Build: how LLMs work, your first API call, a small RAG over your Core CS notes", "Chunk your notes, embed them, retrieve the best chunks and answer with citations. Free tools: Ollama or a free API tier.", "a script that answers 10 questions from your notes, with sources"),
 ("Finish and measure the RAG assistant", "Better chunking and retrieval, a 20-question evaluation set, scores before and after each change.", "a repo with a README and an evaluation table"),
 ("Attack it", "OWASP Top 10 for LLM apps; direct and indirect prompt injection (hide instructions inside a note); Gandalf levels; PortSwigger's LLM labs.", "a write-up of each attack, with what worked and why"),
 ("Defend and ship", "Separate instructions from data, filter outputs, least-privilege tools, re-run every attack; record a 2-minute demo.", "a before/after attack table, a demo video and a resume line"),
]
W0 = dt(2026, 11, 16)
wk = lambda d: (d - W0).days // 7

# ---------- weekly plan ----------
m = re.search(r"var W=", h); dec = json.JSONDecoder(); W, end = dec.raw_decode(h, m.end())
CPB = {12: 800, 13: 800, 14: 800, 15: 900, 16: 900, 17: 900, 20: 1000, 21: 1000, 22: 1000, 23: 1100, 24: 1100, 25: 1100, 26: 1200, 27: 1200}
for i, w in enumerate(W["weeks"]):
    t = []
    for k, v in w["t"]:
        if k in ("AI", "Capstone"): continue
        if k == "CP-31":
            t.append(["CP habit", f"Keeps the Elite door open. CP-31 at rating {CPB.get(i, 1200)}: 2 problems on Tuesday and Thursday. A Codeforces Div 3 or Div 4 round at the weekend, then upsolve one."]); continue
        if k == "Stretch": continue
        if k == "Internship": v = v.replace("It replaces the capstone and most of the sprint", "It replaces most of the sprint")
        t.append([k, v])
    if 24 <= i <= 27:
        n = i - 23; a_, b_, c_ = AIP[n - 1]
        t.append(["AI-security project", f"Week {n} of 4, 1 hour a day: {a_}. {b_} Proof: {c_}."])
    w["t"] = t
    if i == 11: w["ck"].append("Checkpoint 1: Striver core on time, LeetCode Mediums in about 25 minutes")
    if i == 19: w["ck"].append("Checkpoint 2, the HFT gate, 31 Mar: see Elite")
h = h[:m.end()] + json.dumps(W, ensure_ascii=False) + h[end:]

# ---------- day by day ----------
m = re.search(r"var DAYS_D=", h); DD, end = dec.raw_decode(h, m.end())
for k, bl in DD.items():
    d = dt.fromisoformat(k)
    bl[:] = [b for b in bl if not b[0].startswith("AI week")]
    i = wk(d)
    if 24 <= i <= 27 and d.weekday() != 6:
        a_, b_, c_ = AIP[i - 24]
        bl.append([f"AI-security project, week {i - 23} of 4 (1 h)", [a_, "Proof by Sunday: " + c_]])
h = h[:m.end()] + json.dumps(DD, ensure_ascii=False) + h[end:]

# ---------- lanes ----------
def lane(name, body):
    global h
    pat = re.compile(r' \["' + re.escape(name) + r'","",\[\n.*?\]\]\],\n', re.S)
    mm = pat.search(h); assert mm, name
    h = h[:mm.start()] + body + h[mm.end():]
lane("CP", ''' ["CP","",[
  ["CP habit, 800 to 900","2027-02-08","2027-03-21","2 days a week + a weekend round","CP-31 on Tuesday and Thursday, a Codeforces Div 3 or Div 4 round at the weekend. Cheap, and it keeps the Elite door open.","","CP habit"],
  ["CP habit, 1000 to 1200","2027-04-08","2027-05-30","2 days a week + a weekend round","The same rhythm at the next ratings.","","CP habit"],
  ["1500+ and CSES","2027-05-31","2027-07-31","Optional, 1 h","Only if the sprint work is done: harder CP-31 ratings and the matching CSES sections."]]],
 ["Elite","",[
  ["HFT track, only if you pass the 31 Mar checkpoint","2027-04-08","2027-07-25","1 to 1.5 h a day","16 weeks of probability, puzzles, mental maths, contests and low-latency C++. Everything is in the Elite section.","slack","HFT (gated)"]]],
''')
lane("AI", ''' ["AI","",[
  ["AI-security project","2027-05-03","2027-05-30","1 h a day","Four weeks: build a RAG assistant over your notes, attack it with prompt injection, defend it, ship a demo. Your AI and security proof in one project.","","AI-security"]]],
''')
rep('["Internship, if you get one","2027-05-15","2027-07-31","Full time","A summer internship replaces the capstone and most of the sprint.', '["Internship, if you get one","2027-05-15","2027-07-31","Full time","A summer internship replaces most of the sprint.')

# ---------- marks and milestones ----------
rep(' ["Paper submitted","2027-03-21",', ' ["HFT gate","2027-03-31","Checkpoint 2: Codeforces 1400+ or a LeetCode contest rating of 1800+ opens the Elite HFT track. Otherwise stay on Path A.",""],\n ["Paper submitted","2027-03-21",')
rep('["Striver core done","2027-01-30","All 359 Easy and Medium problems solved. End of February is the latest.",""]', '["Striver core done","2027-01-30","Checkpoint 1: all 359 Easy and Medium problems solved, Mediums in about 25 minutes. End of February is the latest.",""]')
rep(' ["m07","Readiness check 2 filled in","2027-03-15",""],', ' ["m18","Checkpoint 1: Striver core on time and LeetCode Mediums in about 25 minutes","2027-01-30","2027-02-28"],\n ["m07","Readiness check 2 filled in","2027-03-15",""],\n ["m19","Checkpoint 2, the HFT gate: Codeforces 1400+ or LeetCode contest 1800+ (opens Elite)","2027-03-31",""],')
rep('["m09","AI projects on GitHub: RAG app, AI feature, security writeups, capstone","2027-05-30","2027-06-30"]', '["m09","AI-security project on GitHub: RAG assistant, attack write-up, defences, demo video","2027-05-30","2027-06-30"]')

# ---------- phases ----------
rep('{t:"Build",a:"2027-02-08",b:"2027-03-21",h:"About 8 h a day",', '{t:"Build",a:"2027-02-08",b:"2027-03-21",h:"About 6 h a day",')
rep('now:"One Hard problem a day, 2 hours of AI, CP-31, cyber at a full hour, AWS exam prep, and a mock interview every week.",',
    'now:"One Hard problem a day, cyber at a full hour (your side track), system design, AWS exam prep, a light CP habit and a mock interview every week. No AI yet: that is May.",')
rep('p:["Hard pass, part 1: 42 Hard problems, one a day","AI weeks 1 to 6: LLM basics through to a shipped, tested AI feature","CP-31 from rating 800 to 1000 · cyber labs 9 to 14 · system design","AWS exam prep · internship applications · TenantWall paper submitted by 21 Mar"],',
    'p:["Hard pass, part 1: 42 Hard problems, one a day","Cyber labs 9 to 14 at a full hour · system design","CP habit: CP-31 on Tuesday and Thursday, a Codeforces round at the weekend","AWS exam prep · internship applications · TenantWall paper submitted by 21 Mar","Checkpoint 1 on 30 Jan · checkpoint 2, the HFT gate, on 31 Mar (see Elite)"],')
rep('{t:"Finish and certify",a:"2027-04-08",b:"2027-05-30",h:"About 8 h a day",', '{t:"Finish and certify",a:"2027-04-08",b:"2027-05-30",h:"About 6 to 7 h a day",')
rep('now:"Finish the Hard pass and the AI track, sit the AWS exam in the week of 19 Apr, then build the capstone.",',
    'now:"Finish the Hard pass, sit the AWS exam in the week of 19 Apr, then the 4-week AI-security project in May.",')
rep('p:["Hard pass, part 2: the other 42 Hard problems, done by 19 May","AI weeks 7 to 12: securing LLM apps, then the intrusion-detection capstone","AWS: second practice exam, then SAA-C03 in the week of 19 Apr","CP-31 from 1100 to 1400 · cyber labs 15 to 20, then the binary taster","With a summer internship offer: it starts around mid-May and replaces the capstone"],',
    'p:["Hard pass, part 2: the other 42 Hard problems, done by 19 May","AWS: second practice exam, then SAA-C03 in the week of 19 Apr","Cyber labs 15 to 20, then the binary taster · CP habit at 1000 to 1200","AI-security project, 3 to 30 May, 1 h a day: build a RAG assistant, attack it, defend it","Passed the HFT gate? The Elite track runs alongside, 1 to 1.5 h a day","With a summer internship offer: it starts around mid-May"],')
rep('d:"you are certified, the Hard pass is done and the capstone has a README, a diagram and real numbers."}', 'd:"you are certified, the Hard pass is done and the AI-security project has a README, an attack write-up and a demo."}')
rep('"Optional: harder CP-31 and CSES, and probability for HFT"]', '"Optional: harder CP-31 and CSES · Elite: the HFT track, only if you passed the gate"]')

# ---------- day shapes ----------
rep('["Revision","Re-solve what is due today.",.5],["Hard pass","One Hard problem, attempted first.",1.25],["LeetCode","One problem; the contest on Sundays.",.5],["CP-31","2 problems at this fortnight\'s rating.",1],\n   ["AI","Build or lab work, then commit.",2],["Cyber","One lab.",1],',
    '["Revision","Re-solve what is due today.",.5],["Hard pass","One Hard problem, attempted first.",1.25],["LeetCode","One problem; the contest on Sundays.",.5],["CP habit","Tuesday and Thursday: 2 CP-31 problems. Weekend: a Codeforces round.",.4],\n   ["Cyber","One lab, your side track.",1],')
rep('note:"One mock interview every week. Five internship applications a week until the end of April."}', 'note:"One mock interview every week. Five internship applications a week until the end of April. In May, add the AI-security project: 1 hour a day."}')

# ---------- rules ----------
s = h.index('id="rules"'); e = h.index('</section>', s); R = h[s:e]
R2 = R.replace("HFT preparation", "The Elite HFT track, if you opened it").replace("CP-31", "The CP habit", 1).replace("AI, down to 1 hour", "The AI-security project, down to 2 weeks")
R2 = R2.replace("Move the end of Striver core to the end of February and start AI at 1 hour a day.", "Move the end of Striver core, and checkpoint 1, to the end of February.")
R2 = R2.replace("CP-31 waits until it is, and AI runs at 1 hour.", "The CP habit waits until it is.")
assert R2 != R; h = h[:s] + R2 + h[e:]

# ---------- targets ----------
rep('<tr><td>SDE at an HFT firm</td><td>Trading firms</td><td>Hard competitive programming, C++ depth, OS, networks, probability</td><td><span class="pill warn">Stretch</span></td></tr>',
    '<tr><td>SDE at an HFT firm (<a href="#elite">Elite</a>, gated)</td><td>Trading firms</td><td>Hard competitive programming, C++ depth, OS, networks, probability</td><td><span class="pill warn">Stretch</span></td></tr>')
rep('CP-31 from 800 to 1400, a Codeforces rating</li>', 'the CP habit from 800 to 1200, a Codeforces rating</li>')
rep('<li><b>AI:</b> a RAG app, an AI feature in your backend project, 4 AI-security writeups, an intrusion-detection capstone</li>', '<li><b>AI:</b> a RAG assistant you attacked and defended, with an OWASP LLM write-up and a demo</li>')
rep('HFT interviews are possible.', 'If you opened the Elite track, HFT interviews are possible.')

rep('Stretch: SDE at an HFT firm</dd>', 'Elite, gated: SDE at an HFT firm (<a href="#elite">see Elite</a>)</dd>')
rep("Gandalf and PortSwigger's LLM labs for security</td><td>From 4 Jan</td></tr>", "Gandalf and PortSwigger's LLM labs for security</td><td>May: the AI-security project</td></tr>")
rep("<tr><td>Probability (stretch)</td><td>Harvard Stat 110 with Blitzstein's book, Brainstellar, Zetamac</td><td>April to July</td></tr>", "<tr><td>Probability (<a href=\"#elite\">Elite</a> only)</td><td>Harvard Stat 110 with Blitzstein's book, Brainstellar, Zetamac</td><td>Only if you pass the 31 Mar gate</td></tr>")

# ---------- Elite section ----------
PH = [("W01–W04", "5 Apr to 2 May", "Counting and basic probability", "Permutations and combinations, inclusion–exclusion, conditional probability, Bayes' rule. Blitzstein and Hwang chapters 1–2 (free) with Stat 110 lectures. 10 easy Brainstellar puzzles a week.", "40 solved problems, each with its idea in one line"),
      ("W05–W08", "3 May to 30 May", "Random variables and expected value", "Linearity of expectation, indicator variables, binomial, geometric and Poisson, variance. Dice, coin and card games: what is the fair price? Mosteller's Fifty Challenging Problems, first 20.", "20 expected-value problems without looking at answers"),
      ("W09–W12", "31 May to 27 Jun", "Interview probability and puzzles", "The probability and brain-teaser chapters of Zhou's green book; Markov chains and random walks (gambler's ruin); Brainstellar medium puzzles.", "A sheet of 30 patterns: symmetry, recursion on states, conditioning on the first step"),
      ("W13–W16", "28 Jun to 25 Jul", "Timed practice and low-latency C++", "Timed puzzle sets, Heard on the Street, market-making games for trader roles. For SDE roles: move semantics, memory layout, cache behaviour, lock-free basics.", "Two timed mock tests a week, scored and logged")]
rows = "".join(f'<tr><td class="mono">{a}<br>{b}</td><td><b>{c}</b></td><td>{d}</td><td>{e}</td></tr>' for a, b, c, d, e in PH)
ELITE = f'''<section class="sec" id="elite">
  <header><p class="label">Elite · opens only if you pass the 31 March checkpoint</p><h2>Elite: the HFT track</h2>
  <p>This is the only place HFT appears in the plan. Everything else is Path A: an SDE profile with security and cloud depth. HFT firms (Tower Research, Graviton, Quadeye, Optiver and others) hire very few freshers, mostly from strong competitive-programming profiles, so the track opens only if your results say it is realistic.</p></header>
  <div class="tw"><table>
    <thead><tr><th>Checkpoint</th><th>Date</th><th>Pass if</th><th>Then</th></tr></thead>
    <tbody>
      <tr><td>1</td><td class="mono">30 Jan 2027</td><td>Striver core finished on time; LeetCode Mediums in about 25 minutes</td><td>Keep the CP habit from 8 Feb. Missed it? Finish Striver first; the gate stays at 31 Mar.</td></tr>
      <tr><td>2, the gate</td><td class="mono">31 Mar 2027</td><td>A Codeforces rating of 1400+ <b>or</b> a LeetCode contest rating of 1800+</td><td><b>Pass:</b> open this track from 8 Apr. <b>Miss:</b> stay on Path A and stop thinking about HFT until placements; the contest practice still makes every online test easier.</td></tr>
    </tbody></table></div>
  <div class="two">
    <div class="plain-wrap" style="display:grid;gap:12px;align-content:start">
      <h3>What changes if you open it</h3>
      <ul class="plain">
        <li><b>Add:</b> 1 to 1.5 hours a day of the HFT track below, 8 Apr to 25 Jul</li>
        <li><b>CP habit becomes daily:</b> 2 CP-31 problems a day, a Codeforces Div 2 round every week, aim for 1600+ by July</li>
        <li><b>Cyber drops to 3 days a week:</b> keep the binary taster, it pairs with low-latency C++</li>
        <li><b>AI-security project shrinks to 2 weeks:</b> build, then attack</li>
        <li><b>Never cut:</b> the Hard pass, Core CS, the AWS exam, mock interviews</li>
      </ul>
    </div>
    <div style="display:grid;gap:12px;align-content:start;min-width:0">
      <h3>Which HFT role fits you</h3>
      <div class="tw"><table>
        <thead><tr><th>Role</th><th>What they test</th><th>Your fit</th></tr></thead>
        <tbody>
          <tr><td>Software engineer (low-latency C++)</td><td>Hard coding tests, C++ depth, OS, networks</td><td><span class="pill ok">Best fit</span></td></tr>
          <tr><td>Quant trader</td><td>Probability, mental maths speed, market-making games</td><td><span class="pill">Possible</span></td></tr>
          <tr><td>Quant researcher</td><td>Deeper probability, statistics, research</td><td><span class="pill warn">Stretch</span></td></tr>
        </tbody></table></div>
    </div>
  </div>
  <h3>The 16-week plan, 1 to 1.5 hours a day</h3>
  <div class="tw"><table>
    <thead><tr><th>Weeks</th><th>Focus</th><th>Inside the hour</th><th>Proof of work</th></tr></thead>
    <tbody>{rows}</tbody></table></div>
  <h3>Every day while the track is open</h3>
  <ul class="plain">
    <li>10 minutes of mental maths on <a href="https://arithmetic.zetamac.com">Zetamac</a>: aim for 40+, then 50+</li>
    <li>One <a href="https://codeforces.com">Codeforces</a> Div 2 round a week, then upsolve one problem</li>
  </ul>
  <h3>Learn from</h3>
  <ul class="plain">
    <li>Free: <a href="https://projects.iq.harvard.edu/stat110">Harvard Stat 110 and the Blitzstein–Hwang book</a>, <a href="https://www.brainstellar.com">Brainstellar</a>, <a href="https://cses.fi/problemset/">CSES</a>, the Knowledge Base pages on <a href="{KB}#probability">probability</a>, <a href="{KB}#cp">contests</a> and <a href="{KB}#vtable">the vtable</a></li>
    <li>Books: Zhou's <i>A Practical Guide to Quantitative Finance Interviews</i>, Mosteller's <i>Fifty Challenging Problems in Probability</i>, Crack's <i>Heard on the Street</i></li>
  </ul>
</section>

'''
rep('<section class="sec" id="rules">', ELITE + '<section class="sec" id="rules">')
rep('<a href="#offcampus">Off-campus</a>', '<a href="#offcampus">Off-campus</a><a href="#elite">Elite</a>')
rep('<a href="#toolkit">Toolkit</a>', '<a href="#toolkit">Toolkit</a><a href="https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT" target="_blank" rel="noopener">Knowledge ↗</a><a href="https://docs.google.com/spreadsheets/d/1JhZAMJmKocsnES-4Rhn-gSnhuJA9XoSHccqPZWZwREY/edit" target="_blank" rel="noopener">Tracker ↗</a>')
open(OUT, "w", encoding="utf-8").write(h)
print("roadmap Path A written:", OUT, len(h))
