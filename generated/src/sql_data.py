"""SQL pack: a small sample database and 40 interview questions. Every query runs in SQLite (see sql_pack.py)."""
SCHEMA = """
CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT NOT NULL, location TEXT);
CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept_id INTEGER REFERENCES departments(id), manager_id INTEGER REFERENCES employees(id), salary INTEGER, hire_date TEXT);
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT, signup_date TEXT);
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT, price INTEGER);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id), order_date TEXT, status TEXT);
CREATE TABLE order_items (order_id INTEGER REFERENCES orders(id), product_id INTEGER REFERENCES products(id), qty INTEGER, PRIMARY KEY (order_id, product_id));
CREATE TABLE logins (user_id INTEGER, login_date TEXT);

INSERT INTO departments VALUES (1,'Engineering','Bengaluru'),(2,'Security','Hyderabad'),(3,'Sales','Mumbai'),(4,'Research','Pune');
INSERT INTO employees VALUES
 (1,'Asha',1,NULL,250000,'2018-03-01'),(2,'Ravi',1,1,180000,'2019-07-15'),(3,'Meera',1,1,180000,'2020-01-10'),
 (4,'Kabir',1,2,120000,'2022-06-01'),(5,'Divya',2,1,200000,'2019-02-20'),(6,'Arjun',2,5,140000,'2021-09-05'),
 (7,'Neha',2,5,95000,'2023-01-16'),(8,'Vikram',3,1,150000,'2020-11-30'),(9,'Isha',3,8,160000,'2022-04-11'),
 (10,'Rohan',3,8,90000,'2023-08-21'),(11,'Sara',NULL,1,70000,'2024-02-01');
INSERT INTO customers VALUES (1,'Anil','Delhi','2024-01-05'),(2,'Bina','Mumbai','2024-01-20'),(3,'Chirag','Delhi','2024-02-11'),
 (4,'Deepa','Chennai','2024-03-02'),(5,'Eshan','Mumbai','2024-03-15'),(6,'Farah','Pune','2024-04-01');
INSERT INTO products VALUES (1,'Laptop','Electronics',60000),(2,'Phone','Electronics',30000),(3,'Headphones','Electronics',3000),
 (4,'Desk','Furniture',12000),(5,'Chair','Furniture',8000),(6,'Notebook','Stationery',100);
INSERT INTO orders VALUES (1,1,'2024-02-01','delivered'),(2,1,'2024-02-15','delivered'),(3,2,'2024-02-20','cancelled'),
 (4,2,'2024-03-05','delivered'),(5,3,'2024-03-07','delivered'),(6,4,'2024-03-20','shipped'),(7,1,'2024-04-02','delivered'),
 (8,5,'2024-04-10','delivered'),(9,3,'2024-04-18','delivered'),(10,2,'2024-04-25','delivered');
INSERT INTO order_items VALUES (1,1,1),(1,3,2),(2,6,10),(3,2,1),(4,2,1),(4,3,1),(5,4,1),(5,5,2),(6,1,1),(7,3,1),(8,5,4),(9,6,5),(9,3,1),(10,1,1),(10,4,1);
INSERT INTO logins VALUES (1,'2024-05-01'),(1,'2024-05-02'),(1,'2024-05-03'),(1,'2024-05-05'),(2,'2024-05-01'),(2,'2024-05-03'),
 (3,'2024-05-02'),(3,'2024-05-03'),(3,'2024-05-04'),(3,'2024-05-05'),(3,'2024-05-05');
"""
# (title, level 1-3, topic, question, sql, explanation, expected first row as a tuple for a sanity check or None)
Q = [
 ("Filter and sort", 1, "Basics", "List employees earning more than 1,50,000, highest first.",
  "SELECT name, salary FROM employees\nWHERE salary > 150000\nORDER BY salary DESC, name;", "WHERE filters rows; a second sort key makes ties deterministic.", ("Asha", 250000)),
 ("DISTINCT", 1, "Basics", "Which cities do customers come from?", "SELECT DISTINCT city FROM customers ORDER BY city;", "DISTINCT removes duplicate rows from the result.", ("Chennai",)),
 ("NULL check", 1, "Basics", "Find employees with no department.", "SELECT name FROM employees WHERE dept_id IS NULL;", "Use IS NULL; dept_id = NULL is never true.", ("Sara",)),
 ("LIKE", 1, "Basics", "Find customers whose name starts with a vowel.",
  "SELECT name FROM customers\nWHERE substr(name, 1, 1) IN ('A','E','I','O','U')\nORDER BY name;", "In MySQL you could also use REGEXP '^[AEIOU]'. LIKE 'A%' handles one letter at a time.", ("Anil",)),
 ("CASE", 1, "Basics", "Label each employee's salary band: High (≥ 2,00,000), Mid (≥ 1,00,000), else Low.",
  "SELECT name,\n  CASE WHEN salary >= 200000 THEN 'High'\n       WHEN salary >= 100000 THEN 'Mid'\n       ELSE 'Low' END AS band\nFROM employees ORDER BY id;", "CASE checks conditions in order and returns the first match.", ("Asha", "High")),
 ("INNER JOIN", 1, "Joins", "Show each employee with their department name.",
  "SELECT e.name, d.name AS dept\nFROM employees e\nJOIN departments d ON d.id = e.dept_id\nORDER BY e.id;", "Inner join drops Sara, who has no department.", ("Asha", "Engineering")),
 ("LEFT JOIN", 1, "Joins", "Show every employee and their department, including those without one.",
  "SELECT e.name, d.name AS dept\nFROM employees e\nLEFT JOIN departments d ON d.id = e.dept_id\nORDER BY e.id DESC\nLIMIT 3;", "Left join keeps all employees; missing departments show as NULL.", ("Sara", None)),
 ("Anti-join", 2, "Joins", "Find departments with no employees.",
  "SELECT d.name\nFROM departments d\nLEFT JOIN employees e ON e.dept_id = d.id\nWHERE e.id IS NULL;", "Left join then keep rows where nothing matched. NOT EXISTS works too.", ("Research",)),
 ("Self join", 2, "Joins", "Show each employee with their manager's name.",
  "SELECT e.name AS employee, m.name AS manager\nFROM employees e\nLEFT JOIN employees m ON m.id = e.manager_id\nORDER BY e.id\nLIMIT 4;", "Join the table to itself with two aliases.", ("Asha", None)),
 ("Earns more than manager", 2, "Joins", "Find employees who earn more than their manager.",
  "SELECT e.name\nFROM employees e\nJOIN employees m ON m.id = e.manager_id\nWHERE e.salary > m.salary;", "Join each employee to their manager row and compare.", ("Isha",)),
 ("Customers who never ordered", 1, "Joins", "Which customers have never placed an order?",
  "SELECT c.name FROM customers c\nWHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);", "NOT EXISTS is safe with NULLs; NOT IN breaks if the subquery returns a NULL.", ("Farah",)),
 ("Three-table join", 2, "Joins", "List the products in order 4 with quantity and line total.",
  "SELECT p.name, oi.qty, oi.qty * p.price AS line_total\nFROM order_items oi\nJOIN products p ON p.id = oi.product_id\nWHERE oi.order_id = 4\nORDER BY p.name;", "Join through the bridge table order_items.", ("Headphones", 1, 3000)),
 ("COUNT and GROUP BY", 1, "Aggregation", "How many employees are in each department?",
  "SELECT d.name, COUNT(e.id) AS headcount\nFROM departments d\nLEFT JOIN employees e ON e.dept_id = d.id\nGROUP BY d.id\nORDER BY headcount DESC, d.name;", "COUNT(e.id) counts 0 for Research; COUNT(*) would wrongly count 1.", ("Engineering", 4)),
 ("AVG and HAVING", 2, "Aggregation", "Departments whose average salary is above 1,30,000.",
  "SELECT d.name, ROUND(AVG(e.salary)) AS avg_salary\nFROM employees e JOIN departments d ON d.id = e.dept_id\nGROUP BY d.id\nHAVING AVG(e.salary) > 130000\nORDER BY avg_salary DESC;", "HAVING filters groups after aggregation; WHERE cannot use AVG.", ("Engineering", 182500.0)),
 ("Revenue per order", 2, "Aggregation", "Total value of each delivered order, largest first.",
  "SELECT o.id, SUM(oi.qty * p.price) AS total\nFROM orders o\nJOIN order_items oi ON oi.order_id = o.id\nJOIN products p ON p.id = oi.product_id\nWHERE o.status = 'delivered'\nGROUP BY o.id\nORDER BY total DESC, o.id\nLIMIT 3;", "Aggregate line totals per order.", (10, 72000)),
 ("Revenue per customer", 2, "Aggregation", "Total delivered revenue per customer.",
  "SELECT c.name, SUM(oi.qty * p.price) AS revenue\nFROM customers c\nJOIN orders o ON o.customer_id = c.id AND o.status = 'delivered'\nJOIN order_items oi ON oi.order_id = o.id\nJOIN products p ON p.id = oi.product_id\nGROUP BY c.id\nORDER BY revenue DESC;", "Putting the status filter in the ON clause keeps the query readable; in an inner join it behaves like WHERE.", ("Bina", 105000)),
 ("Monthly revenue", 2, "Aggregation", "Delivered revenue per month.",
  "SELECT strftime('%Y-%m', o.order_date) AS month, SUM(oi.qty * p.price) AS revenue\nFROM orders o\nJOIN order_items oi ON oi.order_id = o.id\nJOIN products p ON p.id = oi.product_id\nWHERE o.status = 'delivered'\nGROUP BY month ORDER BY month;", "SQLite uses strftime; MySQL uses DATE_FORMAT(order_date, '%Y-%m'); PostgreSQL uses to_char or date_trunc.", ("2024-02", 67000)),
 ("Conditional count", 2, "Aggregation", "For each customer, count delivered and cancelled orders in one row.",
  "SELECT c.name,\n  SUM(o.status = 'delivered') AS delivered,\n  SUM(o.status = 'cancelled') AS cancelled\nFROM customers c JOIN orders o ON o.customer_id = c.id\nGROUP BY c.id ORDER BY c.id;", "A condition is 1 or 0 in SQLite and MySQL. Portable form: SUM(CASE WHEN ... THEN 1 ELSE 0 END).", ("Anil", 3, 0)),
 ("Duplicates", 1, "Aggregation", "Find logins recorded more than once for the same user and day.",
  "SELECT user_id, login_date, COUNT(*) AS n\nFROM logins\nGROUP BY user_id, login_date\nHAVING COUNT(*) > 1;", "Group by every column that defines a duplicate.", (3, "2024-05-05", 2)),
 ("Delete duplicates", 2, "Aggregation", "Delete duplicate logins, keeping one copy (shown as the rows that would remain).",
  "SELECT user_id, login_date FROM logins\nWHERE rowid IN (SELECT MIN(rowid) FROM logins GROUP BY user_id, login_date)\nORDER BY user_id, login_date\nLIMIT 3;", "The real statement is DELETE FROM logins WHERE rowid NOT IN (SELECT MIN(rowid) ... ). Other databases use the primary key or ROW_NUMBER().", (1, "2024-05-01")),
 ("Second-highest salary", 2, "Subqueries", "Find the second-highest distinct salary.",
  "SELECT MAX(salary) AS second_highest\nFROM employees\nWHERE salary < (SELECT MAX(salary) FROM employees);", "Returns NULL if there is no second value, which interviewers like.", (200000,)),
 ("Nth-highest salary", 2, "Subqueries", "Find the 3rd-highest distinct salary.",
  "SELECT DISTINCT salary FROM employees\nORDER BY salary DESC\nLIMIT 1 OFFSET 2;", "DISTINCT first, so 1,80,000 counts once. DENSE_RANK() is the window-function version.", (180000,)),
 ("Above department average", 2, "Subqueries", "Employees earning more than their department's average.",
  "SELECT e.name, e.salary\nFROM employees e\nWHERE e.salary > (SELECT AVG(salary) FROM employees x WHERE x.dept_id = e.dept_id)\nORDER BY e.salary DESC;", "A correlated subquery runs once per outer row.", ("Asha", 250000)),
 ("IN with subquery", 1, "Subqueries", "Customers who bought any Furniture product.",
  "SELECT DISTINCT c.name FROM customers c\nJOIN orders o ON o.customer_id = c.id\nWHERE o.id IN (SELECT oi.order_id FROM order_items oi\n               JOIN products p ON p.id = oi.product_id\n               WHERE p.category = 'Furniture')\nORDER BY c.name;", "IN is fine when the subquery cannot return NULL.", ("Bina",)),
 ("Bought every category", 3, "Subqueries", "Customers who bought from every product category (relational division).",
  "SELECT c.name FROM customers c\nJOIN orders o ON o.customer_id = c.id\nJOIN order_items oi ON oi.order_id = o.id\nJOIN products p ON p.id = oi.product_id\nGROUP BY c.id\nHAVING COUNT(DISTINCT p.category) = (SELECT COUNT(DISTINCT category) FROM products);", "Count distinct categories per customer and compare with the total.", ("Chirag",)),
 ("CTE", 2, "Subqueries", "Using a CTE, list departments whose total salary is above the average department total.",
  "WITH t AS (\n  SELECT dept_id, SUM(salary) AS total FROM employees\n  WHERE dept_id IS NOT NULL GROUP BY dept_id)\nSELECT d.name, t.total FROM t JOIN departments d ON d.id = t.dept_id\nWHERE t.total > (SELECT AVG(total) FROM t);", "A CTE names an intermediate result so you can use it twice.", ("Engineering", 730000)),
 ("Recursive CTE", 3, "Subqueries", "List everyone in Asha's reporting tree with their level.",
  "WITH RECURSIVE tree(id, name, lvl) AS (\n  SELECT id, name, 0 FROM employees WHERE manager_id IS NULL\n  UNION ALL\n  SELECT e.id, e.name, t.lvl + 1 FROM employees e JOIN tree t ON e.manager_id = t.id)\nSELECT name, lvl FROM tree ORDER BY lvl, name\nLIMIT 6;", "The anchor picks the root; the recursive part adds one level per pass.", ("Asha", 0)),
 ("ROW_NUMBER", 2, "Window functions", "Number employees by salary within each department.",
  "SELECT d.name AS dept, e.name, e.salary,\n  ROW_NUMBER() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC, e.name) AS rn\nFROM employees e JOIN departments d ON d.id = e.dept_id\nORDER BY d.name, rn\nLIMIT 4;", "PARTITION BY restarts the numbering for each department.", ("Engineering", "Asha", 250000, 1)),
 ("Top earner per department", 2, "Window functions", "Highest-paid employee(s) in each department.",
  "SELECT dept, name, salary FROM (\n  SELECT d.name AS dept, e.name, e.salary,\n    RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS r\n  FROM employees e JOIN departments d ON d.id = e.dept_id)\nWHERE r = 1 ORDER BY dept;", "RANK keeps ties; ROW_NUMBER would pick one arbitrarily.", ("Engineering", "Asha", 250000)),
 ("Top 2 per department", 2, "Window functions", "Top two distinct salaries per department with names.",
  "SELECT dept, name, salary FROM (\n  SELECT d.name AS dept, e.name, e.salary,\n    DENSE_RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS r\n  FROM employees e JOIN departments d ON d.id = e.dept_id)\nWHERE r <= 2 ORDER BY dept, salary DESC, name;", "DENSE_RANK so Ravi and Meera (tied) are both second in Engineering.", ("Engineering", "Asha", 250000)),
 ("RANK vs DENSE_RANK", 1, "Window functions", "Show ROW_NUMBER, RANK and DENSE_RANK of Engineering salaries side by side.",
  "SELECT name, salary,\n  ROW_NUMBER() OVER w AS row_num, RANK() OVER w AS rnk, DENSE_RANK() OVER w AS dense\nFROM employees WHERE dept_id = 1\nWINDOW w AS (ORDER BY salary DESC)\nORDER BY salary DESC, name;", "Ties: RANK skips the next number, DENSE_RANK does not. (Named WINDOW clauses work in SQLite, MySQL 8 and PostgreSQL.)", ("Asha", 250000, 1, 1, 1)),
 ("Running total", 2, "Window functions", "Running total of delivered revenue by order date.",
  "WITH t AS (\n  SELECT o.order_date, SUM(oi.qty * p.price) AS amt\n  FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id\n  WHERE o.status = 'delivered' GROUP BY o.id)\nSELECT order_date, amt, SUM(amt) OVER (ORDER BY order_date) AS running\nFROM t ORDER BY order_date\nLIMIT 4;", "SUM() OVER (ORDER BY ...) accumulates row by row.", ("2024-02-01", 66000, 66000)),
 ("Moving average", 3, "Window functions", "3-order moving average of delivered order values.",
  "WITH t AS (\n  SELECT o.order_date, SUM(oi.qty * p.price) AS amt\n  FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id\n  WHERE o.status = 'delivered' GROUP BY o.id)\nSELECT order_date, amt,\n  ROUND(AVG(amt) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS ma3\nFROM t ORDER BY order_date\nLIMIT 4;", "The ROWS frame sets exactly which rows are averaged.", ("2024-02-01", 66000, 66000.0)),
 ("LAG", 2, "Window functions", "Days between each customer's consecutive orders.",
  "SELECT customer_id, order_date,\n  julianday(order_date) - julianday(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) AS gap_days\nFROM orders ORDER BY customer_id, order_date\nLIMIT 4;", "LAG reads the previous row in the partition. Date difference: DATEDIFF in MySQL, subtraction in PostgreSQL.", (1, "2024-02-01", None)),
 ("Month-over-month growth", 3, "Window functions", "Month-over-month change in delivered revenue.",
  "WITH m AS (\n  SELECT strftime('%Y-%m', o.order_date) AS month, SUM(oi.qty * p.price) AS rev\n  FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id\n  WHERE o.status = 'delivered' GROUP BY month)\nSELECT month, rev, rev - LAG(rev) OVER (ORDER BY month) AS change\nFROM m ORDER BY month;", "First month has no previous value, so change is NULL.", ("2024-02", 67000, None)),
 ("Share of total", 2, "Window functions", "Each department's share of the total salary bill, in percent.",
  "SELECT d.name, SUM(e.salary) AS total,\n  ROUND(100.0 * SUM(e.salary) / SUM(SUM(e.salary)) OVER (), 1) AS pct\nFROM employees e JOIN departments d ON d.id = e.dept_id\nGROUP BY d.id ORDER BY pct DESC;", "A window over the grouped result: SUM(SUM(x)) OVER () is the grand total.", ("Engineering", 730000, 46.6)),
 ("Consecutive days", 3, "Window functions", "Users who logged in on 3 or more consecutive days.",
  "WITH d AS (SELECT DISTINCT user_id, login_date FROM logins),\ng AS (SELECT user_id, login_date,\n  julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp\n  FROM d)\nSELECT user_id, MIN(login_date) AS start_day, COUNT(*) AS streak\nFROM g GROUP BY user_id, grp HAVING COUNT(*) >= 3\nORDER BY user_id;", "Gaps-and-islands: in a run of consecutive dates, date minus row number is constant.", (1, "2024-05-01", 3)),
 ("First order per customer", 2, "Window functions", "Each customer's first order and its date.",
  "SELECT customer_id, id AS order_id, order_date FROM (\n  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS rn FROM orders o)\nWHERE rn = 1 ORDER BY customer_id;", "Keep row 1 of each partition. Same pattern for 'latest' with DESC.", (1, 1, "2024-02-01")),
 ("Best-selling product per category", 3, "Window functions", "In each category, the product with the most units sold.",
  "WITH s AS (\n  SELECT p.category, p.name, SUM(oi.qty) AS units\n  FROM products p JOIN order_items oi ON oi.product_id = p.id GROUP BY p.id),\nr AS (SELECT *, RANK() OVER (PARTITION BY category ORDER BY units DESC) AS rk FROM s)\nSELECT category, name, units FROM r WHERE rk = 1 ORDER BY category;", "Aggregate first, then rank within each category.", ("Electronics", "Headphones", 5)),
 ("Index and plan", 2, "Performance", "Add an index for lookups of orders by customer, and check the plan uses it.",
  "CREATE INDEX idx_orders_customer ON orders(customer_id);\nEXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 2;", "The plan should say SEARCH ... USING INDEX instead of SCAN. Index the columns in WHERE and JOIN conditions; each index slows writes a little.", None),
]
