import json,datetime,re
dt=datetime.date; TD=datetime.timedelta
pb=open('playbook.html',encoding='utf-8').read()
s=pb.index("\nvar D=")+7; e=pb.index("};",s)+1; D=json.loads(pb[s:e])
AWSW=json.loads(re.search(r'AWS_WEEKS=(\[.*?\]);',pb).group(1))
L={"E":"Easy","M":"Medium","H":"Hard"}
core=[];hard=[];seen=set();names={};csb=[];cy={};ai={}
for k in sorted(D):
    e_=D[k]
    for x in e_.get("steps",[]): names[x[0]]=x[1]
    for x in e_.get("due",[]):
        if (x[0],x[1]) in seen: continue
        seen.add((x[0],x[1])); (hard if x[2]=="H" else core).append(x)
    c=e_.get("cs")
    if c and c[2]:
        key=(c[0],c[2][0])
        if key not in [(a,b) for a,b,_ in csb]: csb.append((c[0],c[2][0],[t.replace("`","") for t in c[2][1]]))
    c=e_.get("cy")
    if c: cy[c[0]]=(c[1],c[2].replace("`",""),c[3])
    c=e_.get("ai")
    if c: ai[c[0]]=(c[1],c[2],c[3])
core.sort(key=lambda x:x[0]); hard.sort(key=lambda x:x[0])
assert len(core)==359 and len(hard)==84 and len(ai)==12 and len(cy)==20, (len(core),len(hard),len(ai),len(cy))
W0=dt(2026,11,16)
def wk(d): return (d-W0).days//7
EX0,EX1=dt(2027,3,22),dt(2027,4,7)
TWD={dt(2026,11,21):("Policies: Policy Generator and explicit deny",["Rebuild the bucket policy (Listing 3) in the AWS Policy Generator and compare it with yours","Run IAM Access Analyzer's policy check on all three policies","Write the explicit versus implicit deny subsection; mark each test in Table II"]),
 dt(2026,11,28):("CloudTrail trail",["Create tenantwall-trail with logs in a separate bucket","Turn on management events, and S3 data events for tenantwallbucket only","Re-run tenantwall_tests.py and find each refusal in the logs"]),
 dt(2026,12,5):("CloudWatch alarm",["Send the trail to CloudWatch Logs","Metric filter for refused calls; alarm at 3 or more in 5 minutes, emailed through SNS","Second filter for tag tampering: CreateTags, TagUser, UntagUser"]),
 dt(2026,12,12):("Diagrams and paper update",["Redraw Fig. 1 with AWS icons, adding CloudTrail, CloudWatch and SNS","Draw the method flowchart","Add the Layer 5: Audit and alerting section; send the paper to the professor"])}
# ---- daily Striver assignment
striver={};q=list(core);d=dt(2026,11,18)
while q:
    if d.weekday()!=6:
        n=6 if q[0][0]<=12 else 5
        striver[d]=q[:n]; q=q[n:]
    d+=TD(days=1)
striver_end=max(striver)
hardday={};q=list(hard);d=dt(2027,2,8)
while q:
    if not(EX0<=d<=EX1): hardday[d]=q.pop(0)
    d+=TD(days=1)
hard_end=max(hardday)
print('striver ends',striver_end,'hard ends',hard_end)
CYMAP=[1,1,2,3,3,4,5,5,6,7,7,8]+[9,10,11,12,13,14]+[None,None]+[15,16,17,18,19,20]
AIMAP={12+i:i+1 for i in range(6)}; AIMAP.update({20+i:i+7 for i in range(6)})
CPMAP={12:800,13:800,14:900,15:900,16:1000,17:1000,20:1100,21:1100,22:1200,23:1200,24:1300,25:1300,26:1400,27:1400}
def csblock(w):
    if w<len(csb): return csb[w]
    return None
BACK={5:"Design it: a study-tracker REST API. Write the endpoints and the SQL schema; create the repo.",6:"Build the CRUD endpoints with a real database (PostgreSQL or MySQL).",7:"Add sign-up and login with hashed passwords and JWT; protect the routes.",8:"Write tests for every endpoint; add input validation and error handling.",9:"Deploy it on AWS (EC2 with RDS, free tier); add a health check.",10:"README, architecture diagram, and the resume line with one real number."}
TWN={5:"Ask the professor for the venue and the deadline.",8:"Start the GitHub repo: policies, scripts, diagrams, README.",13:"Draft the final paper with the audit and alerting section.",16:"Final read-through with the team.",17:"Submit by Sunday 21 Mar, before exams."}
def rngsteps(ps):
    st=sorted({p[0] for p in ps}); return ", ".join(f"Step {k} {names[k]}" for k in st)
