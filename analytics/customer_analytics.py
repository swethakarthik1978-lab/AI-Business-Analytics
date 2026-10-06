import pandas as pd


def analyze_customers(
    customers,
    sales
):

    customers = customers.copy()
    sales = sales.copy()

    # Convert date

    sales["SaleDate"] = (
        pd.to_datetime(
            sales["SaleDate"],
            errors="coerce"
        )
    )

    # ==================================================
    # CUSTOMER SUMMARY
    # ==================================================

    customer_summary = (
        sales
        .groupby(
            "CustomerID",
            as_index=False
        )
        .agg(
            TotalOrders=(
                "OrderID",
                "nunique"
            ),
            TotalQuantity=(
                "Quantity",
                "sum"
            ),
            TotalSpent=(
                "TotalSales",
                "sum"
            ),
            FirstPurchase=(
                "SaleDate",
                "min"
            ),
            LastPurchase=(
                "SaleDate",
                "max"
            )
        )
    )

    # ==================================================
    # MERGE CUSTOMER INFORMATION
    # ==================================================

    result = customers.merge(
        customer_summary,
        on="CustomerID",
        how="left"
    )

    # Fill missing numerical values

    columns_to_fill = [
        "TotalOrders",
        "TotalQuantity",
        "TotalSpent"
    ]

    result[
        columns_to_fill
    ] = result[
        columns_to_fill
    ].fillna(0)

    result[
        "TotalOrders"
    ] = result[
        "TotalOrders"
    ].astype(int)

    # ==================================================
    # AVERAGE ORDER VALUE
    # ==================================================

    result[
        "AverageOrderValue"
    ] = (
        result[
            "TotalSpent"
        ]
        .div(
            result[
                "TotalOrders"
            ].replace(
                0,
                pd.NA
            )
        )
        .fillna(0)
    )

    return result