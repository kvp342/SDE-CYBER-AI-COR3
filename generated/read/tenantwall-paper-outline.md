TENANTWALL · PAPER

# Paper outline

What goes in each section of the TenantWall paper, how long it should be, the figures and tables, a seven-week writing plan ending on the 21 March deadline, and a checklist before submission. The matching LaTeX skeleton (IEEE conference format) is in `generated/tenantwall/paper/`: `main.tex` with a writing prompt in every section, `refs.bib`, and a compiled preview `main.pdf`.

**Before you write.** Ask your professor which venue and template to use and what "explicit deny" should mean in the paper. Write in Overleaf (free) by uploading the three files and the two images.

|                                                 |
|-------------------------------------------------|
| [Section by section](#section-by-section)                   |
| [Figures, tables and writing plan](#figures-tables-and-writing-plan)    |
| [Submission checklist and references](#submission-checklist-and-references) |

## Section by section

Lengths assume a 6-page two-column paper; scale to your venue.

### Abstract 150–200 words, written last

- Problem: tenants sharing S3 and EC2 must not reach each other's data.
- Approach: ABAC with tag-matched policies and explicit denies; CloudTrail → CloudWatch → SNS alerting.
- Evaluation and result in one sentence, with numbers.
- Why it matters.

### I. Introduction about 0.75 page

- Shared resources are cheap but one bad policy exposes a tenant.
- Role-per-tenant RBAC grows with every tenant; ABAC keeps one policy.
- Prevention is not enough: denied attempts must be detected and reported.
- Three contributions as a list, then a one-line roadmap.

### II. Background about 0.75 page

- Multi-tenancy and resource pooling (NIST SP 800-145); isolation risks in shared clouds.
- RBAC and ABAC models; NIST SP 800-162.
- IAM evaluation order (explicit deny \> allow \> implicit deny), ABAC with tags, CloudTrail management vs data events.

### III. Threat model about 0.5 page

- Assets, attacker (a tenant or a stolen tenant credential), trust boundary, out of scope.
- STRIDE table (already in the skeleton; from the security lab notebook).

### IV. Design about 1 page

- Architecture figure.
- Identity policy (prefix and tag matching), explicit-deny policy, TLS-only bucket policy.
- Why denies are separate from allows; one short policy excerpt.

### V. Implementation about 0.5 page

- Region and services; how tenants and roles are created and tagged.
- Trail with S3 data events, metric filter pattern, alarm settings (from the TenantWall helpers).
- Method flowchart; cost controls.

### VI. Evaluation about 1 page

- Research questions: RQ1 isolation holds? RQ2 how fast are denials reported? RQ3 cost and overhead?
- Run the isolation test plan several times; fill the results table.
- Detection delay as median and range; false alerts; monthly cost.

### VII. Discussion and limitations about 0.5 page

- Tags as the trust anchor and who may set them.
- DescribeInstances has no resource-level control.
- CloudTrail delivery delay; scaling to many tenants; production changes.

### VIII. Related work about 0.5 page

- Cloud isolation research, access-control models, cloud audit and monitoring.
- How TenantWall differs: a concrete, tested design on one provider with alerting.

### IX. Conclusion 1 paragraph

- What was built, measured results, one line of future work.

## Figures, tables and writing plan

### Figures and tables

|          |                                                                                                            |
|----------|------------------------------------------------------------------------------------------------------------|
| Fig. 1   | Architecture (generated/tenantwall/architecture.png); redraw with official AWS icons for the final version |
| Fig. 2   | Method flowchart (generated/tenantwall/flowchart.png)                                                      |
| Table I  | STRIDE threats and mitigations                                                                             |
| Table II | Isolation test results: expected, observed, alert delay                                                    |
| Optional | Detection delay over trials (a small bar or box plot)                                                      |

### Seven weeks to 21 March

|     |        |                 |                                                                                            |
|-----|--------|-----------------|--------------------------------------------------------------------------------------------|
| ☐   | Week 1 | 01 Feb – 07 Feb | Related work and background: read the cited sources, write Sections II and VIII            |
| ☐   | Week 2 | 08 Feb – 14 Feb | Design: Section IV with the policy excerpt and Fig. 1                                      |
| ☐   | Week 3 | 15 Feb – 21 Feb | Implementation: Section V; run every isolation test once and save the evidence             |
| ☐   | Week 4 | 22 Feb – 28 Feb | Evaluation runs: repeat tests, measure alert delays and cost; fill Table II                |
| ☐   | Week 5 | 01 Mar – 07 Mar | Results and discussion: Sections VI and VII                                                |
| ☐   | Week 6 | 08 Mar – 14 Mar | Introduction, abstract, conclusion; check every reference; send the draft to the professor |
| ☐   | Week 7 | 15 Mar – 21 Mar | Revise from the professor's comments; final read-through and submit by 21 March            |

This overlaps the Hard pass in your plan: about 45 minutes a day on the paper, more at weekends. Build and test TenantWall in December and January first, as planned; the plan above is for writing.

## Submission checklist and references

|     |                                                                                                    |
|-----|----------------------------------------------------------------------------------------------------|
| ☐   | Page limit and template of the target venue checked (this skeleton uses IEEE conference format)    |
| ☐   | Every number in the paper comes from your own measured runs                                        |
| ☐   | Every reference verified on Google Scholar or the publisher's page (titles, authors, years, pages) |
| ☐   | No account ids, keys, bucket names or emails in figures, listings or screenshots                   |
| ☐   | Figures readable when printed in grey; captions say what to look at                                |
| ☐   | Professor has read and approved the final version                                                  |
| ☐   | Acknowledgement and author order agreed                                                            |
| ☐   | Policies and test scripts published on GitHub (no secrets) if the venue allows a link              |

### References in the skeleton

1.  \[1\] Guide to Attribute Based Access Control (ABAC) Definition and Considerations
2.  \[2\] The NIST Definition of Cloud Computing
3.  \[3\] Role-Based Access Control Models
4.  \[4\] A Unified Attribute-Based Access Control Model Covering DAC
5.  \[5\] Hey, You, Get Off of My Cloud: Exploring Information Leakage in Third-Party Compute Clouds
6.  \[6\] Threat Modeling: Designing for Security
7.  \[7\] What is ABAC for AWS? (IAM User Guide)
8.  \[8\] Policy evaluation logic (IAM User Guide)
9.  \[9\] Logging data events (AWS CloudTrail User Guide)

Full entries are in `refs.bib`. They are well-known sources, but verify every detail before submission and add the papers your professor recommends.