weeks=[];days={}
def add_day(d,blocks): days[d.isoformat()]=blocks
for w in range(37):
    a=W0+TD(days=7*w); ds=[a+TD(days=i) for i in range(7)]; t=[];ck=[]
    exam=all(EX0<=x<=EX1 for x in ds); 
    if w==0: phase="C++ and STL, then DSA heavy"
    elif a<=dt(2027,2,1): phase="DSA heavy"
    elif a<EX0: phase="Build"
    elif exam: phase="Semester exams"
    elif a<dt(2027,5,31): phase="Finish and certify"
    else: phase="Placement sprint"
    sp=[p for x in ds for p in striver.get(x,[])]
    hp=[hardday[x] for x in ds if x in hardday]
    if exam:
        t=[["College","Semester exams. Exam study comes first."],["Minimum day","Revision 30 min, 2 problems, 1 LeetCode problem. Nothing else."]]
        ck=["Semester exams"]
    elif phase=="Placement sprint":
        k=w-28
        REV=["Steps 1 to 5: basics, sorting, arrays, binary search, strings","Steps 6 to 9: linked list, recursion, bits, stacks and queues","Steps 10 to 13: sliding window, heaps, greedy, binary trees","Steps 14 and 15: BST and graphs","Step 16: dynamic programming","Steps 17 and 18, then redo every problem marked F","Mixed timed sets: 3 problems in 90 minutes, daily","Mixed timed sets and company-tagged problems","Mixed timed sets; a light final week before the season"]
        CSR=["OOP","Operating systems","DBMS and SQL","Networks","System design","All five, mixed viva","All five, mixed viva","HR answers and project walk-throughs","HR answers and project walk-throughs"]
        PRO=["Resume final draft; get two people to review it","GitHub: pin 4 projects, each with README and diagram","LinkedIn: post about TenantWall","List 40 target companies; note which hire off-campus","Ask alumni for referrals; apply to the first 10","Company-specific prep for the first drives","Apply to 10 more; practise the project walk-through","Apply to 10 more; rest properly","Sleep, light revision, documents ready"]
        t=[["DSA","Revise Striver, "+REV[k]+". Re-solve from memory, about 15 problems a day."],["Timed test","One full online-test simulation: 3 problems in 90 minutes, plus 20 aptitude questions."],["Mock interviews","One full mock this week. Write down every question you could not answer."],["Core CS","Answers out loud: "+CSR[k]+"."],["Profile",PRO[k]+"."],["CP and CSES","Optional, 1 hour: CP-31 from rating 1500, and the CSES section that matches this week's revision."],["Stretch","Only if everything above is done: 30 minutes of probability for HFT."]]
        if w==36: ck=["Placements open on 1 Aug"]
    else:
        # DSA
        if w==0: t.append(["DSA","Mon and Tue: C++ and STL, then the gate test. Wed to Sat: "+rngsteps(sp)+f" ({len(sp)} problems)."])
        elif sp: t.append(["DSA",rngsteps(sp)+f": {len(sp)} new problems, {6 if sp[0][0]<=12 else 5} a day, Monday to Saturday."+(" Striver core ends this week; then redo every problem marked H or F." if striver_end in ds else "")])
        elif a<dt(2027,2,8): t.append(["DSA","Redo every problem marked H or F from memory, then mixed timed sets: 3 problems in 90 minutes."])
        elif hp: t.append(["DSA",f"Hard pass: {len(hp)} Hard problems, one a day, from "+", ".join(sorted({names[p[0]] for p in hp},key=lambda n:[k for k,v in names.items() if v==n][0]))+". 30 minutes alone before any hint."+(" The Hard pass ends this week." if hard_end in ds else "")])
        else: t.append(["DSA","Two revision problems a day from the weakest topics in your error log."])
        # LeetCode
        if w==0: t.append(["LeetCode","From Wed: 2 problems a day on arrays and maths basics. Sunday contest."])
        elif a<dt(2027,2,8): t.append(["LeetCode","2 problems a day on this week's Striver topic, 35 minutes each."+(" Not on Saturday." if any(x in TWD for x in ds) else "")+" Sunday contest, then upsolve one."])
        else: t.append(["LeetCode","One problem a day. Sunday contest, then upsolve one."])
        if w in CPMAP: t.append(["CP-31",f"Rating {CPMAP[w]}: 2 problems a day. A Codeforces Div 3 or Div 4 round at the weekend."])
        b=csblock(w)
        if b: t.append(["Core CS",f"{b[0]}: {b[1]}. "+"; ".join(b[2])+"."])
        elif a<EX0: t.append(["Core CS","Revision: all five subjects in rotation, 5 questions a day out loud."])
        else: t.append(["Core CS","Mixed viva: 5 questions a day across all five subjects."])
        c=CYMAP[w] if w<len(CYMAP) else None
        if c:
            t.append(["Cyber",f"Lab week {c}: {cy[c][0]}. {cy[c][1]}. Proof: {cy[c][2]}."+(" 30 minutes a day and 2 hours on Sunday; a lab week can take two calendar weeks." if w<12 else " One hour a day.")])
        elif 26<=w<=28:
            t.append(["Cyber",["Binary taster 1 of 3: x86-64 basics (registers, the stack, calling conventions) in GDB with pwndbg.","Binary taster 2 of 3: simple crackmes in Ghidra; three picoCTF reverse-engineering challenges.","Binary taster 3 of 3: one stack buffer overflow, then what canaries, NX and ASLR each stop."][w-26]+" One hour a day."])
        # AWS
        if w<18: t.append(["AWS",AWSW[w]])
        elif w==20: t.append(["AWS",AWSW[18].replace(" and book the exam for April"," and book the exam for the week of 19 Apr")])
        elif w==21: t.append(["AWS","Light review of notes and wrong answers; one more practice exam if the last was under 80%."])
        elif w==22: t.append(["AWS","Sit SAA-C03 this week. June is the latest."]); ck.append("AWS exam, planned")
        elif w==23: t.append(["AWS","Certified: add it to the resume and LinkedIn. If not yet sat, sit it now."])
        if w in AIMAP: n=AIMAP[w]; t.append(["AI",f"Week {n} of 12: {ai[n][0]}. {ai[n][1]} Proof: {ai[n][2]}. Two hours a day."])
        tw=[TWD[x] for x in ds if x in TWD]
        if tw: t.append(["TenantWall","Saturday, 3 hours: "+tw[0][0]+". "+"; ".join(tw[0][1])+"."])
        elif w in TWN: t.append(["TenantWall",TWN[w]])
        if w in BACK: t.append(["Backend project","Sunday, 4 hours. "+BACK[w]])
        if 7<=w<18 or 20<=w<26: t.append(["Aptitude","15 minutes a day: quant, logical and verbal, in rotation."])
        if w==5: t.append(["Profile","Resume version 1. Set up GitHub (pinned repos) and LinkedIn."])
        if w==11: t.append(["Profile","Resume version 2, with the backend project and your problem counts."])
        if w==6: t.append(["Internship","The first 5 applications to good companies. Ask the placement office what counts for the NOC."])
        elif 7<=w<18 or 20<=w<=23: t.append(["Internship","5 applications to good companies and one referral request. Stop when you have an offer."])
        if w==26: t.append(["Internship","With an offer, the internship starts around now. It replaces the capstone and most of the sprint; keep 1 hour of DSA revision a day."])
        if w==9: t.append(["Mock interviews","Your first mock interview: one DSA problem, thinking aloud, with a classmate or senior."])
        elif w==11: t.append(["Mock interviews","Two mock interviews and two timed online-test sets."])
        elif 12<=w<18 or 20<=w<28: t.append(["Mock interviews","One mock interview. Note every question you could not answer."])
        if w in (26,27): t.append(["Capstone",["AI-assisted intrusion detection on TenantWall's CloudTrail logs: dataset, features, baseline model, evaluation.","Alerting demo, README, architecture diagram, a 2-minute demo video, and the resume line."][w-26]])
        if w==4: t.append(["College","Semester starts on 14 Dec. On college days (1 to 2 a week) do the light blocks: revision, Core CS, AWS and 2 Striver problems."])
        if w==17: t.append(["College","Exams start next week. From Wednesday, give the Core CS and cyber time to exam subjects."])
        if w==20: t.insert(0,["College","Exams end around 7 Apr. Rest for two days, then restart at full pace."])
        CK={dt(2026,11,17):"Gate test, 7 to 9 PM",dt(2026,11,18):"Export progress; Claude Pro ends on the 19th",dt(2026,12,20):"Readiness check 1",dt(2027,1,17):"AWS course and practice exam done",dt(2027,3,15):"Readiness check 2",dt(2027,3,21):"Paper submitted"}
        ck+=[v for k_,v in CK.items() if k_ in ds]
        if striver_end in ds: ck.append("Striver core done")
        if hard_end in ds: ck.append("Hard pass done")
    weeks.append({"a":ds[0].isoformat(),"b":ds[-1].isoformat(),"phase":phase,"t":t,"ck":ck})
    # ---- days
    if exam or phase=="Placement sprint": continue
    for x in ds:
        bl=[]
        if x==dt(2026,11,16): bl.append(["C++ day 1",["Learn C++ at 2×: slow down only for what differs from C","Day 1 drills: input and output, types and overflow, loops and patterns, functions and references, vectors and strings","Evening: practice problems D1-1 to D1-10"]])
        elif x==dt(2026,11,17): bl.append(["C++ day 2",["STL video, then the STL I, II and III drills","Recursion, pointers and structs; complexity and hashing","7 to 9 PM: gate test, no notes or AI, pass with 4 of 5"]])
        elif x in striver: bl.append(["Striver: "+", ".join(f"step {k}" for k in sorted({p[0] for p in striver[x]})),[f"{p[1]} ({L[p[2]]})" for p in striver[x]]])
        elif x in hardday: p=hardday[x]; bl.append(["Hard pass",[f"Step {p[0]}: {p[1]}"]])
        elif x.weekday()==6 and x<dt(2027,2,8): bl.append(["Sunday",["Weekly contest, then upsolve one problem","Written weekly review: solved, failed and why, what changes","2 hours of cyber"+("; 4 hours on the backend project" if w in BACK else ""),"Rest"]])
        elif EX0<=x<=EX1: bl.append(["Semester exams",["Minimum day: revision, 2 problems, 1 LeetCode problem"]])
        else: bl.append(["Revision",["Redo problems marked H or F; one timed set of 3 problems in 90 minutes"]])
        if x in TWD: bl.append(["TenantWall, 3 h (in place of LeetCode)",TWD[x][1]])
        if x>dt(2026,11,17) and x.weekday()!=6 and not(EX0<=x<=EX1):
            b=csblock(w)
            if b: bl.append([f"Core CS: {b[0]} · {b[1]}",[b[2][x.weekday()%len(b[2])],"Answer 3 questions on it out loud"]])
            if w in AIMAP: bl.append([f"AI week {AIMAP[w]}: {ai[AIMAP[w]][0]}",["2 hours toward: "+ai[AIMAP[w]][2]]])
        days[x.isoformat()]=bl
