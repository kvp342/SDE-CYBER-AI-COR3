SQL · INTERVIEW PACK II

# 30 harder SQL questions every output checked

The questions product and data-heavy companies ask after the basics: gaps and islands, sessions, running balances, medians, retention and funnels, recursive trees and calendars, pivots, graph-style self-joins, overlapping intervals, deduplication and keyset pagination. One small product-analytics database (users, logins, events, transactions, follows, categories, bookings, baskets, scores). Every query was run in SQLite 3.53.1, and its full output was compared with an answer computed separately in Python. The same questions are in `generated/sql-pack-2.sql` to run yourself. Start with the first SQL pack if window functions are new to you.

**How to use.** Read the question, cover the answer, write your query, then compare. Practise online for free on the [LeetCode SQL 50 study plan](https://leetcode.com/studyplan/top-sql-50/) or [SQLBolt](https://sqlbolt.com/). Dialect differences (SQLite, MySQL, PostgreSQL) are noted where they matter. [Sample database →](#the-sample-database)

| \#  | Question                                     | Topic                | Level |
|-----|----------------------------------------------|----------------------|-------|
| 1   | [Longest login streak](#q1-longest-login-streak-l3)             | Gaps and islands     | L3    |
| 2   | [Sessions with a 30-minute gap](#q2-sessions-with-a-30-minute-gap-l3)    | Gaps and islands     | L3    |
| 3   | [Running balance](#q3-running-balance-l2)                  | Window functions     | L2    |
| 4   | [First day in the red](#q4-first-day-in-the-red-l3)             | Window functions     | L3    |
| 5   | [Top 3 scores with ties](#q5-top-3-scores-with-ties-l2)           | Window functions     | L2    |
| 6   | [Median per group](#q6-median-per-group-l3)                 | Window functions     | L3    |
| 7   | [Split into halves (NTILE)](#q7-split-into-halves-ntile-l2)        | Window functions     | L2    |
| 8   | [Top and bottom per group](#q8-top-and-bottom-per-group-l3)         | Window functions     | L3    |
| 9   | [Time to next event](#q9-time-to-next-event-l2)               | Window functions     | L2    |
| 10  | [Gap to the leader](#q10-gap-to-the-leader-l2)                | Window functions     | L2    |
| 11  | [New users per day, cumulative](#q11-new-users-per-day-cumulative-l2)    | Window functions     | L2    |
| 12  | [Day-1 retention by cohort](#q12-day-1-retention-by-cohort-l3)        | Product analytics    | L3    |
| 13  | [Funnel in order](#q13-funnel-in-order-l3)                  | Product analytics    | L3    |
| 14  | [Spend rising every month](#q14-spend-rising-every-month-l3)         | Product analytics    | L3    |
| 15  | [Category path](#q15-category-path-l3)                    | Recursion            | L3    |
| 16  | [All descendants](#q16-all-descendants-l2)                  | Recursion            | L2    |
| 17  | [Fill missing days with zero](#q17-fill-missing-days-with-zero-l3)      | Recursion            | L3    |
| 18  | [Missing IDs](#q18-missing-ids-l2)                      | Recursion            | L2    |
| 19  | [Pivot months into columns](#q19-pivot-months-into-columns-l2)        | Reshaping            | L2    |
| 20  | [Histogram buckets](#q20-histogram-buckets-l2)                | Reshaping            | L2    |
| 21  | [Mutual follows](#q21-mutual-follows-l2)                   | Joins and sets       | L2    |
| 22  | [People you may know](#q22-people-you-may-know-l3)              | Joins and sets       | L3    |
| 23  | [Bought together](#q23-bought-together-l3)                  | Joins and sets       | L3    |
| 24  | [Overlapping bookings](#q24-overlapping-bookings-l3)             | Joins and sets       | L3    |
| 25  | [Latest row per key](#q25-latest-row-per-key-l2)               | Joins and sets       | L2    |
| 26  | [Swap adjacent seats](#q26-swap-adjacent-seats-l2)              | Joins and sets       | L2    |
| 27  | [Follow but not followed (EXCEPT)](#q27-follow-but-not-followed-except-l1) | Joins and sets       | L1    |
| 28  | [Active every month](#q28-active-every-month-l3)               | Joins and sets       | L3    |
| 29  | [Same category twice in a row](#q29-same-category-twice-in-a-row-l2)     | Window functions     | L2    |
| 30  | [Keyset pagination](#q30-keyset-pagination-l3)                | Performance patterns | L3    |

## The sample database

Small enough to check by hand. Meera (user 3) logs in twice on 2 January; user 4 buys without viewing; transaction ids 7 and 13 are missing; bookings 2 and 3, and 4 and 5, are back to back (not overlapping).

### users 6 rows

| id  | name  | signup_date | city   |
|-----|-------|-------------|--------|
| 1   | Asha  | 2024-01-01  | Delhi  |
| 2   | Ravi  | 2024-01-01  | Mumbai |
| 3   | Meera | 2024-01-02  | Delhi  |
| 4   | Kabir | 2024-02-03  | Pune   |
| 5   | Divya | 2024-02-10  | Mumbai |
| 6   | Arjun | 2024-02-15  | Delhi  |

### logins 17 rows

| user_id | day        |
|---------|------------|
| 1       | 2024-01-01 |
| 1       | 2024-01-02 |
| 1       | 2024-01-03 |
| 1       | 2024-01-05 |
| 1       | 2024-01-06 |
| 1       | 2024-01-10 |
| 2       | 2024-01-01 |
| 2       | 2024-01-03 |
| 2       | 2024-01-04 |
| 2       | 2024-01-05 |
| 2       | 2024-01-06 |
| 3       | 2024-01-02 |
| 3       | 2024-01-02 |
| 3       | 2024-01-03 |
| 4       | 2024-02-03 |
| 4       | 2024-02-04 |
| 5       | 2024-02-10 |

### events 11 rows

| user_id | ts               | type     |
|---------|------------------|----------|
| 1       | 2024-03-01 10:00 | view     |
| 1       | 2024-03-01 10:10 | cart     |
| 1       | 2024-03-01 10:50 | view     |
| 1       | 2024-03-01 10:55 | purchase |
| 2       | 2024-03-01 09:00 | view     |
| 2       | 2024-03-01 09:05 | view     |
| 2       | 2024-03-01 09:20 | cart     |
| 3       | 2024-03-02 12:00 | view     |
| 3       | 2024-03-02 12:31 | view     |
| 4       | 2024-03-02 08:00 | cart     |
| 4       | 2024-03-02 08:10 | purchase |

### txns 13 rows

| id  | user_id | day        | amount | category |
|-----|---------|------------|--------|----------|
| 1   | 1       | 2024-01-05 | 5000   | salary   |
| 2   | 1       | 2024-01-10 | -1200  | food     |
| 3   | 1       | 2024-01-20 | -4500  | rent     |
| 4   | 1       | 2024-02-03 | -800   | food     |
| 5   | 2       | 2024-01-06 | 3000   | salary   |
| 6   | 2       | 2024-02-07 | -500   | travel   |
| 8   | 2       | 2024-02-15 | -700   | food     |
| 9   | 2       | 2024-03-01 | -300   | food     |
| 10  | 3       | 2024-01-15 | -200   | food     |
| 11  | 3       | 2024-02-15 | -900   | travel   |
| 12  | 3       | 2024-03-15 | -1500  | rent     |
| 14  | 4       | 2024-03-02 | -2500  | rent     |
| 15  | 4       | 2024-03-09 | -2500  | rent     |

### follows 7 rows

| follower | followee |
|----------|----------|
| 1        | 2        |
| 2        | 1        |
| 1        | 3        |
| 3        | 4        |
| 4        | 3        |
| 2        | 3        |
| 5        | 1        |

### categories 7 rows

| id  | name           | parent_id |
|-----|----------------|-----------|
| 1   | Electronics    | NULL      |
| 2   | Phones         | 1         |
| 3   | Laptops        | 1         |
| 4   | Android        | 2         |
| 5   | Gaming laptops | 3         |
| 6   | Home           | NULL      |
| 7   | Kitchen        | 6         |

### bookings 6 rows

| id  | room | start_day  | end_day    |
|-----|------|------------|------------|
| 1   | A    | 2024-05-01 | 2024-05-04 |
| 2   | A    | 2024-05-03 | 2024-05-06 |
| 3   | A    | 2024-05-06 | 2024-05-08 |
| 4   | B    | 2024-05-01 | 2024-05-02 |
| 5   | B    | 2024-05-02 | 2024-05-05 |
| 6   | B    | 2024-05-04 | 2024-05-06 |

### basket 11 rows

| order_id | product |
|----------|---------|
| 1        | bread   |
| 1        | milk    |
| 1        | eggs    |
| 2        | bread   |
| 2        | milk    |
| 3        | milk    |
| 3        | eggs    |
| 4        | bread   |
| 4        | milk    |
| 4        | eggs    |
| 5        | tea     |

### profile_updates 5 rows

| user_id | updated_at | email       |
|---------|------------|-------------|
| 1       | 2024-01-01 | a@x.com     |
| 1       | 2024-03-01 | asha@x.com  |
| 2       | 2024-02-01 | r@x.com     |
| 3       | 2024-01-05 | m@x.com     |
| 3       | 2024-02-05 | meera@x.com |

### seats 5 rows

| id  | student |
|-----|---------|
| 1   | Abbot   |
| 2   | Doris   |
| 3   | Emerson |
| 4   | Green   |
| 5   | Jeames  |

### scores 9 rows

| student | subject | score |
|---------|---------|-------|
| Asha    | DSA     | 92    |
| Ravi    | DSA     | 75    |
| Meera   | DSA     | 88    |
| Kabir   | DSA     | 60    |
| Divya   | DSA     | 75    |
| Asha    | OS      | 70    |
| Ravi    | OS      | 85    |
| Meera   | OS      | 90    |
| Kabir   | OS      | 65    |

## Gaps and islands

### Q1. Longest login streak L3

For each user, the longest run of consecutive login days (a user can log in twice a day).

``` sql
WITH d AS (SELECT DISTINCT user_id, day FROM logins),
g AS (SELECT user_id, day,
        julianday(day) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS grp
      FROM d)
SELECT user_id, MAX(len) AS longest
FROM (SELECT user_id, grp, COUNT(*) AS len FROM g GROUP BY user_id, grp)
GROUP BY user_id ORDER BY user_id;
```

Output

| user_id | longest |
|---------|---------|
| 1       | 3       |
| 2       | 4       |
| 3       | 2       |
| 4       | 2       |
| 5       | 1       |

Day number minus row number is constant along a run of consecutive days, so it labels each island. DISTINCT first, or a double login breaks the trick.

### Q2. Sessions with a 30-minute gap L3

Split each user's events into sessions: a new session starts after more than 30 minutes of inactivity. Count sessions per user.

``` sql
WITH e AS (SELECT user_id, ts,
        (julianday(ts) - julianday(LAG(ts) OVER (PARTITION BY user_id ORDER BY ts))) * 1440 AS gap
      FROM events),
s AS (SELECT user_id, SUM(CASE WHEN gap IS NULL OR gap > 30 THEN 1 ELSE 0 END)
        OVER (PARTITION BY user_id ORDER BY ts) AS session_no FROM e)
SELECT user_id, MAX(session_no) AS sessions FROM s GROUP BY user_id ORDER BY user_id;
```

Output

| user_id | sessions |
|---------|----------|
| 1       | 2        |
| 2       | 1        |
| 3       | 2        |
| 4       | 1        |

Flag rows that start a session (first row or gap \> 30), then a running SUM of the flags numbers the sessions. julianday differences are in days; × 1440 gives minutes.

## Window functions

### Q3. Running balance L2

Show user 1's transactions with the balance after each one.

``` sql
SELECT id, day, amount,
       SUM(amount) OVER (PARTITION BY user_id ORDER BY day, id) AS balance
FROM txns WHERE user_id = 1 ORDER BY day, id;
```

Output

| id  | day        | amount | balance |
|-----|------------|--------|---------|
| 1   | 2024-01-05 | 5000   | 5000    |
| 2   | 2024-01-10 | -1200  | 3800    |
| 3   | 2024-01-20 | -4500  | -700    |
| 4   | 2024-02-03 | -800   | -1500   |

A running SUM ordered by day; add id as a tie-breaker so two transactions on one day still get a deterministic order.

### Q4. First day in the red L3

For each user whose balance ever goes negative, the first day it does.

``` sql
WITH b AS (SELECT user_id, day,
        SUM(amount) OVER (PARTITION BY user_id ORDER BY day, id) AS bal FROM txns)
SELECT user_id, MIN(day) AS first_negative FROM b WHERE bal < 0
GROUP BY user_id ORDER BY user_id;
```

Output

| user_id | first_negative |
|---------|----------------|
| 1       | 2024-01-20     |
| 3       | 2024-01-15     |
| 4       | 2024-03-02     |

Compute the running balance first (a window cannot go in WHERE), then filter and take the earliest day.

### Q5. Top 3 scores with ties L2

Per subject, everyone whose score is among the top 3 distinct scores.

``` sql
SELECT subject, student, score FROM (
  SELECT *, DENSE_RANK() OVER (PARTITION BY subject ORDER BY score DESC) AS r FROM scores)
WHERE r <= 3 ORDER BY subject, score DESC, student;
```

Output

| subject | student | score |
|---------|---------|-------|
| DSA     | Asha    | 92    |
| DSA     | Meera   | 88    |
| DSA     | Divya   | 75    |
| DSA     | Ravi    | 75    |
| OS      | Meera   | 90    |
| OS      | Ravi    | 85    |
| OS      | Asha    | 70    |

DENSE_RANK keeps ties and does not skip ranks, so two 75s both count as third. ROW_NUMBER would drop one; RANK would number the next score 5.

### Q6. Median per group L3

Median score per subject (average the middle two when the count is even).

``` sql
WITH r AS (SELECT subject, score,
        ROW_NUMBER() OVER (PARTITION BY subject ORDER BY score) AS rn,
        COUNT(*) OVER (PARTITION BY subject) AS n FROM scores)
SELECT subject, AVG(score) AS median FROM r
WHERE rn IN ((n + 1) / 2, (n + 2) / 2)
GROUP BY subject ORDER BY subject;
```

Output

| subject | median |
|---------|--------|
| DSA     | 75     |
| OS      | 77.5   |

With integer division, (n+1)/2 and (n+2)/2 are the same row when n is odd and the two middle rows when n is even. PostgreSQL has PERCENTILE_CONT(0.5).

### Q7. Split into halves (NTILE) L2

Split the DSA class into a top half and a bottom half by score (ties broken by name).

``` sql
SELECT student, score,
       NTILE(2) OVER (ORDER BY score DESC, student) AS half
FROM scores WHERE subject = 'DSA' ORDER BY half, score DESC, student;
```

Output

| student | score | half |
|---------|-------|------|
| Asha    | 92    | 1    |
| Meera   | 88    | 1    |
| Divya   | 75    | 1    |
| Ravi    | 75    | 2    |
| Kabir   | 60    | 2    |

NTILE(k) deals rows into k nearly equal buckets in order; with 5 rows and 2 buckets the first gets 3. Quartiles are NTILE(4).

### Q8. Top and bottom per group L3

For each subject, its top and bottom scorer, using FIRST_VALUE and LAST_VALUE.

``` sql
SELECT DISTINCT subject,
  FIRST_VALUE(student) OVER w AS top,
  LAST_VALUE(student) OVER w AS bottom
FROM scores
WINDOW w AS (PARTITION BY subject ORDER BY score DESC, student
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
ORDER BY subject;
```

Output

| subject | top   | bottom |
|---------|-------|--------|
| DSA     | Asha  | Kabir  |
| OS      | Meera | Kabir  |

LAST_VALUE needs the explicit frame: the default frame ends at the current row, so it would just return the current student.

### Q9. Time to next event L2

For user 1, minutes from each event to the next one.

``` sql
SELECT ts, type,
  CAST(ROUND((julianday(LEAD(ts) OVER (ORDER BY ts)) - julianday(ts)) * 1440) AS INTEGER) AS mins_to_next
FROM events WHERE user_id = 1 ORDER BY ts;
```

Output

| ts               | type     | mins_to_next |
|------------------|----------|--------------|
| 2024-03-01 10:00 | view     | 10           |
| 2024-03-01 10:10 | cart     | 40           |
| 2024-03-01 10:50 | view     | 5            |
| 2024-03-01 10:55 | purchase | NULL         |

LEAD looks one row ahead; the last row has no next event, so it is NULL. ROUND avoids floating-point noise before the cast.

### Q10. Gap to the leader L2

Show each score and how far it is behind the subject's top score.

``` sql
SELECT subject, student, score,
       MAX(score) OVER (PARTITION BY subject) - score AS behind
FROM scores ORDER BY subject, behind, student;
```

Output

| subject | student | score | behind |
|---------|---------|-------|--------|
| DSA     | Asha    | 92    | 0      |
| DSA     | Meera   | 88    | 4      |
| DSA     | Divya   | 75    | 17     |
| DSA     | Ravi    | 75    | 17     |
| DSA     | Kabir   | 60    | 32     |
| OS      | Meera   | 90    | 0      |
| OS      | Ravi    | 85    | 5      |
| OS      | Asha    | 70    | 20     |
| OS      | Kabir   | 65    | 25     |

An aggregate with OVER keeps every row and adds the group's value to it, so no self-join or subquery is needed.

### Q11. New users per day, cumulative L2

For each day on which someone logged in for the first time: how many new users, and the running total.

``` sql
WITH f AS (SELECT user_id, MIN(day) AS first_day FROM logins GROUP BY user_id)
SELECT first_day, COUNT(*) AS new_users,
       SUM(COUNT(*)) OVER (ORDER BY first_day) AS total_users
FROM f GROUP BY first_day ORDER BY first_day;
```

Output

| first_day  | new_users | total_users |
|------------|-----------|-------------|
| 2024-01-01 | 2         | 2           |
| 2024-01-02 | 1         | 3           |
| 2024-02-03 | 1         | 4           |
| 2024-02-10 | 1         | 5           |

Cumulative distinct counts: find each user's first day, then a running sum of new users. A window over an aggregate (SUM(COUNT(\*)) OVER) runs after GROUP BY.

## Product analytics

### Q12. Day-1 retention by cohort L3

For each signup month, the percentage of users who logged in on the day after signing up.

``` sql
SELECT strftime('%Y-%m', u.signup_date) AS cohort, COUNT(*) AS users,
  ROUND(100.0 * SUM(EXISTS (SELECT 1 FROM logins l WHERE l.user_id = u.id
        AND l.day = date(u.signup_date, '+1 day'))) / COUNT(*), 1) AS day1_pct
FROM users u GROUP BY cohort ORDER BY cohort;
```

Output

| cohort  | users | day1_pct |
|---------|-------|----------|
| 2024-01 | 3     | 66.7     |
| 2024-02 | 3     | 33.3     |

EXISTS returns 1 or 0, so SUM counts retained users. Multiply by 100.0 (not 100) to avoid integer division.

### Q13. Funnel in order L3

How many users viewed, then added to cart after a view, then purchased after that cart?

``` sql
WITH v AS (SELECT user_id, MIN(ts) AS t FROM events WHERE type = 'view' GROUP BY user_id),
c AS (SELECT e.user_id, MIN(e.ts) AS t FROM events e JOIN v ON v.user_id = e.user_id AND e.ts > v.t
      WHERE e.type = 'cart' GROUP BY e.user_id),
p AS (SELECT e.user_id FROM events e JOIN c ON c.user_id = e.user_id AND e.ts > c.t
      WHERE e.type = 'purchase' GROUP BY e.user_id)
SELECT (SELECT COUNT(*) FROM v) AS viewed, (SELECT COUNT(*) FROM c) AS carted, (SELECT COUNT(*) FROM p) AS purchased;
```

Output

| viewed | carted | purchased |
|--------|--------|-----------|
| 3      | 2      | 1         |

Each step joins on the previous step's time, so out-of-order events (user 4 bought without viewing) do not count.

### Q14. Spend rising every month L3

Users whose monthly spending (debits) went up every month, with at least two months.

``` sql
WITH m AS (SELECT user_id, strftime('%Y-%m', day) AS mon, -SUM(amount) AS spend
      FROM txns WHERE amount < 0 GROUP BY user_id, mon),
d AS (SELECT user_id, spend - LAG(spend) OVER (PARTITION BY user_id ORDER BY mon) AS diff FROM m)
SELECT u.name FROM d JOIN users u ON u.id = d.user_id
GROUP BY d.user_id HAVING COUNT(*) >= 2 AND MIN(diff) > 0 ORDER BY u.name;
```

Output

| name  |
|-------|
| Meera |

LAG gives month-on-month change; every change positive means MIN(diff) \> 0 (MIN ignores the first month's NULL). COUNT(\*) ≥ 2 enforces two months.

## Recursion

### Q15. Category path L3

Show every category with its full path from the root and its depth.

``` sql
WITH RECURSIVE t(id, name, path, depth) AS (
  SELECT id, name, name, 0 FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.name, t.path || ' > ' || c.name, t.depth + 1
  FROM categories c JOIN t ON c.parent_id = t.id)
SELECT path, depth FROM t ORDER BY path;
```

Output

| path                                     | depth |
|------------------------------------------|-------|
| Electronics                              | 0     |
| Electronics \> Laptops                   | 1     |
| Electronics \> Laptops \> Gaming laptops | 2     |
| Electronics \> Phones                    | 1     |
| Electronics \> Phones \> Android         | 2     |
| Home                                     | 0     |
| Home \> Kitchen                          | 1     |

Anchor the roots, then repeatedly join children to the rows found so far. The path is built as text on the way down.

### Q16. All descendants L2

List every category under Electronics, at any depth.

``` sql
WITH RECURSIVE sub(id) AS (
  SELECT id FROM categories WHERE name = 'Electronics'
  UNION ALL
  SELECT c.id FROM categories c JOIN sub ON c.parent_id = sub.id)
SELECT name FROM categories WHERE id IN (SELECT id FROM sub) AND name <> 'Electronics' ORDER BY name;
```

Output

| name           |
|----------------|
| Android        |
| Gaming laptops |
| Laptops        |
| Phones         |

Same pattern as an org chart ('everyone under this manager'). UNION ALL is fine for a tree; use UNION to stop cycles in a graph.

### Q17. Fill missing days with zero L3

Distinct users who logged in on each day from 1 to 7 January 2024, showing 0 for days with none.

``` sql
WITH RECURSIVE days(d) AS (
  SELECT '2024-01-01' UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < '2024-01-07')
SELECT d AS day, COUNT(DISTINCT l.user_id) AS users
FROM days LEFT JOIN logins l ON l.day = d
GROUP BY d ORDER BY d;
```

Output

| day        | users |
|------------|-------|
| 2024-01-01 | 2     |
| 2024-01-02 | 2     |
| 2024-01-03 | 3     |
| 2024-01-04 | 1     |
| 2024-01-05 | 2     |
| 2024-01-06 | 2     |
| 2024-01-07 | 0     |

Generate the calendar, then LEFT JOIN the data onto it. COUNT(column) counts only matches, so empty days get 0.

### Q18. Missing IDs L2

Which transaction IDs between the smallest and largest are missing?

``` sql
WITH RECURSIVE n(i) AS (
  SELECT MIN(id) FROM txns UNION ALL SELECT i + 1 FROM n WHERE i < (SELECT MAX(id) FROM txns))
SELECT i AS missing_id FROM n WHERE i NOT IN (SELECT id FROM txns) ORDER BY i;
```

Output

| missing_id |
|------------|
| 7          |
| 13         |

A number series plus an anti-join. Alternative without recursion: rows where LEAD(id) − id \> 1 give the start of each gap.

## Reshaping

### Q19. Pivot months into columns L2

Monthly spending (debits) per user, one column per month, 0 where none.

``` sql
SELECT user_id,
  -SUM(CASE WHEN strftime('%m', day) = '01' AND amount < 0 THEN amount ELSE 0 END) AS jan,
  -SUM(CASE WHEN strftime('%m', day) = '02' AND amount < 0 THEN amount ELSE 0 END) AS feb,
  -SUM(CASE WHEN strftime('%m', day) = '03' AND amount < 0 THEN amount ELSE 0 END) AS mar
FROM txns GROUP BY user_id ORDER BY user_id;
```

Output

| user_id | jan  | feb  | mar  |
|---------|------|------|------|
| 1       | 5700 | 800  | 0    |
| 2       | 0    | 1200 | 300  |
| 3       | 200  | 900  | 1500 |
| 4       | 0    | 0    | 5000 |

Conditional aggregation is the portable pivot: one SUM(CASE …) per output column. SQL Server and Oracle also have a PIVOT clause.

### Q20. Histogram buckets L2

How many debits fall in each size bucket: under 1,000, 1,000–2,999, and 3,000 or more?

``` sql
SELECT CASE WHEN -amount < 1000 THEN '1: under 1000'
            WHEN -amount < 3000 THEN '2: 1000-2999'
            ELSE '3: 3000+' END AS bucket, COUNT(*) AS debits
FROM txns WHERE amount < 0 GROUP BY bucket ORDER BY bucket;
```

Output

| bucket        | debits |
|---------------|--------|
| 1: under 1000 | 6      |
| 2: 1000-2999  | 4      |
| 3: 3000+      | 1      |

Bucket with CASE, then GROUP BY the label. The number prefix keeps the buckets in order when sorted as text.

## Joins and sets

### Q21. Mutual follows L2

Pairs of users who follow each other, each pair once.

``` sql
SELECT a.follower AS user_a, a.followee AS user_b
FROM follows a JOIN follows b ON b.follower = a.followee AND b.followee = a.follower
WHERE a.follower < a.followee ORDER BY user_a, user_b;
```

Output

| user_a | user_b |
|--------|--------|
| 1      | 2      |
| 3      | 4      |

Self-join each edge to its reverse; follower \< followee keeps one copy of each pair.

### Q22. People you may know L3

Suggest accounts for user 1: followed by people user 1 follows, not already followed, not user 1; rank by how many such paths.

``` sql
SELECT f2.followee AS suggest, COUNT(*) AS via
FROM follows f1 JOIN follows f2 ON f2.follower = f1.followee
WHERE f1.follower = 1 AND f2.followee <> 1
  AND f2.followee NOT IN (SELECT followee FROM follows WHERE follower = 1)
GROUP BY f2.followee ORDER BY via DESC, suggest;
```

Output

| suggest | via |
|---------|-----|
| 4       | 1   |

Two hops through the graph, then remove yourself and people you already follow. COUNT(\*) is the number of mutual connections.

### Q23. Bought together L3

Pairs of products in the same order at least twice, most frequent first.

``` sql
SELECT a.product AS p1, b.product AS p2, COUNT(*) AS orders
FROM basket a JOIN basket b ON a.order_id = b.order_id AND a.product < b.product
GROUP BY p1, p2 HAVING COUNT(*) >= 2 ORDER BY orders DESC, p1, p2;
```

Output

| p1    | p2   | orders |
|-------|------|--------|
| bread | milk | 3      |
| eggs  | milk | 3      |
| bread | eggs | 2      |

Self-join on the order with a.product \< b.product so each unordered pair appears once per order (market-basket analysis).

### Q24. Overlapping bookings L3

Find pairs of bookings in the same room that overlap (end days are exclusive).

``` sql
SELECT a.id AS booking_a, b.id AS booking_b, a.room
FROM bookings a JOIN bookings b
  ON a.room = b.room AND a.id < b.id
 AND a.start_day < b.end_day AND b.start_day < a.end_day
ORDER BY a.id, b.id;
```

Output

| booking_a | booking_b | room |
|-----------|-----------|------|
| 1         | 2         | A    |
| 5         | 6         | B    |

Two intervals overlap exactly when each starts before the other ends. With exclusive ends, back-to-back bookings (one ends the day the next starts) do not overlap.

### Q25. Latest row per key L2

Each user's current email (the most recent update).

``` sql
SELECT user_id, email FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) AS rn
  FROM profile_updates)
WHERE rn = 1 ORDER BY user_id;
```

Output

| user_id | email       |
|---------|-------------|
| 1       | asha@x.com  |
| 2       | r@x.com     |
| 3       | meera@x.com |

The standard deduplication pattern. Add a tie-breaker to ORDER BY if two updates can share a timestamp.

### Q26. Swap adjacent seats L2

Swap every pair of adjacent students (1↔2, 3↔4, …); an odd last seat stays put.

``` sql
SELECT CASE WHEN id % 2 = 1 AND id = (SELECT MAX(id) FROM seats) THEN id
            WHEN id % 2 = 1 THEN id + 1 ELSE id - 1 END AS id, student
FROM seats ORDER BY id;
```

Output

| id  | student |
|-----|---------|
| 1   | Doris   |
| 2   | Abbot   |
| 3   | Green   |
| 4   | Emerson |
| 5   | Jeames  |

Rewrite the ids rather than moving rows: odd ids go up one, even ids down one, except a final odd id.

### Q27. Follow but not followed (EXCEPT) L1

Users who follow someone but whom nobody follows.

``` sql
SELECT follower AS user_id FROM follows
EXCEPT
SELECT followee FROM follows ORDER BY user_id;
```

Output

| user_id |
|---------|
| 5       |

EXCEPT returns distinct rows from the first query that are not in the second (MINUS in Oracle). INTERSECT keeps rows in both.

### Q28. Active every month L3

Users with at least one transaction in every month that has any transactions.

``` sql
SELECT user_id FROM txns
GROUP BY user_id
HAVING COUNT(DISTINCT strftime('%Y-%m', day)) =
       (SELECT COUNT(DISTINCT strftime('%Y-%m', day)) FROM txns)
ORDER BY user_id;
```

Output

| user_id |
|---------|
| 2       |
| 3       |

Relational division by counting: a user covers every month when their distinct-month count equals the total.

## Window functions

### Q29. Same category twice in a row L2

Transactions in the same category as the same user's previous transaction.

``` sql
SELECT id, user_id, category FROM (
  SELECT *, LAG(category) OVER (PARTITION BY user_id ORDER BY day, id) AS prev FROM txns)
WHERE category = prev ORDER BY id;
```

Output

| id  | user_id | category |
|-----|---------|----------|
| 9   | 2       | food     |
| 15  | 4       | rent     |

Compare each row with the previous one using LAG; the first row per user has prev NULL, and NULL = anything is never true.

## Performance patterns

### Q30. Keyset pagination L3

Ordered by score (high first), then student, then subject, return the 3 rows after (85, 'Ravi', 'OS').

``` sql
SELECT score, student, subject FROM scores
WHERE score < 85 OR (score = 85 AND (student, subject) > ('Ravi', 'OS'))
ORDER BY score DESC, student, subject LIMIT 3;
```

Output

| score | student | subject |
|-------|---------|---------|
| 75    | Divya   | DSA     |
| 75    | Ravi    | DSA     |
| 70    | Asha    | OS      |

Seek pagination: filter past the last row seen instead of OFFSET, so an index can jump straight there and pages do not shift when rows are inserted. Row values ((a, b) \> (x, y)) work in SQLite, PostgreSQL and MySQL.
