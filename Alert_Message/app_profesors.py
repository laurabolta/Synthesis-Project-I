import streamlit as st
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Panel Profesor", layout="wide")
st.title("Panel del Profesor")

# ---------------------- Cargar IDs desde los CSV ----------------------
carpeta_profesores = "Profesors"
profesor_sheets = {}  # Diccionario: id_anonim -> nombre pestaña

for archivo in os.listdir(carpeta_profesores):
    if archivo.endswith(".csv"):
        df = pd.read_csv(os.path.join(carpeta_profesores, archivo))

        # Renombrar columna si es necesario
        if 'Id Anonim' in df.columns:
            df.rename(columns={'Id Anonim': 'id_anonim'}, inplace=True)
        elif 'Id Anònim' in df.columns:
            df.rename(columns={'Id Anònim': 'id_anonim'}, inplace=True)

        # Asumimos que cada archivo es de un profesor y que su nombre = pestaña en Google Sheet
        nombre_pestanya = os.path.splitext(archivo)[0]
        for id_anonim in df["id_anonim"].dropna().astype(str).unique():
            profesor_sheets[id_anonim] = nombre_pestanya

# ---------------------- Login del profesor ----------------------
user_id = st.text_input("Introduce tu ID de Profesor")

if user_id in profesor_sheets:
    st.success(f"Bienvenido/a Profesor/a {user_id}")
    nombre_pestanya = profesor_sheets[user_id]

    # ------------------ Cargar datos del profesor desde Google Sheets ------------------
    
    def load_profesor_data(sheet_name):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales_google.json", scope)
        client = gspread.authorize(creds)

        sheet = client.open("Notas_Profesores").worksheet(sheet_name)
        data = pd.DataFrame(sheet.get_all_records())
        return data, sheet

    df, sheet = load_profesor_data(nombre_pestanya)

    st.subheader("Editar notas de tus alumnos:")
    edit_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

    if st.button("Guardar cambios"):
        sheet.update([edit_df.columns.values.tolist()] + edit_df.values.tolist())
        st.success("Cambios guardados en Google Sheet")
else:
    st.warning("ID no reconocido.")