MONTHS=[
 ["Aug 2027","Final placements","First drives. Sit every test that fits. After each one, write down what was asked and fix that gap the same week. 10 off-campus applications and 5 referral requests a week. One contest and 10 problems a week to stay sharp."],
 ["Sep 2027","Final placements","Peak season. Keep the weekly rhythm: Monday shortlist, Tuesday apply, Wednesday referrals, Friday follow-ups. One mock interview every two weeks. Re-read the error log before every test."],
 ["Oct 2027","Final placements","If no offer yet: widen to cloud, DevSecOps and security roles, where TenantWall and the AWS certification carry more weight. Ask each interviewer for feedback."],
 ["Nov 2027","Final placements","Continue drives and off-campus. Start the final-year project proposal: extend TenantWall or the intrusion-detection work."],
 ["Dec 2027","Final placements","Season winds down. Review in writing: offer in hand, or the list of what interviews exposed and a 6-week plan to fix it."],
 ["Jan 2028","Final year","Final-year project build begins. If no offer: off-campus hiring continues, with 10 applications a week."],
 ["Feb 2028","Final year","Project build. Start a second certification: AWS Security Specialty or Security+."],
 ["Mar 2028","Final year","Project evaluation and results. Draft a second paper if the results are worth it."],
 ["Apr 2028","Final year","Sit the second certification. Project report."],
 ["May 2028","Final year","Final exams and project viva. With an offer: read up on your team's stack and system design."],
 ["Jun 2028","Final year","Graduate. First job starts in July."]]
