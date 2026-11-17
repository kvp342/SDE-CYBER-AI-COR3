"""SQL pack II: 30 harder interview questions on one product-analytics database. The data lives in Python lists, which
build both the SQL INSERTs and the independent Python answers in test_sql2.py."""
T = {
 "users": ("id INTEGER PRIMARY KEY, name TEXT, signup_date TEXT, city TEXT", [
   (1, "Asha", "2024-01-01", "Delhi"), (2, "Ravi", "2024-01-01", "Mumbai"), (3, "Meera", "2024-01-02", "Delhi"),
   (4, "Kabir", "2024-02-03", "Pune"), (5, "Divya", "2024-02-10", "Mumbai"), (6, "Arjun", "2024-02-15", "Delhi")]),
 "logins": ("user_id INTEGER, day TEXT", [
   (1, "2024-01-01"), (1, "2024-01-02"), (1, "2024-01-03"), (1, "2024-01-05"), (1, "2024-01-06"), (1, "2024-01-10"),
   (2, "2024-01-01"), (2, "2024-01-03"), (2, "2024-01-04"), (2, "2024-01-05"), (2, "2024-01-06"),
   (3, "2024-01-02"), (3, "2024-01-02"), (3, "2024-01-03"), (4, "2024-02-03"), (4, "2024-02-04"), (5, "2024-02-10")]),
 "events": ("user_id INTEGER, ts TEXT, type TEXT", [
   (1, "2024-03-01 10:00", "view"), (1, "2024-03-01 10:10", "cart"), (1, "2024-03-01 10:50", "view"), (1, "2024-03-01 10:55", "purchase"),
   (2, "2024-03-01 09:00", "view"), (2, "2024-03-01 09:05", "view"), (2, "2024-03-01 09:20", "cart"),
   (3, "2024-03-02 12:00", "view"), (3, "2024-03-02 12:31", "view"), (4, "2024-03-02 08:00", "cart"), (4, "2024-03-02 08:10", "purchase")]),
 "txns": ("id INTEGER PRIMARY KEY, user_id INTEGER, day TEXT, amount INTEGER, category TEXT", [
   (1, 1, "2024-01-05", 5000, "salary"), (2, 1, "2024-01-10", -1200, "food"), (3, 1, "2024-01-20", -4500, "rent"), (4, 1, "2024-02-03", -800, "food"),
   (5, 2, "2024-01-06", 3000, "salary"), (6, 2, "2024-02-07", -500, "travel"), (8, 2, "2024-02-15", -700, "food"), (9, 2, "2024-03-01", -300, "food"),
   (10, 3, "2024-01-15", -200, "food"), (11, 3, "2024-02-15", -900, "travel"), (12, 3, "2024-03-15", -1500, "rent"),
   (14, 4, "2024-03-02", -2500, "rent"), (15, 4, "2024-03-09", -2500, "rent")]),
 "follows": ("follower INTEGER, followee INTEGER", [(1, 2), (2, 1), (1, 3), (3, 4), (4, 3), (2, 3), (5, 1)]),
 "categories": ("id INTEGER PRIMARY KEY, name TEXT, parent_id INTEGER", [
   (1, "Electronics", None), (2, "Phones", 1), (3, "Laptops", 1), (4, "Android", 2), (5, "Gaming laptops", 3), (6, "Home", None), (7, "Kitchen", 6)]),
 "bookings": ("id INTEGER PRIMARY KEY, room TEXT, start_day TEXT, end_day TEXT", [
   (1, "A", "2024-05-01", "2024-05-04"), (2, "A", "2024-05-03", "2024-05-06"), (3, "A", "2024-05-06", "2024-05-08"),
   (4, "B", "2024-05-01", "2024-05-02"), (5, "B", "2024-05-02", "2024-05-05"), (6, "B", "2024-05-04", "2024-05-06")]),
 "basket": ("order_id INTEGER, product TEXT", [
   (1, "bread"), (1, "milk"), (1, "eggs"), (2, "bread"), (2, "milk"), (3, "milk"), (3, "eggs"), (4, "bread"), (4, "milk"), (4, "eggs"), (5, "tea")]),
 "profile_updates": ("user_id INTEGER, updated_at TEXT, email TEXT", [
   (1, "2024-01-01", "a@x.com"), (1, "2024-03-01", "asha@x.com"), (2, "2024-02-01", "r@x.com"), (3, "2024-01-05", "m@x.com"), (3, "2024-02-05", "meera@x.com")]),
 "seats": ("id INTEGER PRIMARY KEY, student TEXT", [(1, "Abbot"), (2, "Doris"), (3, "Emerson"), (4, "Green"), (5, "Jeames")]),
 "scores": ("student TEXT, subject TEXT, score INTEGER", [
   ("Asha", "DSA", 92), ("Ravi", "DSA", 75), ("Meera", "DSA", 88), ("Kabir", "DSA", 60), ("Divya", "DSA", 75),
   ("Asha", "OS", 70), ("Ravi", "OS", 85), ("Meera", "OS", 90), ("Kabir", "OS", 65)]),
}
def lit(v): return "NULL" if v is None else str(v) if isinstance(v, int) else "'" + v.replace("'", "''") + "'"
SCHEMA = "\n".join(f"CREATE TABLE {t} ({cols});" for t, (cols, _) in T.items()) + "\n\n" + "\n".join(
    f"INSERT INTO {t} VALUES " + ",".join("(" + ",".join(lit(v) for v in r) + ")" for r in rows) + ";" for t, (_, rows) in T.items()) + "\n"

