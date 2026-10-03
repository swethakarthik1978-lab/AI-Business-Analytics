# ==================================================
# IMPORTS
# ==================================================

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

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


# ==================================================
# PROJECT PATHS
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"


# ==================================================
# MAIN ANALYTICS PROGRAM
# ==================================================

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

        # Save processed data back into CSV files
        feature_df.to_csv(
            DATA_DIR / f"{name}.csv",
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

    customer_analysis.to_csv(
        DATA_DIR / "customer_analysis.csv",
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

    inventory_analysis.to_csv(
        DATA_DIR / "inventory_analysis.csv",
        index=False
    )

    print("Inventory analytics saved successfully!")

    # ==================================================
    # FINANCIAL ANALYTICS
    # ==================================================

    print("\n" + "=" * 50)
    print("FINANCIAL ANALYTICS")
    print("=" * 50)

    finance = clean_datasets["finance"]
    sales = clean_datasets["sales"]

    financial_analysis = analyze_financial(
        finance,
        sales
    )

    print("\nFinancial Summary:")

    print(
        financial_analysis["financial_summary"]
    )

    financial_analysis["financial_summary"].to_csv(
        DATA_DIR / "financial_summary.csv",
        index=False
    )

    print("Financial analytics saved successfully!")

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

    # ==================================================
    # TOTAL SALES
    # ==================================================

    print("\nTotal Sales:")

    print(
        round(
            sales_analysis["total_sales"],
            2
        )
    )

    # ==================================================
    # MONTHLY SALES
    # ==================================================

    print("\nMonthly Sales:")

    print(
        sales_analysis["monthly_sales"]
    )

    sales_analysis["monthly_sales"].to_csv(
        DATA_DIR / "monthly_sales.csv",
        index=False
    )

    # ==================================================
    # BEST SELLING PRODUCTS
    # ==================================================

    print("\nBest Selling Products:")

    print(
        sales_analysis[
            "best_selling_products"
        ].head(10)
    )

    sales_analysis[
        "best_selling_products"
    ].to_csv(
        DATA_DIR / "best_selling_products.csv",
        index=False
    )

    # ==================================================
    # CUSTOMER SPENDING
    # ==================================================

    print("\nTop Customers by Spending:")

    customer_spending = sales_analysis[
        "customer_spending"
    ]

    print(
        customer_spending.head(10)
    )

    customer_spending.to_csv(
        DATA_DIR / "customer_spending.csv",
        index=False
    )

    print("Customer spending saved successfully!")

    # ==================================================
    # PRODUCT REVENUE
    # ==================================================

    print("\nProduct Wise Revenue:")

    product_revenue = sales_analysis[
        "product_revenue"
    ]

    print(
        product_revenue.head(10)
    )

    product_revenue.to_csv(
        DATA_DIR / "product_revenue.csv",
        index=False
    )

    print("Product revenue saved successfully!")

    # ==================================================
    # CATEGORY SALES
    # ==================================================

    print("\nCategory Wise Sales:")

    category_sales = sales_analysis[
        "category_sales"
    ]

    print(category_sales)

    category_sales.to_csv(
        DATA_DIR / "category_sales.csv",
        index=False
    )

    print("Category sales saved successfully!")

    print("Sales analytics saved successfully!")

    # ==================================================
    # BUSINESS SUMMARY
    # ==================================================

    print("\n" + "=" * 50)
    print("BUSINESS SUMMARY")
    print("=" * 50)

    total_sales = sales["TotalSales"].sum()

    average_sale = sales["TotalSales"].mean()

    units_sold = sales["Quantity"].sum()

    total_orders = sales["OrderID"].nunique()

    total_customers = sales["CustomerID"].nunique()

    print(
        "Total Sales: $",
        round(total_sales, 2)
    )

    print(
        "Average Sale: $",
        round(average_sale, 2)
    )

    print(
        "Units Sold:",
        int(units_sold)
    )

    print(
        "Total Orders:",
        total_orders
    )

    print(
        "Customers:",
        total_customers
    )

    # ==================================================
    # DATABASE
    # ==================================================

    print("\n" + "=" * 50)
    print("DATABASE")
    print("=" * 50)

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "All tables created successfully!"
    )

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

    print(
        "Database updated successfully!"
    )

    # ==================================================
    # SALES FORECASTING
    # ==================================================

    print("\n" + "=" * 50)
    print("SALES FORECASTING")
    print("=" * 50)

    daily_sales = prepare_sales_data(
        sales
    )

    print("\nDaily sales data:")

    print(
        daily_sales.head()
    )

    # Train forecasting model

    model = train_sales_model(
        daily_sales
    )

    print(
        "\nSales forecasting model "
        "trained successfully!"
    )

    # Predict next seven days

    forecast = predict_sales(
        model,
        days=7
    )

    print(
        "\nNEXT 7 DAYS SALES FORECAST"
    )

    print(
        forecast.tail(7).to_string(
            index=False
        )
    )

    # Save forecast

    save_forecast(
        forecast,
        DATA_DIR / "sales_forecast.csv"
    )

    print(
        "\nSales forecast saved successfully!"
    )

    # Create forecasting graph

    print(
        "\nCreating Actual vs "
        "Predicted Sales graph..."
    )

    plot_actual_vs_predicted(
        daily_sales,
        forecast
    )

    print(
        "Sales visualization completed!"
    )


# ==================================================
# STREAMLIT DASHBOARD
# ==================================================

def run_dashboard():

    # ==================================================
    # PAGE CONFIGURATION
    # ==================================================

    st.set_page_config(
        page_title="AI Business Analytics Dashboard",
        page_icon="📊",
        layout="wide"
    )

    # ==================================================
    # LOAD DASHBOARD DATA
    # ==================================================

    @st.cache_data
    def load_dashboard_data():

        sales = pd.read_csv(
            DATA_DIR / "sales.csv"
        )

        products = pd.read_csv(
            DATA_DIR / "products.csv"
        )

        customers = pd.read_csv(
            DATA_DIR / "customers.csv"
        )

        inventory = pd.read_csv(
            DATA_DIR / "inventory.csv"
        )

        finance = pd.read_csv(
            DATA_DIR / "finance.csv"
        )

        return (
            sales,
            products,
            customers,
            inventory,
            finance
        )

    try:

        (
            sales,
            products,
            customers,
            inventory,
            finance
        ) = load_dashboard_data()

    except FileNotFoundError:

        st.error(
            "Required CSV files were not found. "
            "Run 'python main.py' first."
        )

        st.stop()

    # ==================================================
    # REVENUE COLUMN
    # ==================================================

    # TotalSales is the preferred column.
    # TotalAmount is only used as a fallback.

    if "TotalSales" in sales.columns:

        revenue_column = "TotalSales"

    elif "TotalAmount" in sales.columns:

        revenue_column = "TotalAmount"

    else:

        st.error(
            "Sales data must contain TotalSales."
        )

        st.stop()

    # ==================================================
    # PAGE HEADER
    # ==================================================

    st.title(
        "📊 AI Business Analytics Dashboard"
    )

    st.write(
        "Sales, Customer, Product, "
        "Inventory and Financial Analytics"
    )

    st.divider()

    # ==================================================
    # SIDEBAR
    # ==================================================

    st.sidebar.title(
        "🎛 Dashboard Controls"
    )

    st.sidebar.subheader(
        "Filters"
    )

    # ==================================================
    # CATEGORY FILTER
    # ==================================================

    categories = (
        ["All"]
        + sorted(
            products[
                "Category"
            ]
            .dropna()
            .unique()
            .tolist()
        )
    )

    selected_category = (
        st.sidebar.selectbox(
            "Select Category",
            categories
        )
    )

    # ==================================================
    # APPLY CATEGORY FILTER
    # ==================================================

    if selected_category != "All":

        filtered_products = (
            products[
                products["Category"]
                == selected_category
            ].copy()
        )

        filtered_sales = (
            sales[
                sales["ProductID"].isin(
                    filtered_products[
                        "ProductID"
                    ]
                )
            ].copy()
        )

    else:

        filtered_products = (
            products.copy()
        )

        filtered_sales = (
            sales.copy()
        )

    # ==================================================
    # SIDEBAR SECTIONS
    # ==================================================

    st.sidebar.divider()

    st.sidebar.subheader(
        "Dashboard Sections"
    )

    st.sidebar.write(
        "📌 Business Overview"
    )

    st.sidebar.write(
        "📈 Sales Performance"
    )

    st.sidebar.write(
        "📦 Product Performance"
    )

    st.sidebar.write(
        "🔮 Sales Forecast"
    )

    st.sidebar.write(
        "📋 Detailed Data"
    )

    # ==================================================
    # REFRESH BUTTON
    # ==================================================

    st.sidebar.divider()

    if st.sidebar.button(
        "🔄 Refresh Dashboard"
    ):

        st.cache_data.clear()

        st.rerun()

    # ==================================================
    # KPI CALCULATIONS
    # ==================================================

    total_revenue = (
        filtered_sales[
            revenue_column
        ].sum()
    )

    total_orders = (
        filtered_sales[
            "OrderID"
        ].nunique()
    )

    total_customers = (
        filtered_sales[
            "CustomerID"
        ].nunique()
    )

    total_quantity = (
        filtered_sales[
            "Quantity"
        ].sum()
    )

    # ==================================================
    # BUSINESS OVERVIEW
    # ==================================================

    st.subheader(
        "📌 Business Overview"
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        st.metric(
            "💰 Total Revenue",
            f"${total_revenue:,.0f}"
        )

    with col2:

        st.metric(
            "🛒 Total Orders",
            f"{total_orders:,}"
        )

    with col3:

        st.metric(
            "👥 Customers",
            f"{total_customers:,}"
        )

    with col4:

        st.metric(
            "📦 Items Sold",
            f"{total_quantity:,.0f}"
        )

    st.divider()

    # ==================================================
    # SALES PERFORMANCE
    # ==================================================

    st.subheader(
        "📈 Sales Performance"
    )

    # Convert sales date to datetime

    filtered_sales[
        "SaleDate"
    ] = pd.to_datetime(
        filtered_sales[
            "SaleDate"
        ],
        errors="coerce"
    )

    # ==================================================
    # MONTHLY SALES
    # ==================================================

    monthly_data = (
        filtered_sales
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
        )[revenue_column]
        .sum()
    )

    # ==================================================
    # MONTHLY LINE CHART
    # ==================================================

    fig_monthly = px.line(
        monthly_sales,
        x="Month",
        y=revenue_column,
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig_monthly.update_layout(
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),
        xaxis_title="Month",
        yaxis_title="Revenue"
    )

    # ==================================================
    # CATEGORY SALES
    # ==================================================

    category_sales = (
        filtered_sales
        .merge(
            products[
                [
                    "ProductID",
                    "Category"
                ]
            ],
            on="ProductID",
            how="left"
        )
        .groupby(
            "Category",
            as_index=False
        )[revenue_column]
        .sum()
    )

    # ==================================================
    # CATEGORY PIE CHART
    # ==================================================

    fig_category = px.pie(
        category_sales,
        names="Category",
        values=revenue_column,
        title=(
            "Revenue Distribution "
            "by Category"
        )
    )

    fig_category.update_layout(
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    # ==================================================
    # DISPLAY SALES CHARTS SIDE BY SIDE
    # ==================================================

    chart_col1, chart_col2 = (
        st.columns(2)
    )

    with chart_col1:

        st.plotly_chart(
            fig_monthly,
            use_container_width=True
        )

    with chart_col2:

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    st.divider()

    # ==================================================
    # PRODUCT PERFORMANCE
    # ==================================================

    st.subheader(
        "📦 Product Performance"
    )

    product_sales = (
        filtered_sales
        .merge(
            products[
                [
                    "ProductID",
                    "ProductName"
                ]
            ],
            on="ProductID",
            how="left"
        )
        .groupby(
            "ProductName",
            as_index=False
        )[revenue_column]
        .sum()
        .sort_values(
            revenue_column,
            ascending=False
        )
    )

    # Show top 15 products so chart
    # remains readable.

    top_products = (
        product_sales.head(15)
    )

    fig_products = px.bar(
        top_products,
        x="ProductName",
        y=revenue_column,
        title="Revenue by Product"
    )

    fig_products.update_layout(
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),
        xaxis_title="Product",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # SALES FORECAST
    # ==================================================

    st.subheader(
        "🔮 Sales Forecast"
    )

    forecast_file = (
        DATA_DIR
        / "sales_forecast.csv"
    )

    if forecast_file.exists():

        forecast = pd.read_csv(
            forecast_file
        )

        forecast[
            "ds"
        ] = pd.to_datetime(
            forecast["ds"],
            errors="coerce"
        )

        # Use complete sales data to determine
        # the latest historical sales date.

        all_sales_dates = (
            pd.to_datetime(
                sales["SaleDate"],
                errors="coerce"
            )
        )

        last_sales_date = (
            all_sales_dates.max()
        )

        # Get future predictions only.

        future_forecast = (
            forecast[
                forecast["ds"]
                > last_sales_date
            ]
            .sort_values("ds")
            .head(7)
        )

        if not future_forecast.empty:

            fig_forecast = px.line(
                future_forecast,
                x="ds",
                y="yhat",
                markers=True,
                title=(
                    "Next 7 Days "
                    "Sales Forecast"
                )
            )

            fig_forecast.update_layout(
                template="plotly_white",
                margin=dict(
                    l=20,
                    r=20,
                    t=50,
                    b=20
                ),
                xaxis_title="Date",
                yaxis_title=(
                    "Predicted Revenue"
                )
            )

            st.plotly_chart(
                fig_forecast,
                use_container_width=True
            )

            st.write(
                "Forecasted Sales:"
            )

            forecast_display = (
                future_forecast[
                    [
                        "ds",
                        "yhat",
                        "yhat_lower",
                        "yhat_upper"
                    ]
                ]
                .copy()
            )

            forecast_display = (
                forecast_display.rename(
                    columns={
                        "ds": "Date",
                        "yhat":
                            "Predicted Sales",
                        "yhat_lower":
                            "Lower Estimate",
                        "yhat_upper":
                            "Upper Estimate"
                    }
                )
            )

            st.dataframe(
                forecast_display,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No future forecast "
                "records were found."
            )

    else:

        st.info(
            "Run python main.py first "
            "to generate the sales forecast."
        )

    st.caption(
        "The sales forecast represents the "
        "overall business and is not changed "
        "by the category filter."
    )

    st.divider()

    # ==================================================
    # FINANCIAL OVERVIEW
    # ==================================================

    st.subheader(
        "💵 Financial Overview"
    )

    if (
        "Revenue" in finance.columns
        and "Expenses" in finance.columns
    ):

        finance_revenue = (
            finance[
                "Revenue"
            ].sum()
        )

        finance_expenses = (
            finance[
                "Expenses"
            ].sum()
        )

        if "Profit" in finance.columns:

            finance_profit = (
                finance[
                    "Profit"
                ].sum()
            )

        else:

            finance_profit = (
                finance_revenue
                - finance_expenses
            )

        fin1, fin2, fin3 = (
            st.columns(3)
        )

        fin1.metric(
            "Revenue",
            f"${finance_revenue:,.0f}"
        )

        fin2.metric(
            "Expenses",
            f"${finance_expenses:,.0f}"
        )

        fin3.metric(
            "Profit",
            f"${finance_profit:,.0f}"
        )

    st.divider()

    # ==================================================
    # DETAILED SALES DATA
    # ==================================================

    st.subheader(
        "📋 Detailed Sales Data"
    )

    st.write(
        f"Showing "
        f"{len(filtered_sales):,} "
        f"sales records."
    )

    st.dataframe(
        filtered_sales,
        use_container_width=True,
        hide_index=True
    )

    # ==================================================
    # DOWNLOAD DATA
    # ==================================================

    st.subheader(
        "⬇ Download Report"
    )

    csv_data = (
        filtered_sales.to_csv(
            index=False
        )
    )

    st.download_button(
        label=(
            "📥 Download Sales Data"
        ),
        data=csv_data,
        file_name="sales_report.csv",
        mime="text/csv"
    )

    # ==================================================
    # FOOTER
    # ==================================================

    st.divider()

    st.caption(
        "AI Business Analytics Platform • "
        "Sales & Business Intelligence Dashboard"
    )


# ==================================================
# DETECT HOW MAIN.PY IS BEING RUN
# ==================================================

def running_in_streamlit():

    try:

        from streamlit.runtime.scriptrunner import (
            get_script_run_ctx
        )

        return (
            get_script_run_ctx(
                suppress_warning=True
            )
            is not None
        )

    except Exception:

        return False


# ==================================================
# RUN PROGRAM
# ==================================================

if running_in_streamlit():

    run_dashboard()

elif __name__ == "__main__":

    main()
