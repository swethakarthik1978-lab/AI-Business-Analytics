import pandas as pd


def clean_dataframe(df):
    # Work on a copy so the original dataframe is not changed
    df = df.copy()

    print("MISSING VALUES")
    print(df.isnull().sum())

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing values
    for column in df.columns:
        if pd.api.types.is_string_dtype(df[column]) or df[column].dtype == "object":
            df[column] = df[column].fillna("Unknown")
        else:
            median_value = df[column].median()

            if pd.notna(median_value):
                df[column] = df[column].fillna(median_value)

    return df