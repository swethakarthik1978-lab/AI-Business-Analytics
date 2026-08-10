import csv
import random
from faker import Faker


categories = [
    "Electronics",
    "Home Appliances",
    "Furniture",
    "Clothing",
    "Books"
]

products = [
    "Laptop",
    "Mouse",
    "Keyboard",
    "Monitor",
    "Printer",
    "Tablet",
    "Camera",
    "Chair",
    "Table",
    "Sofa",
    "T-Shirt",
    "Jeans",
    "Jacket",
    "Book",
    "Speaker"
]


# =========================================================
# PRODUCTS
# =========================================================

with open("data/products.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "ProductID",
        "ProductName",
        "Category",
        "Price",
        "Stock"
    ])

    for i in range(1, 101):
        writer.writerow([
            i,
            random.choice(products),
            random.choice(categories),
            random.randint(500, 80000),
            random.randint(5, 200)
        ])

print("products.csv created successfully")


# =========================================================
# CUSTOMERS
# =========================================================

fake = Faker("en_US")

with open("data/customers.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "CustomerID",
        "CustomerName",
        "Email",
        "Phone",
        "City"
    ])

    for i in range(1, 101):
        writer.writerow([
            i,
            fake.name(),
            fake.email(),
            fake.msisdn()[:10],
            fake.city()
        ])

print("customers.csv created successfully")


# =========================================================
# INVENTORY
# =========================================================

with open("data/inventory.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "InventoryID",
        "ProductID",
        "CurrentStock",
        "ReorderLevel"
    ])

    for i in range(1, 101):
        writer.writerow([
            i,
            i,
            random.randint(10, 300),
            random.randint(5, 50)
        ])

print("inventory.csv created successfully")


# =========================================================
# FINANCE
# =========================================================

with open("data/finance.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "FinanceID",
        "Revenue",
        "Expenses",
        "Profit"
    ])

    for i in range(1, 101):
        revenue = random.randint(50000, 500000)
        expenses = random.randint(30000, revenue)
        profit = revenue - expenses

        writer.writerow([
            i,
            revenue,
            expenses,
            profit
        ])

print("finance.csv created successfully")


# =========================================================
# SALES
# =========================================================

sales = [
    [1, 1001, 1, 1, 2, 499.99, 999.98, "2026-07-01"],
    [2, 1002, 2, 2, 1, 899.00, 899.00, "2026-07-02"],
    [3, 1003, 3, 3, 3, 299.50, 898.50, "2026-07-03"]
]

with open("data/sales.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "SaleID",
        "OrderID",
        "ProductID",
        "CustomerID",
        "Quantity",
        "UnitPrice",
        "TotalAmount",
        "SaleDate"
    ])

    writer.writerows(sales)

print("sales.csv created successfully")