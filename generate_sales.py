# ==================================================
# IMPORTS
# ==================================================

from pathlib import Path
import random

import pandas as pd


# ==================================================
# PROJECT PATHS
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

PRODUCTS_FILE = DATA_DIR / "products.csv"
CUSTOMERS_FILE = DATA_DIR / "customers.csv"
SALES_FILE = DATA_DIR / "sales.csv"


# ==================================================
# SETTINGS
# ==================================================

NUMBER_OF_ORDERS = 100

MIN_PRODUCTS_PER_ORDER = 2
MAX_PRODUCTS_PER_ORDER = 5

MIN_QUANTITY = 1
MAX_QUANTITY = 5

START_DATE = "2026-01-01"
END_DATE = "2026-08-27"

RANDOM_SEED = 42


# ==================================================
# LOAD PRODUCT AND CUSTOMER DATA
# ==================================================

def load_source_data():

    if not PRODUCTS_FILE.exists():

        raise FileNotFoundError(
            "data/products.csv was not found."
        )

    if not CUSTOMERS_FILE.exists():

        raise FileNotFoundError(
            "data/customers.csv was not found."
        )

    products = pd.read_csv(
        PRODUCTS_FILE
    )

    customers = pd.read_csv(
        CUSTOMERS_FILE
    )

    return products, customers


# ==================================================
# FIND PRODUCT PRICE COLUMN
# ==================================================

def get_price_column(products):

    if "Price" in products.columns:

        return "Price"

    if "UnitPrice" in products.columns:

        return "UnitPrice"

    raise ValueError(
        "products.csv must contain either "
        "'Price' or 'UnitPrice'."
    )


# ==================================================
# GENERATE RANDOM DATE
# ==================================================

def random_date(
    start_date,
    end_date
):

    dates = pd.date_range(
        start=start_date,
        end=end_date,
        freq="D"
    )

    return random.choice(
        dates
    ).strftime(
        "%Y-%m-%d"
    )


# ==================================================
# CHOOSE PRODUCTS FOR AN ORDER
# ==================================================

def choose_products_for_order(
    products,
    number_of_products
):

    # --------------------------------------------------
    # 70% chance:
    # choose products from the same category
    #
    # This creates realistic product relationships
    # for Frequently Bought Together.
    # --------------------------------------------------

    use_same_category = (
        random.random()
        < 0.70
    )

    if (
        use_same_category
        and
        "Category"
        in products.columns
    ):

        available_categories = (
            products[
                "Category"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        if available_categories:

            selected_category = (
                random.choice(
                    available_categories
                )
            )

            category_products = (
                products[
                    products[
                        "Category"
                    ]
                    == selected_category
                ]
            )

            if (
                len(category_products)
                >= number_of_products
            ):

                return (
                    category_products.sample(
                        n=number_of_products
                    )
                )

    # --------------------------------------------------
    # Otherwise choose random products
    # --------------------------------------------------

    number_of_products = min(
        number_of_products,
        len(products)
    )

    return products.sample(
        n=number_of_products
    )


# ==================================================
# GENERATE SALES
# ==================================================

def generate_sales():

    random.seed(
        RANDOM_SEED
    )

    products, customers = (
        load_source_data()
    )

    price_column = (
        get_price_column(
            products
        )
    )

    required_product_columns = {
        "ProductID"
    }

    required_customer_columns = {
        "CustomerID"
    }

    if not required_product_columns.issubset(
        products.columns
    ):

        raise ValueError(
            "products.csv must contain ProductID."
        )

    if not required_customer_columns.issubset(
        customers.columns
    ):

        raise ValueError(
            "customers.csv must contain CustomerID."
        )

    sales_rows = []

    sale_id = 1

    # ==================================================
    # CREATE ORDERS
    # ==================================================

    for order_number in range(
        NUMBER_OF_ORDERS
    ):

        order_id = (
            1001
            + order_number
        )

        customer_id = (
            random.choice(
                customers[
                    "CustomerID"
                ].tolist()
            )
        )

        sale_date = random_date(
            START_DATE,
            END_DATE
        )

        number_of_products = (
            random.randint(
                MIN_PRODUCTS_PER_ORDER,
                MAX_PRODUCTS_PER_ORDER
            )
        )

        order_products = (
            choose_products_for_order(
                products,
                number_of_products
            )
        )

        # ==================================================
        # CREATE ONE SALES ROW PER PRODUCT
        # ==================================================

        for _, product in (
            order_products.iterrows()
        ):

            product_id = (
                product[
                    "ProductID"
                ]
            )

            unit_price = float(
                product[
                    price_column
                ]
            )

            quantity = (
                random.randint(
                    MIN_QUANTITY,
                    MAX_QUANTITY
                )
            )

            total_sales = (
                quantity
                * unit_price
            )

            sales_rows.append(
                {
                    "SaleID":
                        sale_id,

                    "OrderID":
                        order_id,

                    "ProductID":
                        product_id,

                    "CustomerID":
                        customer_id,

                    "Quantity":
                        quantity,

                    "UnitPrice":
                        unit_price,

                    "SaleDate":
                        sale_date,

                    "TotalSales":
                        total_sales
                }
            )

            sale_id += 1

    # ==================================================
    # CREATE DATAFRAME
    # ==================================================

    sales = pd.DataFrame(
        sales_rows
    )

    # ==================================================
    # SORT DATA
    # ==================================================

    sales = sales.sort_values(
        [
            "OrderID",
            "SaleID"
        ]
    ).reset_index(
        drop=True
    )

    # ==================================================
    # SAVE CSV
    # ==================================================

    sales.to_csv(
        SALES_FILE,
        index=False
    )

    # ==================================================
    # SUMMARY
    # ==================================================

    print(
        "=" * 50
    )

    print(
        "SALES DATA GENERATED"
    )

    print(
        "=" * 50
    )

    print(
        "Orders:",
        sales[
            "OrderID"
        ].nunique()
    )

    print(
        "Sales rows:",
        len(
            sales
        )
    )

    print(
        "Customers:",
        sales[
            "CustomerID"
        ].nunique()
    )

    print(
        "Products:",
        sales[
            "ProductID"
        ].nunique()
    )

    average_products = (
        sales.groupby(
            "OrderID"
        )[
            "ProductID"
        ]
        .nunique()
        .mean()
    )

    print(
        "Average products per order:",
        round(
            average_products,
            2
        )
    )

    print(
        "\nSaved to:"
    )

    print(
        SALES_FILE
    )

    # ==================================================
    # EXAMPLE ORDERS
    # ==================================================

    print(
        "\nExample orders:"
    )

    print(
        sales[
            [
                "SaleID",
                "OrderID",
                "ProductID",
                "Quantity",
                "TotalSales"
            ]
        ].head(
            15
        )
    )

    return sales


# ==================================================
# RUN
# ==================================================

if __name__ == "__main__":

    generate_sales()