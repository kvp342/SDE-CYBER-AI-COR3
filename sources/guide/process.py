"""Efficiency pages inserted after page 02. Uses helpers from build.py (exec'd there)."""
G = "#16a34a"

def steps(rows):
    return '<div class="flow">' + "".join(
        f'<div class="fs"><b>{i}</b><h3>{E(t)}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(rows, 1)) + '</div>'

# ---- 02A: operating modes + loops
page("", head("02·A", "EFFICIENT PROCESS", "Run your prep like a system", "Decide once, not every morning. Pick today's mode, follow its recipe, and let the loops catch what slips.", G) + f'''
<h2>Five day modes: pick one each morning in 10 seconds</h2>
{table(["Mode", "When", "Minimum that counts as a win", "Drop"], [
 ["<b style='color:#16a34a'>Full force</b>", "Home, no college", "6–8 deep blocks: 5–6 Striver, 1 LC, Core CS, cyber, AWS", "nothing"],
 ["<b style='color:#0891b2'>College day</b>", "Attending (1–2/week)", "2 problems on the commute/evening + AWS 30 min + 10 Core CS flashcards", "cyber, new topics"],
 ["<b style='color:#7c3aed'>Exam mode</b>", "22 Mar – 7 Apr", "1 revision problem from the 1-3-7-21 list", "everything else"],
 ["<b style='color:#a16207'>Low energy</b>", "Tired, ill, bad day", "1 Easy re-solve + read your error log (20 min)", "the guilt"],
 ["<b style='color:#c2410c'>Sprint</b>", "31 May – 31 Jul", "Mock or OA sim + company-tagged set + 5 applications", "new learning"],
])}
<aside class="call" style="--k:{G}"><b>Never-zero rule</b><p>The streak is "at least one problem touched", not "a perfect day". A low-energy day that keeps the streak is worth more than a perfect day followed by four days off.</p></aside>
<h2>Four loops that keep the plan honest</h2>
<div class="loops">
<div style="--k:#16a34a"><b>Daily · 5 min at night</b><p>Pick tomorrow's 3 problems and 1 Core CS topic. Write them down. Mornings start with no decisions.</p></div>
<div style="--k:#0891b2"><b>Weekly · Sun 30 min</b><p>Count problems, contests, blocks. Re-solve the week's failed problems. Move unfinished items, never stack them.</p></div>
<div style="--k:#2563eb"><b>Monthly · last Sun 1 h</b><p>Check the milestone box (section 13). One timed mock on old topics. Cut whatever isn't moving a number.</p></div>
<div style="--k:#c2410c"><b>Phase · each milestone</b><p>Rewrite the resume, update LinkedIn/GitHub, adjust the next phase's daily quota up or down by one problem.</p></div>
</div>
<h2>Decision rules: so you never waste an hour deciding</h2>
<ul class="rules">
<li><b>Stuck?</b> 20 min (Easy/Med) or 40 min (Hard) → read only the approach → code it yourself → add to the 1-3-7-21 list.</li>
<li><b>Video or article?</b> Article first (faster, searchable). Video only if the article didn't click, at 1.5×.</li>
<li><b>New resource tempting you?</b> Only if the current one has no material on that topic. Finish the sheet before switching.</li>
<li><b>Behind schedule?</b> Cut in this order: the Elite track (if open), the CP habit, the AI-security project. Never DSA or revision. Never double tomorrow's quota.</li>
<li><b>Two good options?</b> Pick the one that produces a proof (solved problem, lab, PR, resume line).</li>
<li><b>Feeling ready to apply?</b> You never will. Apply when the checklist says so (≈150 problems + 1 project).</li>
</ul>
''')

# ---- 02B: per-problem workflow + revision + notes + OA tactics
page("", head("02·B", "EFFICIENT PROCESS", "One problem, done the efficient way", "The same 7 steps for every problem. This turns 550 problems into skill instead of a number.", G) +
 steps([
  ("Read + restate (2 min)", "Rewrite the task in one line. Note n's limit → target complexity (table in section 04). List 3 edge cases: empty, one element, max/duplicates/negatives."),
  ("Brute force first (3 min)", "Say or write the simplest correct idea and its complexity. Interviewers reward this; it also gives you a checker."),
  ("Name the pattern (2 min)", "Use the trigger table. If none fits, try: sort it? hash it? binary search the answer? think in states (DP)?"),
  ("Code it (≤15 min)", "Clean names, no premature tricks. C++ template below. Stop at the timebox and take the hint."),
  ("Dry run (3 min)", "Trace one normal + one edge case by hand before submitting. Catches most WA."),
  ("Log it (1 min)", "Sheet row: link · pattern · trigger line · mistake · next revision date. This is the most valuable minute."),
  ("Revise on schedule", "Day 1, 3, 7, 21: re-solve from a blank file in ≤10 min. Pass twice in a row → retire it."),
 ]) + f'''
<div class="two"><div>
<h3>Tracker sheet columns (Google Sheets, free)</h3>
<p class="mono">Date · Problem · Link · Level · Pattern · Trigger · Time · Hint? · Mistake · R1 · R3 · R7 · R21</p>
<p>Formula for next revision: <span class="mono">=A2+1</span>, <span class="mono">=A2+3</span>… then filter "due ≤ today" each morning. 10 minutes of setup saves hundreds of re-solves.</p>
<h3>Reading an editorial efficiently</h3>
<ol><li>Read only until you see the key idea, then close it.</li><li>Code it yourself without looking.</li><li>Only then read their code and compare.</li><li>Write the one line you missed.</li></ol>
</div><div>
<h3>Contest C++ template (compile-checked)</h3>
<pre>#include &lt;bits/stdc++.h&gt;
using namespace std;
using ll = long long;
#define all(x) (x).begin(), (x).end()
const ll INF = 4e18; const int MOD = 1e9 + 7;
void solve() {{
    int n; cin &gt;&gt; n;
    vector&lt;ll&gt; a(n);
    for (auto &amp;x : a) cin &gt;&gt; x;
    // brute force first, then optimise
}}
int main() {{
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int t = 1; cin &gt;&gt; t;
    while (t--) solve();
}}</pre>
</div></div>
<h2>Online assessment and contest tactics</h2>
<div class="eff">{"".join(f'<div class="ef"><h3>{E(t)}</h3><p>{d}</p></div>' for t, d in [
 ("Read all problems first", "2 minutes. Solve in order of confidence, not order given."),
 ("Partial scores count", "HackerRank-style OAs score test cases. A correct brute force on half the tests beats a perfect idea not submitted."),
 ("Watch overflow", "Sums/products of ints → <code>long long</code>. Most silent WA in OAs."),
 ("Custom tests", "Run the edge cases you listed before submitting. Empty, 1, max n, all equal."),
 ("Last 10 minutes", "Stop optimising. Submit what passes, add guards for edge cases."),
 ("Same environment", "Practise on HackerRank/HackerEarth too; their I/O and editors differ from LeetCode."),
])}</div>
''')

# ---- 02C: AI as tutor + 80/20 + tools
PROMPTS = [
 ("Hint-only tutor", "I'm solving [problem link/text]. Don't give the solution or code. Give me one hint at a time, the smallest nudge first. Wait for me to say 'next' before the next hint."),
 ("Mock interviewer", "Act as an Amazon SDE interviewer. Give me one Medium DSA problem. Stay silent while I think aloud, ask about edge cases and complexity, then score me 1–5 on problem solving, code and communication with one fix each."),
 ("Code reviewer", "Here is my accepted C++ solution. Don't rewrite it. Point out: bugs on edge cases, complexity, unclear names, and one cleaner STL idiom I could have used."),
 ("Feynman checker", "I'll explain [deadlock / B+ tree / TCP handshake] in 5 lines. Find what's wrong or missing, then ask me 3 interview follow-up questions on it."),
 ("Flashcard maker", "Turn these notes into 10 question–answer flashcards, one fact each, in 'Q; A' format for Anki import."),
 ("Resume reviewer", "Review this resume for an SDE intern role at a product company. For each bullet: is there a number? an action verb? a technology? Rewrite the weakest 3."),
]
page("", head("02·C", "EFFICIENT PROCESS", "Use AI, tools and the 80/20 rule", "AI is a tutor and interviewer, never your hands. Tools remove friction. The 80/20 list tells you what to learn first.", G) +
 '<h2>Six prompts for Claude or Gemini</h2><div class="pr">' + "".join(f'<div class="pp"><b>{E(t)}</b><p>{E(p)}</p></div>' for t, p in PROMPTS) + '</div>' + f'''
<aside class="call" style="--k:#be123c"><b>The AI rule</b><p>Never paste a problem and ask for the solution before your 20/40-minute timebox is up. Copying AI code feels like progress and gives zero interview skill — interviewers can tell in 2 minutes.</p></aside>
<h2>The 20% that gets 80% of the questions</h2>
{table(["Area", "Learn these first"], [
 ["DSA", "Arrays + hashing, two pointers, sliding window, binary search, trees (traversals, BST, LCA), graphs (BFS/DFS, topo, Dijkstra), DP (1D, 2D grid, knapsack, LIS, LCS), heaps, stacks"],
 ["OS", "Process/thread, scheduling, deadlock, paging + virtual memory, synchronisation (mutex, semaphore)"],
 ["DBMS + SQL", "Normalisation, ACID + isolation, indexing, joins, GROUP BY + HAVING, window functions, Nth highest"],
 ["CN", "OSI/TCP-IP, TCP vs UDP, handshake, HTTP/HTTPS/TLS, DNS, 'type a URL' walkthrough"],
 ["OOP", "4 pillars, virtual/vtable, overloading vs overriding, SOLID, 3 patterns"],
 ["Security", "OWASP Top 10, auth vs authz, hashing vs encryption, TLS, IAM least privilege"],
])}
<h2>Free tool stack</h2>
{table(["Need", "Tool", "Why it saves time"], [
 ["Tracker + revision dates", "Google Sheets", "Filter 'due today' in one click"],
 ["Core CS memory", a("https://apps.ankiweb.net", "Anki"), "Spaced repetition done for you, 10 min/day"],
 ["Focus blocks", a("https://pomofocus.io", "Pomofocus") + " + phone in another room", "Counts blocks, not hours"],
 ["Diagrams (LLD/HLD, TenantWall)", a("https://excalidraw.com", "Excalidraw") + ", " + a("https://app.diagrams.net", "diagrams.net") + " (AWS icons)", "Fast, exportable, looks pro"],
 ["Contest calendar", a("https://clist.by", "clist.by"), "All contests in one place"],
 ["Mock interviews", a("https://www.pramp.com", "Pramp") + ", peers, AI mock prompt", "Free, real-time speaking practice"],
 ["Job alerts", "LinkedIn + Naukri + company career pages saved searches", "Jobs come to you; apply within 48 h"],
])}
''')

# ---- 02D: application + interview efficiency + energy
page("", head("02·D", "EFFICIENT PROCESS", "Apply, interview and last the distance", "Batch the boring parts, reuse everything, and protect the energy that does the real work.", G) + '''
<div class="two"><div>
<h2>Application pipeline in 90 min/week</h2>
<ol class="tight">
<li><b>Master resume</b> with every bullet you have (2 pages, private).</li>
<li><b>3 role versions</b> cut from it: SDE, Security/AppSec, Cloud. One page each.</li>
<li><b>Tailor in 5 min</b>: swap 2 bullets and the skills order to match the job's top 5 keywords. Nothing more.</li>
<li><b>Batch</b>: Mon + Thu evening, 45 min each. Alerts collected, applications sent, referral messages sent, tracker updated.</li>
<li><b>Follow up</b> once after 5–7 days, from the tracker's "next action" column.</li>
<li><b>Reuse answers</b>: keep a doc of "Why this company / Tell me about yourself / Strengths" answers, edit per company.</li>
</ol>
<h2>Company-specific prep in 1 week</h2>
<ol class="tight">
<li>Read 5–10 recent interview experiences for that company and role (LeetCode Discuss, GfG).</li>
<li>Solve its last-6-months LeetCode tag list, top 30 by frequency.</li>
<li>Map its values (e.g. Amazon Leadership Principles) to your 6 STAR stories.</li>
<li>Know its product: use it, find one thing you'd improve, one security thought.</li>
</ol>
</div><div>
<h2>Interview day: efficient habits</h2>
<ul class="tight">
<li>Night before: no new topics. Re-read your error log, pattern sheet and STAR stories.</li>
<li>Have a 60-second "tell me about yourself": who you are, 2 proofs (rating, TenantWall), why this role.</li>
<li>Think aloud from second one; silence is scored as stuck.</li>
<li>State brute force, then improve. Ask before coding: "Shall I code this approach?"</li>
<li>End every round with one smart question about the team's work.</li>
<li>After: write down every question within 1 hour. That list is your next week's revision.</li>
</ul>
<h2>Energy: the hidden multiplier</h2>
<ul class="tight">
<li><b>Sleep 7–8 h</b> at a fixed time; it's when memory consolidates.</li>
<li><b>Hardest work first</b> (new DSA) in your sharpest hours; revision and AWS when tired.</li>
<li><b>Move 20–30 min</b> daily (walk, cricket, gym). Improves focus more than coffee.</li>
<li><b>Phone out of the room</b> during blocks; social apps only after block 4.</li>
<li><b>One rest half-day a week.</b> Burnout costs weeks; rest costs hours.</li>
<li><b>Compare with your last month</b>, not with LinkedIn posts.</li>
</ul>
</div></div>
<aside class="call" style="--k:#16a34a"><b>Efficiency in one line</b><p>Fixed modes, a 7-step problem routine, a revision sheet that tells you what to redo, AI as a tutor not a solver, batched applications, and sleep. Everything else in this guide plugs into those six.</p></aside>
''')
