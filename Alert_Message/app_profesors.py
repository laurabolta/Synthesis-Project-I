import streamlit as st
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---------------------- Configuración de la página ----------------------
st.set_page_config(page_title="Panel Profesor", layout="wide")
st.title("Panel del Profesor")

# ---------------------- Configuración y utilidades ----------------------
carpeta_profesores = "Profesors"
base_csv = "base_inicial.csv"
credenciales = "credenciales_google.json"

# Función para detectar el delimitador (coma o punto y coma)
def detectar_delimitador(ruta_csv):
    with open(ruta_csv, 'r', encoding='utf-8') as archivo:
        primera_linea = archivo.readline()
        return ',' if primera_linea.count(',') > primera_linea.count(';') else ';'

# Función para cargar credenciales y autorizar con Google Sheets
def cargar_credenciales():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credenciales, scope)
    return gspread.authorize(creds)

client = cargar_credenciales()

# ---------------------- Cargar IDs desde los CSVs ----------------------
ids_unicos = set()

# Recorre los CSVs en la carpeta de profesores
for archivo in os.listdir(carpeta_profesores):
    if archivo.endswith(".csv"):
        ruta_csv = os.path.join(carpeta_profesores, archivo)
        sep = detectar_delimitador(ruta_csv)
        df = pd.read_csv(ruta_csv, sep=sep)
        df.columns = df.columns.str.strip().str.lower()

        # Renombrar columna a 'id_anonim'
        for col in df.columns:
            if col in ["id anonim pd", "id anònim pd", "id_anònim_pd", "id_anonim pd", "id_anonim"]:
                df.rename(columns={col: "id_anonim"}, inplace=True)

        # Si la columna 'id_anonim' existe, agrega los ID únicos
        if "id_anonim" in df.columns:
            ids_unicos.update(df["id_anonim"].dropna().astype(str).unique())

# ---------------------- Crear libros si no existen ----------------------
base_inicial = pd.read_csv(base_csv, sep=";")  # Asegúrate de usar el delimitador correcto
valores = [base_inicial.columns.tolist()] + base_inicial.values.tolist()

# Crear o acceder a los libros de Google Sheets para cada profesor
for id_profesor in ids_unicos:
    try:
        nombre_libro = f"Notas_{id_profesor}"  # Nombre del libro basado en el ID del profesor
        
        # Evitar duplicados: si el libro ya existe, solo lo abre
        try:
            client.open(nombre_libro)
        except:
            # Si no existe, crea uno nuevo
            nuevo_libro = client.create(nombre_libro)
            hoja = nuevo_libro.sheet1
            hoja.update(valores)  # Actualizar la hoja con los valores iniciales
            st.success(f"✅ Hoja creada para el profesor {id_profesor}")
    except Exception as e:
        st.warning(f"No se pudo crear o acceder a la hoja para {id_profesor}: {e}")

# ---------------------- Interfaz para el profesor ----------------------
user_id = st.text_input("Introduce tu ID de Profesor")

# Si el ID del profesor es reconocido, mostrar la interfaz de edición
if user_id in ids_unicos:
    st.success(f"Bienvenido/a Profesor/a {user_id}")
    
    # Función para cargar los datos de la hoja de Google Sheets del profesor
    def load_profesor_data(book_name):
        try:
            sheet = client.open(book_name).sheet1
            data = pd.DataFrame(sheet.get_all_records())
            return data, sheet
        except Exception as e:
            st.error(f"Error al cargar la hoja: {e}")
            return None, None

    sheet_name = f"Notas_{user_id}"
    df, sheet = load_profesor_data(sheet_name)

    if df is not None:
        st.subheader("Editar notas de tus alumnos:")
        # Mostrar la tabla para que el profesor edite las notas
        edit_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

        if st.button("Guardar cambios"):
            try:
                # Actualizar la hoja de Google Sheets con los cambios
                sheet.update([edit_df.columns.values.tolist()] + edit_df.values.tolist())
                st.success("Cambios guardados en Google Sheet")
            except Exception as e:
                st.error(f"No se pudieron guardar los cambios: {e}")
else:
    if user_id:
        st.warning("ID no reconocido o no asignado a ninguna hoja.")