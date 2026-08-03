import pandas as pd 
import sqlite3

customers = pd.read_csv("data/customers.csv")
finance = pd.read_csv("data/finance.csv")
inventory = pd.read_csv("data/inventory.csv")
products = pd.read_csv("data/products.csv")
sales = pd.read_csv("data/sales.csv")

sales.head()

print(sales.head())
print(sales.info())
print(sales.describe()) 

print("MISSING VALUES")
print(sales.isnull().sum())

sales["Quantity"] = sales["Quantity"].fillna(sales["Quantity"].mean())
sales["TotalAmount"] = sales["TotalAmount"].fillna(sales["TotalAmount"].mean())