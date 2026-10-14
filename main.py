import sqlite3
import pandas as pd

conn = sqlite3.Connection('data.sqlite')

#Rewrite below JOIN to use SubQuery/Write an equivalent query using a subquery
q = """
SELECT
    customerNumber,
    contactLastName,
    contactFirstName
FROM customers
JOIN orders 
    USING(customerNumber)
WHERE orderDate = '2003-01-31'

;

"""
pd.read_sql(q, conn)

q = """
SELECT
    customerNumber,
    contactLastName,
    contactFirstName
FROM customers
JOIN orders 
    USING(customerNumber)
WHERE orderDate = '2003-01-31'

;
"""
df = pd.read_sql(q, conn)
print(df)

#Select the total number of orders for each product name. Sort the results by the total number of items sold for that product.
q = """
SELECT
    productName,
    COUNT(orderNumber) AS numberOrders,
    SUM(quantityOrdered) AS totalUnitsSold
FROM products
JOIN orderdetails
    USING (productCode)
GROUP BY productName
ORDER BY totalUnitsSold DESC
;
"""
df = pd.read_sql(q, conn)
print(df)

#Select the product name and the total number of people who have ordered each product. Sort the results in descending order.
q = """
SELECT productName, COUNT(DISTINCT customerNumber) AS numPurchasers
FROM products
JOIN orderdetails
    USING(productCode)
JOIN orders
    USING(orderNumber)
GROUP BY productName
ORDER BY numPurchasers DESC
;
"""
df = pd.read_sql(q, conn)
print(df)

#Select the employee number, first name, last name, city (of the office), and office code of the employees who sold products that have been ordered by fewer than 20 people.
q = """
SELECT
    DISTINCT employeeNumber,
    officeCode,
    o.city,
    firstName,
    lastName
FROM employees AS e
JOIN offices AS o
    USING(officeCode)
JOIN customers AS c
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders
    USING(customerNumber)
JOIN orderdetails
    USING(orderNumber)
WHERE productCode IN (
    SELECT productCode
    FROM products
    JOIN orderdetails
        USING(productCode)
    JOIN orders
        USING(orderNumber)
    GROUP BY productCode
    HAVING COUNT(DISTINCT customerNumber) < 20
)
;
"""
df = pd.read_sql(q, conn)
print(df)

#Select the employee number, first name, last name, and number of customers for employees whose customers have an average credit limit over 15K
q = """
SELECT
    employeeNumber,
    firstName,
    lastName,
    COUNT(customerNumber) AS numCustomers
FROM employees AS e
JOIN customers As c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY employeeNumber
HAVING AVG(creditLimit) > 15000
;
"""
df = pd.read_sql(q, conn)
print(df)

conn.close()