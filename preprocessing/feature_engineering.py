import pandas as pd


def create_features(df):

    data = df.copy()

    # ==================================================
    # SALES FEATURES
    # ==================================================

    required_sales_columns = {
        "Quantity",
        "UnitPrice"
    }

    if required_sales_columns.issubset(
        data.columns
    ):

        data["Quantity"] = (
            pd.to_numeric(
                data["Quantity"],
                errors="coerce"
            )
        )

        data["UnitPrice"] = (
            pd.to_numeric(
                data["UnitPrice"],
                errors="coerce"
            )
        )

        # Calculate revenue

        data["TotalSales"] = (
            data["Quantity"]
            * data["UnitPrice"]
        )

        # Remove duplicate revenue column

        data = data.drop(
            columns=[
                "TotalAmount"
            ],
            errors="ignore"
        )

    return data