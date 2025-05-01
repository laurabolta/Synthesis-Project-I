import csv
from collections import defaultdict
import pandas as pd
import re
import numpy as np

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

# Convert the dataframe into numerical values
def df_to_numerical(df):
    df = df.copy()

    # CONVERT 'estudi' TO NUMERICAL VALUES
    df['estudi'] = df['estudi'].map({'Graduat en intel·ligència artificial / artificial intelligence': 0, 'Graduat en enginyeria informàtica': 1})

    # CONVERT 'sexe' TO NUMERICAL VALUES
    df['sexe'] = df['sexe'].map({'Home': 0, 'Dona': 1})

    # CONVERT 'curs_academic' TO NUMERICAL VALUES
    df['curs_academic'] = df['curs_academic'].map({'2020/21': 0, '2021/22': 1, '2022/23': 2, '2023/24': 3, '2024/25': 4})

    # CONVERT 'via_acces_estudi' TO NUMERICAL VALUES
    df['via_acces_estudi'] = df['via_acces_estudi'].map({
        'Batx. / cou amb pau': 0,                       # Traditional route via high school + PAU
        'Universitaris batx. / cou amb pau': 1,          # University entrance via high school + PAU
        'Fp2, cfgs': 2,                                 # Vocational training (FP2)
        'Universitaris fp2 / cfgs': 3,                  # University entrance via vocational training (FP2)
        'Majors de 25 anys': 4,                         # Age-based access (over 25)
        'Diplomat, llicenciat': 5,                      # University degree holders
        'Majors de 40 anys amb experiencia laboral': 6,  # Age-based access with work experience (over 40)
        'Sense assignar': 7                             # Unassigned, missing data (could be treated as NaN or specific category)
    })

    df['via_acces_estudi'] = df['via_acces_estudi']
                                           
    # CONVERT 'dedicacio_de_l_estudiant' TO NUMERICAL VALUES
    df['dedicacio_de_l_estudiant'] = df['dedicacio_de_l_estudiant'].map({'Temps complet': 0, 'Temps variable': 1, 'Sense assignar': 2, 'Temps parcial': 3})

    # CONVERT 'discapacitat' TO NUMERICAL VALUES
    df['discapacitat'] = df['discapacitat'].map({'N': 0, '\'-2': 1, 'S': 2})

    # CONVERT 'beca_concedida' TO NUMERICAL VALUES
    df['beca_concedida'] = df['beca_concedida'].map({'Sí': 0, 'No': 1})

    # CONVERT 'estudis_mare' and 'estudis_pare' TO NUMERICAL VALUES
    education_order = {
        'Sense estudis': 0,
        'Estudis primaris': 1,
        "Primera etapa d'educació secundària i similar (eso, egb)": 2,
        'Egb o fp 1er grau': 3,
        'Cicles formatius de grau mitjà i similars (formació professional de primer grau)': 4,
        'Batxillerat': 5,
        'Batxillerat o fp 2n grau': 6,
        'Cicles formatius de grau superior i similars (formació professional de segon grau)': 7,
        'Diplomat o enginyer tèc.': 8,
        'Graus universitaris o diplomatures universitàries': 9,
        'Màsters o antigues llicenciatures': 10,
        'Doctorat universitari': 11,
        'Altres / ns / nc': -1,
        'Sense assignar': -2
    }
    df['estudis_mare'] = df['estudis_mare'].map(education_order)
    df['estudis_pare'] = df['estudis_pare'].map(education_order)

    missing_values = df.isnull().sum().sum()

    if missing_values == 0:
        print("Numerical DataFrame created with no missing values!\n")
    else:
        print(f"Warning: There are {missing_values} missing values in the DataFrame.")


    # Replace each subject code with the average mark or grade of students in that subject
    subject_means = df.groupby('codi_assignatura')['nota_assignatura'].mean().to_dict()
    df['dificultat_assignatura'] = df['codi_assignatura'].map(subject_means)

    # DROP NON-RELEVANT FEATURES
    df = df.drop(columns=['assignatura', 'id_anonim', 'codi_assignatura'])

    return df