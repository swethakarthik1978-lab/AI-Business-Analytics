import pandas as pd


def load_data():
    datasets = {
        "customers": pd.read_csv("data/customers.csv"),
        "finance": pd.read_csv("data/finance.csv"),
        "inventory": pd.read_csv("data/inventory.csv"),
        "products": pd.read_csv("data/products.csv"),
        "sales": pd.read_csv("data/sales.csv")
    }

    return datasets


