-- SQL interview pack: sample database and 40 questions. Tested with SQLite 3.53.1.
-- Load: sqlite3 practice.db < sql-pack.sql   (or paste the schema into any SQL playground)

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

-- Q1. Filter and sort [Basics, L1]
-- List employees earning more than 1,50,000, highest first.
SELECT name, salary FROM employees
WHERE salary > 150000
ORDER BY salary DESC, name;

-- Q2. DISTINCT [Basics, L1]
-- Which cities do customers come from?
SELECT DISTINCT city FROM customers ORDER BY city;

-- Q3. NULL check [Basics, L1]
-- Find employees with no department.
SELECT name FROM employees WHERE dept_id IS NULL;

-- Q4. LIKE [Basics, L1]
-- Find customers whose name starts with a vowel.
SELECT name FROM customers
WHERE substr(name, 1, 1) IN ('A','E','I','O','U')
ORDER BY name;

-- Q5. CASE [Basics, L1]
-- Label each employee's salary band: High (≥ 2,00,000), Mid (≥ 1,00,000), else Low.
SELECT name,
  CASE WHEN salary >= 200000 THEN 'High'
       WHEN salary >= 100000 THEN 'Mid'
       ELSE 'Low' END AS band
FROM employees ORDER BY id;

-- Q6. INNER JOIN [Joins, L1]
-- Show each employee with their department name.
SELECT e.name, d.name AS dept
FROM employees e
JOIN departments d ON d.id = e.dept_id
ORDER BY e.id;

-- Q7. LEFT JOIN [Joins, L1]
-- Show every employee and their department, including those without one.
SELECT e.name, d.name AS dept
FROM employees e
LEFT JOIN departments d ON d.id = e.dept_id
ORDER BY e.id DESC
LIMIT 3;

-- Q8. Anti-join [Joins, L2]
-- Find departments with no employees.
SELECT d.name
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
WHERE e.id IS NULL;

-- Q9. Self join [Joins, L2]
-- Show each employee with their manager's name.
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id
ORDER BY e.id
LIMIT 4;

-- Q10. Earns more than manager [Joins, L2]
-- Find employees who earn more than their manager.
SELECT e.name
FROM employees e
JOIN employees m ON m.id = e.manager_id
WHERE e.salary > m.salary;

-- Q11. Customers who never ordered [Joins, L1]
-- Which customers have never placed an order?
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- Q12. Three-table join [Joins, L2]
-- List the products in order 4 with quantity and line total.
SELECT p.name, oi.qty, oi.qty * p.price AS line_total
FROM order_items oi
JOIN products p ON p.id = oi.product_id
WHERE oi.order_id = 4
ORDER BY p.name;

-- Q13. COUNT and GROUP BY [Aggregation, L1]
-- How many employees are in each department?
SELECT d.name, COUNT(e.id) AS headcount
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
GROUP BY d.id
ORDER BY headcount DESC, d.name;

-- Q14. AVG and HAVING [Aggregation, L2]
-- Departments whose average salary is above 1,30,000.
SELECT d.name, ROUND(AVG(e.salary)) AS avg_salary
FROM employees e JOIN departments d ON d.id = e.dept_id
GROUP BY d.id
HAVING AVG(e.salary) > 130000
ORDER BY avg_salary DESC;

-- Q15. Revenue per order [Aggregation, L2]
-- Total value of each delivered order, largest first.
SELECT o.id, SUM(oi.qty * p.price) AS total
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE o.status = 'delivered'
GROUP BY o.id
ORDER BY total DESC, o.id
LIMIT 3;

-- Q16. Revenue per customer [Aggregation, L2]
-- Total delivered revenue per customer.
SELECT c.name, SUM(oi.qty * p.price) AS revenue
FROM customers c
JOIN orders o ON o.customer_id = c.id AND o.status = 'delivered'
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
GROUP BY c.id
ORDER BY revenue DESC;

