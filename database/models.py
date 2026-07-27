from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from database.database import Base

class Product(Base):
    __tablename__ = "products"

    ProductID = Column(Integer, primary_key=True, index=True)
    ProductName = Column(String)
    Category = Column(String)
    Price = Column(Float)
    Stock = Column(Integer)

class Customer (Base):
    __tablename__ = "cutomers"

    CustomerID = Column(Integer, primary_key=True, index=True)
    CustomerName = Column(String)
    Email = Column(String)
    Phone = Column(String)
    City = Column(String)

class Order(Base):
    __tablename__ = "orders"

    OrderID = Column(Integer, primary_key=True, index=True)

    CustomerID = Column(Integer, ForeignKey("customers.CustomerID"))

    ProductID = Column(Integer, ForeignKey("products.ProductID"))

    Quantity = Column(Integer)

    OrderDate = Column(Date)

    TotalAmount = Column(Float)

class Inventory(Base):
    __tablename__ = "inventory"

    InventoryID = Column(Integer, primary_key=True, index=True)

    ProductID = Column(Integer, ForeignKey("products.ProductID"))

    StockAdded = Column(Integer)

    StockRemoved = Column(Integer)

    CurrentStock = Column(Integer)

class Finance(Base):
    __tablename__ = "finance"

    FinanceID = Column(Integer, primary_key=True, index=True)

    Date = Column(Date)

    Income = Column(Float)

    Expense = Column(Float)

    Profit = Column(Float)