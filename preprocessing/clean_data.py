import pandas as pd


def clean_dataframe(df):
    print("MISSING VALUES")
    print(df.isnull().sum())

    for column in df.columns:
        if df[column].dtype == "object":
            df[column] = df[column].fillna("Unknown")
        else:
            df[column] = df[column].fillna(df[column].median())

    return df