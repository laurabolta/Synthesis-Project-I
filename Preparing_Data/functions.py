import csv
from collections import defaultdict
import pandas as pd

# FUCNTIONS TO PREPROCESS AND CLEAN DATA -----------------------------------------------------------------

# Clean and standardize the names of columns
def clean_df_columns(df):
    df.columns = (
        df.columns.str.strip()                 # remove white spaces
                .str.lower()                 # conver to lowercase
                .str.replace('à', 'a')       # normalize accents
                .str.replace('è', 'e')
                .str.replace('é', 'e')
                .str.replace('í', 'i')
                .str.replace('ó', 'o')
                .str.replace('ú', 'u')
                .str.replace('ç', 'c')
                .str.replace(r"[^a-z0-9_]+", "_", regex=True)  # replace symbols by '-'
                .str.strip('_')                                
    )

# Clean text strings entries in the columns
def clean_text_strings(df):
    text_cols = df.select_dtypes(include='object').columns

    for col in text_cols:
        df[col] = (
            df[col].astype(str)
                .str.strip()
                .str.lower()
                .str.title()
        )
    
    return df

# Fill missing data with 'Desconegut'
def handle_missing_data(df):
    text_cols = df.select_dtypes(include='object').columns

    for col in text_cols:
        df[col] = df[col].fillna("Desconegut")

    return df