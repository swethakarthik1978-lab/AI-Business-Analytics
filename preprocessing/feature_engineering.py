def create_features(df):
    df = df.copy() 

    if "quantity" in df.columns and "unit_price" in df.columns:
        df["total_sales"] = df["quantity"] * df["unit_price"]

    if "total_sales" in df.columns and "cost" in df.columns:
        df["profit"] = df["total_sales"] - df["cost"]

    if "total_sales" in df.columns:
        df["profit_margin"] = df["profit"] / df["total_sales"] * 100

    return df 