# (title, level, topic, question, sql, explanation, None); the full output of every query is checked in test_sql2.py
Q = [
 ("Longest login streak", 3, "Gaps and islands", "For each user, the longest run of consecutive login days (a user can log in twice a day).",
  """WITH d AS (SELECT DISTINCT user_id, day FROM logins),
g AS (SELECT user_id, day,
        julianday(day) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS grp
      FROM d)
SELECT user_id, MAX(len) AS longest
FROM (SELECT user_id, grp, COUNT(*) AS len FROM g GROUP BY user_id, grp)
GROUP BY user_id ORDER BY user_id;""",
  "Day number minus row number is constant along a run of consecutive days, so it labels each island. DISTINCT first, or a double login breaks the trick.", None),
 ("Sessions with a 30-minute gap", 3, "Gaps and islands", "Split each user's events into sessions: a new session starts after more than 30 minutes of inactivity. Count sessions per user.",
  """WITH e AS (SELECT user_id, ts,
        (julianday(ts) - julianday(LAG(ts) OVER (PARTITION BY user_id ORDER BY ts))) * 1440 AS gap
      FROM events),
s AS (SELECT user_id, SUM(CASE WHEN gap IS NULL OR gap > 30 THEN 1 ELSE 0 END)
        OVER (PARTITION BY user_id ORDER BY ts) AS session_no FROM e)
SELECT user_id, MAX(session_no) AS sessions FROM s GROUP BY user_id ORDER BY user_id;""",
  "Flag rows that start a session (first row or gap > 30), then a running SUM of the flags numbers the sessions. julianday differences are in days; × 1440 gives minutes.", None),
 ("Running balance", 2, "Window functions", "Show user 1's transactions with the balance after each one.",
  """SELECT id, day, amount,
       SUM(amount) OVER (PARTITION BY user_id ORDER BY day, id) AS balance
FROM txns WHERE user_id = 1 ORDER BY day, id;""",
  "A running SUM ordered by day; add id as a tie-breaker so two transactions on one day still get a deterministic order.", None),
 ("First day in the red", 3, "Window functions", "For each user whose balance ever goes negative, the first day it does.",
  """WITH b AS (SELECT user_id, day,
        SUM(amount) OVER (PARTITION BY user_id ORDER BY day, id) AS bal FROM txns)
SELECT user_id, MIN(day) AS first_negative FROM b WHERE bal < 0
GROUP BY user_id ORDER BY user_id;""",
  "Compute the running balance first (a window cannot go in WHERE), then filter and take the earliest day.", None),
 ("Top 3 scores with ties", 2, "Window functions", "Per subject, everyone whose score is among the top 3 distinct scores.",
  """SELECT subject, student, score FROM (
  SELECT *, DENSE_RANK() OVER (PARTITION BY subject ORDER BY score DESC) AS r FROM scores)
WHERE r <= 3 ORDER BY subject, score DESC, student;""",
  "DENSE_RANK keeps ties and does not skip ranks, so two 75s both count as third. ROW_NUMBER would drop one; RANK would number the next score 5.", None),
 ("Median per group", 3, "Window functions", "Median score per subject (average the middle two when the count is even).",
  """WITH r AS (SELECT subject, score,
        ROW_NUMBER() OVER (PARTITION BY subject ORDER BY score) AS rn,
        COUNT(*) OVER (PARTITION BY subject) AS n FROM scores)
SELECT subject, AVG(score) AS median FROM r
WHERE rn IN ((n + 1) / 2, (n + 2) / 2)
GROUP BY subject ORDER BY subject;""",
  "With integer division, (n+1)/2 and (n+2)/2 are the same row when n is odd and the two middle rows when n is even. PostgreSQL has PERCENTILE_CONT(0.5).", None),
 ("Split into halves (NTILE)", 2, "Window functions", "Split the DSA class into a top half and a bottom half by score (ties broken by name).",
  """SELECT student, score,
       NTILE(2) OVER (ORDER BY score DESC, student) AS half
FROM scores WHERE subject = 'DSA' ORDER BY half, score DESC, student;""",
  "NTILE(k) deals rows into k nearly equal buckets in order; with 5 rows and 2 buckets the first gets 3. Quartiles are NTILE(4).", None),
 ("Top and bottom per group", 3, "Window functions", "For each subject, its top and bottom scorer, using FIRST_VALUE and LAST_VALUE.",
  """SELECT DISTINCT subject,
  FIRST_VALUE(student) OVER w AS top,
  LAST_VALUE(student) OVER w AS bottom
FROM scores
WINDOW w AS (PARTITION BY subject ORDER BY score DESC, student
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
ORDER BY subject;""",
  "LAST_VALUE needs the explicit frame: the default frame ends at the current row, so it would just return the current student.", None),
 ("Time to next event", 2, "Window functions", "For user 1, minutes from each event to the next one.",
  """SELECT ts, type,
  CAST(ROUND((julianday(LEAD(ts) OVER (ORDER BY ts)) - julianday(ts)) * 1440) AS INTEGER) AS mins_to_next
FROM events WHERE user_id = 1 ORDER BY ts;""",
  "LEAD looks one row ahead; the last row has no next event, so it is NULL. ROUND avoids floating-point noise before the cast.", None),
 ("Gap to the leader", 2, "Window functions", "Show each score and how far it is behind the subject's top score.",
  """SELECT subject, student, score,
       MAX(score) OVER (PARTITION BY subject) - score AS behind
FROM scores ORDER BY subject, behind, student;""",
  "An aggregate with OVER keeps every row and adds the group's value to it, so no self-join or subquery is needed.", None),
 ("New users per day, cumulative", 2, "Window functions", "For each day on which someone logged in for the first time: how many new users, and the running total.",
  """WITH f AS (SELECT user_id, MIN(day) AS first_day FROM logins GROUP BY user_id)
SELECT first_day, COUNT(*) AS new_users,
       SUM(COUNT(*)) OVER (ORDER BY first_day) AS total_users
FROM f GROUP BY first_day ORDER BY first_day;""",
  "Cumulative distinct counts: find each user's first day, then a running sum of new users. A window over an aggregate (SUM(COUNT(*)) OVER) runs after GROUP BY.", None),
 ("Day-1 retention by cohort", 3, "Product analytics", "For each signup month, the percentage of users who logged in on the day after signing up.",
  """SELECT strftime('%Y-%m', u.signup_date) AS cohort, COUNT(*) AS users,
  ROUND(100.0 * SUM(EXISTS (SELECT 1 FROM logins l WHERE l.user_id = u.id
        AND l.day = date(u.signup_date, '+1 day'))) / COUNT(*), 1) AS day1_pct
FROM users u GROUP BY cohort ORDER BY cohort;""",
  "EXISTS returns 1 or 0, so SUM counts retained users. Multiply by 100.0 (not 100) to avoid integer division.", None),
 ("Funnel in order", 3, "Product analytics", "How many users viewed, then added to cart after a view, then purchased after that cart?",
  """WITH v AS (SELECT user_id, MIN(ts) AS t FROM events WHERE type = 'view' GROUP BY user_id),
c AS (SELECT e.user_id, MIN(e.ts) AS t FROM events e JOIN v ON v.user_id = e.user_id AND e.ts > v.t
      WHERE e.type = 'cart' GROUP BY e.user_id),
p AS (SELECT e.user_id FROM events e JOIN c ON c.user_id = e.user_id AND e.ts > c.t
      WHERE e.type = 'purchase' GROUP BY e.user_id)
SELECT (SELECT COUNT(*) FROM v) AS viewed, (SELECT COUNT(*) FROM c) AS carted, (SELECT COUNT(*) FROM p) AS purchased;""",
  "Each step joins on the previous step's time, so out-of-order events (user 4 bought without viewing) do not count.", None),
 ("Spend rising every month", 3, "Product analytics", "Users whose monthly spending (debits) went up every month, with at least two months.",
  """WITH m AS (SELECT user_id, strftime('%Y-%m', day) AS mon, -SUM(amount) AS spend
      FROM txns WHERE amount < 0 GROUP BY user_id, mon),
d AS (SELECT user_id, spend - LAG(spend) OVER (PARTITION BY user_id ORDER BY mon) AS diff FROM m)
SELECT u.name FROM d JOIN users u ON u.id = d.user_id
GROUP BY d.user_id HAVING COUNT(*) >= 2 AND MIN(diff) > 0 ORDER BY u.name;""",
  "LAG gives month-on-month change; every change positive means MIN(diff) > 0 (MIN ignores the first month's NULL). COUNT(*) ≥ 2 enforces two months.", None),
 ("Category path", 3, "Recursion", "Show every category with its full path from the root and its depth.",
  """WITH RECURSIVE t(id, name, path, depth) AS (
  SELECT id, name, name, 0 FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.name, t.path || ' > ' || c.name, t.depth + 1
  FROM categories c JOIN t ON c.parent_id = t.id)
SELECT path, depth FROM t ORDER BY path;""",
  "Anchor the roots, then repeatedly join children to the rows found so far. The path is built as text on the way down.", None),
 ("All descendants", 2, "Recursion", "List every category under Electronics, at any depth.",
  """WITH RECURSIVE sub(id) AS (
  SELECT id FROM categories WHERE name = 'Electronics'
  UNION ALL
  SELECT c.id FROM categories c JOIN sub ON c.parent_id = sub.id)
SELECT name FROM categories WHERE id IN (SELECT id FROM sub) AND name <> 'Electronics' ORDER BY name;""",
  "Same pattern as an org chart ('everyone under this manager'). UNION ALL is fine for a tree; use UNION to stop cycles in a graph.", None),
 ("Fill missing days with zero", 3, "Recursion", "Distinct users who logged in on each day from 1 to 7 January 2024, showing 0 for days with none.",
  """WITH RECURSIVE days(d) AS (
  SELECT '2024-01-01' UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < '2024-01-07')
SELECT d AS day, COUNT(DISTINCT l.user_id) AS users
FROM days LEFT JOIN logins l ON l.day = d
GROUP BY d ORDER BY d;""",
  "Generate the calendar, then LEFT JOIN the data onto it. COUNT(column) counts only matches, so empty days get 0.", None),
 ("Missing IDs", 2, "Recursion", "Which transaction IDs between the smallest and largest are missing?",
  """WITH RECURSIVE n(i) AS (
  SELECT MIN(id) FROM txns UNION ALL SELECT i + 1 FROM n WHERE i < (SELECT MAX(id) FROM txns))
SELECT i AS missing_id FROM n WHERE i NOT IN (SELECT id FROM txns) ORDER BY i;""",
  "A number series plus an anti-join. Alternative without recursion: rows where LEAD(id) − id > 1 give the start of each gap.", None),
 ("Pivot months into columns", 2, "Reshaping", "Monthly spending (debits) per user, one column per month, 0 where none.",
  """SELECT user_id,
  -SUM(CASE WHEN strftime('%m', day) = '01' AND amount < 0 THEN amount ELSE 0 END) AS jan,
  -SUM(CASE WHEN strftime('%m', day) = '02' AND amount < 0 THEN amount ELSE 0 END) AS feb,
  -SUM(CASE WHEN strftime('%m', day) = '03' AND amount < 0 THEN amount ELSE 0 END) AS mar
FROM txns GROUP BY user_id ORDER BY user_id;""",
  "Conditional aggregation is the portable pivot: one SUM(CASE …) per output column. SQL Server and Oracle also have a PIVOT clause.", None),
 ("Histogram buckets", 2, "Reshaping", "How many debits fall in each size bucket: under 1,000, 1,000–2,999, and 3,000 or more?",
  """SELECT CASE WHEN -amount < 1000 THEN '1: under 1000'
            WHEN -amount < 3000 THEN '2: 1000-2999'
            ELSE '3: 3000+' END AS bucket, COUNT(*) AS debits
FROM txns WHERE amount < 0 GROUP BY bucket ORDER BY bucket;""",
  "Bucket with CASE, then GROUP BY the label. The number prefix keeps the buckets in order when sorted as text.", None),
 ("Mutual follows", 2, "Joins and sets", "Pairs of users who follow each other, each pair once.",
  """SELECT a.follower AS user_a, a.followee AS user_b
FROM follows a JOIN follows b ON b.follower = a.followee AND b.followee = a.follower
WHERE a.follower < a.followee ORDER BY user_a, user_b;""",
  "Self-join each edge to its reverse; follower < followee keeps one copy of each pair.", None),
 ("People you may know", 3, "Joins and sets", "Suggest accounts for user 1: followed by people user 1 follows, not already followed, not user 1; rank by how many such paths.",
  """SELECT f2.followee AS suggest, COUNT(*) AS via
FROM follows f1 JOIN follows f2 ON f2.follower = f1.followee
WHERE f1.follower = 1 AND f2.followee <> 1
  AND f2.followee NOT IN (SELECT followee FROM follows WHERE follower = 1)
GROUP BY f2.followee ORDER BY via DESC, suggest;""",
  "Two hops through the graph, then remove yourself and people you already follow. COUNT(*) is the number of mutual connections.", None),
 ("Bought together", 3, "Joins and sets", "Pairs of products in the same order at least twice, most frequent first.",
  """SELECT a.product AS p1, b.product AS p2, COUNT(*) AS orders
FROM basket a JOIN basket b ON a.order_id = b.order_id AND a.product < b.product
GROUP BY p1, p2 HAVING COUNT(*) >= 2 ORDER BY orders DESC, p1, p2;""",
  "Self-join on the order with a.product < b.product so each unordered pair appears once per order (market-basket analysis).", None),
 ("Overlapping bookings", 3, "Joins and sets", "Find pairs of bookings in the same room that overlap (end days are exclusive).",
  """SELECT a.id AS booking_a, b.id AS booking_b, a.room
FROM bookings a JOIN bookings b
  ON a.room = b.room AND a.id < b.id
 AND a.start_day < b.end_day AND b.start_day < a.end_day
ORDER BY a.id, b.id;""",
  "Two intervals overlap exactly when each starts before the other ends. With exclusive ends, back-to-back bookings (one ends the day the next starts) do not overlap.", None),
 ("Latest row per key", 2, "Joins and sets", "Each user's current email (the most recent update).",
  """SELECT user_id, email FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) AS rn
  FROM profile_updates)
WHERE rn = 1 ORDER BY user_id;""",
  "The standard deduplication pattern. Add a tie-breaker to ORDER BY if two updates can share a timestamp.", None),
 ("Swap adjacent seats", 2, "Joins and sets", "Swap every pair of adjacent students (1↔2, 3↔4, …); an odd last seat stays put.",
  """SELECT CASE WHEN id % 2 = 1 AND id = (SELECT MAX(id) FROM seats) THEN id
            WHEN id % 2 = 1 THEN id + 1 ELSE id - 1 END AS id, student
FROM seats ORDER BY id;""",
  "Rewrite the ids rather than moving rows: odd ids go up one, even ids down one, except a final odd id.", None),
 ("Follow but not followed (EXCEPT)", 1, "Joins and sets", "Users who follow someone but whom nobody follows.",
  """SELECT follower AS user_id FROM follows
EXCEPT
SELECT followee FROM follows ORDER BY user_id;""",
  "EXCEPT returns distinct rows from the first query that are not in the second (MINUS in Oracle). INTERSECT keeps rows in both.", None),
 ("Active every month", 3, "Joins and sets", "Users with at least one transaction in every month that has any transactions.",
  """SELECT user_id FROM txns
GROUP BY user_id
HAVING COUNT(DISTINCT strftime('%Y-%m', day)) =
       (SELECT COUNT(DISTINCT strftime('%Y-%m', day)) FROM txns)
ORDER BY user_id;""",
  "Relational division by counting: a user covers every month when their distinct-month count equals the total.", None),
 ("Same category twice in a row", 2, "Window functions", "Transactions in the same category as the same user's previous transaction.",
  """SELECT id, user_id, category FROM (
  SELECT *, LAG(category) OVER (PARTITION BY user_id ORDER BY day, id) AS prev FROM txns)
WHERE category = prev ORDER BY id;""",
  "Compare each row with the previous one using LAG; the first row per user has prev NULL, and NULL = anything is never true.", None),
 ("Keyset pagination", 3, "Performance patterns", "Ordered by score (high first), then student, then subject, return the 3 rows after (85, 'Ravi', 'OS').",
  """SELECT score, student, subject FROM scores
WHERE score < 85 OR (score = 85 AND (student, subject) > ('Ravi', 'OS'))
ORDER BY score DESC, student, subject LIMIT 3;""",
  "Seek pagination: filter past the last row seen instead of OFFSET, so an index can jump straight there and pages do not shift when rows are inserted. Row values ((a, b) > (x, y)) work in SQLite, PostgreSQL and MySQL.", None),
]
