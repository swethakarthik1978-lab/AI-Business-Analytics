import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
def prepare_sales_data(df):
    """
    Convert transaction-level sales into daily sales.
    """

    df = df.copy()

    df["SaleDate"] = pd.to_datetime(df["SaleDate"])

    daily_sales = (
        df.groupby("SaleDate")["TotalAmount"]
        .sum()
        .reset_index()
    )

    daily_sales = daily_sales.rename(
        columns={
            "SaleDate": "ds",
            "TotalAmount": "y"
        }
    )

    daily_sales = daily_sales.sort_values("ds")

    return daily_sales

def train_sales_model(sales_data):
    """
    Train Prophet forecasting model.
    """

    model = Prophet()

    model.fit(sales_data)

    return(model) 

def predict_sales(model, days=7):
    """
    Predict future sales.
    """

    future = model.make_future_dataframe(
        periods=days
    )

    forecast = model.predict(future)

    forecast = forecast[
        [
            "ds",
            "yhat",
            "yhat_lower",
            "yhat_upper"
        ]
    ]

    return forecast

def save_forecast(forecast, filename):
    """
    Save forecast to CSV.
    """

    forecast.to_csv(
        filename,
        index=False
    )
def plot_actual_vs_predicted(actual_data, forecast):
    """
    Plot actual sales against predicted sales.
    """

    plt.figure(figsize=(12, 6))

    # Actual sales
    plt.plot(
        actual_data["ds"],
        actual_data["y"],
        label="Actual Sales"
    )

    # Predicted sales
    plt.plot(
        forecast["ds"],
        forecast["yhat"],
        label="Predicted Sales"
    )

    plt.xlabel("Date")
    plt.ylabel("Sales")

    plt.title(
        "Actual Sales vs Predicted Sales"
    )

    plt.legend()

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()
