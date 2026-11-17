-- SQL interview pack II: sample database and 30 harder questions. Tested with SQLite 3.53.1.
-- Load: sqlite3 practice2.db < sql-pack-2.sql   (or paste the schema into any SQL playground)

CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, signup_date TEXT, city TEXT);
CREATE TABLE logins (user_id INTEGER, day TEXT);
CREATE TABLE events (user_id INTEGER, ts TEXT, type TEXT);
CREATE TABLE txns (id INTEGER PRIMARY KEY, user_id INTEGER, day TEXT, amount INTEGER, category TEXT);
CREATE TABLE follows (follower INTEGER, followee INTEGER);
CREATE TABLE categories (id INTEGER PRIMARY KEY, name TEXT, parent_id INTEGER);
CREATE TABLE bookings (id INTEGER PRIMARY KEY, room TEXT, start_day TEXT, end_day TEXT);
CREATE TABLE basket (order_id INTEGER, product TEXT);
CREATE TABLE profile_updates (user_id INTEGER, updated_at TEXT, email TEXT);
CREATE TABLE seats (id INTEGER PRIMARY KEY, student TEXT);
CREATE TABLE scores (student TEXT, subject TEXT, score INTEGER);

INSERT INTO users VALUES (1,'Asha','2024-01-01','Delhi'),(2,'Ravi','2024-01-01','Mumbai'),(3,'Meera','2024-01-02','Delhi'),(4,'Kabir','2024-02-03','Pune'),(5,'Divya','2024-02-10','Mumbai'),(6,'Arjun','2024-02-15','Delhi');
INSERT INTO logins VALUES (1,'2024-01-01'),(1,'2024-01-02'),(1,'2024-01-03'),(1,'2024-01-05'),(1,'2024-01-06'),(1,'2024-01-10'),(2,'2024-01-01'),(2,'2024-01-03'),(2,'2024-01-04'),(2,'2024-01-05'),(2,'2024-01-06'),(3,'2024-01-02'),(3,'2024-01-02'),(3,'2024-01-03'),(4,'2024-02-03'),(4,'2024-02-04'),(5,'2024-02-10');
INSERT INTO events VALUES (1,'2024-03-01 10:00','view'),(1,'2024-03-01 10:10','cart'),(1,'2024-03-01 10:50','view'),(1,'2024-03-01 10:55','purchase'),(2,'2024-03-01 09:00','view'),(2,'2024-03-01 09:05','view'),(2,'2024-03-01 09:20','cart'),(3,'2024-03-02 12:00','view'),(3,'2024-03-02 12:31','view'),(4,'2024-03-02 08:00','cart'),(4,'2024-03-02 08:10','purchase');
INSERT INTO txns VALUES (1,1,'2024-01-05',5000,'salary'),(2,1,'2024-01-10',-1200,'food'),(3,1,'2024-01-20',-4500,'rent'),(4,1,'2024-02-03',-800,'food'),(5,2,'2024-01-06',3000,'salary'),(6,2,'2024-02-07',-500,'travel'),(8,2,'2024-02-15',-700,'food'),(9,2,'2024-03-01',-300,'food'),(10,3,'2024-01-15',-200,'food'),(11,3,'2024-02-15',-900,'travel'),(12,3,'2024-03-15',-1500,'rent'),(14,4,'2024-03-02',-2500,'rent'),(15,4,'2024-03-09',-2500,'rent');
INSERT INTO follows VALUES (1,2),(2,1),(1,3),(3,4),(4,3),(2,3),(5,1);
INSERT INTO categories VALUES (1,'Electronics',NULL),(2,'Phones',1),(3,'Laptops',1),(4,'Android',2),(5,'Gaming laptops',3),(6,'Home',NULL),(7,'Kitchen',6);
INSERT INTO bookings VALUES (1,'A','2024-05-01','2024-05-04'),(2,'A','2024-05-03','2024-05-06'),(3,'A','2024-05-06','2024-05-08'),(4,'B','2024-05-01','2024-05-02'),(5,'B','2024-05-02','2024-05-05'),(6,'B','2024-05-04','2024-05-06');
INSERT INTO basket VALUES (1,'bread'),(1,'milk'),(1,'eggs'),(2,'bread'),(2,'milk'),(3,'milk'),(3,'eggs'),(4,'bread'),(4,'milk'),(4,'eggs'),(5,'tea');
INSERT INTO profile_updates VALUES (1,'2024-01-01','a@x.com'),(1,'2024-03-01','asha@x.com'),(2,'2024-02-01','r@x.com'),(3,'2024-01-05','m@x.com'),(3,'2024-02-05','meera@x.com');
INSERT INTO seats VALUES (1,'Abbot'),(2,'Doris'),(3,'Emerson'),(4,'Green'),(5,'Jeames');
INSERT INTO scores VALUES ('Asha','DSA',92),('Ravi','DSA',75),('Meera','DSA',88),('Kabir','DSA',60),('Divya','DSA',75),('Asha','OS',70),('Ravi','OS',85),('Meera','OS',90),('Kabir','OS',65);

