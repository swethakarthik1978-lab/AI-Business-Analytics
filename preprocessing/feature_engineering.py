def create_features(df):
    df = df.copy()

    # Calculate total sales
    if "Quantity" in df.columns and "UnitPrice" in df.columns:
        df["TotalSales"] = df["Quantity"] * df["UnitPrice"]

    # Create inventory stock status
    if "CurrentStock" in df.columns and "ReorderLevel" in df.columns:
        df["StockStatus"] = df.apply(
            lambda row: "Reorder"
            if row["CurrentStock"] <= row["ReorderLevel"]
            else "In Stock",
            axis=1
        )

    return df