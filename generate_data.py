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
    "Laptop", "Mouse", "Keyboard", "Monitor", "Printer",
    "Tablet", "Camera", "Chair", "Table", "Sofa",
    "T-Shirt", "Jeans", "Jacket", "Book", "Speaker"
]

with open("data/products.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "ProductID",
        "ProductName",
        "Category",
        "Price",
        "Stock"
    ])

    for i in range(1,101):
        writer.writerow([
            i,
            random.choice(products),
            random.choice(categories),
            random.randint(500,80000),
            random.randint(5,200)
        ])

print("products.csv created successfully")

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

    for i in range(1,101):
        writer.writerow([
            i,
            fake.name(),
            fake.email(),
            fake.msisdn()[:10],
            fake.city()
        ])

print("customers.csv created successfully")

with open("data/inventory.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "InventoryID",
        "ProductID",
        "CurrentStock",
        "ReorderLevel"
    ])

    for i in range(1,101):
        writer.writerow([
            i,
            i,
            random.randint(10,300),
            random.randint(5,50)
        ])

print("inventory.csv created successfully")

with open("data/finance.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "FinanceID",
        "Revenue",
        "Expenses",
        "Profit"
    ])

    for i in range(1,101):
        revenue = random.randint(50000,500000)

        expenses = random.randint(30000, revenue)

        profit = revenue - expenses

        writer.writerow([
            i,
            revenue,
            expenses,
            profit
        ])

print("finance.csv created successfully")