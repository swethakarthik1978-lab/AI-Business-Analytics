
import pandas as pd


def analyze_sales(sales, products, customers):

    # ==================================================
    # COPY DATA
    # ==================================================

    sales = sales.copy()
    products = products.copy()
    customers = customers.copy()


    # ==================================================
    # TOTAL SALES
    # ==================================================

    total_sales = sales["TotalSales"].sum()

    print("\nTotal Sales:", round(total_sales, 2))


    # ==================================================
    # MONTHLY SALES
    # ==================================================

    # Convert SaleDate to datetime
    sales["SaleDate"] = pd.to_datetime(sales["SaleDate"])

    # Extract month
    sales["Month"] = sales["SaleDate"].dt.to_period("M")

    monthly_sales = (
        sales.groupby("Month")["TotalSales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Month"] = monthly_sales["Month"].astype(str)

    monthly_sales = monthly_sales.rename(
        columns={
            "TotalSales": "MonthlySales"
        }
    )


    # ==================================================
    # BEST-SELLING PRODUCTS
    # ==================================================

    best_selling_products = (
        sales.groupby("ProductID")["Quantity"]
        .sum()
        .reset_index()
    )

    best_selling_products = best_selling_products.rename(
        columns={
            "Quantity": "UnitsSold"
        }
    )

    best_selling_products = best_selling_products.sort_values(
        "UnitsSold",
        ascending=False
    )

    # Add product information
    best_selling_products = best_selling_products.merge(
        products[
            [
                "ProductID",
                "ProductName",
                "Category"
            ]
        ],
        on="ProductID",
        how="left"
    )


    # ==================================================
    # CUSTOMER SPENDING
    # ==================================================

    customer_spending = (
        sales.groupby("CustomerID")["TotalSales"]
        .sum()
        .reset_index()
    )

    customer_spending = customer_spending.rename(
        columns={
            "TotalSales": "TotalSpent"
        }
    )

    # Sort customers by spending
    customer_spending = customer_spending.sort_values(
        "TotalSpent",
        ascending=False
    )

    # Add customer information
    customer_spending = customer_spending.merge(
        customers[
            [
                "CustomerID",
                "CustomerName"
            ]
        ],
        on="CustomerID",
        how="left"
    )


    # ==================================================
    # PRODUCT WISE REVENUE
    # ==================================================

    product_revenue = (
        sales.groupby("ProductID")
        .agg(
            TotalQuantity=("Quantity", "sum"),
            TotalRevenue=("TotalSales", "sum")
        )
        .reset_index()
    )

    # Add product information
    product_revenue = product_revenue.merge(
        products[
            [
                "ProductID",
                "ProductName",
                "Category"
            ]
        ],
        on="ProductID",
        how="left"
    )

    # Sort products by revenue
    product_revenue = product_revenue.sort_values(
        "TotalRevenue",
        ascending=False
    )


    # ==================================================
    # CATEGORY WISE SALES
    # ==================================================

    category_sales = (
        product_revenue.groupby("Category")["TotalRevenue"]
        .sum()
        .reset_index()
    )

    category_sales = category_sales.rename(
        columns={
            "TotalRevenue": "CategorySales"
        }
    )

    # Sort categories by sales
    category_sales = category_sales.sort_values(
        "CategorySales",
        ascending=False
    )


    # ==================================================
    # RETURN RESULTS
    # ==================================================

    return {
        "total_sales": total_sales,
        "monthly_sales": monthly_sales,
        "best_selling_products": best_selling_products,
        "customer_spending": customer_spending,
        "product_revenue": product_revenue,
        "category_sales": category_sales
    }