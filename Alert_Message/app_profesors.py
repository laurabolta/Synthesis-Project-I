import streamlit as st
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Panel Profesor", layout="wide")
st.title("Panel del Profesor")

# ---------------------- Cargar IDs desde los CSV ----------------------
carpeta_profesores = "Profesors"
profesor_sheets = {}

def detectar_delimitador(ruta_csv):
    with open(ruta_csv, 'r', encoding='utf-8') as archivo:
        primera_linea = archivo.readline()
        return ',' if primera_linea.count(',') > primera_linea.count(';') else ';'

for archivo in os.listdir(carpeta_profesores):
    if archivo.endswith(".csv"):
        ruta_csv = os.path.join(carpeta_profesores, archivo)
        sep = detectar_delimitador(ruta_csv)
        df = pd.read_csv(ruta_csv, sep=sep)

        # Normalizar nombres de columna
        df.columns = df.columns.str.strip().str.lower()

        for col in df.columns:
            if col in ["id anonim", "id anònim", "id_anònim"]:
                df.rename(columns={col: "id_anonim"}, inplace=True)

        if "id_anonim" in df.columns and "assignatura" in df.columns:
            for _, fila in df.iterrows():
                id_profe = str(fila["id_anonim"])
                nombre_pestanya = str(fila["assignatura"]).strip()

                # Añadir al diccionario si no está
                if id_profe not in profesor_sheets:
                    profesor_sheets[id_profe] = nombre_pestanya

# ---------------------- Asociar IDs a pestañas de Google Sheet ----------------------

# ---------------------- Login del profesor ----------------------
user_id = st.text_input("Introduce tu ID de Profesor")

if user_id in profesor_sheets:
    st.success(f"Bienvenido/a Profesor/a {user_id}")
    nombre_pestanya = profesor_sheets[user_id]

    # ------------------ Cargar datos desde Google Sheets ------------------
    def load_profesor_data(sheet_name):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales_google.json", scope)
        client = gspread.authorize(creds)

        try:
            sheet = client.open("Notas_Profesores").worksheet(sheet_name)
            data = pd.DataFrame(sheet.get_all_records())
            return data, sheet
        except Exception as e:
            st.error(f"Error al cargar la hoja: {e}")
            return None, None

    df, sheet = load_profesor_data(nombre_pestanya)

    if df is not None:
        st.subheader("Editar notas de tus alumnos:")
        edit_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

        if st.button("Guardar cambios"):
            try:
                sheet.update([edit_df.columns.values.tolist()] + edit_df.values.tolist())
                st.success("Cambios guardados en Google Sheet")
            except Exception as e:
                st.error(f"No se pudieron guardar los cambios: {e}")
else:
    if user_id:
        st.warning("ID no reconocido o no asignado a una pestaña de Google Sheet.")
