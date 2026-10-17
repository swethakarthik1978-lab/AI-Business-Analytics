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

from recommend_system import (
    recommend_similar_products,
    frequently_bought_together,
    personalized_recommendations
)


# ==================================================
# PROJECT PATHS
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==================================================
# HTML HELPER
# ==================================================

def render_html(html):

    st.html(html)


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

        print(
            "CLEANING",
            name
        )

        clean_datasets[name] = clean_dataframe(
            df
        )

    # ==================================================
    # FEATURE ENGINEERING
    # ==================================================

    print("\nFEATURE ENGINEERING")

    for name, df in clean_datasets.items():

        feature_df = create_features(
            df
        )

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

    customers = clean_datasets[
        "customers"
    ]

    products = clean_datasets[
        "products"
    ]

    inventory = clean_datasets[
        "inventory"
    ]

    finance = clean_datasets[
        "finance"
    ]

    # ==================================================
    # CUSTOMER ANALYTICS
    # ==================================================

    print(
        "\n" + "=" * 50
    )

    print(
        "CUSTOMER ANALYTICS"
    )

    print(
        "=" * 50
    )

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

    print(
        "\n" + "=" * 50
    )

    print(
        "INVENTORY ANALYTICS"
    )

    print(
        "=" * 50
    )

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
    # TOTALAMOUNT COMPATIBILITY
    # ==================================================

    legacy_sales = sales.copy()

    if (
        "TotalAmount"
        not in legacy_sales.columns
        and
        "TotalSales"
        in legacy_sales.columns
    ):

        legacy_sales[
            "TotalAmount"
        ] = legacy_sales[
            "TotalSales"
        ]

    # ==================================================
    # FINANCIAL ANALYTICS
    # ==================================================

    print(
        "\n" + "=" * 50
    )

    print(
        "FINANCIAL ANALYTICS"
    )

    print(
        "=" * 50
    )

    financial_analysis = analyze_financial(
        finance,
        legacy_sales
    )

    print(
        "\nFinancial Summary:"
    )

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

    print(
        "\n" + "=" * 50
    )

    print(
        "SALES ANALYTICS"
    )

    print(
        "=" * 50
    )

    sales_analysis = analyze_sales(
        sales,
        products,
        customers
    )

    print(
        "\nTotal Sales:"
    )

    print(
        round(
            sales_analysis[
                "total_sales"
            ],
            2
        )
    )

    # ==================================================
    # SAVE SALES REPORTS
    # ==================================================

    monthly_sales = sales_analysis[
        "monthly_sales"
    ]

    best_selling_products = (
        sales_analysis[
            "best_selling_products"
        ]
    )

    customer_spending = (
        sales_analysis[
            "customer_spending"
        ]
    )

    product_revenue = (
        sales_analysis[
            "product_revenue"
        ]
    )

    category_sales = (
        sales_analysis[
            "category_sales"
        ]
    )

    monthly_sales.to_csv(
        DATA_DIR / "monthly_sales.csv",
        index=False
    )

    best_selling_products.to_csv(
        DATA_DIR / "best_selling_products.csv",
        index=False
    )

    customer_spending.to_csv(
        DATA_DIR / "customer_spending.csv",
        index=False
    )

    product_revenue.to_csv(
        DATA_DIR / "product_revenue.csv",
        index=False
    )

    category_sales.to_csv(
        DATA_DIR / "category_sales.csv",
        index=False
    )

    print(
        "\nMonthly Sales:"
    )

    print(
        monthly_sales
    )

    print(
        "\nBest Selling Products:"
    )

    print(
        best_selling_products.head(
            10
        )
    )

    print(
        "\nCustomer Spending:"
    )

    print(
        customer_spending.head(
            10
        )
    )

    print(
        "\nProduct Revenue:"
    )

    print(
        product_revenue.head(
            10
        )
    )

    print(
        "\nCategory Sales:"
    )

    print(
        category_sales
    )

    # ==================================================
    # BUSINESS SUMMARY
    # ==================================================

    print(
        "\n" + "=" * 50
    )

    print(
        "BUSINESS SUMMARY"
    )

    print(
        "=" * 50
    )

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
        round(
            total_sales,
            2
        )
    )

    print(
        "Average Sale: $",
        round(
            average_sale,
            2
        )
    )

    print(
        "Units Sold:",
        int(
            units_sold
        )
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

    print(
        "\n" + "=" * 50
    )

    print(
        "DATABASE"
    )

    print(
        "=" * 50
    )

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

    print(
        "\n" + "=" * 50
    )

    print(
        "SALES FORECASTING"
    )

    print(
        "=" * 50
    )

    daily_sales = prepare_sales_data(
        sales
    )

    print(
        "\nDaily sales data:"
    )

    print(
        daily_sales.head()
    )

    model = train_sales_model(
        daily_sales
    )

    print(
        "\nSales forecasting model "
        "trained successfully!"
    )

    forecast = predict_sales(
        model,
        days=7
    )

    print(
        "\nNEXT 7 DAYS SALES FORECAST"
    )

    print(
        forecast.tail(
            7
        ).to_string(
            index=False
        )
    )

    save_forecast(
        forecast,
        DATA_DIR / "sales_forecast.csv"
    )

    print(
        "\nSales forecast saved successfully!"
    )

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

        plot_actual_vs_predicted(
            daily_sales,
            forecast
        )

    print(
        "Sales visualization completed!"
    )


# ==================================================
# LOCAL CHATBOT ANSWERS
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

    question_lower = (
        question
        .lower()
        .strip()
        .replace(
            "_",
            " "
        )
    )

    # ==================================================
    # FINANCE REVENUE
    # ==================================================

    if (
        "finance revenue"
        in question_lower
        or
        "financial revenue"
        in question_lower
    ):

        return (
            f"The finance dataset reports "
            f"${finance_revenue:,.2f} "
            f"in revenue."
        )

    # ==================================================
    # SALES REVENUE
    # ==================================================

    if (
        "total revenue"
        in question_lower
        or
        "total sales"
        in question_lower
        or
        "totalsales"
        in question_lower
        or
        "total amount"
        in question_lower
        or
        "totalamount"
        in question_lower
        or
        question_lower
        == "revenue"
    ):

        return (
            f"The total sales revenue is "
            f"${total_revenue:,.2f}."
        )

    # ==================================================
    # ORDERS
    # ==================================================

    if (
        "order"
        in question_lower
    ):

        return (
            f"The total number of orders "
            f"is {total_orders:,}."
        )

    # ==================================================
    # CUSTOMERS
    # ==================================================

    if (
        "customer"
        in question_lower
    ):

        return (
            f"There are "
            f"{total_customers:,} "
            f"customers with purchases."
        )

    # ==================================================
    # QUANTITY
    # ==================================================

    if (
        "quantity"
        in question_lower
        or
        "items sold"
        in question_lower
        or
        "item sold"
        in question_lower
        or
        "units sold"
        in question_lower
        or
        "unit sold"
        in question_lower
        or
        "how many items"
        in question_lower
        or
        "how many units"
        in question_lower
    ):

        return (
            f"The total quantity sold is "
            f"{total_quantity:,.0f} items."
        )

    # ==================================================
    # TOP PRODUCT
    # ==================================================

    if (
        "top product"
        in question_lower
        or
        "best product"
        in question_lower
        or
        "best selling product"
        in question_lower
        or
        "best-selling product"
        in question_lower
        or
        "highest revenue product"
        in question_lower
    ):

        return (
            f"The top product by revenue is "
            f"{top_product_name}, with "
            f"revenue of "
            f"${top_product_revenue:,.2f}."
        )

    # ==================================================
    # EXPENSES
    # ==================================================

    if (
        "expense"
        in question_lower
    ):

        return (
            f"The total expenses are "
            f"${finance_expenses:,.2f}."
        )

    # ==================================================
    # PROFIT
    # ==================================================

    if (
        "profit"
        in question_lower
    ):

        return (
            f"The total profit is "
            f"${finance_profit:,.2f}."
        )

    return None


# ==================================================
# SECTION HEADER
# ==================================================

def section_header(
    icon,
    title,
    description=None
):

    if description:

        html = f"""
<div class="section-heading">
    <h2>{icon} {title}</h2>
    <p>{description}</p>
</div>
"""

    else:

        html = f"""
<div class="section-heading">
    <h2>{icon} {title}</h2>
</div>
"""

    render_html(
        html
    )


# ==================================================
# PLOTLY CHART STYLE
# ==================================================

def style_chart(
    figure,
    height=None
):

    figure.update_layout(

        template="plotly_dark",

        paper_bgcolor=(
            "rgba(0,0,0,0)"
        ),

        plot_bgcolor=(
            "rgba(0,0,0,0)"
        ),

        font=dict(
            size=13
        ),

        title=dict(
            font=dict(
                size=19
            )
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    if height:

        figure.update_layout(
            height=height
        )

    return figure


# ==================================================
# STREAMLIT DASHBOARD
# ==================================================

def run_dashboard():

    # ==================================================
    # PAGE CONFIG
    # ==================================================

    st.set_page_config(
        page_title=(
            "AI Business Analytics Dashboard"
        ),
        page_icon="📊",
        layout="wide"
    )

    # ==================================================
    # CUSTOM CSS
    # ==================================================

    st.html(
        """
<style>

.stApp {
    background-color: #0E1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    padding-left: 3rem;
    padding-right: 3rem;
    max-width: 1500px;
}

h1 {
    font-weight: 800 !important;
    letter-spacing: -1px;
}

h2 {
    font-weight: 750 !important;
}

h3 {
    font-weight: 700 !important;
}

.section-heading {
    margin-top: 18px;
    margin-bottom: 20px;
}

.section-heading h2 {
    margin-bottom: 4px;
    font-size: 28px;
}

.section-heading p {
    margin-top: 0;
    margin-bottom: 0;
    color: #8E9AAF;
    font-size: 15px;
}

div[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #171B24,
        #202633
    );

    border: 1px solid #2E3645;
    padding: 20px;
    border-radius: 16px;

    box-shadow:
        0px 6px 20px
        rgba(0,0,0,0.20);

    transition: all 0.25s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #5B8DEF;

    box-shadow:
        0px 10px 30px
        rgba(0,0,0,0.35);
}

div[data-testid="stMetricLabel"] {
    font-size: 14px;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    font-size: 27px;
    font-weight: 800;
}

section[data-testid="stSidebar"] {
    background-color: #151922;
    border-right: 1px solid #2A303C;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #394150;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #5B8DEF;
    transform: translateY(-2px);
}

.stDownloadButton > button {
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 18px;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #2E3645;
}

div[data-testid="stChatMessage"] {
    border: 1px solid #252C38;
    border-radius: 15px;
    padding: 8px;
}

button[data-baseweb="tab"] {
    font-size: 15px;
    font-weight: 600;
}

hr {
    border-color: #272D38;
}

</style>
"""
    )

    # ==================================================
    # LOAD DATA
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

    if (
        "TotalSales"
        in sales.columns
    ):

        revenue_column = (
            "TotalSales"
        )

    elif (
        "TotalAmount"
        in sales.columns
    ):

        revenue_column = (
            "TotalAmount"
        )

    else:

        st.error(
            "sales.csv must contain "
            "TotalSales or TotalAmount."
        )

        st.stop()

    # ==================================================
    # SIDEBAR HEADER
    # ==================================================

    st.sidebar.html(
        """
<div style="
    text-align:center;
    padding:15px 5px 20px 5px;
">

    <div style="font-size:44px;">
        📊
    </div>

    <h2 style="margin-bottom:3px;">
        Business AI
    </h2>

    <p style="
        color:#8E9AAF;
        margin-top:0;
    ">
        Analytics Platform
    </p>

</div>
"""
    )

    st.sidebar.subheader(
        "Filters"
    )

    # ==================================================
    # CATEGORY FILTER
    # ==================================================

    categories = (
        ["All"]
        +
        sorted(
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
            "Product Category",
            categories
        )
    )

    # ==================================================
    # APPLY FILTER
    # ==================================================

    if (
        selected_category
        != "All"
    ):

        filtered_products = (
            products[
                products[
                    "Category"
                ]
                == selected_category
            ].copy()
        )

        filtered_sales = (
            sales[
                sales[
                    "ProductID"
                ].isin(
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
    # SIDEBAR NAVIGATION
    # ==================================================

    st.sidebar.divider()

    st.sidebar.markdown(
        "### Dashboard"
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
        "🎯 Recommendation System"
    )

    st.sidebar.write(
        "🔮 Sales Forecast"
    )

    st.sidebar.write(
        "💵 Financial Overview"
    )

    st.sidebar.write(
        "🤖 AI Business Assistant"
    )

    st.sidebar.write(
        "📋 Detailed Data"
    )

    st.sidebar.divider()

    if (
        st.sidebar.button(
            "🔄 Refresh Dashboard"
        )
    ):

        st.cache_data.clear()

        st.rerun()

    # ==================================================
    # MAIN HEADER
    # ==================================================

    st.html(
        """
<div style="
    padding:28px 30px;
    border-radius:20px;
    background:linear-gradient(
        135deg,
        #1B2230,
        #11151D
    );
    border:1px solid #2C3545;
    margin-bottom:15px;
    box-shadow:
        0px 8px 30px
        rgba(0,0,0,0.20);
">

    <h1 style="
        margin-bottom:8px;
        font-size:42px;
    ">
        📊 AI Business Analytics Dashboard
    </h1>

    <p style="
        font-size:17px;
        color:#AEB8C7;
        margin-bottom:0;
    ">
        Sales • Customers • Products •
        Recommendations • Forecasting • Finance
    </p>

</div>
"""
    )

    st.caption(
        "🟢 Dashboard online • "
        "Latest business data loaded successfully"
    )

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

    section_header(
        "📌",
        "Business Overview",
        "Key performance indicators for the selected business data."
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        st.metric(
            "💰 REVENUE",
            f"${total_revenue:,.0f}"
        )

    with col2:

        st.metric(
            "🛒 ORDERS",
            f"{total_orders:,}"
        )

    with col3:

        st.metric(
            "👥 CUSTOMERS",
            f"{total_customers:,}"
        )

    with col4:

        st.metric(
            "📦 UNITS SOLD",
            f"{total_quantity:,.0f}"
        )

    st.divider()

    # ==================================================
    # SALES PERFORMANCE
    # ==================================================

    section_header(
        "📈",
        "Sales Performance",
        "Track monthly revenue trends and category performance."
    )

    filtered_sales[
        "SaleDate"
    ] = pd.to_datetime(
        filtered_sales[
            "SaleDate"
        ],
        errors="coerce"
    )

    monthly_data = (
        filtered_sales
        .dropna(
            subset=[
                "SaleDate"
            ]
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
        .to_period(
            "M"
        )
        .astype(
            str
        )
    )

    monthly_sales = (
        monthly_data
        .groupby(
            "Month",
            as_index=False
        )[
            revenue_column
        ]
        .sum()
    )

    # ==================================================
    # MONTHLY CHART
    # ==================================================

    fig_monthly = px.line(
        monthly_sales,
        x="Month",
        y=revenue_column,
        markers=True,
        title=(
            "Monthly Revenue Trend"
        )
    )

    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue",
        hovermode="x unified"
    )

    fig_monthly = style_chart(
        fig_monthly,
        height=420
    )

    # ==================================================
    # CATEGORY CHART
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
        )[
            revenue_column
        ]
        .sum()
    )

    fig_category = px.pie(
        category_sales,
        names="Category",
        values=revenue_column,
        hole=0.35,
        title=(
            "Revenue by Category"
        )
    )

    fig_category = style_chart(
        fig_category,
        height=420
    )

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

    section_header(
        "📦",
        "Product Performance",
        "Identify products generating the highest sales revenue."
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
        )[
            revenue_column
        ]
        .sum()
        .sort_values(
            revenue_column,
            ascending=False
        )
    )

    top_products = (
        product_sales
        .head(10)
        .sort_values(
            revenue_column,
            ascending=True
        )
    )

    fig_products = px.bar(
        top_products,
        x=revenue_column,
        y="ProductName",
        orientation="h",
        title=(
            "Top 10 Products by Revenue"
        )
    )

    fig_products.update_layout(
        xaxis_title="Revenue",
        yaxis_title=""
    )

    fig_products = style_chart(
        fig_products,
        height=500
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # RECOMMENDATION SYSTEM
    # ==================================================

    section_header(
        "🎯",
        "Product Recommendation System",
        "Explore product relationships and personalized suggestions."
    )

    rec1, rec2, rec3 = (
        st.columns(3)
    )

    with rec1:

        st.info(
            "🔎 **Similar Products**\n\n"
            "Finds products belonging "
            "to the same category."
        )

    with rec2:

        st.info(
            "🛒 **Bought Together**\n\n"
            "Finds products appearing "
            "in the same orders."
        )

    with rec3:

        st.info(
            "👤 **Personalized**\n\n"
            "Suggests products based "
            "on customer purchase history."
        )

    tab1, tab2, tab3 = st.tabs(
        [
            "🔎 Similar Products",
            "🛒 Frequently Bought Together",
            "👤 Personalized"
        ]
    )

    # ==================================================
    # PRODUCT LOOKUP
    # ==================================================

    product_options = (
        products[
            [
                "ProductID",
                "ProductName"
            ]
        ]
        .drop_duplicates(
            subset="ProductID"
        )
        .sort_values(
            "ProductName"
        )
    )

    product_lookup = {}

    for _, row in (
        product_options.iterrows()
    ):

        label = (
            f"{row['ProductName']} "
            f"(ID: "
            f"{int(row['ProductID'])})"
        )

        product_lookup[
            label
        ] = row[
            "ProductID"
        ]

    # ==================================================
    # TAB 1 - SIMILAR PRODUCTS
    # ==================================================

    with tab1:

        if product_lookup:

            selected_product_label = (
                st.selectbox(
                    "Select a product",
                    list(
                        product_lookup.keys()
                    ),
                    key=(
                        "similar_products"
                    )
                )
            )

            selected_product_id = (
                product_lookup[
                    selected_product_label
                ]
            )

            similar_results = (
                recommend_similar_products(
                    products,
                    selected_product_id,
                    n=5
                )
            )

            if (
                similar_results.empty
            ):

                st.info(
                    "No similar products found."
                )

            else:

                display_columns = [
                    column
                    for column in [
                        "ProductID",
                        "ProductName",
                        "Category",
                        "Price"
                    ]
                    if column
                    in similar_results.columns
                ]

                st.dataframe(
                    similar_results[
                        display_columns
                    ],
                    use_container_width=True,
                    hide_index=True
                )

        else:

            st.info(
                "No products are available."
            )

    # ==================================================
    # TAB 2 - FREQUENTLY BOUGHT TOGETHER
    # ==================================================

    with tab2:

        if product_lookup:

            selected_frequent_label = (
                st.selectbox(
                    "Select a product",
                    list(
                        product_lookup.keys()
                    ),
                    key=(
                        "frequent_products"
                    )
                )
            )

            selected_frequent_id = (
                product_lookup[
                    selected_frequent_label
                ]
            )

            frequent_results = (
                frequently_bought_together(
                    sales,
                    selected_frequent_id,
                    n=5
                )
            )

            if (
                frequent_results.empty
            ):

                st.info(
                    "No frequently bought together "
                    "products were found. "
                    "This can happen when each order "
                    "contains only one product."
                )

            else:

                frequent_results = (
                    frequent_results.merge(
                        products[
                            [
                                "ProductID",
                                "ProductName",
                                "Category"
                            ]
                        ]
                        .drop_duplicates(
                            subset="ProductID"
                        ),
                        on="ProductID",
                        how="left"
                    )
                )

                st.dataframe(
                    frequent_results[
                        [
                            "ProductID",
                            "ProductName",
                            "Category",
                            "Frequency"
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True
                )

    # ==================================================
    # TAB 3 - PERSONALIZED
    # ==================================================

    with tab3:

        customer_options = (
            customers[
                [
                    "CustomerID",
                    "CustomerName"
                ]
            ]
            .drop_duplicates(
                subset="CustomerID"
            )
            .sort_values(
                "CustomerName"
            )
        )

        customer_lookup = {}

        for _, row in (
            customer_options.iterrows()
        ):

            label = (
                f"{row['CustomerName']} "
                f"(ID: "
                f"{int(row['CustomerID'])})"
            )

            customer_lookup[
                label
            ] = row[
                "CustomerID"
            ]

        if customer_lookup:

            selected_customer_label = (
                st.selectbox(
                    "Select a customer",
                    list(
                        customer_lookup.keys()
                    ),
                    key=(
                        "customer_recommendations"
                    )
                )
            )

            selected_customer_id = (
                customer_lookup[
                    selected_customer_label
                ]
            )

            personalized_results = (
                personalized_recommendations(
                    sales,
                    products,
                    selected_customer_id,
                    n=5
                )
            )

            if (
                personalized_results.empty
            ):

                st.info(
                    "No personalized recommendations "
                    "were found for this customer."
                )

            else:

                display_columns = [
                    column
                    for column in [
                        "ProductID",
                        "ProductName",
                        "Category",
                        "Price"
                    ]
                    if column
                    in personalized_results.columns
                ]

                st.dataframe(
                    personalized_results[
                        display_columns
                    ],
                    use_container_width=True,
                    hide_index=True
                )

        else:

            st.info(
                "No customers are available."
            )

    st.divider()

    # ==================================================
    # SALES FORECAST
    # ==================================================

    section_header(
        "🔮",
        "Sales Forecast",
        "Machine-learning estimates for upcoming sales."
    )

    forecast_file = (
        DATA_DIR
        / "sales_forecast.csv"
    )

    if (
        forecast_file.exists()
    ):

        forecast = pd.read_csv(
            forecast_file
        )

        forecast[
            "ds"
        ] = pd.to_datetime(
            forecast[
                "ds"
            ],
            errors="coerce"
        )

        sales_dates = pd.to_datetime(
            sales[
                "SaleDate"
            ],
            errors="coerce"
        )

        last_sale_date = (
            sales_dates.max()
        )

        future_forecast = (
            forecast[
                forecast[
                    "ds"
                ]
                > last_sale_date
            ]
            .sort_values(
                "ds"
            )
            .head(
                7
            )
        )

        if (
            not
            future_forecast.empty
        ):

            fig_forecast = (
                px.line(
                    future_forecast,
                    x="ds",
                    y="yhat",
                    markers=True,
                    title=(
                        "Next 7 Days "
                        "Sales Forecast"
                    )
                )
            )

            fig_forecast.update_layout(
                xaxis_title="Date",
                yaxis_title=(
                    "Predicted Revenue"
                )
            )

            fig_forecast = (
                style_chart(
                    fig_forecast,
                    height=440
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

    st.divider()

    # ==================================================
    # FINANCIAL OVERVIEW
    # ==================================================

    section_header(
        "💵",
        "Financial Overview",
        "Review revenue, expenses and overall profit."
    )

    finance_revenue = 0
    finance_expenses = 0
    finance_profit = 0

    if (
        "Revenue"
        in finance.columns
    ):

        finance_revenue = (
            finance[
                "Revenue"
            ].sum()
        )

    if (
        "Expenses"
        in finance.columns
    ):

        finance_expenses = (
            finance[
                "Expenses"
            ].sum()
        )

    if (
        "Profit"
        in finance.columns
    ):

        finance_profit = (
            finance[
                "Profit"
            ].sum()
        )

    elif (
        "Revenue"
        in finance.columns
        and
        "Expenses"
        in finance.columns
    ):

        finance_profit = (
            finance_revenue
            -
            finance_expenses
        )

    fin1, fin2, fin3 = (
        st.columns(3)
    )

    with fin1:

        st.metric(
            "💰 REVENUE",
            f"${finance_revenue:,.0f}"
        )

    with fin2:

        st.metric(
            "💳 EXPENSES",
            f"${finance_expenses:,.0f}"
        )

    with fin3:

        st.metric(
            "📊 PROFIT",
            f"${finance_profit:,.0f}"
        )

    st.divider()

    # ==================================================
    # AI BUSINESS ASSISTANT
    # ==================================================

    section_header(
        "🤖",
        "AI Business Assistant",
        "Ask questions about your business performance."
    )

    st.html(
        """
<div style="
    padding:18px;
    background:#171C26;
    border:1px solid #2D3646;
    border-radius:15px;
    margin-bottom:18px;
">

    <strong>
        💡 Example questions
    </strong>

    <p style="
        margin-top:15px;
        line-height:2;
    ">
        • What is the total revenue?<br>
        • What is the quantity sold?<br>
        • How many customers are there?<br>
        • What is the top product?<br>
        • What are the total expenses?
    </p>

</div>
"""
    )

    # ==================================================
    # TOP PRODUCT
    # ==================================================

    top_product_name = (
        "N/A"
    )

    top_product_revenue = (
        0
    )

    if (
        not
        product_sales.empty
    ):

        top_product_name = (
            product_sales.iloc[
                0
            ][
                "ProductName"
            ]
        )

        top_product_revenue = (
            product_sales.iloc[
                0
            ][
                revenue_column
            ]
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

    if (
        "messages"
        not in st.session_state
    ):

        st.session_state[
            "messages"
        ] = []

    for message in (
        st.session_state[
            "messages"
        ]
    ):

        with st.chat_message(
            message[
                "role"
            ]
        ):

            st.write(
                message[
                    "content"
                ]
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

    if (
        user_question
    ):

        st.session_state[
            "messages"
        ].append(
            {
                "role":
                    "user",

                "content":
                    user_question
            }
        )

        with st.chat_message(
            "user"
        ):

            st.write(
                user_question
            )

        answer = (
            answer_local_business_question(
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
        )

        if (
            answer is None
        ):

            answer = (
                ask_business_chatbot(
                    user_question,
                    business_context
                )
            )

        st.session_state[
            "messages"
        ].append(
            {
                "role":
                    "assistant",

                "content":
                    answer
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

    if (
        st.button(
            "🗑 Clear Chat"
        )
    ):

        st.session_state[
            "messages"
        ] = []

        st.rerun()

    st.divider()

    # ==================================================
    # DETAILED SALES DATA
    # ==================================================

    section_header(
        "📋",
        "Detailed Sales Data",
        "Review individual sales transactions."
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
        file_name=(
            "sales_report.csv"
        ),
        mime="text/csv"
    )

    # ==================================================
    # FOOTER
    # ==================================================

    st.divider()

    st.html(
        """
<div style="
    text-align:center;
    color:#7F8998;
    padding:15px;
">

    AI Business Analytics Platform

    <br>

    Sales • Intelligence •
    Forecasting • Recommendations

</div>
"""
    )


# ==================================================
# CHECK IF RUNNING IN STREAMLIT
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
# RUN
# ==================================================

if (
    running_in_streamlit()
):

    run_dashboard()

elif (
    __name__
    == "__main__"
):

    main()