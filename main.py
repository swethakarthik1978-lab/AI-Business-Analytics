from config import PROJECT_NAME, VERSION
from database.database import engine, Base, SessionLocal
from database.models import Product, Customer, Order, Inventory, Finance
from database.crud import *
from data_collection import load_data
from preprocessing.clean_data import clean_dataframe
from preprocessing.feature_engineering import create_features
from ML.sales_forecasting import (prepare_sales_data, train_sales_model, predict_sales, save_forecast, plot_actual_vs_predicted)

def main():
    print("=" * 50)
    print(PROJECT_NAME)
    print("Version", VERSION)
    print("=" * 50)
    print("Welcome to the AI Business Analytics Platform")


    print("LOADING DATA")

    datasets = load_data()

    for name, df in datasets.items():
        print(name, df.shape)


    print("CLEANING DATA")

    clean_datasets = {}

    for name, df in datasets.items():
        print("CLEANING", name)
        clean_datasets[name] = clean_dataframe(df)


    print("FEATURE ENGINEERING")



    for name, df in clean_datasets.items():
        feature_df = create_features(df)

        clean_datasets[name] = feature_df

        # Save updated data back to CSV files
        feature_df.to_csv(
            f"data/{name}.csv",
            index=False
        )

        print(name, "updated successfully")


    sales = clean_datasets["sales"]

    print("=" * 50)
    print("BUSINESS SUMMARY")
    print("=" * 50)

    total_sales = sales["TotalSales"].sum()
    average_sale = sales["TotalSales"].mean()
    units_sold = sales["Quantity"].sum()

    print("Total Sales: $", round(total_sales, 2))
    print("Average Sale: $", round(average_sale, 2))
    print("Units Sold:", int(units_sold))


    Base.metadata.create_all(bind=engine)

    print("All tables created successfully!")

    db = SessionLocal()

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

    db.close()

    print("Database updated successfully!")
print("SALES FORECASTING")
sales = clean_dataframe["sales"]
daily_sales = prepare_sales_data(sales)
print("\nDaily sales data:")
print(daily_sales.head())

# Train model
model = train_sales_model(daily_sales)

print("\nSales forecasting model trained successfully!")

# Generate predictions
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

print("\nSales forecast saved successfully!")

print("\nCreating Actual vs Predicted Sales graph...")

plot_actual_vs_predicted(
    daily_sales,
    forecast
)

print("Sales visualization completed!")


if __name__ == "__main__":
    main()