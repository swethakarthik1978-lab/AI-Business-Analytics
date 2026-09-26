
from config import PROJECT_NAME, VERSION

from database.database import engine, Base, SessionLocal
from database.models import Product, Customer, Order, Inventory, Finance
from database.crud import *

from data_collection import load_data

from preprocessing.clean_data import clean_dataframe
from preprocessing.feature_engineering import create_features

from analytics.customer_analytics import analyze_customers
from analytics.inventory_analytics import analyze_inventory
from analytics.sales_analytics import analyze_sales
from analytics.financial_analytics import analyze_financial

from ML.sales_forecasting import (
    prepare_sales_data,
    train_sales_model,
    predict_sales,
    save_forecast,
    plot_actual_vs_predicted
)


def main():

    # ==================================================
    # PROJECT INFORMATION
    # ==================================================

    print("=" * 50)
    print(PROJECT_NAME)
    print("Version", VERSION)
    print("=" * 50)

    print("Welcome to the AI Business Analytics Platform")


    # ==================================================
    # LOAD DATA
    # ==================================================

    print("\nLOADING DATA")

    datasets = load_data()

    for name, df in datasets.items():
        print(name, df.shape)


    # ==================================================
    # CLEAN DATA
    # ==================================================

    print("\nCLEANING DATA")

    clean_datasets = {}

    for name, df in datasets.items():

        print("CLEANING", name)

        clean_datasets[name] = clean_dataframe(df)


    # ==================================================
    # FEATURE ENGINEERING
    # ==================================================

    print("\nFEATURE ENGINEERING")

    for name, df in clean_datasets.items():

        feature_df = create_features(df)

        clean_datasets[name] = feature_df

        # Save feature-engineered data back to CSV
        feature_df.to_csv(
            f"data/{name}.csv",
            index=False
        )

        print(name, "updated successfully")


    # ==================================================
    # CUSTOMER ANALYTICS
    # ==================================================

    print("\n" + "=" * 50)
    print("CUSTOMER ANALYTICS")
    print("=" * 50)

    customer_analysis = analyze_customers(
        clean_datasets["customers"],
        clean_datasets["sales"]
    )

    print(customer_analysis.head())

    # Save customer analytics
    customer_analysis.to_csv(
        "data/customer_analysis.csv",
        index=False
    )

    print("Customer analytics saved successfully!")


    # ==================================================
    # INVENTORY ANALYTICS
    # ==================================================

    print("\n" + "=" * 50)
    print("INVENTORY ANALYTICS")
    print("=" * 50)

    inventory = clean_datasets["inventory"]
    products = clean_datasets["products"]

    inventory_analysis = analyze_inventory(
        inventory,
        products
    )

    print(inventory_analysis.head())

    # Save inventory analytics
    inventory_analysis.to_csv(
        "data/inventory_analysis.csv",
        index=False
    )

    print("Inventory analytics saved successfully!")


    # ==================================================
    # FINANCIAL ANALYTICS
    # ==================================================

    print("\n" + "=" * 50)
    print("FINANCIAL ANALYTICS")
    print("=" * 50)

    # Retrieve cleaned financial and sales datasets
    finance = clean_datasets["finance"]
    sales = clean_datasets["sales"]

    # Perform financial analysis
    financial_analysis = analyze_financial(
        finance,
        sales
    )

    # Display financial summary
    print("\nFinancial Summary:")

    print(
        financial_analysis["financial_summary"]
    )

    # Save financial summary to CSV
    financial_analysis["financial_summary"].to_csv(
        "data/financial_summary.csv",
        index=False
    )

    print("\nFinancial analytics saved successfully!")


    # ==================================================
    # SALES ANALYTICS
    # ==================================================

    print("\n" + "=" * 50)
    print("SALES ANALYTICS")
    print("=" * 50)

    sales_analysis = analyze_sales(
        clean_datasets["sales"],
        clean_datasets["products"],
        clean_datasets["customers"]
    )

    print("\nTotal Sales:")
    print(round(sales_analysis["total_sales"], 2))

    print("\nMonthly Sales:")
    print(sales_analysis["monthly_sales"])

    sales_analysis["monthly_sales"].to_csv(
        "data/monthly_sales.csv",
        index=False
    )

    print("\nBest Selling Products:")

    print(
        sales_analysis["best_selling_products"].head(10)
    )

    sales_analysis["best_selling_products"].to_csv(
        "data/best_selling_products.csv",
        index=False
    )

    print("Sales analytics saved successfully!")


    # ==================================================
    # CUSTOMER SPENDING
    # ==================================================

    print("\n" + "=" * 50)
    print("CUSTOMER SPENDING")
    print("=" * 50)

    sales = clean_datasets["sales"]
    customers = clean_datasets["customers"]
    products = clean_datasets["products"]

    # Calculate total spending for each customer
    customer_spending = (
        sales.groupby(
            "CustomerID",
            as_index=False
        )["TotalSales"]
        .sum()
    )

    # Add customer names
    customer_spending = customer_spending.merge(
        customers[["CustomerID", "CustomerName"]],
        on="CustomerID",
        how="left"
    )

    # Rename total spending column
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

    print("\nTop 10 Customers by Spending:")
    print(customer_spending.head(10))

    # Save customer spending
    customer_spending.to_csv(
        "data/customer_spending.csv",
        index=False
    )

    print("Customer spending saved successfully!")


    # ==================================================
    # PRODUCT WISE REVENUE
    # ==================================================

    print("\n" + "=" * 50)
    print("PRODUCT WISE REVENUE")
    print("=" * 50)

    # Calculate revenue and quantity for each product
    product_revenue = (
        sales.groupby(
            "ProductID",
            as_index=False
        )
        .agg(
            ProductRevenue=("TotalSales", "sum"),
            QuantitySold=("Quantity", "sum")
        )
    )

    # Add product names and categories
    product_revenue = product_revenue.merge(
        products[["ProductID", "ProductName", "Category"]],
        on="ProductID",
        how="left"
    )

    # Sort products by revenue
    product_revenue = product_revenue.sort_values(
        "ProductRevenue",
        ascending=False
    )

    print("\nTop 10 Products by Revenue:")
    print(product_revenue.head(10))

    # Save product revenue
    product_revenue.to_csv(
        "data/product_revenue.csv",
        index=False
    )

    print("Product revenue saved successfully!")


    # ==================================================
    # CATEGORY WISE SALES
    # ==================================================

    print("\n" + "=" * 50)
    print("CATEGORY WISE SALES")
    print("=" * 50)

    # Calculate sales and quantity for each category
    category_sales = (
        product_revenue.groupby(
            "Category",
            as_index=False
        )
        .agg(
            TotalSales=("ProductRevenue", "sum"),
            QuantitySold=("QuantitySold", "sum")
        )
    )

    # Sort categories by total sales
    category_sales = category_sales.sort_values(
        "TotalSales",
        ascending=False
    )

    print("\nSales by Category:")
    print(category_sales)

    # Save category sales
    category_sales.to_csv(
        "data/category_sales.csv",
        index=False
    )

    print("Category sales saved successfully!")


    # ==================================================
    # BUSINESS SUMMARY
    # ==================================================

    print("\n" + "=" * 50)
    print("BUSINESS SUMMARY")
    print("=" * 50)

    total_sales = sales["TotalSales"].sum()
    average_sale = sales["TotalSales"].mean()
    units_sold = sales["Quantity"].sum()

    print("Total Sales: $", round(total_sales, 2))
    print("Average Sale: $", round(average_sale, 2))
    print("Units Sold:", int(units_sold))


    # ==================================================
    # DATABASE
    # ==================================================

    print("\n" + "=" * 50)
    print("DATABASE")
    print("=" * 50)

    Base.metadata.create_all(bind=engine)

    print("All tables created successfully!")

    db = SessionLocal()

    try:

        add_customers(
            db,
            clean_datasets["customers"]
        )

        add_products(
            db,
            clean_datasets["products"]
        )

        add_inventory(
            db,
            clean_datasets["inventory"]
        )

        add_finance(
            db,
            clean_datasets["finance"]
        )

        add_orders(
            db,
            clean_datasets["sales"]
        )

    finally:
        db.close()

    print("Database updated successfully!")


    # ==================================================
    # SALES FORECASTING
    # ==================================================

    print("\n" + "=" * 50)
    print("SALES FORECASTING")
    print("=" * 50)

    daily_sales = prepare_sales_data(sales)

    print("\nDaily sales data:")
    print(daily_sales.head())

    # Train forecasting model
    model = train_sales_model(
        daily_sales
    )

    print(
        "\nSales forecasting model trained successfully!"
    )

    # Predict next 7 days
    forecast = predict_sales(
        model,
        days=7
    )

    print("\nNEXT 7 DAYS SALES FORECAST")

    print(
        forecast.tail(7).to_string(
            index=False
        )
    )

    # Save forecast
    save_forecast(
        forecast,
        "data/sales_forecast.csv"
    )

    print(
        "\nSales forecast saved successfully!"
    )

    # Create graph
    print(
        "\nCreating Actual vs Predicted Sales graph..."
    )

    plot_actual_vs_predicted(
        daily_sales,
        forecast
    )

    print("Sales visualization completed!")


if __name__ == "__main__":
    main()
