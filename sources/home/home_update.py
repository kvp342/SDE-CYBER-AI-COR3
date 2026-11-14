import sys, re
KBW = "https://claude.ai/artifact/McuS723LTAb16Q6SpdUsAT"; TRK = "https://docs.google.com/spreadsheets/d/1JhZAMJmKocsnES-4Rhn-gSnhuJA9XoSHccqPZWZwREY/edit"; CHW = "https://claude.ai/artifact/8Gu8a2jRrGd6wGqvA2VwY2"
def update(path, kb, cheat):
    h = open(path, encoding="utf-8").read()
    def rep(a, b):
        nonlocal h
        assert h.count(a) == 1, (path, a[:70]); h = h.replace(a, b)
    h = h.replace('<p class="muted">The daily playbook and the full roadmap, in one app that works offline.</p>', '<p class="muted">Your daily playbook and your full roadmap, from one page.</p>')
    tip = re.search(r'<p class="tip">.*?</p>', h).group(0)
    h = h.replace(tip, '<p class="tip">Both pages open in a new tab. Back up your ticks from the playbook, Part 09, before your Claude plan changes, and keep the offline copies as a fallback.</p>')
    rep('<p class="muted">Your daily playbook and your full roadmap, from one page.</p>', '<p class="muted">Path A: SDE with security and cloud depth. Your playbook, roadmap, knowledge base, tracker and cheat sheet, from one page.</p>')
    rep('Lessons for C++, Striver, Core CS, cyber, AWS and AI. Five themes: Space, Café, Night café, Garden and Professional.</p>', 'Lessons for C++, Striver, Core CS, cyber, AWS, the AI-security project and the Elite HFT track. Five themes.</p>')
    rep('the intensive track, how to learn faster, and the off-campus system.</p>', 'the two checkpoints, the Elite HFT track, how to learn faster, and the off-campus system.</p>')
    door = f'''
    <a class="door" href="{kb}">
      <p class="label">When stuck</p>
      <h2>Knowledge Base</h2>
      <p class="muted">147 pages: every concept in depth, 43 tested worked solutions, model answers for Core CS and security, and the Elite pages.</p>
      <span class="go">Look something up</span>
    </a>
    <a class="door" href="{TRK}">
      <p class="label">Every morning</p>
      <h2>Revision tracker</h2>
      <p class="muted">Google Sheet. Log each problem; the 1-3-7-21 revision dates fill in and the Due today tab lists what to re-solve.</p>
      <span class="go">Open the tracker</span>
    </a>
    <a class="door" href="{cheat}">
      <p class="label">Before a test</p>
      <h2>Cheat sheet</h2>
      <p class="muted">Rules, complexity, STL, pattern triggers, templates, DP, Core CS, SQL, security, AWS and interview answers.</p>
      <span class="go">Open the cheat sheet</span>
    </a>
  </nav>'''
    i = h.index('<span class="go">Open the roadmap</span>'); j = h.index('</nav>', i)
    h = h[:j].rstrip() + door + h[j + len('</nav>'):]
    old = h[h.index('var P=['): h.index('var cur=P[0]')]
    new = '''var P=[["2026-11-07","Village week","On your phone, an hour a day: Learn C++ at 2×, Time complexity and the Patterns lessons. Write code in a notebook."],
    ["2026-11-16","C++ and STL","Day 1: drills and D1-1 to D1-10. Day 2: STL drills, recursion, complexity, and the gate test from 7 to 9 PM."],
    ["2026-11-18","DSA heavy","Striver first, 5 to 6 new problems in sheet order. Then LeetCode on the same topic, Core CS, AWS and cyber. Sunday: contest and review."],
    ["2026-12-14","Semester starts","College 1 to 2 days a week. Keep Striver daily; use college days for revision, Core CS and AWS."],
    ["2027-01-31","Redo week","Checkpoint 1 was 30 Jan. Redo every problem marked H or F from memory, then timed sets."],
    ["2027-02-08","Build","Hard pass one a day, cyber at a full hour, system design, AWS exam prep, the CP habit, the paper by 21 Mar. No AI yet."],
    ["2027-03-22","Semester exams","Minimum day only. On 31 Mar check the HFT gate: Codeforces 1400+ or LeetCode contest 1800+."],
    ["2027-04-08","Finish and certify","Hard pass 2, the AWS exam in the week of 19 Apr, the AI-security project in May. Elite HFT track only if you passed the gate."],
    ["2027-05-31","Placement sprint","Revise Striver, timed tests, a mock interview every week."],
    ["2027-08-01","Final placements","On-campus drives, plus off-campus applications and referrals every week."],
    ["2028-01-01","Final year","Final-year project, a second certification, and off-campus applications if needed."]];
  '''
    h = h.replace(old, new)
    rep('var d=days(D("2026-11-05"),today)+1;document.getElementById("f-day").innerHTML=d<1?"Starts 16 Nov":(d>144?"Plan complete":"<b>"+d+"</b>of 144");',
        'var d=days(D("2026-11-16"),today)+1;document.getElementById("f-day").innerHTML=d<1?"Starts 16 Nov":(d>196?"Sprint and placements":"<b>"+d+"</b>of 196");')
    rep('Both pages open in a new tab. Back up your ticks from the playbook, Part 09, before your Claude plan changes, and keep the offline copies as a fallback.',
        'Back up your ticks from the playbook (Part 09, Back up progress) before 19 Nov, and keep the PDFs and offline copies as a fallback.')
    open(path, "w", encoding="utf-8").write(h)
update(sys.argv[2], "knowledge-base.html", "cheat-sheet.html")
print("ok")