-- Q1. Longest login streak [Gaps and islands, L3]
-- For each user, the longest run of consecutive login days (a user can log in twice a day).
WITH d AS (SELECT DISTINCT user_id, day FROM logins),
g AS (SELECT user_id, day,
        julianday(day) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS grp
      FROM d)
SELECT user_id, MAX(len) AS longest
FROM (SELECT user_id, grp, COUNT(*) AS len FROM g GROUP BY user_id, grp)
GROUP BY user_id ORDER BY user_id;

-- Q2. Sessions with a 30-minute gap [Gaps and islands, L3]
-- Split each user's events into sessions: a new session starts after more than 30 minutes of inactivity. Count sessions per user.
WITH e AS (SELECT user_id, ts,
        (julianday(ts) - julianday(LAG(ts) OVER (PARTITION BY user_id ORDER BY ts))) * 1440 AS gap
      FROM events),
s AS (SELECT user_id, SUM(CASE WHEN gap IS NULL OR gap > 30 THEN 1 ELSE 0 END)
        OVER (PARTITION BY user_id ORDER BY ts) AS session_no FROM e)
SELECT user_id, MAX(session_no) AS sessions FROM s GROUP BY user_id ORDER BY user_id;

-- Q3. Running balance [Window functions, L2]
-- Show user 1's transactions with the balance after each one.
SELECT id, day, amount,
       SUM(amount) OVER (PARTITION BY user_id ORDER BY day, id) AS balance
FROM txns WHERE user_id = 1 ORDER BY day, id;

-- Q4. First day in the red [Window functions, L3]
-- For each user whose balance ever goes negative, the first day it does.
WITH b AS (SELECT user_id, day,
        SUM(amount) OVER (PARTITION BY user_id ORDER BY day, id) AS bal FROM txns)
SELECT user_id, MIN(day) AS first_negative FROM b WHERE bal < 0
GROUP BY user_id ORDER BY user_id;

-- Q5. Top 3 scores with ties [Window functions, L2]
-- Per subject, everyone whose score is among the top 3 distinct scores.
SELECT subject, student, score FROM (
  SELECT *, DENSE_RANK() OVER (PARTITION BY subject ORDER BY score DESC) AS r FROM scores)
WHERE r <= 3 ORDER BY subject, score DESC, student;

-- Q6. Median per group [Window functions, L3]
-- Median score per subject (average the middle two when the count is even).
WITH r AS (SELECT subject, score,
        ROW_NUMBER() OVER (PARTITION BY subject ORDER BY score) AS rn,
        COUNT(*) OVER (PARTITION BY subject) AS n FROM scores)
SELECT subject, AVG(score) AS median FROM r
WHERE rn IN ((n + 1) / 2, (n + 2) / 2)
GROUP BY subject ORDER BY subject;

-- Q7. Split into halves (NTILE) [Window functions, L2]
-- Split the DSA class into a top half and a bottom half by score (ties broken by name).
SELECT student, score,
       NTILE(2) OVER (ORDER BY score DESC, student) AS half
FROM scores WHERE subject = 'DSA' ORDER BY half, score DESC, student;

-- Q8. Top and bottom per group [Window functions, L3]
-- For each subject, its top and bottom scorer, using FIRST_VALUE and LAST_VALUE.
SELECT DISTINCT subject,
  FIRST_VALUE(student) OVER w AS top,
  LAST_VALUE(student) OVER w AS bottom
