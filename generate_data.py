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
product_data = []

with open("data/products.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:
        product_data.append(row)


sales = []

for sale_id in range(1, 101):

    order_id = 1000 + sale_id

    product = random.choice(product_data)

    product_id = int(product["ProductID"])

    customer_id = random.randint(1, 100)

    quantity = random.randint(1, 5)

    unit_price = float(product["Price"])

    total_amount = quantity * unit_price

    year = 2026
    month = random.randint(1, 8)
    day = random.randint(1, 28)

    sale_date = f"{year}-{month:02d}-{day:02d}"

    sales.append([
        sale_id,
        order_id,
        product_id,
        customer_id,
        quantity,
        unit_price,
        total_amount,
        sale_date
    ])

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