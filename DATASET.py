# Import necessary libraries
import pandas as pd
from Preparing_Data import functions
# PATHS TO THE CSV FILES -----------------------------------------------------------------

student_success_csv_path = './Students/Estudiants_èxit_accés_anònim.csv'
student_marks_csv_path = './Students/Estudiants_notes_assignatures_anònim.csv'
student_abandonment_csv_path = './Students/Estudiants_abandonament_anònim.csv'

# LOAD DATA -----------------------------------------------------------------

background_df = pd.read_csv(student_success_csv_path)
grades_df = pd.read_csv(student_marks_csv_path)
abandonment_df = pd.read_csv(student_abandonment_csv_path)

# Preprocess Background Data -----------------------------------------------------------------

# Choose relevant background features
background_features = [
    'Id Anonim',
    'Via Accés Estudi',
    'Nota d\'accés (preinscripció)',
    'Dedicació de l\'estudiant',
    'S/N Discapacitat',
    'Beca Concedida?',
    'Estudis Mare',
    'Estudis Pare',
    'Taxa èxit',   
]

background_df = background_df[background_features]

# Rename for simplicity
background_df.rename(columns={'Nota d\'accés (preinscripció)': 'Nota d\'accés'}, inplace=True)
background_df.rename(columns={'S/N Discapacitat': 'Discapacitat'}, inplace=True)
# Preprocess Grades Data -----------------------------------------------------------------

# Rename columns with students ids for the name to match
grades_df.rename(columns={'Alumne': 'Id Anonim'}, inplace=True)
# Ensure grades are numeric
grades_df['Nota_assignatura'] = pd.to_numeric(grades_df['Nota_assignatura'], errors='coerce')

# Preprocess Abandonment Data -----------------------------------------------------------------

# Choose relevant abandonment features
abandonment_features = [
    'Id Anonim',
    'Nombre Abandonaments Universitat Reals'
]

# Keep only relevant features
abandonment_df = abandonment_df[abandonment_features]
# Replace name for simplicity
abandonment_df.rename(columns={'Nombre Abandonaments Universitat Reals': 'Abandonament'}, inplace=True)

# MERGE THE DATA -----------------------------------------------------------------

# First, merge background info with grades
merged_df = grades_df.merge(background_df, on='Id Anonim', how='left')

# Then, merge abandonment info
merged_df = merged_df.merge(abandonment_df, on='Id Anonim', how='left')

# Visualize merged dataframe
print(merged_df.head())
print(f"Number of entries: {len(merged_df)}")
print("--------------------------------------")
# Visualize features present in our dataset
print(merged_df.columns)
print("--------------------------------------")
# Visualize an example of an entry in our dataset
print(merged_df.iloc[10])
print("--------------------------------------")

# PREPROCESS AND CLEAN DATA -----------------------------------------------------------------

# Search for missing values
print('Missing values per column:\n', merged_df.isnull().sum()) # there aren't any missing values 
print("--------------------------------------")

clean_df = functions.load_and_clean_data(merged_df)
clean_df = clean_df.drop_duplicates()

# Guarda en CSV si lo necesitas
clean_df.to_csv("DATASET.csv", index=False)

# Visualize an example of an entry in our dataset
print(clean_df.iloc[10])