FROM scores
WINDOW w AS (PARTITION BY subject ORDER BY score DESC, student
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
ORDER BY subject;

-- Q9. Time to next event [Window functions, L2]
-- For user 1, minutes from each event to the next one.
SELECT ts, type,
  CAST(ROUND((julianday(LEAD(ts) OVER (ORDER BY ts)) - julianday(ts)) * 1440) AS INTEGER) AS mins_to_next
FROM events WHERE user_id = 1 ORDER BY ts;

-- Q10. Gap to the leader [Window functions, L2]
-- Show each score and how far it is behind the subject's top score.
SELECT subject, student, score,
       MAX(score) OVER (PARTITION BY subject) - score AS behind
FROM scores ORDER BY subject, behind, student;

-- Q11. New users per day, cumulative [Window functions, L2]
-- For each day on which someone logged in for the first time: how many new users, and the running total.
WITH f AS (SELECT user_id, MIN(day) AS first_day FROM logins GROUP BY user_id)
SELECT first_day, COUNT(*) AS new_users,
       SUM(COUNT(*)) OVER (ORDER BY first_day) AS total_users
FROM f GROUP BY first_day ORDER BY first_day;

-- Q12. Day-1 retention by cohort [Product analytics, L3]
-- For each signup month, the percentage of users who logged in on the day after signing up.
SELECT strftime('%Y-%m', u.signup_date) AS cohort, COUNT(*) AS users,
  ROUND(100.0 * SUM(EXISTS (SELECT 1 FROM logins l WHERE l.user_id = u.id
        AND l.day = date(u.signup_date, '+1 day'))) / COUNT(*), 1) AS day1_pct
FROM users u GROUP BY cohort ORDER BY cohort;

-- Q13. Funnel in order [Product analytics, L3]
-- How many users viewed, then added to cart after a view, then purchased after that cart?
WITH v AS (SELECT user_id, MIN(ts) AS t FROM events WHERE type = 'view' GROUP BY user_id),
c AS (SELECT e.user_id, MIN(e.ts) AS t FROM events e JOIN v ON v.user_id = e.user_id AND e.ts > v.t
      WHERE e.type = 'cart' GROUP BY e.user_id),
p AS (SELECT e.user_id FROM events e JOIN c ON c.user_id = e.user_id AND e.ts > c.t
      WHERE e.type = 'purchase' GROUP BY e.user_id)
SELECT (SELECT COUNT(*) FROM v) AS viewed, (SELECT COUNT(*) FROM c) AS carted, (SELECT COUNT(*) FROM p) AS purchased;

-- Q14. Spend rising every month [Product analytics, L3]
-- Users whose monthly spending (debits) went up every month, with at least two months.
WITH m AS (SELECT user_id, strftime('%Y-%m', day) AS mon, -SUM(amount) AS spend
      FROM txns WHERE amount < 0 GROUP BY user_id, mon),
d AS (SELECT user_id, spend - LAG(spend) OVER (PARTITION BY user_id ORDER BY mon) AS diff FROM m)
SELECT u.name FROM d JOIN users u ON u.id = d.user_id
GROUP BY d.user_id HAVING COUNT(*) >= 2 AND MIN(diff) > 0 ORDER BY u.name;

-- Q15. Category path [Recursion, L3]
-- Show every category with its full path from the root and its depth.
WITH RECURSIVE t(id, name, path, depth) AS (
  SELECT id, name, name, 0 FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.name, t.path || ' > ' || c.name, t.depth + 1
  FROM categories c JOIN t ON c.parent_id = t.id)
SELECT path, depth FROM t ORDER BY path;

-- Q16. All descendants [Recursion, L2]
-- List every category under Electronics, at any depth.
WITH RECURSIVE sub(id) AS (
  SELECT id FROM categories WHERE name = 'Electronics'
  UNION ALL
  SELECT c.id FROM categories c JOIN sub ON c.parent_id = sub.id)
SELECT name FROM categories WHERE id IN (SELECT id FROM sub) AND name <> 'Electronics' ORDER BY name;

-- Q17. Fill missing days with zero [Recursion, L3]
-- Distinct users who logged in on each day from 1 to 7 January 2024, showing 0 for days with none.
WITH RECURSIVE days(d) AS (
  SELECT '2024-01-01' UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < '2024-01-07')
SELECT d AS day, COUNT(DISTINCT l.user_id) AS users
FROM days LEFT JOIN logins l ON l.day = d
GROUP BY d ORDER BY d;

-- Q18. Missing IDs [Recursion, L2]
-- Which transaction IDs between the smallest and largest are missing?
WITH RECURSIVE n(i) AS (
  SELECT MIN(id) FROM txns UNION ALL SELECT i + 1 FROM n WHERE i < (SELECT MAX(id) FROM txns))
SELECT i AS missing_id FROM n WHERE i NOT IN (SELECT id FROM txns) ORDER BY i;

-- Q19. Pivot months into columns [Reshaping, L2]
-- Monthly spending (debits) per user, one column per month, 0 where none.
SELECT user_id,
  -SUM(CASE WHEN strftime('%m', day) = '01' AND amount < 0 THEN amount ELSE 0 END) AS jan,
  -SUM(CASE WHEN strftime('%m', day) = '02' AND amount < 0 THEN amount ELSE 0 END) AS feb,
  -SUM(CASE WHEN strftime('%m', day) = '03' AND amount < 0 THEN amount ELSE 0 END) AS mar
FROM txns GROUP BY user_id ORDER BY user_id;

-- Q20. Histogram buckets [Reshaping, L2]
-- How many debits fall in each size bucket: under 1,000, 1,000–2,999, and 3,000 or more?
SELECT CASE WHEN -amount < 1000 THEN '1: under 1000'
            WHEN -amount < 3000 THEN '2: 1000-2999'
            ELSE '3: 3000+' END AS bucket, COUNT(*) AS debits
FROM txns WHERE amount < 0 GROUP BY bucket ORDER BY bucket;

-- Q21. Mutual follows [Joins and sets, L2]
-- Pairs of users who follow each other, each pair once.
SELECT a.follower AS user_a, a.followee AS user_b
FROM follows a JOIN follows b ON b.follower = a.followee AND b.followee = a.follower
WHERE a.follower < a.followee ORDER BY user_a, user_b;

-- Q22. People you may know [Joins and sets, L3]
-- Suggest accounts for user 1: followed by people user 1 follows, not already followed, not user 1; rank by how many such paths.
SELECT f2.followee AS suggest, COUNT(*) AS via
FROM follows f1 JOIN follows f2 ON f2.follower = f1.followee
WHERE f1.follower = 1 AND f2.followee <> 1
  AND f2.followee NOT IN (SELECT followee FROM follows WHERE follower = 1)
GROUP BY f2.followee ORDER BY via DESC, suggest;

-- Q23. Bought together [Joins and sets, L3]
-- Pairs of products in the same order at least twice, most frequent first.
SELECT a.product AS p1, b.product AS p2, COUNT(*) AS orders
FROM basket a JOIN basket b ON a.order_id = b.order_id AND a.product < b.product
GROUP BY p1, p2 HAVING COUNT(*) >= 2 ORDER BY orders DESC, p1, p2;

-- Q24. Overlapping bookings [Joins and sets, L3]
-- Find pairs of bookings in the same room that overlap (end days are exclusive).
SELECT a.id AS booking_a, b.id AS booking_b, a.room
FROM bookings a JOIN bookings b
  ON a.room = b.room AND a.id < b.id
 AND a.start_day < b.end_day AND b.start_day < a.end_day
ORDER BY a.id, b.id;

-- Q25. Latest row per key [Joins and sets, L2]
-- Each user's current email (the most recent update).
SELECT user_id, email FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) AS rn
  FROM profile_updates)
