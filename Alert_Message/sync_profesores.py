import sqlite3
import pandas as pd

# Leer archivo Excel actualizado por el profesor
df_prof = pd.read_excel("datos_profesores.xlsx")

# Validar columnas necesarias
required_columns = {"id_anonim", "assignatura", "nota_assignatura"}
if not required_columns.issubset(df_prof.columns):
    raise ValueError("El archivo Excel no contiene las columnas requeridas.")

# Conectar a la base de datos y guardar en tabla 'profesores_notas'
conn = sqlite3.connect("database.db")
df_prof.to_sql("profesores_notas", conn, if_exists="replace", index=False)
conn.close()

print("Datos de profesores sincronizados en la base de datos.")