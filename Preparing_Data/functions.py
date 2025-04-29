import csv
from collections import defaultdict
import pandas as pd
import re

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
                .str.capitalize()
        )
    
    return df

# Convert necessary columns to numerical values
def to_number(df, col_name):
    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
    return df

# Convert percentage values into numerical values, float (decimals)
def convert_percentages_to_decimal(df, column_name):

    df[column_name] = (
        df[column_name]
        .astype(str)  # Ensure all entries are strings
        .str.strip()  # Remove any surrounding whitespace
        .str.replace('%', '')  # Remove the percent sign
        .astype(float) / 100  # Convert to float and divide by 100
    )
    
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

    return df

def load_and_clean_data(merged_df):
    # Standardize names of the columns
    clean_df_columns(merged_df)

    # Clean text strings entries in the columns
    merged_df = clean_text_strings(merged_df)

    # Convert necessary columns to numerical values
    merged_df = to_number(merged_df, 'abandonament')

    # Convert percentages to numerical values
    merged_df = convert_percentages_to_decimal(merged_df, 'taxa_exit')
    
    return merged_df
