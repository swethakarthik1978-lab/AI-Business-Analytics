from config import PROJECT_NAME, VERSION
from database.database import engine, Base, SessionLocal
from database.models import Product, Customer, Order, Inventory, Finance
from database.crud import *
from data_collection import load_data
from preprocessing.clean_data import clean_dataframe
from preprocessing.feature_engineering import create_features

def main():
    print("=" * 50)
    print(PROJECT_NAME)
    print("Version", VERSION)
    print("=" * 50)
    print("Welcome to the AI Business Analytics Platform")

    print("LOADING DATA")
    datasets = load_data()

    for name, df in datasets.items():
        print(name, df.shape)

    print("CLEANING DATA")
    clean_datasets = {}

    for name, df in datasets.items():
        print("CLEANING", name)
        clean_datasets[name] = clean_dataframe(df)

    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

    db = SessionLocal()

    add_customers(db, clean_datasets["customers"])
    add_products(db, clean_datasets["products"])
    add_inventory(db, clean_datasets["inventory"])
    add_finance(db, clean_datasets["finance"])

    df = create_features(df)

    print(clean_datasets["sales"])

    db.close()


if __name__ == "__main__":
    main()