
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Business Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI BUSINESS ANALYTICS DASHBOARD")
st.write("Sales, Customer, Product and Financial Analytics")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data(filename):
    path = DATA_DIR / filename

    if path.exists():
        return pd.read_csv(path)

    return None


sales = load_data("sales.csv")
finance = load_data("finance.csv")
products = load_data("products.csv")

monthly_sales = load_data("monthly_sales.csv")
product_revenue = load_data("product_revenue.csv")
customer_spending = load_data("customer_spending.csv")
category_sales = load_data("category_sales.csv")
forecast = load_data("sales_forecast.csv")


if sales is None:
    st.error("Sales data not found. Run main.py first.")
    st.stop()

if "TotalSales" not in sales.columns:
    st.error("TotalSales column is missing. Run main.py.")
    st.stop()


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Dashboard Controls")

if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()

top_n = st.sidebar.slider(
    "Number of top products",
    min_value=5,
    max_value=20,
    value=10
)


# ==================================================
# BUSINESS OVERVIEW
# ==================================================

st.header("1. Business Overview")

total_revenue = sales["TotalSales"].sum()

total_orders = (
    sales["OrderID"].nunique()
    if "OrderID" in sales.columns
    else len(sales)
)

total_customers = sales["CustomerID"].nunique()

total_quantity = sales["Quantity"].sum()

total_profit = None

if finance is not None:
    if "Profit" in finance.columns:
        total_profit = finance["Profit"].sum()
    elif {"Revenue", "Expenses"}.issubset(finance.columns):
        total_profit = (
            finance["Revenue"].sum()
            - finance["Expenses"].sum()
        )


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "TOTAL REVENUE",
    f"${total_revenue:,.2f}"
)

col2.metric(
    "TOTAL PROFIT",
    f"${total_profit:,.2f}"
    if total_profit is not None
    else "N/A"
)

col3.metric(
    "TOTAL ORDERS" if "OrderID" in sales.columns
    else "SALES RECORDS",
    total_orders
)

col4.metric(
    "TOTAL CUSTOMERS",
    total_customers
)

st.metric("TOTAL UNITS SOLD", int(total_quantity))

st.divider()


# ==================================================
# MONTHLY SALES
# ==================================================

st.header("2. Monthly Sales Analysis")

if (
    monthly_sales is not None
    and {"Month", "MonthlySales"}.issubset(
        monthly_sales.columns
    )
):

    monthly_sales = monthly_sales.sort_values("Month")

    fig = px.line(
        monthly_sales,
        x="Month",
        y="MonthlySales",
        markers=True,
        title="Monthly Sales Trend"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Sales ($)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.warning("Monthly sales data not available.")


# ==================================================
# PRODUCT-WISE REVENUE
# ==================================================

st.header("3. Product-wise Revenue")

if (
    product_revenue is not None
    and "ProductRevenue" in product_revenue.columns
):

    product_label = (
        "ProductName"
        if "ProductName" in product_revenue.columns
        else "ProductID"
    )

    top_products = product_revenue.nlargest(
        top_n,
        "ProductRevenue"
    )

    fig = px.bar(
        top_products,
        x=product_label,
        y="ProductRevenue",
        title="Top Products by Revenue",
        color="ProductRevenue"
    )

    fig.update_layout(
        xaxis_title="Product",
        yaxis_title="Revenue ($)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.warning("Product revenue data not available.")


# ==================================================
# CATEGORY-WISE SALES
# ==================================================

st.header("4. Category-wise Sales")

if (
    category_sales is not None
    and {"Category", "TotalSales"}.issubset(
        category_sales.columns
    )
):

    fig = px.pie(
        category_sales,
        names="Category",
        values="TotalSales",
        title="Sales Distribution by Category",
        hole=0.3
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.warning("Category sales data not available.")


# ==================================================
# CUSTOMER SPENDING
# ==================================================

st.header("5. Customer Spending Analysis")

if (
    customer_spending is not None
    and "TotalSpent" in customer_spending.columns
):

    customer_label = (
        "CustomerName"
        if "CustomerName" in customer_spending.columns
        else "CustomerID"
    )

    top_customers = customer_spending.nlargest(
        10,
        "TotalSpent"
    )

    fig = px.bar(
        top_customers,
        x=customer_label,
        y="TotalSpent",
        title="Top 10 Customers by Spending",
        color="TotalSpent"
    )

    fig.update_layout(
        xaxis_title="Customer",
        yaxis_title="Total Spending ($)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.warning("Customer spending data not available.")


# ==================================================
# SALES FORECASTING
# ==================================================

st.header("6. AI Sales Forecasting")

if (
    forecast is not None
    and {"ds", "yhat"}.issubset(forecast.columns)
):

    forecast["ds"] = pd.to_datetime(
        forecast["ds"],
        errors="coerce"
    )

    # Show future predictions if historical dates exist
    if "SaleDate" in sales.columns:

        last_date = pd.to_datetime(
            sales["SaleDate"],
            errors="coerce"
        ).max()

        future = forecast[
            forecast["ds"] > last_date
        ].sort_values("ds").head(7)

    else:
        future = forecast.tail(7)

    if not future.empty:

        fig = px.line(
            future,
            x="ds",
            y="yhat",
            markers=True,
            title="Next 7 Days Sales Forecast"
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Predicted Sales ($)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Forecast Data")

        st.dataframe(
            future,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No future forecast dates found.")

else:
    st.warning("Forecast data not available.")


# ==================================================
# RAW SALES DATA
# ==================================================

st.header("7. Sales Data")

with st.expander("View Sales Dataset"):
    st.dataframe(
        sales,
        use_container_width=True
    )


# ==================================================
# DOWNLOAD REPORT
# ==================================================

st.header("8. Download Sales Report")

csv = sales.to_csv(index=False)

st.download_button(
    label="Download Sales Data",
    data=csv,
    file_name="sales_report.csv",
    mime="text/csv"
)


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.success("Dashboard loaded successfully!")
