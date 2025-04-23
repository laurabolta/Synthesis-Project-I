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

# Read moodle activities of Engineria informatica
# Read the CSV files and filter the data

asignaturas_informatica = [
    "Àlgebra",
    "Fonaments d'Informàtica",
    "Electricitat i Electrònica",
    "Fonaments d'Enginyeria",
    "Càlcul",
    "Organització i Gestió d'Empreses",
    "Fonaments dels Computadors",
    "Metodologia de la Programació",
    "Matemàtica Discreta",
    "Estadística",
    "Estructura de Computadors",
    "Sistemes Operatius",
    "Laboratori de Programació",
    "Bases de Dades",
    "Arquitectura de Computadors",
    "Xarxes",
    "Intel·ligència Artificial",
    "Enginyeria del Software",
    "Informació i Seguretat",
    "Tecnologies de Desenvolupament per a Internet i Web",
    "Ètica per a l'Enginyeria",
    "Legislació",
    "Disseny de Software",
    "Requisits del Software",
    "Gestió i Administració de Bases de Dades",
    "Test i Qualitat del Software",
    "Gestió del Desenvolupament del Software",
    "Models de Qualitat en la Gestió de les TIC",
    "Arquitectura i Tecnologies de Software",
    "Laboratori Integrat de Software",
    "Sistemes Distribuïts",
    "Sistemes Encastats",
    "Gestió i Administració de Xarxes",
    "Arquitectures Avançades",
    "Microprocessadors i Perifèrics",
    "Computació d'Altes Prestacions",
    "Integració Hardware / Software",
    "Prototipatge de Sistemes Encastats",
    "Anàlisi i Disseny d'Algorismes",
    "Coneixement, Raonament i Incertesa",
    "Aprenentatge Computacional",
    "Visualització Gràfica Interactiva",
    "Compiladors",
    "Visió per Computador",
    "Robòtica, Llenguatge i Planificació",
    "Sistemes Multimèdia",
    "Fonaments de Tecnologia de la Informació",
    "Sistemes d'Informació",
    "Disseny del Software",
    "Infraestructura i Tecnologia de Xarxes",
    "Tecnologies Avançades d'Internet",
    "Sistemes i Tecnologies Web",
    "Garantia de la Informació i Seguretat",
    "Direcció de les TIC",
    "Tècniques de Gestió Empresarial",
    "Laboratori de Sistemes de la Informació",
    "Solucions TIC Estandaritzades",
    "Gestió de Projectes",
    "Treball de Final de Grau",
    "Anglès Professional I",
    "Anglès Professional II",
    "Tendències Actuals",
    "Aplicacions de la Teoria de Codis (1)",
    "Internet de les Coses",
    "Tecnologia Blockchain i Criptomonedes (1)",
    "Tecnologies de Compressió de la Informació (1)"
]

def read_filtered_moodle_csv(path, source_name):
    use_columns = [
        "Assignatura",
        "Id Anonim",
        "Nota",
        "Nota numèrica (Mitjana)",
        "Nota numèrica ponderada (Mitjana)",
        "Tasca_lliurada",
        "Tasca_pendents"
    ]

    # Normaliza nombres de asignaturas para comparación más robusta
    asignaturas_normalizadas = [a.lower().strip() for a in asignaturas_informatica]

    # Lista donde guardaremos los trozos que sí nos interesan
    chunks_filtrados = []

    # Leer el archivo en partes
    for chunk in pd.read_csv(path, skiprows=4, sep=';', encoding='utf-8', usecols=use_columns, chunksize=10000):
        chunk.columns = chunk.columns.str.strip().str.lower()
        chunk["assignatura"] = chunk["assignatura"].str.strip().str.lower()
        chunk_filtrado = chunk[chunk["assignatura"].isin(asignaturas_normalizadas)]
        chunk_filtrado["source_file"] = source_name
        if not chunk_filtrado.empty:
            chunks_filtrados.append(chunk_filtrado)

    df_resultado = pd.concat(chunks_filtrados, ignore_index=True)
    return df_resultado

moodle_paths = [
    (moodle_activities_csv_path1, "ALUMNES_anònim_1"),
    (moodle_activities_csv_path2, "ALUMNES_anònim_2"),
    (moodle_activities_csv_path3, "ALUMNES_anònim_3"),
    (moodle_activities_csv_path4, "ALUMNES_anònim_4"),
    (moodle_activities_csv_path5, "ALUMNES_anònim_5")
]

moodle_dfs = [read_filtered_moodle_csv(path, name) for path, name in moodle_paths]
df_moodle_activities = pd.concat(moodle_dfs, ignore_index=True)
print(df_moodle_activities.head())

""""
# Read moodle activities data
def read_moodle_csv(path, source_name):
    use_columns = [
        "Assignatura",
        "Id Anonim",
        "Nota",
        "Nota numèrica (Mitjana)",
        "Nota numèrica ponderada (Mitjana)",
        "Tasca_lliurada",
        "Tasca_pendents"
    ]
    df = pd.read_csv(path, skiprows=4, sep=';', encoding='utf-8', usecols=use_columns, nrows=50)
    df["source_file"] = source_name  # Añadir columna indicando el origen
    df.columns = df.columns.str.strip().str.lower()
    return df

moodle_paths = [
    (moodle_activities_csv_path1, "ALUMNES_anònim_1"),
    (moodle_activities_csv_path2, "ALUMNES_anònim_2"),
    (moodle_activities_csv_path3, "ALUMNES_anònim_3"),
    (moodle_activities_csv_path4, "ALUMNES_anònim_4"),
    (moodle_activities_csv_path5, "ALUMNES_anònim_5")
]

moodle_dfs = [read_moodle_csv(path, name) for path, name in moodle_paths]
df_moodle_activities = pd.concat(moodle_dfs, ignore_index=True)

# Limpieza básica si es necesario
functions.clean_df_columns(df_moodle_activities)
df_moodle_activities = functions.clean_text_strings(df_moodle_activities)
df_moodle_activities = functions.handle_missing_data(df_moodle_activities)
"""

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


# 1. Fill missing data with 'Desconegut'
df_students_marks = functions.handle_missing_data(df_students_marks)
main_df = functions.handle_missing_data(main_df)


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