-- Q17. Monthly revenue [Aggregation, L2]
-- Delivered revenue per month.
SELECT strftime('%Y-%m', o.order_date) AS month, SUM(oi.qty * p.price) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE o.status = 'delivered'
GROUP BY month ORDER BY month;

-- Q18. Conditional count [Aggregation, L2]
-- For each customer, count delivered and cancelled orders in one row.
SELECT c.name,
  SUM(o.status = 'delivered') AS delivered,
  SUM(o.status = 'cancelled') AS cancelled
FROM customers c JOIN orders o ON o.customer_id = c.id
GROUP BY c.id ORDER BY c.id;

-- Q19. Duplicates [Aggregation, L1]
-- Find logins recorded more than once for the same user and day.
SELECT user_id, login_date, COUNT(*) AS n
FROM logins
GROUP BY user_id, login_date
HAVING COUNT(*) > 1;

-- Q20. Delete duplicates [Aggregation, L2]
-- Delete duplicate logins, keeping one copy (shown as the rows that would remain).
SELECT user_id, login_date FROM logins
WHERE rowid IN (SELECT MIN(rowid) FROM logins GROUP BY user_id, login_date)
ORDER BY user_id, login_date
LIMIT 3;

-- Q21. Second-highest salary [Subqueries, L2]
-- Find the second-highest distinct salary.
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Q22. Nth-highest salary [Subqueries, L2]
-- Find the 3rd-highest distinct salary.
SELECT DISTINCT salary FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 2;

-- Q23. Above department average [Subqueries, L2]
-- Employees earning more than their department's average.
SELECT e.name, e.salary
FROM employees e
WHERE e.salary > (SELECT AVG(salary) FROM employees x WHERE x.dept_id = e.dept_id)
ORDER BY e.salary DESC;

-- Q24. IN with subquery [Subqueries, L1]
-- Customers who bought any Furniture product.
SELECT DISTINCT c.name FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE o.id IN (SELECT oi.order_id FROM order_items oi
               JOIN products p ON p.id = oi.product_id
               WHERE p.category = 'Furniture')
ORDER BY c.name;

-- Q25. Bought every category [Subqueries, L3]
-- Customers who bought from every product category (relational division).
SELECT c.name FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
GROUP BY c.id
HAVING COUNT(DISTINCT p.category) = (SELECT COUNT(DISTINCT category) FROM products);

-- Q26. CTE [Subqueries, L2]
-- Using a CTE, list departments whose total salary is above the average department total.
WITH t AS (
  SELECT dept_id, SUM(salary) AS total FROM employees
  WHERE dept_id IS NOT NULL GROUP BY dept_id)
SELECT d.name, t.total FROM t JOIN departments d ON d.id = t.dept_id
WHERE t.total > (SELECT AVG(total) FROM t);

-- Q27. Recursive CTE [Subqueries, L3]
-- List everyone in Asha's reporting tree with their level.
WITH RECURSIVE tree(id, name, lvl) AS (
  SELECT id, name, 0 FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, t.lvl + 1 FROM employees e JOIN tree t ON e.manager_id = t.id)
SELECT name, lvl FROM tree ORDER BY lvl, name
LIMIT 6;

-- Q28. ROW_NUMBER [Window functions, L2]
-- Number employees by salary within each department.
SELECT d.name AS dept, e.name, e.salary,
  ROW_NUMBER() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC, e.name) AS rn
FROM employees e JOIN departments d ON d.id = e.dept_id
ORDER BY d.name, rn
LIMIT 4;

-- Q29. Top earner per department [Window functions, L2]
-- Highest-paid employee(s) in each department.
SELECT dept, name, salary FROM (
  SELECT d.name AS dept, e.name, e.salary,
    RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS r
  FROM employees e JOIN departments d ON d.id = e.dept_id)
WHERE r = 1 ORDER BY dept;

