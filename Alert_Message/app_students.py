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
        df = pd.read_csv("alertas_academicas.csv")

        # Ensure numeric conversion
        df["nota_assignatura"] = pd.to_numeric(df["nota_assignatura"], errors='coerce')
        df["predicted_nota_assignatura"] = pd.to_numeric(df["predicted_nota_assignatura"], errors='coerce')

        # Filter by user and grade drop > 2
        data_estudiant = df[df["id_anonim"] == user_id]
        data_dropped = data_estudiant[
            (data_estudiant["predicted_nota_assignatura"] - data_estudiant["nota_assignatura"]) > 2
        ]

        if not data_dropped.empty:
            st.markdown("### Assignatures amb baixada de nota > 2 punts:")
            for _, row in data_dropped.iterrows():
                st.markdown(f'''
                    <div class="uab-subtitle">
                        {row["assignatura"]} — Predicció: <b>{row["predicted_nota_assignatura"]}</b>,
                        Real: <b>{row["nota_assignatura"]}</b>
                    </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No hi ha assignatures amb una baixada de més de 2 punts.")
    except FileNotFoundError:
        st.error("El fitxer alertas_academicas.csv no s'ha trobat.")
    except Exception as e:
        st.error(f"Error carregant dades: {e}")