WHERE rn = 1 ORDER BY user_id;

-- Q26. Swap adjacent seats [Joins and sets, L2]
-- Swap every pair of adjacent students (1↔2, 3↔4, …); an odd last seat stays put.
SELECT CASE WHEN id % 2 = 1 AND id = (SELECT MAX(id) FROM seats) THEN id
            WHEN id % 2 = 1 THEN id + 1 ELSE id - 1 END AS id, student
FROM seats ORDER BY id;

-- Q27. Follow but not followed (EXCEPT) [Joins and sets, L1]
-- Users who follow someone but whom nobody follows.
SELECT follower AS user_id FROM follows
EXCEPT
SELECT followee FROM follows ORDER BY user_id;

-- Q28. Active every month [Joins and sets, L3]
-- Users with at least one transaction in every month that has any transactions.
SELECT user_id FROM txns
GROUP BY user_id
HAVING COUNT(DISTINCT strftime('%Y-%m', day)) =
       (SELECT COUNT(DISTINCT strftime('%Y-%m', day)) FROM txns)
ORDER BY user_id;

-- Q29. Same category twice in a row [Window functions, L2]
-- Transactions in the same category as the same user's previous transaction.
SELECT id, user_id, category FROM (
  SELECT *, LAG(category) OVER (PARTITION BY user_id ORDER BY day, id) AS prev FROM txns)
WHERE category = prev ORDER BY id;

-- Q30. Keyset pagination [Performance patterns, L3]
-- Ordered by score (high first), then student, then subject, return the 3 rows after (85, 'Ravi', 'OS').
SELECT score, student, subject FROM scores
WHERE score < 85 OR (score = 85 AND (student, subject) > ('Ravi', 'OS'))
ORDER BY score DESC, student, subject LIMIT 3;
