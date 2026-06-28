import sqlite3
import os

def create_department_store():
    conn = sqlite3.connect('../databases/department_store.sqlite')
    c = conn.cursor()
    
    # Drop existing
    c.execute('DROP TABLE IF EXISTS Customers')
    c.execute('DROP TABLE IF EXISTS Customer_Orders')
    c.execute('DROP TABLE IF EXISTS Suppliers')
    c.execute('DROP TABLE IF EXISTS Product_Suppliers')
    
    # Create tables
    c.execute('CREATE TABLE Customers (customer_id INTEGER PRIMARY KEY, payment_method_code TEXT)')
    c.execute('CREATE TABLE Customer_Orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER)')
    c.execute('CREATE TABLE Suppliers (supplier_id INTEGER PRIMARY KEY, supplier_name TEXT)')
    c.execute('CREATE TABLE Product_Suppliers (product_id INTEGER PRIMARY KEY, product_name TEXT, supplier_id INTEGER, total_amount_purchased INTEGER)')
    
    # Insert Customers and Orders
    # We want 45% Credit Card, 25% Bank Transfer, 20% PayPal, 10% Cash (out of ~100 orders for simplicity)
    c.execute("INSERT INTO Customers VALUES (1, 'Credit Card')")
    c.execute("INSERT INTO Customers VALUES (2, 'Bank Transfer')")
    c.execute("INSERT INTO Customers VALUES (3, 'PayPal')")
    c.execute("INSERT INTO Customers VALUES (4, 'Cash')")
    
    import random
    order_id = 1
    for _ in range(45):
        c.execute(f"INSERT INTO Customer_Orders VALUES ({order_id}, 1, {random.randint(101, 105)})")
        order_id += 1
    for _ in range(25):
        c.execute(f"INSERT INTO Customer_Orders VALUES ({order_id}, 2, {random.randint(101, 105)})")
        order_id += 1
    for _ in range(20):
        c.execute(f"INSERT INTO Customer_Orders VALUES ({order_id}, 3, {random.randint(101, 105)})")
        order_id += 1
    for _ in range(10):
        c.execute(f"INSERT INTO Customer_Orders VALUES ({order_id}, 4, {random.randint(101, 105)})")
        order_id += 1

    # Insert Suppliers
    suppliers = [(1, 'Sports Inc.'), (2, 'Premium Goods Co.'), (3, 'Fashion Hub'), (4, 'Global Tech')]
    c.executemany("INSERT INTO Suppliers VALUES (?, ?)", suppliers)
    
    # Insert Product_Suppliers
    products = [
        (101, 'Running Shoes', 1, 87),
        (102, 'Wireless Earbuds', 2, 134),
        (103, 'Smart Watch', 3, 215),
        (104, 'Leather Jacket', 4, 302),
        (105, 'Luxury Handbag', 4, 451)
    ]
    c.executemany("INSERT INTO Product_Suppliers VALUES (?, ?, ?, ?)", products)
    
    conn.commit()
    conn.close()

def create_hr_management():
    conn = sqlite3.connect('../databases/hr_management.sqlite')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS Departments')
    c.execute('DROP TABLE IF EXISTS Employees')
    
    c.execute('CREATE TABLE Departments (Department_ID INTEGER PRIMARY KEY, Department_Name TEXT)')
    c.execute('CREATE TABLE Employees (Employee_ID INTEGER PRIMARY KEY, Department_ID INTEGER, Salary INTEGER)')
    
    depts = [(1, 'Executive'), (2, 'Engineering'), (3, 'Marketing'), (4, 'Sales'), (5, 'HR')]
    c.executemany("INSERT INTO Departments VALUES (?, ?)", depts)
    
    # Insert Employees to get avg salary close to our mock (152k, 115k, 92k, 85k, 78k)
    emps = [
        (1, 1, 150000), (2, 1, 154000), # Exec avg 152k
        (3, 2, 110000), (4, 2, 120000), # Eng avg 115k
        (5, 3, 90000), (6, 3, 94000),   # Mkt avg 92k
        (7, 4, 80000), (8, 4, 90000),   # Sales avg 85k
        (9, 5, 75000), (10, 5, 81000)   # HR avg 78k
    ]
    c.executemany("INSERT INTO Employees VALUES (?, ?, ?)", emps)
    
    conn.commit()
    conn.close()

def create_financial_logs():
    conn = sqlite3.connect('../databases/financial_logs.sqlite')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS Financial_Logs')
    
    c.execute('CREATE TABLE Financial_Logs (Log_ID INTEGER PRIMARY KEY, Log_Month TEXT, Log_Year INTEGER, Revenue_Amount INTEGER)')
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    revenue = [420, 450, 410, 580, 620, 690, 710, 730, 810, 850, 920, 1050]
    
    logs = [(i+1, months[i], 2023, revenue[i]) for i in range(12)]
    c.executemany("INSERT INTO Financial_Logs VALUES (?, ?, ?, ?)", logs)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_department_store()
    create_hr_management()
    create_financial_logs()
    print("Created 3 SQLite databases.")
