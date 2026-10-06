import pandas as pd


def create_business_context(
    sales,
    products,
    customers,
    inventory,
    finance
):

    total_revenue = sales["TotalSales"].sum()

    total_orders = sales["OrderID"].nunique()

    total_customers = sales["CustomerID"].nunique()

    total_quantity = sales["Quantity"].sum()

    average_sale = sales["TotalSales"].mean()

    # Product revenue
    product_revenue = (
        sales
        .merge(
            products[["ProductID", "ProductName"]],
            on="ProductID",
            how="left"
        )
        .groupby("ProductName")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    # Category revenue
    category_revenue = (
        sales
        .merge(
            products[["ProductID", "Category"]],
            on="ProductID",
            how="left"
        )
        .groupby("Category")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    # Financial information
    total_expenses = finance["Expenses"].sum()

    if "Profit" in finance.columns:
        total_profit = finance["Profit"].sum()
    else:
        total_profit = total_revenue - total_expenses

    context = f"""
BUSINESS INFORMATION

Total Revenue:
{total_revenue:.2f}

Total Orders:
{total_orders}

Total Customers:
{total_customers}

Total Quantity Sold:
{total_quantity}

Average Sale:
{average_sale:.2f}

Total Expenses:
{total_expenses:.2f}

Total Profit:
{total_profit:.2f}


TOP PRODUCTS

{product_revenue.head(10).to_string()}


CATEGORY REVENUE

{category_revenue.to_string()}
"""

    return context