# intensive table rows from the computed weeks
rows=[]
for w in range(12):
    wkd=weeks[w]; a=dt.fromisoformat(wkd["a"])
    dsa=[x[1] for x in wkd["t"] if x[0]=="DSA"][0]
    dsa=re.sub(r": \d+ new problems.*","",dsa); dsa=re.sub(r"^Mon and Tue: C\+\+ and STL, then the gate test\. Wed to Sat: (.*?) \(\d+ problems\)\.$",r"C++, STL; \1",dsa)
    also=[]
    b=csblock(w); 
    if b: also.append(b[0].replace(" (C++)",""))
    for x in wkd["t"]:
        if x[0] in("TenantWall","Backend project","Mock interviews","Profile") : also.append(x[0] if x[0]!="Profile" else x[1].split(".")[0])
        if x[0]=="Internship": also.append("applications")
    rows.append(f'<tr><td class="mono">{w+1} · {a.day} {a.strftime("%b")}</td><td>{dsa}</td><td>{"; ".join(dict.fromkeys(also))}</td></tr>')
json.dump({"W":{"weeks":weeks,"months":MONTHS},"days":days,"rows":rows,"striver_end":striver_end.isoformat(),"hard_end":hard_end.isoformat()},open('roadmap/rebuild.json','w'),ensure_ascii=False)
for w in (0,1,6,10,11,13,21,27,30): print(w,json.dumps(weeks[w],ensure_ascii=False)[:700],'\n')
print("\n".join(rows))
