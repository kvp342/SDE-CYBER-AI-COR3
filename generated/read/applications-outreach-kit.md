APPLICATIONS · TRACKER AND OUTREACH

# Track every application and every message

A spreadsheet that tells you who to follow up with and how your funnel is doing, five message templates the interview day kit does not have, and a weekly routine that keeps applications and outreach moving from February 2027.

| Part                                   |
|----------------------------------------|
| [1. The applications tracker](#the-applications-tracker) |
| [2. Five outreach templates](#five-outreach-templates)  |
| [3. The weekly routine](#the-weekly-routine)       |

Files: [generated/outreach/applications-tracker.csv](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/outreach/applications-tracker.csv) (import into Google Sheets: File → Import → Upload; formulas work there and in Excel) and [generated/outreach/outreach-templates.md](https://github.com/kvp342/intrusion-detection-and-prevention/blob/ccr-ca7232a7-t7lq94/generated/outreach/outreach-templates.md). The three example rows are fictional; delete them when you start.

## The applications tracker

| Column                 | What goes in it                                                             |
|------------------------|-----------------------------------------------------------------------------|
| `Company`              | Company name                                                                |
| `Role`                 | Exact role title                                                            |
| `Link`                 | Job posting link (keep it: postings disappear)                              |
| `Applied (YYYY-MM-DD)` | Date you applied                                                            |
| `Referral (who)`       | Who referred you, if anyone                                                 |
| `Status`               | One of: Saved, Applied, Referred, OA, Interview, Offer, Rejected, Withdrawn |
| `Next action`          | The single next step, with a date                                           |
| `Follow up on`         | Formula: applied date + 7 days, blank once the application is closed        |
| `Notes`                | Anything useful: recruiter name, OA platform, questions asked               |

### Summary block (columns K–L)

| Metric              | Formula                                                                        |
|---------------------|--------------------------------------------------------------------------------|
| Applications        | `=COUNTA(A2:A200)`                                                             |
| Referred            | `=COUNTIF(F2:F200,"Referred")+COUNTIF(E2:E200,"?*")`                           |
| Reached OA or later | `=COUNTIF(F2:F200,"OA")+COUNTIF(F2:F200,"Interview")+COUNTIF(F2:F200,"Offer")` |
| Interviews          | `=COUNTIF(F2:F200,"Interview")+COUNTIF(F2:F200,"Offer")`                       |
| Offers              | `=COUNTIF(F2:F200,"Offer")`                                                    |

Checked: on the three example rows the follow-up dates come out as 8 Feb and 10 Feb (and blank for the rejected one), and the summary counts 3 applications, 1 referral, 1 at OA or later. Format column H as a date (Format → Number → Date) so the formula shows a date rather than a serial number. Sort by "Follow up on" every Thursday. Use Data → Data validation on column F with the status list so spelling stays consistent (the counts depend on it).

## Five outreach templates

Fill every \[bracket\]; send nothing with a bracket left in. The referral request, thank-you, follow-up and offer-extension emails are in the interview day kit.

### LinkedIn connection note

``` text
Hi [Name], I'm a [year] B.Tech CSE (Cybersecurity) student preparing for [Company]'s [role] internship. I enjoyed your post on [topic] and would value connecting.
```

Short, specific, no request in the first message. Personalise the topic.

### Cold email to a recruiter

``` text
Subject: [Role] internship – [Your name], B.Tech CSE (Cybersecurity), [College], [Year]

Hi [Recruiter name],

I applied for the [Role] internship ([job ID or link]) on [date]. I'm a [year] student focusing on backend and cloud security. Two things relevant to the role:
- [Project 1: one line with a number, e.g. multi-tenant AWS isolation tested with 12 scenarios]
- [Project 2 or achievement: one line, link]

Resume: [link]. GitHub: [link].
If the role is filled, I'd be grateful to be considered for similar openings.

Thank you,
[Your name]
[Phone] · [LinkedIn]
```

Always include the job ID. Two proof points, not a life story. One email, one follow-up after a week.

### Asking an alumnus for advice (not a referral)

``` text
Hi [Name], I'm [Your name], a [year] student from [College] (your college too). I'm preparing for SDE internships with a security and cloud focus and saw you moved from [College] to [Company]. Could I ask two quick questions over chat this week?
1. What mattered most in your [Company] interviews?
2. Is there a team where security or cloud interns fit well?
Thank you, [Your name]
```

Advice first builds the relationship; ask for a referral only after they reply and you have a specific job ID.

### Email to a professor for a research internship

``` text
Subject: Summer research internship – [Your name], B.Tech CSE (Cybersecurity), [College]

Dear Prof. [Surname],

I read your [year] paper "[Title]" on [topic]. [One sentence on what you understood or a question it raised.]

I'm a [year] student and have built [one project related to their area, with a link], and I'm writing a paper on [your research topic] due in March 2027. I'd like to work in your group in summer 2027, for example through [programme name, e.g. the institute's summer research programme], if that is possible.

CV: [link]. Transcript on request.

Thank you for your time,
[Your name]
```

Read the paper first: one real sentence about it is what separates you from mass emails. Apply through the official programme too.

### Status check after an interview or OA

``` text
Subject: [Role] application – status check ([job ID])

Hi [Name],

Thank you again for the [OA / interview] on [date]. I wanted to check whether there is an update on next steps, and whether you need anything else from me.

Best regards,
[Your name]
```

Send once, about a week after the date they gave (or two weeks if none). Stay polite even after a rejection; ask for feedback.

## The weekly routine

| Day           | About 45 minutes                                                                                                                                       |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Monday**    | Find 10 openings (careers pages, LinkedIn jobs, trackers); add them to the sheet as Saved.                                                             |
| **Tuesday**   | Tailor the resume's top 3 bullets for the best 5; apply; status Applied.                                                                               |
| **Wednesday** | 5 messages: 2 alumni (advice), 2 referral requests with job IDs, 1 recruiter email.                                                                    |
| **Thursday**  | Follow-ups: everything whose 'Follow up on' date has passed gets one polite message.                                                                   |
| **Friday**    | Apply to the other 5 saved openings; update statuses.                                                                                                  |
| **Saturday**  | OA practice set (the OA packs) or a real OA.                                                                                                           |
| **Sunday**    | Review the summary: applications → OA → interviews. If replies are under 10% after 30 applications, fix the resume first (resume kit), not the volume. |

Ten applications and five messages a week, as in the final plan. Quality beats volume: a tailored application with a referral and a job ID is worth more than twenty one-click applies.
