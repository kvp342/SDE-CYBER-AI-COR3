# SQL injection

## The bug
SQL injection happens when user input is concatenated into a SQL query, so the input changes the query structure instead of being treated as data.

## The fix
Use parameterised queries or prepared statements. The database then receives the query and the values separately, so input can never become SQL code.

## Defence in depth
Give the database account least privilege, validate input types, and avoid detailed database errors in responses. A web application firewall can block common payloads but is not a fix.

## Testing
Test with a single quote, boolean conditions and time delays, only on systems you are allowed to test, such as PortSwigger Web Security Academy labs.
