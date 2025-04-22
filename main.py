# Import necessary libraries
import csv
from collections import defaultdict
import pandas as pd
import functions

# PATHS TO THE CSV FILES -----------------------------------------------------------------

# Information about students access to the university:
students_success_csv_path = './Students/Estudiants_èxit_accés_anònim.csv'
# Information about moodle activities/deliveries of the students:
moodle_activities_csv_path1 = './Students/ALUMNES_anònim_1.csv'
moodle_activities_csv_path2 = './Students/ALUMNES_anònim_2.csv'
moodle_activities_csv_path3 = './Students/ALUMNES_anònim_3.csv'
moodle_activities_csv_path4 = './Students/ALUMNES_anònim_4.csv'
moodle_activities_csv_path5 = './Students/ALUMNES_anònim_5.csv'
# Information about the marks obtained by students on particular subjects:
student_marks_csv_path = './Students/Estudiants_notes_assignatures_anònim.csv'

# PREPROCESS AND CLEAN DATA -----------------------------------------------------------------

# Read data as a pandas DataFrame
df_students_marks = pd.read_csv(student_marks_csv_path)
main_df = pd.read_csv(students_success_csv_path, encoding='utf-8')

# Visualize some information about our data
print("\nDataFrame info (without cleaning):")
print("--------------------------------------")
print(main_df.head())
print(main_df.info())
print("--------------------------------------")

# Standardize names of the columns
functions.clean_df_columns(df_students_marks)
functions.clean_df_columns(main_df)

# Clean text strings entries in the columns
df_students_marks = functions.clean_text_strings(df_students_marks)
main_df = functions.clean_text_strings(main_df) 

# Convert numerical entries to numbers and formate them properly:
# Entry grades
if "nota_d_acces_preinscripcio" in main_df.columns:
    main_df["nota_d_acces_preinscripcio"] = (
        main_df["nota_d_acces_preinscripcio"]
        .astype(str) #ensure it is formated as a string
        .str.replace(',', '.', regex=False)
        .str.extract(r'([\d.]+)')[0]
        .astype(float)
    )

# Change success rate percentage into a numerical value
if "taxa_exit" in main_df.columns:
    main_df["taxa_exit"] = (
        main_df["taxa_exit"]
          .str.replace('%', '', regex=False)
          .str.extract(r'([\d.]+)')[0]
          .astype(float)
    )

# HANDLE MISSING DATA, 2 OPTIONS:

# 1. Fill missing data with 'Desconegut'
df_students_marks = functions.handle_missing_data(df_students_marks)
main_df = functions.handle_missing_data(main_df)

#2. Remove rows which lack information (contain the word 'Desconegut' in some of the fields)
#df = df.dropna(subset=["estudi", "curs_academic", "sexe", "curs_academic_acces_estudi", "nota_d_acces_preinscripcio", "taxa_exit"])
#df = df[~df["sexe"].isin(["Desconegut", "No especificat"])]

# Remove duplicate rows
main_df = main_df.drop_duplicates()

# Store clean DataFrame
main_df.to_csv("student_data_UNLABELLED.csv", index=False, encoding='utf-8')

print("\nClean DataFrame info:")
print("--------------------------------------")
print(main_df.head())
print(main_df.info())
print("--------------------------------------")

# MODIFY THIS TO TAKE INTO ACCOUNT MARKS INSTEAD OF TAXA EXIT!
"""
# Add a column, 'risk_factor' taking into account 'taxa_exit'
df["risk_factor"] = df["taxa_exit"].apply(lambda x: "Yes" if pd.notnull(x) and x < 50 else "No")

# Save labelled dataframe
df.to_csv("student_data_LABELLED.csv", index=False, encoding='utf-8')

print("\nColumna 'risk_factor' añadida:")
print(df[["taxa_exit", "risk_factor"]].head())
"""