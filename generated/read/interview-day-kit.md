PLACEMENTS · THE DAY ITSELF

# Interview day kit

Checklists for online-assessment days and interview days, phrases for the moments you get stuck, four email templates (referral request, thank-you, follow-up, more time on an offer), and a way to compare offers fairly. The templates are also in `generated/interview-day/email-templates.md`; the offer sheet is `generated/interview-day/offer-comparison.csv` (opens in Google Sheets with its formulas).

|                                                |
|------------------------------------------------|
| [OA day and interview day checklists](#checklists) |
| [What to say when you are stuck](#what-to-say-when-you-are-stuck)      |
| [Email templates](#email-templates)                     |
| [Comparing offers](#comparing-offers)                   |

## Checklists

### Online assessment day

|     |                                                                                                                                                     |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| ☐   | Day before: test the platform link, webcam and microphone if proctored; read the instructions email twice (allowed languages, tab switching rules). |
| ☐   | Laptop charged and plugged in; stable internet with a phone hotspot as backup; notifications off; desk clear.                                       |
| ☐   | Your C++ template typed and tested: fast I/O, long long, common includes (from the STL card).                                                       |
| ☐   | First 5 minutes: read every problem and its constraints; pick the order (easiest first).                                                            |
| ☐   | When stuck past your time budget: submit a correct brute force for partial marks and move on.                                                       |
| ☐   | Before each submit: run the samples plus one edge case (n = 1, all equal, maximum values).                                                          |
| ☐   | Last 10 minutes: no new problems; make sure every attempted problem has a submission.                                                               |

### Interview day

|     |                                                                                                                                                         |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| ☐   | Day before: reread the company file, your resume line by line, and your six story cards; prepare two questions to ask.                                  |
| ☐   | Online: quiet room, plain background, camera at eye level, headphones, a notebook and pen; join 5 minutes early.                                        |
| ☐   | In person: printed resume, ID, the call letter; arrive 30 minutes early.                                                                                |
| ☐   | Coding round: restate the problem, ask about input size and edge cases, say a brute force and its complexity, then improve, then code, then test aloud. |
| ☐   | Design round: requirements first, then estimates, API, data model, diagram, deep dive, trade-offs (system design one-pager).                            |
| ☐   | Behavioural round: STAR, about 2 minutes, 'I' not 'we', a result with a number.                                                                         |
| ☐   | Within an hour after: write down every question asked; send a short thank-you if you have the recruiter's email.                                        |

See also the [OA tactics](knowledge-base/career.md#online-assessments-oas) and [STAR](knowledge-base/career.md#behavioural-interviews-and-star-stories) pages, the company files and the mock interview scripts.

## What to say when you are stuck

|                                   |                                                                                                                        |
|-----------------------------------|------------------------------------------------------------------------------------------------------------------------|
| You do not understand the problem | "Let me restate it to check: … Is that right? Could you walk me through the second example?"                           |
| No idea where to start            | "Let me start with a brute force: … that's O(n²). The repeated work is …, so I'm thinking of a hash map to remove it." |
| Your idea might be wrong          | "I think this works because …. Let me test it on a small case before coding."                                          |
| You find a bug                    | "This fails when n = 1 because …. I'll fix the loop bound." Interviewers value finding your own bugs.                  |
| Out of time                       | "I won't finish the code, so here's the rest of the approach and its complexity: …."                                   |
| You do not know a fact            | "I'm not sure. My understanding is …; I'd confirm it in the documentation." Never bluff.                               |

Silence is the main thing to avoid: interviewers can only give credit and hints for thinking they can hear.

## Email templates

### Referral request (to an alumnus or senior)

``` text
Subject: Referral for [Role] at [Company]

Hi [Name],

I'm [Your name], a [year] B.Tech CSE (Cyber Security) student at [College], and I saw that you work on [team or product] at [Company]. I'm applying for [Role] ([job link or ID]).

Relevant work: [one line on TenantWall with a result], [one line on another project], and [DSA or contest result].

Would you be comfortable referring me? My resume is here: [link]. Happy to answer any questions, and thank you for your time either way.

Best,
[Your name]
[LinkedIn] · [GitHub]
```

### Thank-you after an interview

``` text
Subject: Thank you, [Role] interview on [date]

Hi [Interviewer or recruiter name],

Thank you for the conversation today about [team or topic]. I enjoyed discussing [one specific thing from the interview], and it made me more interested in the role.

[Optional one line: a short follow-up thought on a question you discussed.]

Best regards,
[Your name]
```

### Follow-up on status (after the promised date)

``` text
Subject: Following up, [Role] application

Hi [Recruiter name],

I interviewed for [Role] on [date] and wanted to check whether there is any update on the next steps. I remain very interested in the position.

Thank you,
[Your name]
```

### Asking for more time on an offer

``` text
Subject: [Role] offer, timeline

Hi [Recruiter name],

Thank you for the offer for [Role]; I'm grateful and excited about it. I'm completing one more process that ends on [date]. Would it be possible to share my decision by [date]?

Best regards,
[Your name]
```

## Comparing offers

A "CTC" figure often adds one-time and uncertain parts to fixed pay. Compare offers on two numbers: what year one is worth, and what a normal year after that is worth. Then weigh the parts money does not show.

### What to ask for, item by item

|     |                                    |
|-----|------------------------------------|
| ☐   | Base salary (annual)               |
| ☐   | Joining bonus (one time)           |
| ☐   | Performance bonus (annual, target) |
| ☐   | Stocks / RSUs (total grant)        |
| ☐   | Vesting years                      |
| ☐   | Relocation (one time)              |
| ☐   | Bond or service agreement (months) |
| ☐   | Notice period (days)               |
| ☐   | City                               |
| ☐   | Role and team                      |

### Worked example (made-up numbers)

|                            | Offer A                 | Offer B    |
|----------------------------|-------------------------|------------|
| Base salary                | ₹18.0 lakh              | ₹22.0 lakh |
| Joining bonus              | ₹2.0 lakh               | ₹0.0 lakh  |
| Performance bonus (target) | 10%                     | 0%         |
| Stocks over vesting        | ₹24.0 lakh over 4 years | none       |
| First-year value           | ₹27.8 lakh              | ₹22.0 lakh |
| Recurring yearly value     | ₹25.8 lakh              | ₹22.0 lakh |

First-year value = base + joining bonus + base × bonus% + stock grant ÷ vesting years. Recurring = the same without the joining bonus. Offer A has the larger "CTC" but part of it is a one-time bonus and stock that may change in value; Offer B is all fixed pay. Neither is automatically better: also weigh the bond, the city's cost of living, the team and what you will learn. These numbers are computed by the build script and match the formulas in the CSV.

### Rules

- Get the offer in writing, with the breakdown, before deciding.
- Ask politely about any part that is unclear (vesting schedule, bonus conditions, bond terms).
- Do not accept an offer you intend to break; companies and colleges remember.
- Follow your college placement cell's rules on accepting offers (many allow only one).
