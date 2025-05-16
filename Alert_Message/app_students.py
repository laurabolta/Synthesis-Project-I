import streamlit as st
import pandas as pd
import gspread
from datetime import datetime

# ---------------------- Page config ----------------------
st.set_page_config(page_title="Campus Virtual - Student Panel", layout="wide")

# ---------------------- UAB CV Style ----------------------
st.markdown("""
    <style>
        .titulo-uab {
            background-color: #f1f1f1;
            padding: 20px;
            border-radius: 8px;
            border-left: 8px solid #00703c;
        }
        .titulo-uab h1 {
            margin: 0;
            font-size: 28px;
            color: #333333;
        }
        .uab-subtitle {
            color: #00703c;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .uab-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Config & Google Sheets ----------------------
csv_estudiants = "estudiants_AI.csv"
credenciales = "credenciales_google.json"


# ---------------------- Utilidades ----------------------
def obtener_curs_academic_actual():
    hoy = datetime.today()
    any_actual = hoy.year
    if hoy.month >= 9:  # nuevo curso empieza en septiembre
        return f"{any_actual}/{str(any_actual+1)[-2:]}"
    else:
        return f"{any_actual-1}/{str(any_actual)[-2:]}"


# ---------------------- Interfaz ----------------------
st.markdown('<div class="titulo-uab"><h1>Campus Virtual - Student Panel</h1></div>', unsafe_allow_html=True)

user_id = st.text_input("Enter your student ID (Alumne)")

if user_id:
    try:
        df = pd.read_csv("Students/estudiants_AI.csv", dtype=str)
        curs_actual = obtener_curs_academic_actual()

        # Filtrar por el estudiante y el curso actual
        data_estudiant = df[(df["Alumne"] == user_id.upper()) & (df["Curs acadèmic"] == curs_actual)]

        if not data_estudiant.empty:
            estudi = data_estudiant.iloc[0]["Assignatura"]
            st.markdown("###  Assignatures cursades:")

            for _, row in data_estudiant.iterrows():
                st.markdown(f'<div class="uab-subtitle"> {row["Assignatura"]} — Nota: <b>{row["Nota_assignatura"]}</b></div>', unsafe_allow_html=True)
        else:
            st.warning(f"No s’han trobat assignatures per a l’alumne <b>{user_id}</b> al curs <b>{curs_actual}</b>.", icon="⚠️")

    except FileNotFoundError:
        st.error("El fitxer estudiants_AI.csv no s'ha trobat.")
    except Exception as e:
        st.error(f"Error carregant dades: {e}")
