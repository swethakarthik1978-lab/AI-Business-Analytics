from config import PROJECT_NAME, VERSION
from database.database import engine, Base, SessionLocal
from database.models import Product, Customer, Order, Inventory, Finance
from database.crud import * 
from data_collection import load_data
from preprocessing.clean_data import clean_dataframe

def main():
    print("=" * 50)
    print(PROJECT_NAME)
    print("Version", VERSION)
    print("=" * 50)
    print("Welcome to the AI Business Analytics Platform")

    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

    db = SessionLocal() 
    
    product = Product( ProductName="Laptop", Category="Electronics", Price=75000, Stock=25)
    add_product(db, product)
    for p in get_products(db):
        print( p.ProductID, p.ProductName, p.Category, p.Price, p.Stock )
    update_product_stock(db, product.ProductID, 10)
    p = get_product_by_id (db, product.ProductID) 
    print(p.ProductID, p.ProductName, p.Stock)

    db.close()

if __name__ == "__main__": 
    main() 