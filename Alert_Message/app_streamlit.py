import streamlit as st
import pandas as pd


# Cargar las alertas
df = pd.read_csv('alertas_academicas.csv')

st.title("📊 Alertas Académicas de Predicción")
st.write("Este panel muestra asignaturas con riesgo de suspenso según el modelo.")

# Selección por estudiante
ids = df['id_anonim'].unique()
selected_id = st.selectbox("Selecciona un estudiante:", ids)

# Mostrar alertas del estudiante
df_alumno = df[df['id_anonim'] == selected_id]
st.subheader(f"Asignaturas con alerta para el estudiante {selected_id}")
st.dataframe(df_alumno[['assignatura', 'predicted_nota_assignatura', 'nota_assignatura']])


# ---------------------------
# Conectar a la base de datos
# --------------------------
import sqlite3

conn = sqlite3.connect("database.db")

st.title("📚 Alertas Académicas")

# Leer los datos
df = pd.read_sql("SELECT * FROM alertas", conn)

# Selección de alumno
alumnos = df['id_anonim'].unique()
alumno = st.selectbox("Selecciona un alumno:", alumnos)

# Mostrar resultados
df_alumno = df[df['id_anonim'] == alumno]
st.write(f"Alertas para el alumno `{alumno}`:")
st.dataframe(df_alumno)

conn.close()

#---------
# Estilo CSS
#---------

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")



