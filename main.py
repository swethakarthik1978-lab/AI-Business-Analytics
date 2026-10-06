# ==================================================
# IMPORTS
# ==================================================

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from config import PROJECT_NAME, VERSION

from database.database import engine, Base, SessionLocal
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

from chatbot.chatbot import ask_business_chatbot


# ==================================================
# PROJECT PATHS
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"


# ==================================================
# MAIN BACKEND PROGRAM
# ==================================================

def main():

    # ==================================================
    # PROJECT INFORMATION
    # ==================================================

    print("=" * 50)
    print(PROJECT_NAME)
    print("Version", VERSION)
    print("=" * 50)

    print(
        "Welcome to the AI Business Analytics Platform"
    )

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

        feature_df.to_csv(
            DATA_DIR / f"{name}.csv",
            index=False
        )

        print(
            name,
            "updated successfully"
        )

    # ==================================================
    # COMMON DATASETS
    # ==================================================

    sales = clean_datasets["sales"]
    customers = clean_datasets["customers"]
    products = clean_datasets["products"]
    inventory = clean_datasets["inventory"]
    finance = clean_datasets["finance"]

    # ==================================================
    # CUSTOMER ANALYTICS
    # ==================================================

    print("\n" + "=" * 50)
    print("CUSTOMER ANALYTICS")
    print("=" * 50)

    customer_analysis = analyze_customers(
        customers,
        sales
    )

    print(
        customer_analysis.head()
    )

    customer_analysis.to_csv(
        DATA_DIR / "customer_analysis.csv",
        index=False
    )

    print(
        "Customer analytics saved successfully!"
    )

    # ==================================================
    # INVENTORY ANALYTICS
    # ==================================================

    print("\n" + "=" * 50)
    print("INVENTORY ANALYTICS")
    print("=" * 50)

    inventory_analysis = analyze_inventory(
        inventory,
        products
    )

    print(
        inventory_analysis.head()
    )

    inventory_analysis.to_csv(
        DATA_DIR / "inventory_analysis.csv",
        index=False
    )

    print(
        "Inventory analytics saved successfully!"
    )

    # ==================================================
    # LEGACY TOTALAMOUNT COMPATIBILITY
    # ==================================================

    # TotalSales is the main revenue column.
    # Some older files may still expect TotalAmount.
    # This creates a temporary copy only.

    legacy_sales = sales.copy()

    if (
        "TotalAmount" not in legacy_sales.columns
        and "TotalSales" in legacy_sales.columns
    ):

        legacy_sales["TotalAmount"] = (
            legacy_sales["TotalSales"]
        )

    # ==================================================
    # FINANCIAL ANALYTICS
    # ==================================================

    print("\n" + "=" * 50)
    print("FINANCIAL ANALYTICS")
    print("=" * 50)

    financial_analysis = analyze_financial(
        finance,
        legacy_sales
    )

    print("\nFinancial Summary:")

    print(
        financial_analysis[
            "financial_summary"
        ]
    )

    financial_analysis[
        "financial_summary"
    ].to_csv(
        DATA_DIR / "financial_summary.csv",
        index=False
    )

    print(
        "Financial analytics saved successfully!"
    )

    # ==================================================
    # SALES ANALYTICS
    # ==================================================

    print("\n" + "=" * 50)
    print("SALES ANALYTICS")
    print("=" * 50)

    sales_analysis = analyze_sales(
        sales,
        products,
        customers
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

    monthly_sales = sales_analysis[
        "monthly_sales"
    ]

    print("\nMonthly Sales:")

    print(monthly_sales)

    monthly_sales.to_csv(
        DATA_DIR / "monthly_sales.csv",
        index=False
    )

    # ==================================================
    # BEST SELLING PRODUCTS
    # ==================================================

    best_selling_products = (
        sales_analysis[
            "best_selling_products"
        ]
    )

    print("\nBest Selling Products:")

    print(
        best_selling_products.head(10)
    )

    best_selling_products.to_csv(
        DATA_DIR / "best_selling_products.csv",
        index=False
    )

    # ==================================================
    # CUSTOMER SPENDING
    # ==================================================

    customer_spending = (
        sales_analysis[
            "customer_spending"
        ]
    )

    print("\nCustomer Spending:")

    print(
        customer_spending.head(10)
    )

    customer_spending.to_csv(
        DATA_DIR / "customer_spending.csv",
        index=False
    )

    # ==================================================
    # PRODUCT REVENUE
    # ==================================================

    product_revenue = (
        sales_analysis[
            "product_revenue"
        ]
    )

    print("\nProduct Revenue:")

    print(
        product_revenue.head(10)
    )

    product_revenue.to_csv(
        DATA_DIR / "product_revenue.csv",
        index=False
    )

    # ==================================================
    # CATEGORY SALES
    # ==================================================

    category_sales = (
        sales_analysis[
            "category_sales"
        ]
    )

    print("\nCategory Sales:")

    print(category_sales)

    category_sales.to_csv(
        DATA_DIR / "category_sales.csv",
        index=False
    )

    print(
        "Sales analytics saved successfully!"
    )

    # ==================================================
    # BUSINESS SUMMARY
    # ==================================================

    print("\n" + "=" * 50)
    print("BUSINESS SUMMARY")
    print("=" * 50)

    total_sales = sales[
        "TotalSales"
    ].sum()

    average_sale = sales[
        "TotalSales"
    ].mean()

    units_sold = sales[
        "Quantity"
    ].sum()

    total_orders = sales[
        "OrderID"
    ].nunique()

    total_customers = sales[
        "CustomerID"
    ].nunique()

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
            customers
        )

        add_products(
            db,
            products
        )

        add_inventory(
            db,
            inventory
        )

        add_finance(
            db,
            finance
        )

        add_orders(
            db,
            legacy_sales
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

    # Train model

    model = train_sales_model(
        daily_sales
    )

    print(
        "\nSales forecasting model "
        "trained successfully!"
    )

    # Predict seven days

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

    # Forecast visualization

    print(
        "\nCreating Actual vs "
        "Predicted Sales graph..."
    )

    try:

        plot_actual_vs_predicted(
            daily_sales,
            forecast,
            DATA_DIR / "actual_vs_predicted.png"
        )

    except TypeError:

        # Compatibility if your old function
        # still accepts only two arguments.

        plot_actual_vs_predicted(
            daily_sales,
            forecast
        )

    print(
        "Sales visualization completed!"
    )


# ==================================================
# LOCAL BUSINESS QUESTION FUNCTION
# ==================================================

def answer_local_business_question(
    question,
    total_revenue,
    total_orders,
    total_customers,
    total_quantity,
    top_product_name,
    top_product_revenue,
    finance_revenue,
    finance_expenses,
    finance_profit
):

    # Normalize wording.

    question_lower = (
        question
        .lower()
        .strip()
        .replace("_", " ")
    )

    # ==================================================
    # TOTAL REVENUE / TOTAL SALES / TOTAL AMOUNT
    # ==================================================

    if (
        "revenue" in question_lower
        and "finance" not in question_lower
    ):

        return (
            f"The total revenue is "
            f"${total_revenue:,.2f}."
        )

    if (
        "total sales" in question_lower
        or "totalsales" in question_lower
        or "total amount" in question_lower
        or "totalamount" in question_lower
    ):

        return (
            f"The total revenue is "
            f"${total_revenue:,.2f}."
        )

    # ==================================================
    # ORDERS
    # ==================================================

    if "order" in question_lower:

        return (
            f"The total number of orders is "
            f"{total_orders:,}."
        )

    # ==================================================
    # CUSTOMERS
    # ==================================================

    if "customer" in question_lower:

        return (
            f"There are "
            f"{total_customers:,} "
            f"customers with purchases."
        )

    # ==================================================
    # QUANTITY / ITEMS / UNITS
    # ==================================================

    if (
        "quantity" in question_lower
        or "items sold" in question_lower
        or "item sold" in question_lower
        or "units sold" in question_lower
        or "unit sold" in question_lower
        or "how many items" in question_lower
        or "how many units" in question_lower
    ):

        return (
            f"The total quantity sold is "
            f"{total_quantity:,.0f} items."
        )

    # ==================================================
    # TOP PRODUCT
    # ==================================================

    if (
        "top product" in question_lower
        or "best product" in question_lower
        or "best selling product" in question_lower
        or "best-selling product" in question_lower
        or "highest revenue product" in question_lower
        or "most revenue product" in question_lower
    ):

        return (
            f"The top product by revenue is "
            f"{top_product_name}, with revenue of "
            f"${top_product_revenue:,.2f}."
        )

    # ==================================================
    # EXPENSES
    # ==================================================

    if "expense" in question_lower:

        return (
            f"The total expenses are "
            f"${finance_expenses:,.2f}."
        )

    # ==================================================
    # PROFIT
    # ==================================================

    if "profit" in question_lower:

        return (
            f"The total profit is "
            f"${finance_profit:,.2f}."
        )

    # ==================================================
    # FINANCE REVENUE
    # ==================================================

    if (
        "finance revenue" in question_lower
        or "financial revenue" in question_lower
    ):

        return (
            f"The finance dataset reports "
            f"${finance_revenue:,.2f} in revenue."
        )

    # No local answer available.

    return None


# ==================================================
# STREAMLIT DASHBOARD
# ==================================================

def run_dashboard():

    # ==================================================
    # PAGE CONFIGURATION
    # ==================================================

    st.set_page_config(
        page_title=(
            "AI Business Analytics Dashboard"
        ),
        page_icon="📊",
        layout="wide"
    )

    # ==================================================
    # LOAD DASHBOARD DATA
    # ==================================================

    @st.cache_data
    def load_dashboard_data():

        sales_data = pd.read_csv(
            DATA_DIR / "sales.csv"
        )

        products_data = pd.read_csv(
            DATA_DIR / "products.csv"
        )

        customers_data = pd.read_csv(
            DATA_DIR / "customers.csv"
        )

        inventory_data = pd.read_csv(
            DATA_DIR / "inventory.csv"
        )

        finance_data = pd.read_csv(
            DATA_DIR / "finance.csv"
        )

        return (
            sales_data,
            products_data,
            customers_data,
            inventory_data,
            finance_data
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
            "Required CSV files are missing. "
            "Run python main.py first."
        )

        st.stop()

    # ==================================================
    # REVENUE COLUMN
    # ==================================================

    if "TotalSales" in sales.columns:

        revenue_column = "TotalSales"

    elif "TotalAmount" in sales.columns:

        revenue_column = "TotalAmount"

    else:

        st.error(
            "sales.csv must contain "
            "TotalSales or TotalAmount."
        )

        st.stop()

    # ==================================================
    # HEADER
    # ==================================================

    st.title(
        "📊 AI Business Analytics Dashboard"
    )

    st.write(
        "Sales, Customer, Product, Inventory "
        "and Financial Analytics"
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

    # Category filter

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
        "🤖 AI Business Assistant"
    )

    st.sidebar.write(
        "📋 Detailed Data"
    )

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
            f"${total_revenue:,.2f}"
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

    monthly_data["Month"] = (
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

    fig_monthly = px.line(
        monthly_sales,
        x="Month",
        y=revenue_column,
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig_monthly.update_layout(
        template="plotly_white",
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

    fig_category = px.pie(
        category_sales,
        names="Category",
        values=revenue_column,
        title=(
            "Revenue Distribution by Category"
        )
    )

    # ==================================================
    # SHOW SALES CHARTS
    # ==================================================

    chart1, chart2 = (
        st.columns(2)
    )

    with chart1:

        st.plotly_chart(
            fig_monthly,
            use_container_width=True
        )

    with chart2:

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

        forecast["ds"] = (
            pd.to_datetime(
                forecast["ds"],
                errors="coerce"
            )
        )

        sales_dates = pd.to_datetime(
            sales["SaleDate"],
            errors="coerce"
        )

        last_sale_date = (
            sales_dates.max()
        )

        future_forecast = (
            forecast[
                forecast["ds"]
                > last_sale_date
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
                    "Next 7 Days Sales Forecast"
                )
            )

            fig_forecast.update_layout(
                template="plotly_white",
                xaxis_title="Date",
                yaxis_title=(
                    "Predicted Revenue"
                )
            )

            st.plotly_chart(
                fig_forecast,
                use_container_width=True
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
                .rename(
                    columns={
                        "ds":
                            "Date",
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
            "to generate the forecast."
        )

    st.caption(
        "The forecast represents overall "
        "business sales."
    )

    st.divider()

    # ==================================================
    # FINANCIAL OVERVIEW
    # ==================================================

    st.subheader(
        "💵 Financial Overview"
    )

    finance_revenue = 0
    finance_expenses = 0
    finance_profit = 0

    if "Revenue" in finance.columns:

        finance_revenue = (
            finance["Revenue"].sum()
        )

    if "Expenses" in finance.columns:

        finance_expenses = (
            finance["Expenses"].sum()
        )

    if "Profit" in finance.columns:

        finance_profit = (
            finance["Profit"].sum()
        )

    elif (
        "Revenue" in finance.columns
        and
        "Expenses" in finance.columns
    ):

        finance_profit = (
            finance_revenue
            - finance_expenses
        )

    fin1, fin2, fin3 = (
        st.columns(3)
    )

    fin1.metric(
        "Revenue",
        f"${finance_revenue:,.2f}"
    )

    fin2.metric(
        "Expenses",
        f"${finance_expenses:,.2f}"
    )

    fin3.metric(
        "Profit",
        f"${finance_profit:,.2f}"
    )

    st.divider()

    # ==================================================
    # AI BUSINESS ASSISTANT
    # ==================================================

    st.subheader(
        "🤖 AI Business Assistant"
    )

    st.write(
        "Ask questions about your business data."
    )

    # ==================================================
    # TOP PRODUCT
    # ==================================================

    top_product_name = "N/A"
    top_product_revenue = 0

    if not product_sales.empty:

        top_product_name = (
            product_sales.iloc[
                0
            ]["ProductName"]
        )

        top_product_revenue = (
            product_sales.iloc[
                0
            ][revenue_column]
        )

    # ==================================================
    # BUSINESS CONTEXT
    # ==================================================

    business_context = f"""
Selected Category: {selected_category}

Total Revenue: ${total_revenue:,.2f}

Total Orders: {total_orders}

Total Customers: {total_customers}

Total Quantity Sold: {total_quantity:,.0f}

Top Product: {top_product_name}

Top Product Revenue:
${top_product_revenue:,.2f}

Finance Revenue:
${finance_revenue:,.2f}

Finance Expenses:
${finance_expenses:,.2f}

Finance Profit:
${finance_profit:,.2f}
"""

    # ==================================================
    # CHAT HISTORY
    # ==================================================

    if "messages" not in st.session_state:

        st.session_state[
            "messages"
        ] = []

    for message in (
        st.session_state[
            "messages"
        ]
    ):

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    # ==================================================
    # CHAT INPUT
    # ==================================================

    user_question = (
        st.chat_input(
            "Ask a question "
            "about your business..."
        )
    )

    if user_question:

        # Save user message

        st.session_state[
            "messages"
        ].append(
            {
                "role": "user",
                "content": user_question
            }
        )

        with st.chat_message(
            "user"
        ):

            st.write(
                user_question
            )

        # ==================================================
        # TRY LOCAL ANSWER FIRST
        # ==================================================

        answer = answer_local_business_question(
            question=user_question,
            total_revenue=total_revenue,
            total_orders=total_orders,
            total_customers=total_customers,
            total_quantity=total_quantity,
            top_product_name=top_product_name,
            top_product_revenue=top_product_revenue,
            finance_revenue=finance_revenue,
            finance_expenses=finance_expenses,
            finance_profit=finance_profit
        )

        # ==================================================
        # USE OPENAI ONLY IF LOCAL ANSWER NOT FOUND
        # ==================================================

        if answer is None:

            answer = ask_business_chatbot(
                user_question,
                business_context
            )

        # Save assistant response

        st.session_state[
            "messages"
        ].append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message(
            "assistant"
        ):

            st.write(
                answer
            )

    # ==================================================
    # CLEAR CHAT
    # ==================================================

    if st.button(
        "🗑 Clear Chat"
    ):

        st.session_state[
            "messages"
        ] = []

        st.rerun()

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
    # DOWNLOAD REPORT
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
# CHECK IF STREAMLIT IS RUNNING
# ==================================================

def running_in_streamlit():

    try:

        from streamlit.runtime.scriptrunner import (
            get_script_run_ctx
        )

        context = (
            get_script_run_ctx(
                suppress_warning=True
            )
        )

        return (
            context is not None
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