-- Q30. Top 2 per department [Window functions, L2]
-- Top two distinct salaries per department with names.
SELECT dept, name, salary FROM (
  SELECT d.name AS dept, e.name, e.salary,
    DENSE_RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS r
  FROM employees e JOIN departments d ON d.id = e.dept_id)
WHERE r <= 2 ORDER BY dept, salary DESC, name;

-- Q31. RANK vs DENSE_RANK [Window functions, L1]
-- Show ROW_NUMBER, RANK and DENSE_RANK of Engineering salaries side by side.
SELECT name, salary,
  ROW_NUMBER() OVER w AS row_num, RANK() OVER w AS rnk, DENSE_RANK() OVER w AS dense
FROM employees WHERE dept_id = 1
WINDOW w AS (ORDER BY salary DESC)
ORDER BY salary DESC, name;

-- Q32. Running total [Window functions, L2]
-- Running total of delivered revenue by order date.
WITH t AS (
  SELECT o.order_date, SUM(oi.qty * p.price) AS amt
  FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id
  WHERE o.status = 'delivered' GROUP BY o.id)
SELECT order_date, amt, SUM(amt) OVER (ORDER BY order_date) AS running
FROM t ORDER BY order_date
LIMIT 4;

-- Q33. Moving average [Window functions, L3]
-- 3-order moving average of delivered order values.
WITH t AS (
  SELECT o.order_date, SUM(oi.qty * p.price) AS amt
  FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id
  WHERE o.status = 'delivered' GROUP BY o.id)
SELECT order_date, amt,
  ROUND(AVG(amt) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS ma3
FROM t ORDER BY order_date
LIMIT 4;

-- Q34. LAG [Window functions, L2]
-- Days between each customer's consecutive orders.
SELECT customer_id, order_date,
  julianday(order_date) - julianday(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) AS gap_days
FROM orders ORDER BY customer_id, order_date
LIMIT 4;

-- Q35. Month-over-month growth [Window functions, L3]
-- Month-over-month change in delivered revenue.
WITH m AS (
  SELECT strftime('%Y-%m', o.order_date) AS month, SUM(oi.qty * p.price) AS rev
  FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id
  WHERE o.status = 'delivered' GROUP BY month)
SELECT month, rev, rev - LAG(rev) OVER (ORDER BY month) AS change
FROM m ORDER BY month;

-- Q36. Share of total [Window functions, L2]
-- Each department's share of the total salary bill, in percent.
SELECT d.name, SUM(e.salary) AS total,
  ROUND(100.0 * SUM(e.salary) / SUM(SUM(e.salary)) OVER (), 1) AS pct
FROM employees e JOIN departments d ON d.id = e.dept_id
GROUP BY d.id ORDER BY pct DESC;

-- Q37. Consecutive days [Window functions, L3]
-- Users who logged in on 3 or more consecutive days.
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins),
g AS (SELECT user_id, login_date,
  julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM d)
SELECT user_id, MIN(login_date) AS start_day, COUNT(*) AS streak
FROM g GROUP BY user_id, grp HAVING COUNT(*) >= 3
ORDER BY user_id;

-- Q38. First order per customer [Window functions, L2]
-- Each customer's first order and its date.
SELECT customer_id, id AS order_id, order_date FROM (
  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS rn FROM orders o)
WHERE rn = 1 ORDER BY customer_id;

-- Q39. Best-selling product per category [Window functions, L3]
-- In each category, the product with the most units sold.
WITH s AS (
  SELECT p.category, p.name, SUM(oi.qty) AS units
  FROM products p JOIN order_items oi ON oi.product_id = p.id GROUP BY p.id),
r AS (SELECT *, RANK() OVER (PARTITION BY category ORDER BY units DESC) AS rk FROM s)
SELECT category, name, units FROM r WHERE rk = 1 ORDER BY category;

-- Q40. Index and plan [Performance, L2]
-- Add an index for lookups of orders by customer, and check the plan uses it.
CREATE INDEX idx_orders_customer ON orders(customer_id);
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 2;
