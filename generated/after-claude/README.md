# Studying after Claude: prompt pack

Copy-paste prompts for any free AI chat (Gemini, ChatGPT, Copilot, Claude free tier). For the whole kit, first paste `GEMINI-HANDOFF.md` from the repository root so the AI knows every file.

## Safety rules (read once)

1. **Never paste secrets:** AWS access keys, passwords, your AWS account ID, your bucket names, or `~/.aws/credentials`. Replace them with `ACCOUNT-ID` and `YOUR-BUCKET`.
2. **Never let an AI run AWS commands on your account without reading them first.** Anything with `delete`, `terminate`, `put-bucket-policy` or `attach-*-policy` changes real things and can cost money.
3. **Check facts against the official page** (AWS docs, cppreference, LeetCode editorial). AIs can be confidently wrong, especially about limits, prices and exam details.
4. **Code: run it.** An answer is right only when your tests pass.
5. **Do the thinking first.** Use AI after 25 minutes stuck (the stuck rule in the final plan), not before.

## DSA

**Hint, not answer**
```
I am solving this problem: [paste problem]. My idea so far: [your idea]. I am stuck on [where].
Give me ONE hint only, no code, no full solution. Ask me a question that points to the key idea.
```

**Find my bug**
```
Here is my C++ solution: [code]. It fails on this input: [input], expected [x], got [y].
Do not rewrite it. Point to the line(s) causing the bug and explain why, in under 5 sentences.
```

**After solving: compare**
```
I solved [problem] with [approach], complexity O(...). Is there a better approach?
Name the pattern, the better complexity, and one similar problem to practise. No code.
```

**Dry-run drill**
```
Give me a small tricky input for [problem] and ask me to dry-run my approach step by step.
Correct me after each step.
```

## Core CS and SQL

**Viva drill**
```
Ask me 10 interview questions on [OS / DBMS / CN / OOP topic], one at a time.
After each answer, score it 0-2, give the ideal one-line answer, then ask the next.
```

**SQL check**
```
Schema: [tables]. Question: [question]. My query: [query].
Is it correct for all cases (NULLs, ties, duplicates, empty groups)? If not, give one input row set that breaks it.
```

## Cloud (Solutions Architect)

**Daily recall (block 3 of the 2-hour routine)**
```
Today I studied [topics]. Quiz me with 8 SAA-C03-style scenario questions, 4 options each, one at a time.
After each answer explain why each wrong option is wrong. Keep score.
```

**Which service?**
```
Give me 15 one-line requirements ("needs X with least operational overhead") and I will name the AWS service.
Correct me and give the deciding keyword in the requirement.
```

## TenantWall (viva and paper)

**Viva practice** (paste pages 2–8 of `tenantwall-explained.md` first)
```
You are my professor examining my project TenantWall (above). Ask me 10 hard questions one at a time:
policy design, explicit vs implicit deny, CloudTrail data events, alarms, limitations.
After each answer, tell me what was missing.
```

**Paper language** (paste one paragraph you wrote yourself)
```
Improve the clarity and grammar of this paragraph for an IEEE conference paper.
Keep my meaning, numbers and technical terms exactly. Show the changes as a list, not only the new text.
```

## Interviews and applications

**Mock interview**
```
Act as an interviewer for a [SDE intern / security intern] role at [company type].
Ask one behavioural question, then one DSA question (medium), then one question about my project TenantWall.
Wait for my answer each time; at the end give scores and 3 improvements.
```

**Resume bullet**
```
Rewrite this resume bullet with the formula "action verb + what + how + measurable result", max 25 words.
Do not invent numbers: [bullet]
```

## Weekly review (Sunday)

```
This week I planned: [plan]. I did: [done]. I missed: [missed and why].
Give me 3 priorities for next week and one thing to cut, based on my final plan.
```
