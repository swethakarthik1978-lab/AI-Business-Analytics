import pandas as pd


def analyze_customers(customers, sales):

    # Copy data
    customers = customers.copy()
    sales = sales.copy()

    # Make sure dates are datetime
    sales["SaleDate"] = pd.to_datetime(
        sales["SaleDate"]
    )

    # Group sales by customer
    customer_summary = (
        sales.groupby("CustomerID")
        .agg(
            TotalOrders=("SaleDate", "count"),
            TotalQuantity=("Quantity", "sum"),
            TotalSpent=("TotalAmount", "sum"),
            AverageOrderValue=("TotalAmount", "mean"),
            FirstPurchase=("SaleDate", "min"),
            LastPurchase=("SaleDate", "max")
        )
        .reset_index()
    )

    # Merge with customer information
    customer_analysis = customers.merge(
        customer_summary,
        on="CustomerID",
        how="left"
    )

    # Customers with no purchases
    customer_analysis["TotalOrders"] = (
        customer_analysis["TotalOrders"]
        .fillna(0)
    )

    customer_analysis["TotalQuantity"] = (
        customer_analysis["TotalQuantity"]
        .fillna(0)
    )

    customer_analysis["TotalSpent"] = (
        customer_analysis["TotalSpent"]
        .fillna(0)
    )

    customer_analysis["AverageOrderValue"] = (
        customer_analysis["AverageOrderValue"]
        .fillna(0)
    )

    return customer_analysis