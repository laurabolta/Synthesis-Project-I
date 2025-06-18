import streamlit as st
import pandas as pd
import gspread
from datetime import datetime
import base64


# ---------------------- Page config ----------------------
st.set_page_config(page_title="Campus Virtual - Student Panel", layout="wide")

# ---------------------- Background ----------------------
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    background_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

set_background("files/campus.png")

# ---------------------- UAB CV Style ----------------------
st.markdown("""
    <style>
    <style>
        .stApp {
            background-image: url("data:image/png;base64,..."); /* ja el tens configurat */
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white !important;  /* <- això fa que tot el text sigui blanc */
        }
        .titulo-uab {
            background-color: #147d00cc;
            padding: 20px;
            border-radius: 8px;
            border-left: 8px solid #ffffff;
        }
        .titulo-uab h1 {
            margin: 0;
            font-size: 28px;
            color: white;
        }
        .uab-subtitle {
            color: #ffffff;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .uab-box {
            background-color: #ffffff33;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            border-left: 5px solid #00a8cc;
        }
        h2, h3, h4, p, div, span, li {
            color: white !important;
        }
        label {
            color: white !important;
        }
        .stTextInput label {
            color: white !important;
        }
        .stAlert {
            color: white !important;
            background-color: #00a8cc33 !important;
            border-left: 5px solid #ffffff !important;
        }
        h1, h2, h3, h4 {
            color: white !important;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.6);
            font-weight: 700;
        }
    </style>
""", unsafe_allow_html=True)


# ---------------------- Config & Google Sheets ----------------------
csv_estudiants = "Students/estudiants_AI.csv"
credenciales = "files/credenciales_google.json"
tutoria_link = "https://calendly.com/dkaratzas/tutoring?month=2025-05"

# ---------------------- Utilidades ----------------------
def obtener_curs_academic_actual():
    hoy = datetime.today()
    any_actual = hoy.year
    if hoy.month >= 9:  # new course starts in September
        return f"{any_actual}/{str(any_actual+1)[-2:]}"
    else:
        return f"{any_actual-1}/{str(any_actual)[-2:]}"


# ---------------------- Interfaz ----------------------
st.markdown('<div class="titulo-uab"><h1>Campus Virtual - Student Panel</h1></div>', unsafe_allow_html=True)

user_id = st.text_input("Enter your student ID (Alumne)")
if user_id:
    try:
        df = pd.read_csv("files/alertas_academicas.csv")

        # Ensure numeric conversion
        df["nota_assignatura"] = pd.to_numeric(df["nota_assignatura"], errors='coerce')
        df["predicted_nota_assignatura"] = pd.to_numeric(df["predicted_nota_assignatura"], errors='coerce')

        # Filter data for the current user
        data_estudiant = df[df["id_anonim"] == user_id]

        # Detect subjects with issues
        data_problemes = data_estudiant[
            ((data_estudiant["predicted_nota_assignatura"] - data_estudiant["nota_assignatura"]) > 2) |
            (data_estudiant["nota_assignatura"] < 7)
        ]

        if not data_problemes.empty:
            st.markdown("### Subjects with Identified Difficulties")
            for _, row in data_problemes.iterrows():
                assignatura = row["assignatura"]
                prediccio = row["predicted_nota_assignatura"]
                id_assig = assignatura.replace(" ", "_").replace("/", "_")  # Clean-up for file name

                # links
                # to use the exercises of each subject we use this line of code
                # pdf_link = f"/files/ejercicios_{id_assig}.pdf"
                # now we use an example file
                pdf_path = "files/Exercises_example.pdf"
                tutoria_link = "https://calendly.com/dkaratzas/tutoring?month=2025-05"

                st.write(f"#### {assignatura}")
                # st.write(f"**Predicted grade:** {prediccio:.2f}")
                st.write(f"#### There's still time to improve! Try these practice exercises:")

                st.write("##### Practice Exercises")
                try:
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                    st.download_button(
                        label=" Download Practice Exercises PDF",
                        data=pdf_bytes,
                        file_name="Exercises_example.pdf",
                        mime="application/pdf"
                    )
                except FileNotFoundError:
                    st.warning("Practice exercises file not found.")

                st.write("##### Schedule a Tutoring Session with the Teacher")
                st.markdown(f"[Book a tutoring session on Calendly]({tutoria_link})", unsafe_allow_html=False)

                st.markdown("---")
        else:
            st.info("There are currently no subjects with identified difficulties.")
    except FileNotFoundError:
        st.error("The file 'alertas_academicas.csv' was not found.")
    except Exception as e:
        st.error(f"Error loading data: {e}")