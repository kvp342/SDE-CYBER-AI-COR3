SQL · INTERVIEW PACK

# 40 SQL questions run on a real database

From filters and joins to window functions, on one small company database (employees, departments, customers, orders, products, logins). Every query was run in SQLite 3.53.1; the output shown under it is what it returned. The same schema, data and queries are in **sql-pack.sql** next to this PDF.

**How to use.** Read the question, cover the answer, write your query, then compare. Practise online for free on the [LeetCode SQL 50 study plan](https://leetcode.com/studyplan/top-sql-50/) or [SQLBolt](https://sqlbolt.com/). Dialect differences (SQLite, MySQL, PostgreSQL) are noted where they matter. [Sample database →](#the-sample-database)

| \#  | Question                                      | Topic            | Level |
|-----|-----------------------------------------------|------------------|-------|
| 1   | [Filter and sort](#q1-filter-and-sort-l1)                   | Basics           | L1    |
| 2   | [DISTINCT](#q2-distinct-l1)                          | Basics           | L1    |
| 3   | [NULL check](#q3-null-check-l1)                        | Basics           | L1    |
| 4   | [LIKE](#q4-like-l1)                              | Basics           | L1    |
| 5   | [CASE](#q5-case-l1)                              | Basics           | L1    |
| 6   | [INNER JOIN](#q6-inner-join-l1)                        | Joins            | L1    |
| 7   | [LEFT JOIN](#q7-left-join-l1)                         | Joins            | L1    |
| 8   | [Anti-join](#q8-anti-join-l2)                         | Joins            | L2    |
| 9   | [Self join](#q9-self-join-l2)                         | Joins            | L2    |
| 10  | [Earns more than manager](#q10-earns-more-than-manager-l2)           | Joins            | L2    |
| 11  | [Customers who never ordered](#q11-customers-who-never-ordered-l1)       | Joins            | L1    |
| 12  | [Three-table join](#q12-three-table-join-l2)                  | Joins            | L2    |
| 13  | [COUNT and GROUP BY](#q13-count-and-group-by-l1)                | Aggregation      | L1    |
| 14  | [AVG and HAVING](#q14-avg-and-having-l2)                    | Aggregation      | L2    |
| 15  | [Revenue per order](#q15-revenue-per-order-l2)                 | Aggregation      | L2    |
| 16  | [Revenue per customer](#q16-revenue-per-customer-l2)              | Aggregation      | L2    |
| 17  | [Monthly revenue](#q17-monthly-revenue-l2)                   | Aggregation      | L2    |
| 18  | [Conditional count](#q18-conditional-count-l2)                 | Aggregation      | L2    |
| 19  | [Duplicates](#q19-duplicates-l1)                        | Aggregation      | L1    |
| 20  | [Delete duplicates](#q20-delete-duplicates-l2)                 | Aggregation      | L2    |
| 21  | [Second-highest salary](#q21-second-highest-salary-l2)             | Subqueries       | L2    |
| 22  | [Nth-highest salary](#q22-nth-highest-salary-l2)                | Subqueries       | L2    |
| 23  | [Above department average](#q23-above-department-average-l2)          | Subqueries       | L2    |
| 24  | [IN with subquery](#q24-in-with-subquery-l1)                  | Subqueries       | L1    |
| 25  | [Bought every category](#q25-bought-every-category-l3)             | Subqueries       | L3    |
| 26  | [CTE](#q26-cte-l2)                               | Subqueries       | L2    |
| 27  | [Recursive CTE](#q27-recursive-cte-l3)                     | Subqueries       | L3    |
| 28  | [ROW_NUMBER](#q28-row_number-l2)                        | Window functions | L2    |
| 29  | [Top earner per department](#q29-top-earner-per-department-l2)         | Window functions | L2    |
| 30  | [Top 2 per department](#q30-top-2-per-department-l2)              | Window functions | L2    |
| 31  | [RANK vs DENSE_RANK](#q31-rank-vs-dense_rank-l1)                | Window functions | L1    |
| 32  | [Running total](#q32-running-total-l2)                     | Window functions | L2    |
| 33  | [Moving average](#q33-moving-average-l3)                    | Window functions | L3    |
| 34  | [LAG](#q34-lag-l2)                               | Window functions | L2    |
| 35  | [Month-over-month growth](#q35-month-over-month-growth-l3)           | Window functions | L3    |
| 36  | [Share of total](#q36-share-of-total-l2)                    | Window functions | L2    |
| 37  | [Consecutive days](#q37-consecutive-days-l3)                  | Window functions | L3    |
| 38  | [First order per customer](#q38-first-order-per-customer-l2)          | Window functions | L2    |
| 39  | [Best-selling product per category](#q39-best-selling-product-per-category-l3) | Window functions | L3    |
| 40  | [Index and plan](#q40-index-and-plan-l2)                    | Performance      | L2    |

## The sample database

Small enough to check every answer by hand. Sara has no department, Research has no employees, Farah never ordered, order 3 was cancelled and user 3 has a duplicate login: each is there for a question. See also the [Knowledge Base DBMS pages](knowledge-base/core-cs.md#normalisation-and-keys).

### departments 4 rows

| id  | name        | location  |
|-----|-------------|-----------|
| 1   | Engineering | Bengaluru |
| 2   | Security    | Hyderabad |
| 3   | Sales       | Mumbai    |
| 4   | Research    | Pune      |

### employees 11 rows

| id  | name   | dept_id | manager_id | salary | hire_date  |
|-----|--------|---------|------------|--------|------------|
| 1   | Asha   | 1       | NULL       | 250000 | 2018-03-01 |
| 2   | Ravi   | 1       | 1          | 180000 | 2019-07-15 |
| 3   | Meera  | 1       | 1          | 180000 | 2020-01-10 |
| 4   | Kabir  | 1       | 2          | 120000 | 2022-06-01 |
| 5   | Divya  | 2       | 1          | 200000 | 2019-02-20 |
| 6   | Arjun  | 2       | 5          | 140000 | 2021-09-05 |
| 7   | Neha   | 2       | 5          | 95000  | 2023-01-16 |
| 8   | Vikram | 3       | 1          | 150000 | 2020-11-30 |
| 9   | Isha   | 3       | 8          | 160000 | 2022-04-11 |
| 10  | Rohan  | 3       | 8          | 90000  | 2023-08-21 |
| 11  | Sara   | NULL    | 1          | 70000  | 2024-02-01 |

### customers 6 rows

| id  | name   | city    | signup_date |
|-----|--------|---------|-------------|
| 1   | Anil   | Delhi   | 2024-01-05  |
| 2   | Bina   | Mumbai  | 2024-01-20  |
| 3   | Chirag | Delhi   | 2024-02-11  |
| 4   | Deepa  | Chennai | 2024-03-02  |
| 5   | Eshan  | Mumbai  | 2024-03-15  |
| 6   | Farah  | Pune    | 2024-04-01  |

### products 6 rows

| id  | name       | category    | price |
|-----|------------|-------------|-------|
| 1   | Laptop     | Electronics | 60000 |
| 2   | Phone      | Electronics | 30000 |
| 3   | Headphones | Electronics | 3000  |
| 4   | Desk       | Furniture   | 12000 |
| 5   | Chair      | Furniture   | 8000  |
| 6   | Notebook   | Stationery  | 100   |

### orders 10 rows

| id  | customer_id | order_date | status    |
|-----|-------------|------------|-----------|
| 1   | 1           | 2024-02-01 | delivered |
| 2   | 1           | 2024-02-15 | delivered |
| 3   | 2           | 2024-02-20 | cancelled |
| 4   | 2           | 2024-03-05 | delivered |
| 5   | 3           | 2024-03-07 | delivered |
| 6   | 4           | 2024-03-20 | shipped   |
| 7   | 1           | 2024-04-02 | delivered |
| 8   | 5           | 2024-04-10 | delivered |
| 9   | 3           | 2024-04-18 | delivered |
| 10  | 2           | 2024-04-25 | delivered |

### order_items 15 rows

| order_id | product_id | qty |
|----------|------------|-----|
| 1        | 1          | 1   |
| 1        | 3          | 2   |
| 2        | 6          | 10  |
| 3        | 2          | 1   |
| 4        | 2          | 1   |
| 4        | 3          | 1   |
| 5        | 4          | 1   |
| 5        | 5          | 2   |
| 6        | 1          | 1   |
| 7        | 3          | 1   |
| 8        | 5          | 4   |
| 9        | 6          | 5   |
| 9        | 3          | 1   |
| 10       | 1          | 1   |
| 10       | 4          | 1   |

### logins 11 rows

| user_id | login_date |
|---------|------------|
| 1       | 2024-05-01 |
| 1       | 2024-05-02 |
| 1       | 2024-05-03 |
| 1       | 2024-05-05 |
| 2       | 2024-05-01 |
| 2       | 2024-05-03 |
| 3       | 2024-05-02 |
| 3       | 2024-05-03 |
| 3       | 2024-05-04 |
| 3       | 2024-05-05 |
| 3       | 2024-05-05 |

## Basics

### Q1. Filter and sort L1

List employees earning more than 1,50,000, highest first.

``` sql
SELECT name, salary FROM employees
WHERE salary > 150000
ORDER BY salary DESC, name;
```

Output

| name  | salary |
|-------|--------|
| Asha  | 250000 |
| Divya | 200000 |
| Meera | 180000 |
| Ravi  | 180000 |
| Isha  | 160000 |

WHERE filters rows; a second sort key makes ties deterministic.

### Q2. DISTINCT L1

Which cities do customers come from?

``` sql
SELECT DISTINCT city FROM customers ORDER BY city;
```

Output

| city    |
|---------|
| Chennai |
| Delhi   |
| Mumbai  |
| Pune    |

DISTINCT removes duplicate rows from the result.

### Q3. NULL check L1

Find employees with no department.

``` sql
SELECT name FROM employees WHERE dept_id IS NULL;
```

Output

| name |
|------|
| Sara |

Use IS NULL; dept_id = NULL is never true.

### Q4. LIKE L1

Find customers whose name starts with a vowel.

``` sql
SELECT name FROM customers
WHERE substr(name, 1, 1) IN ('A','E','I','O','U')
ORDER BY name;
```

Output

| name  |
|-------|
| Anil  |
| Eshan |

In MySQL you could also use REGEXP '^\[AEIOU\]'. LIKE 'A%' handles one letter at a time.

### Q5. CASE L1

Label each employee's salary band: High (≥ 2,00,000), Mid (≥ 1,00,000), else Low.

``` sql
SELECT name,
  CASE WHEN salary >= 200000 THEN 'High'
       WHEN salary >= 100000 THEN 'Mid'
       ELSE 'Low' END AS band
FROM employees ORDER BY id;
```

Output

| name   | band |
|--------|------|
| Asha   | High |
| Ravi   | Mid  |
| Meera  | Mid  |
| Kabir  | Mid  |
| Divya  | High |
| Arjun  | Mid  |
| Neha   | Low  |
| Vikram | Mid  |
| Isha   | Mid  |
| Rohan  | Low  |
| Sara   | Low  |

CASE checks conditions in order and returns the first match.

## Joins

### Q6. INNER JOIN L1

Show each employee with their department name.

``` sql
SELECT e.name, d.name AS dept
FROM employees e
JOIN departments d ON d.id = e.dept_id
ORDER BY e.id;
```

Output

| name   | dept        |
|--------|-------------|
| Asha   | Engineering |
| Ravi   | Engineering |
| Meera  | Engineering |
| Kabir  | Engineering |
| Divya  | Security    |
| Arjun  | Security    |
| Neha   | Security    |
| Vikram | Sales       |
| Isha   | Sales       |
| Rohan  | Sales       |

Inner join drops Sara, who has no department.

### Q7. LEFT JOIN L1

Show every employee and their department, including those without one.

``` sql
SELECT e.name, d.name AS dept
FROM employees e
LEFT JOIN departments d ON d.id = e.dept_id
ORDER BY e.id DESC
LIMIT 3;
```

Output

| name  | dept  |
|-------|-------|
| Sara  | NULL  |
| Rohan | Sales |
| Isha  | Sales |

Left join keeps all employees; missing departments show as NULL.

### Q8. Anti-join L2

Find departments with no employees.

``` sql
SELECT d.name
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
WHERE e.id IS NULL;
```

Output

| name     |
|----------|
| Research |

Left join then keep rows where nothing matched. NOT EXISTS works too.

### Q9. Self join L2

Show each employee with their manager's name.

``` sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id
ORDER BY e.id
LIMIT 4;
```

Output

| employee | manager |
|----------|---------|
| Asha     | NULL    |
| Ravi     | Asha    |
| Meera    | Asha    |
| Kabir    | Ravi    |

Join the table to itself with two aliases.

### Q10. Earns more than manager L2

Find employees who earn more than their manager.

``` sql
SELECT e.name
FROM employees e
JOIN employees m ON m.id = e.manager_id
WHERE e.salary > m.salary;
```

Output

| name |
|------|
| Isha |

Join each employee to their manager row and compare.

### Q11. Customers who never ordered L1

Which customers have never placed an order?

``` sql
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

Output

| name  |
|-------|
| Farah |

NOT EXISTS is safe with NULLs; NOT IN breaks if the subquery returns a NULL.

### Q12. Three-table join L2

List the products in order 4 with quantity and line total.

``` sql
SELECT p.name, oi.qty, oi.qty * p.price AS line_total
FROM order_items oi
JOIN products p ON p.id = oi.product_id
WHERE oi.order_id = 4
ORDER BY p.name;
```

Output

| name       | qty | line_total |
|------------|-----|------------|
| Headphones | 1   | 3000       |
| Phone      | 1   | 30000      |

Join through the bridge table order_items.

## Aggregation

### Q13. COUNT and GROUP BY L1

How many employees are in each department?

``` sql
SELECT d.name, COUNT(e.id) AS headcount
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.id
GROUP BY d.id
ORDER BY headcount DESC, d.name;
```

Output

| name        | headcount |
|-------------|-----------|
| Engineering | 4         |
| Sales       | 3         |
| Security    | 3         |
| Research    | 0         |

COUNT(e.id) counts 0 for Research; COUNT(\*) would wrongly count 1.

### Q14. AVG and HAVING L2

Departments whose average salary is above 1,30,000.

``` sql
SELECT d.name, ROUND(AVG(e.salary)) AS avg_salary
FROM employees e JOIN departments d ON d.id = e.dept_id
GROUP BY d.id
HAVING AVG(e.salary) > 130000
ORDER BY avg_salary DESC;
```

Output

| name        | avg_salary |
|-------------|------------|
| Engineering | 182500     |
| Security    | 145000     |
| Sales       | 133333     |

HAVING filters groups after aggregation; WHERE cannot use AVG.

### Q15. Revenue per order L2

Total value of each delivered order, largest first.

``` sql
SELECT o.id, SUM(oi.qty * p.price) AS total
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE o.status = 'delivered'
GROUP BY o.id
ORDER BY total DESC, o.id
LIMIT 3;
```

Output

| id  | total |
|-----|-------|
| 10  | 72000 |
| 1   | 66000 |
| 4   | 33000 |

Aggregate line totals per order.

### Q16. Revenue per customer L2

Total delivered revenue per customer.

``` sql
SELECT c.name, SUM(oi.qty * p.price) AS revenue
FROM customers c
JOIN orders o ON o.customer_id = c.id AND o.status = 'delivered'
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
GROUP BY c.id
ORDER BY revenue DESC;
```

Output

| name   | revenue |
|--------|---------|
| Bina   | 105000  |
| Anil   | 70000   |
| Eshan  | 32000   |
| Chirag | 31500   |

Putting the status filter in the ON clause keeps the query readable; in an inner join it behaves like WHERE.

### Q17. Monthly revenue L2

Delivered revenue per month.

``` sql
SELECT strftime('%Y-%m', o.order_date) AS month, SUM(oi.qty * p.price) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE o.status = 'delivered'
GROUP BY month ORDER BY month;
```

Output

| month   | revenue |
|---------|---------|
| 2024-02 | 67000   |
| 2024-03 | 61000   |
| 2024-04 | 110500  |

SQLite uses strftime; MySQL uses DATE_FORMAT(order_date, '%Y-%m'); PostgreSQL uses to_char or date_trunc.

### Q18. Conditional count L2

For each customer, count delivered and cancelled orders in one row.

``` sql
SELECT c.name,
  SUM(o.status = 'delivered') AS delivered,
  SUM(o.status = 'cancelled') AS cancelled
FROM customers c JOIN orders o ON o.customer_id = c.id
GROUP BY c.id ORDER BY c.id;
```

Output

| name   | delivered | cancelled |
|--------|-----------|-----------|
| Anil   | 3         | 0         |
| Bina   | 2         | 1         |
| Chirag | 2         | 0         |
| Deepa  | 0         | 0         |
| Eshan  | 1         | 0         |

A condition is 1 or 0 in SQLite and MySQL. Portable form: SUM(CASE WHEN ... THEN 1 ELSE 0 END).

### Q19. Duplicates L1

Find logins recorded more than once for the same user and day.

``` sql
SELECT user_id, login_date, COUNT(*) AS n
FROM logins
GROUP BY user_id, login_date
HAVING COUNT(*) > 1;
```

Output

| user_id | login_date | n   |
|---------|------------|-----|
| 3       | 2024-05-05 | 2   |

Group by every column that defines a duplicate.

### Q20. Delete duplicates L2

Delete duplicate logins, keeping one copy (shown as the rows that would remain).

``` sql
SELECT user_id, login_date FROM logins
WHERE rowid IN (SELECT MIN(rowid) FROM logins GROUP BY user_id, login_date)
ORDER BY user_id, login_date
LIMIT 3;
```

Output

| user_id | login_date |
|---------|------------|
| 1       | 2024-05-01 |
| 1       | 2024-05-02 |
| 1       | 2024-05-03 |

The real statement is DELETE FROM logins WHERE rowid NOT IN (SELECT MIN(rowid) ... ). Other databases use the primary key or ROW_NUMBER().

## Subqueries

### Q21. Second-highest salary L2

Find the second-highest distinct salary.

``` sql
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

Output

| second_highest |
|----------------|
| 200000         |

Returns NULL if there is no second value, which interviewers like.

### Q22. Nth-highest salary L2

Find the 3rd-highest distinct salary.

``` sql
SELECT DISTINCT salary FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 2;
```

Output

| salary |
|--------|
| 180000 |

DISTINCT first, so 1,80,000 counts once. DENSE_RANK() is the window-function version.

### Q23. Above department average L2

Employees earning more than their department's average.

``` sql
SELECT e.name, e.salary
FROM employees e
WHERE e.salary > (SELECT AVG(salary) FROM employees x WHERE x.dept_id = e.dept_id)
ORDER BY e.salary DESC;
```

Output

| name   | salary |
|--------|--------|
| Asha   | 250000 |
| Divya  | 200000 |
| Isha   | 160000 |
| Vikram | 150000 |

A correlated subquery runs once per outer row.

### Q24. IN with subquery L1

Customers who bought any Furniture product.

``` sql
SELECT DISTINCT c.name FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE o.id IN (SELECT oi.order_id FROM order_items oi
               JOIN products p ON p.id = oi.product_id
               WHERE p.category = 'Furniture')
ORDER BY c.name;
```

Output

| name   |
|--------|
| Bina   |
| Chirag |
| Eshan  |

IN is fine when the subquery cannot return NULL.

### Q25. Bought every category L3

Customers who bought from every product category (relational division).

``` sql
SELECT c.name FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
GROUP BY c.id
HAVING COUNT(DISTINCT p.category) = (SELECT COUNT(DISTINCT category) FROM products);
```

Output

| name   |
|--------|
| Chirag |

Count distinct categories per customer and compare with the total.

### Q26. CTE L2

Using a CTE, list departments whose total salary is above the average department total.

``` sql
WITH t AS (
  SELECT dept_id, SUM(salary) AS total FROM employees
  WHERE dept_id IS NOT NULL GROUP BY dept_id)
SELECT d.name, t.total FROM t JOIN departments d ON d.id = t.dept_id
WHERE t.total > (SELECT AVG(total) FROM t);
```

Output

| name        | total  |
|-------------|--------|
| Engineering | 730000 |

A CTE names an intermediate result so you can use it twice.

### Q27. Recursive CTE L3

List everyone in Asha's reporting tree with their level.

``` sql
WITH RECURSIVE tree(id, name, lvl) AS (
  SELECT id, name, 0 FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, t.lvl + 1 FROM employees e JOIN tree t ON e.manager_id = t.id)
SELECT name, lvl FROM tree ORDER BY lvl, name
LIMIT 6;
```

Output

| name   | lvl |
|--------|-----|
| Asha   | 0   |
| Divya  | 1   |
| Meera  | 1   |
| Ravi   | 1   |
| Sara   | 1   |
| Vikram | 1   |

The anchor picks the root; the recursive part adds one level per pass.

## Window functions

### Q28. ROW_NUMBER L2

Number employees by salary within each department.

``` sql
SELECT d.name AS dept, e.name, e.salary,
  ROW_NUMBER() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC, e.name) AS rn
FROM employees e JOIN departments d ON d.id = e.dept_id
ORDER BY d.name, rn
LIMIT 4;
```

Output

| dept        | name  | salary | rn  |
|-------------|-------|--------|-----|
| Engineering | Asha  | 250000 | 1   |
| Engineering | Meera | 180000 | 2   |
| Engineering | Ravi  | 180000 | 3   |
| Engineering | Kabir | 120000 | 4   |

PARTITION BY restarts the numbering for each department.

### Q29. Top earner per department L2

Highest-paid employee(s) in each department.

``` sql
SELECT dept, name, salary FROM (
  SELECT d.name AS dept, e.name, e.salary,
    RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS r
  FROM employees e JOIN departments d ON d.id = e.dept_id)
WHERE r = 1 ORDER BY dept;
```

Output

| dept        | name  | salary |
|-------------|-------|--------|
| Engineering | Asha  | 250000 |
| Sales       | Isha  | 160000 |
| Security    | Divya | 200000 |

RANK keeps ties; ROW_NUMBER would pick one arbitrarily.

### Q30. Top 2 per department L2

Top two distinct salaries per department with names.

``` sql
SELECT dept, name, salary FROM (
  SELECT d.name AS dept, e.name, e.salary,
    DENSE_RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS r
  FROM employees e JOIN departments d ON d.id = e.dept_id)
WHERE r <= 2 ORDER BY dept, salary DESC, name;
```

Output

| dept        | name   | salary |
|-------------|--------|--------|
| Engineering | Asha   | 250000 |
| Engineering | Meera  | 180000 |
| Engineering | Ravi   | 180000 |
| Sales       | Isha   | 160000 |
| Sales       | Vikram | 150000 |
| Security    | Divya  | 200000 |
| Security    | Arjun  | 140000 |

DENSE_RANK so Ravi and Meera (tied) are both second in Engineering.

### Q31. RANK vs DENSE_RANK L1

Show ROW_NUMBER, RANK and DENSE_RANK of Engineering salaries side by side.

``` sql
SELECT name, salary,
  ROW_NUMBER() OVER w AS row_num, RANK() OVER w AS rnk, DENSE_RANK() OVER w AS dense
FROM employees WHERE dept_id = 1
WINDOW w AS (ORDER BY salary DESC)
ORDER BY salary DESC, name;
```

Output

| name  | salary | row_num | rnk | dense |
|-------|--------|---------|-----|-------|
| Asha  | 250000 | 1       | 1   | 1     |
| Meera | 180000 | 3       | 2   | 2     |
| Ravi  | 180000 | 2       | 2   | 2     |
| Kabir | 120000 | 4       | 4   | 3     |

Ties: RANK skips the next number, DENSE_RANK does not. (Named WINDOW clauses work in SQLite, MySQL 8 and PostgreSQL.)

### Q32. Running total L2

Running total of delivered revenue by order date.

``` sql
WITH t AS (
  SELECT o.order_date, SUM(oi.qty * p.price) AS amt
  FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id
  WHERE o.status = 'delivered' GROUP BY o.id)
SELECT order_date, amt, SUM(amt) OVER (ORDER BY order_date) AS running
FROM t ORDER BY order_date
LIMIT 4;
```

Output

| order_date | amt   | running |
|------------|-------|---------|
| 2024-02-01 | 66000 | 66000   |
| 2024-02-15 | 1000  | 67000   |
| 2024-03-05 | 33000 | 100000  |
| 2024-03-07 | 28000 | 128000  |

SUM() OVER (ORDER BY ...) accumulates row by row.

### Q33. Moving average L3

3-order moving average of delivered order values.

``` sql
WITH t AS (
  SELECT o.order_date, SUM(oi.qty * p.price) AS amt
  FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id
  WHERE o.status = 'delivered' GROUP BY o.id)
SELECT order_date, amt,
  ROUND(AVG(amt) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS ma3
FROM t ORDER BY order_date
LIMIT 4;
```

Output

| order_date | amt   | ma3   |
|------------|-------|-------|
| 2024-02-01 | 66000 | 66000 |
| 2024-02-15 | 1000  | 33500 |
| 2024-03-05 | 33000 | 33333 |
| 2024-03-07 | 28000 | 20667 |

The ROWS frame sets exactly which rows are averaged.

### Q34. LAG L2

Days between each customer's consecutive orders.

``` sql
SELECT customer_id, order_date,
  julianday(order_date) - julianday(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) AS gap_days
FROM orders ORDER BY customer_id, order_date
LIMIT 4;
```

Output

| customer_id | order_date | gap_days |
|-------------|------------|----------|
| 1           | 2024-02-01 | NULL     |
| 1           | 2024-02-15 | 14       |
| 1           | 2024-04-02 | 47       |
| 2           | 2024-02-20 | NULL     |

LAG reads the previous row in the partition. Date difference: DATEDIFF in MySQL, subtraction in PostgreSQL.

### Q35. Month-over-month growth L3

Month-over-month change in delivered revenue.

``` sql
WITH m AS (
  SELECT strftime('%Y-%m', o.order_date) AS month, SUM(oi.qty * p.price) AS rev
  FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id
  WHERE o.status = 'delivered' GROUP BY month)
SELECT month, rev, rev - LAG(rev) OVER (ORDER BY month) AS change
FROM m ORDER BY month;
```

Output

| month   | rev    | change |
|---------|--------|--------|
| 2024-02 | 67000  | NULL   |
| 2024-03 | 61000  | -6000  |
| 2024-04 | 110500 | 49500  |

First month has no previous value, so change is NULL.

### Q36. Share of total L2

Each department's share of the total salary bill, in percent.

``` sql
SELECT d.name, SUM(e.salary) AS total,
  ROUND(100.0 * SUM(e.salary) / SUM(SUM(e.salary)) OVER (), 1) AS pct
FROM employees e JOIN departments d ON d.id = e.dept_id
GROUP BY d.id ORDER BY pct DESC;
```

Output

| name        | total  | pct  |
|-------------|--------|------|
| Engineering | 730000 | 46.6 |
| Security    | 435000 | 27.8 |
| Sales       | 400000 | 25.6 |

A window over the grouped result: SUM(SUM(x)) OVER () is the grand total.

### Q37. Consecutive days L3

Users who logged in on 3 or more consecutive days.

``` sql
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins),
g AS (SELECT user_id, login_date,
  julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM d)
SELECT user_id, MIN(login_date) AS start_day, COUNT(*) AS streak
FROM g GROUP BY user_id, grp HAVING COUNT(*) >= 3
ORDER BY user_id;
```

Output

| user_id | start_day  | streak |
|---------|------------|--------|
| 1       | 2024-05-01 | 3      |
| 3       | 2024-05-02 | 4      |

Gaps-and-islands: in a run of consecutive dates, date minus row number is constant.

### Q38. First order per customer L2

Each customer's first order and its date.

``` sql
SELECT customer_id, id AS order_id, order_date FROM (
  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS rn FROM orders o)
WHERE rn = 1 ORDER BY customer_id;
```

Output

| customer_id | order_id | order_date |
|-------------|----------|------------|
| 1           | 1        | 2024-02-01 |
| 2           | 3        | 2024-02-20 |
| 3           | 5        | 2024-03-07 |
| 4           | 6        | 2024-03-20 |
| 5           | 8        | 2024-04-10 |

Keep row 1 of each partition. Same pattern for 'latest' with DESC.

### Q39. Best-selling product per category L3

In each category, the product with the most units sold.

``` sql
WITH s AS (
  SELECT p.category, p.name, SUM(oi.qty) AS units
  FROM products p JOIN order_items oi ON oi.product_id = p.id GROUP BY p.id),
r AS (SELECT *, RANK() OVER (PARTITION BY category ORDER BY units DESC) AS rk FROM s)
SELECT category, name, units FROM r WHERE rk = 1 ORDER BY category;
```

Output

| category    | name       | units |
|-------------|------------|-------|
| Electronics | Headphones | 5     |
| Furniture   | Chair      | 6     |
| Stationery  | Notebook   | 15    |

Aggregate first, then rank within each category.

## Performance

### Q40. Index and plan L2

Add an index for lookups of orders by customer, and check the plan uses it.

``` sql
CREATE INDEX idx_orders_customer ON orders(customer_id);
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 2;
```

Output

| id  | parent | notused | detail                                                        |
|-----|--------|---------|---------------------------------------------------------------|
| 3   | 0      | 61      | SEARCH orders USING INDEX idx_orders_customer (customer_id=?) |

The plan should say SEARCH ... USING INDEX instead of SCAN. Index the columns in WHERE and JOIN conditions; each index slows writes a little.
