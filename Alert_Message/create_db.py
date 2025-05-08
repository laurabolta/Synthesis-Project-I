import sqlite3
import pandas as pd

# Cargar el CSV con alertas generadas
df = pd.read_csv("alertas_academicas.csv")  # Asegúrate de que el archivo esté en la misma carpeta

# Conectar a SQLite y guardar el DataFrame en la tabla 'alertas'
conn = sqlite3.connect("database.db")
df.to_sql("alertas", conn, if_exists="replace", index=False)
conn.close()

print("Base de datos actualizada con datos de 'clean_df.csv'")