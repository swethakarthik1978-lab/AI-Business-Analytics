from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from prophet import Prophet


# ==================================================
# PREPARE SALES DATA
# ==================================================

def prepare_sales_data(df):

    data = df.copy()

    data["SaleDate"] = (
        pd.to_datetime(
            data["SaleDate"],
            errors="coerce"
        )
    )

    data = data.dropna(
        subset=["SaleDate"]
    )

    daily_sales = (
        data
        .groupby(
            "SaleDate",
            as_index=False
        )["TotalSales"]
        .sum()
        .rename(
            columns={
                "SaleDate": "ds",
                "TotalSales": "y"
            }
        )
        .sort_values(
            "ds"
        )
    )

    return daily_sales


# ==================================================
# TRAIN MODEL
# ==================================================

def train_sales_model(
    sales_data
):

    model = Prophet()

    model.fit(
        sales_data
    )

    return model


# ==================================================
# PREDICT SALES
# ==================================================

def predict_sales(
    model,
    days=7
):

    future = (
        model
        .make_future_dataframe(
            periods=days,
            freq="D"
        )
    )

    forecast = (
        model.predict(
            future
        )
    )

    forecast = (
        forecast[
            [
                "ds",
                "yhat",
                "yhat_lower",
                "yhat_upper"
            ]
        ]
    )

    return forecast


# ==================================================
# SAVE FORECAST
# ==================================================

def save_forecast(
    forecast,
    filepath=(
        "data/sales_forecast.csv"
    )
):

    filepath = Path(
        filepath
    )

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    forecast.to_csv(
        filepath,
        index=False
    )

    return filepath


# ==================================================
# ACTUAL VS PREDICTED GRAPH
# ==================================================

def plot_actual_vs_predicted(
    actual_sales,
    forecast,
    filepath=(
        "data/actual_vs_predicted.png"
    )
):

    filepath = Path(
        filepath
    )

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fig, ax = plt.subplots(
        figsize=(
            11,
            5
        )
    )

    # Actual

    ax.plot(
        actual_sales["ds"],
        actual_sales["y"],
        label="Actual Sales"
    )

    # Prediction

    ax.plot(
        forecast["ds"],
        forecast["yhat"],
        label="Predicted Sales"
    )

    ax.set_title(
        "Actual vs Predicted Sales"
    )

    ax.set_xlabel(
        "Date"
    )

    ax.set_ylabel(
        "Sales"
    )

    ax.legend()

    fig.autofmt_xdate()

    fig.tight_layout()

    fig.savefig(
        filepath,
        dpi=150
    )

    plt.close(
        fig
    )

    return filepath
