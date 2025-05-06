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