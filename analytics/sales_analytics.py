import pandas as pd


def analyze_sales(
    sales,
    products,
    customers
):

    sales = sales.copy()
    products = products.copy()
    customers = customers.copy()

    # ==================================================
    # DATE
    # ==================================================

    sales["SaleDate"] = (
        pd.to_datetime(
            sales["SaleDate"],
            errors="coerce"
        )
    )

    # ==================================================
    # TOTAL SALES
    # ==================================================

    total_sales = (
        sales[
            "TotalSales"
        ].sum()
    )

    # ==================================================
    # MONTHLY SALES
    # ==================================================

    monthly_data = (
        sales
        .dropna(
            subset=["SaleDate"]
        )
        .copy()
    )

    monthly_data[
        "Month"
    ] = (
        monthly_data[
            "SaleDate"
        ]
        .dt
        .to_period("M")
        .astype(str)
    )

    monthly_sales = (
        monthly_data
        .groupby(
            "Month",
            as_index=False
        )["TotalSales"]
        .sum()
        .rename(
            columns={
                "TotalSales":
                    "MonthlySales"
            }
        )
        .sort_values(
            "Month"
        )
    )

    # ==================================================
    # PRODUCT INFORMATION
    # ==================================================

    product_details = (
        products[
            [
                "ProductID",
                "ProductName",
                "Category"
            ]
        ]
        .drop_duplicates(
            subset=[
                "ProductID"
            ]
        )
    )

    # ==================================================
    # BEST SELLING PRODUCTS
    # ==================================================

    best_selling_products = (
        sales
        .groupby(
            "ProductID",
            as_index=False
        )["Quantity"]
        .sum()
        .rename(
            columns={
                "Quantity":
                    "UnitsSold"
            }
        )
        .merge(
            product_details,
            on="ProductID",
            how="left"
        )
        .sort_values(
            "UnitsSold",
            ascending=False
        )
    )

    # ==================================================
    # CUSTOMER SPENDING
    # ==================================================

    customer_details = (
        customers[
            [
                "CustomerID",
                "CustomerName"
            ]
        ]
        .drop_duplicates(
            subset=[
                "CustomerID"
            ]
        )
    )

    customer_spending = (
        sales
        .groupby(
            "CustomerID",
            as_index=False
        )["TotalSales"]
        .sum()
        .rename(
            columns={
                "TotalSales":
                    "TotalSpent"
            }
        )
        .merge(
            customer_details,
            on="CustomerID",
            how="left"
        )
        .sort_values(
            "TotalSpent",
            ascending=False
        )
    )

    # ==================================================
    # PRODUCT REVENUE
    # ==================================================

    product_revenue = (
        sales
        .groupby(
            "ProductID",
            as_index=False
        )
        .agg(
            ProductRevenue=(
                "TotalSales",
                "sum"
            ),
            QuantitySold=(
                "Quantity",
                "sum"
            )
        )
        .merge(
            product_details,
            on="ProductID",
            how="left"
        )
        .sort_values(
            "ProductRevenue",
            ascending=False
        )
    )

    # ==================================================
    # CATEGORY SALES
    # ==================================================

    category_sales = (
        product_revenue
        .groupby(
            "Category",
            as_index=False
        )
        .agg(
            TotalSales=(
                "ProductRevenue",
                "sum"
            ),
            QuantitySold=(
                "QuantitySold",
                "sum"
            )
        )
        .sort_values(
            "TotalSales",
            ascending=False
        )
    )

    # ==================================================
    # RETURN RESULTS
    # ==================================================

    return {

        "total_sales":
            total_sales,

        "monthly_sales":
            monthly_sales,

        "best_selling_products":
            best_selling_products,

        "customer_spending":
            customer_spending,

        "product_revenue":
            product_revenue,

        "category_sales":
            category_sales
    }