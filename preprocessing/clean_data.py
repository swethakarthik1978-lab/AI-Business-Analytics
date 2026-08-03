print("MISSING VALUES")
print(sales.isnull().sum())

sales["Quantity"] = sales["Quantity"].fillna(sales["Quantity"].mean())
sales["TotalAmount"] = sales["TotalAmount"].fillna(sales["TotalAmount"].mean())