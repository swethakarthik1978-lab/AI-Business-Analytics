import pandas as pd


def clean_dataframe(df):

    print("MISSING VALUES")
    print(df.isnull().sum())

    df = df.drop_duplicates()

    for column in df.columns:
        if pd.api.types.is_string_dtype(df[column]) or df[column].dtype == "object":
            df[column] = df[column].fillna("Unknown")
        else:
            median_value = df[column].median()

            if pd.notna(median_value):
                df[column] = df[column].fillna(median_value)

    return df