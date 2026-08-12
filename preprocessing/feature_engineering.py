def create_features(df):
    df = df.copy()

    # Create total sales for sales data
    if "Quantity" in df.columns and "UnitPrice" in df.columns:
        df["TotalSales"] = df["Quantity"] * df["UnitPrice"]

    # Calculate profit only if Cost exists
    if "TotalSales" in df.columns and "Cost" in df.columns:
        df["Profit"] = df["TotalSales"] - df["Cost"]

    # Calculate profit margin only if Profit was created
    if "Profit" in df.columns and "TotalSales" in df.columns:
        df["ProfitMargin"] = (
            df["Profit"] / df["TotalSales"] * 100
        )

    return df