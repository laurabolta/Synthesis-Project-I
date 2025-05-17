import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
import os
import json
# ---------------------- Page config ----------------------
st.set_page_config(page_title="Campus Virtual - Teacher Panel", layout="wide")

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
credenciales = "credenciales_google.json"
base_csv = "base_inicial.csv"
curso_actual = "2024/2025"
csv_central = "estudiants_net.csv"
sheet_map_file = "sheet_map.json" 

if os.path.exists(sheet_map_file):
    with open(sheet_map_file, "r") as f:
        sheet_map = json.load(f)
else:
    sheet_map = {}

def cargar_credenciales():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credenciales, scope)
    return gspread.authorize(creds)

client = cargar_credenciales()

def get_or_create_sheet(client, sheet_name, base_inicial):
    """
    Intenta abrir una Google Sheet con el nombre sheet_name.
    Si no existe, la crea y la inicializa con base_inicial.
    """
    try:
        sheet_file = client.open(sheet_name)
        return sheet_file
    except gspread.exceptions.SpreadsheetNotFound:
        sheet_file = client.create(sheet_name)
        hoja = sheet_file.sheet1
        hoja.update([base_inicial.columns.tolist()] + base_inicial.values.tolist())
        # Opcional: compartir la hoja con tu email o con la cuenta de servicio
        # sheet_file.share('tu-email@dominio.com', perm_type='user', role='writer')
        st.success(f"Google Sheet '{sheet_name}' creada desde base_inicial.csv")
        return sheet_file

def crear_sheet(user_id, base_inicial):
    sheet_name = f"Notas_{user_id}"
    sheet_file = client.create(sheet_name)
    hoja = sheet_file.sheet1
    hoja.update([base_inicial.columns.tolist()] + base_inicial.values.tolist())
    # Guardar ID en map
    sheet_map[user_id] = sheet_file.id
    guardar_map()
    st.success(f"Google Sheet '{sheet_name}' creada desde base_inicial.csv")
    return sheet_file

def guardar_map():
    with open(sheet_map_file, "w") as f:
        json.dump(sheet_map, f)

# ---------------------- Processing ----------------------
st.markdown('<div class="titulo-uab"><h1>Campus Virtual - Teacher Panel</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="uab-subtitle">Welcome to Subject X</div>', unsafe_allow_html=True)

user_id = st.text_input("Enter your teacher ID")

if user_id:
    st.markdown(f"Welcome Teacher: **{user_id}**")
    try:
        base_inicial = pd.read_csv(base_csv, sep=";")
        sheet_file = get_or_create_sheet(user_id, base_inicial)
        sheet = sheet_file.sheet1
        st.info(f"[Open your Google Sheet here]({sheet_file.url})")

        st.subheader("Fill in the marks:")
        edit_df = st.data_editor(base_inicial, use_container_width=True, num_rows="dynamic")

        if st.button("Save changes to your private Google Sheet"):
            try:
                sheet.update([edit_df.columns.values.tolist()] + edit_df.values.tolist())
                st.success("Changes successfully saved to Google Sheet")
                ruta_central = "estudiants_net.csv"
                df_central = pd.read_csv(ruta_central)
                if "nota_parcial" not in df_central.columns:
                    df_central["nota_parcial"] = None

                if "id_anonim" in edit_df.columns and "nota_parcial" in edit_df.columns:
                    df_central["id_anonim"] = df_central["id_anonim"].astype(str)
                    edit_df["id_anonim"] = edit_df["id_anonim"].astype(str)

                    df_actualizado = df_central.merge(edit_df[["id_anonim", "nota_parcial"]], on="id_anonim", how="left")

                    df_actualizado.to_csv(ruta_central, index=False)
                    st.success("Archivo central 'estudiants_net.csv' actualizado con nuevas notas.")
                else:
                    st.warning("No se encontró la columna 'nota_parcial' o 'id_anonim' para actualizar el CSV central.")
            except Exception as e:
                st.error(f"No se pudieron guardar los cambios: {e}")

        # Convert marks columns to numeric safely (handling commas and points)
        try:
            if 'nota_parcial' in edit_df.columns:
                edit_df['nota_parcial'] = edit_df['nota_parcial'].astype(str).str.replace(',', '.').astype(float)

            if 'nota_final' in edit_df.columns:
                edit_df['nota_final'] = edit_df['nota_final'].astype(str).str.replace(',', '.').astype(float)

            # Unified Statistics block
            st.subheader("Class Statistics:")
            stats = {}

            if 'nota_parcial' in edit_df.columns:
                stats['Partial Marks'] = {
                    'Average Mark': edit_df['nota_parcial'].mean(),
                    'Maximum Mark': edit_df['nota_parcial'].max(),
                    'Minimum Mark': edit_df['nota_parcial'].min()
                }

            if 'nota_final' in edit_df.columns:
                stats['Final Marks'] = {
                    'Average Mark': edit_df['nota_final'].mean(),
                    'Maximum Mark': edit_df['nota_final'].max(),
                    'Minimum Mark': edit_df['nota_final'].min()
                }

            for category, values in stats.items():
                st.write(f"**{category}:**")
                for stat_name, stat_value in values.items():
                    st.write(f"- {stat_name}: {stat_value:.2f}")

        except Exception as e:
            st.error(f"Error in statistics: {e}")

    except Exception as e:
        st.error(f"Error loading or creating the sheet: {e}")
    st.subheader("Grades Distribution:")

    # This is just if we want to print one plot. They appeared TOO BIG and I 
    # thought that maybe just putting both side by side would be useful but 
    # this could not be done if we dont have both grades (parcial and final)...

    # I write everything as # as if not, it will appear in the website (even if i used "")

    #try:
        #if 'nota_parcial' in edit_df.columns and not edit_df['nota_parcial'].dropna().empty:
            #fig_parcial, ax = plt.subplots(figsize=(4, 2))  # smaller figure
            #ax.hist(edit_df['nota_parcial'].dropna(), bins=10, edgecolor='black', color='#1f77b4')  # blue
            #ax.set_title("Partial Marks Distribution")
            #ax.set_xlabel("Mark")
            #ax.set_ylabel("Number of Students")
            #st.pyplot(fig_parcial)

        #if 'nota_final' in edit_df.columns and not edit_df['nota_final'].dropna().empty:
            #fig_final, ax = plt.subplots(figsize=(4, 2))  # smaller figure
            #ax.hist(edit_df['nota_final'].dropna(), bins=10, edgecolor='black', color='#ff7f0e')  # orange
            #ax.set_title("Final Marks Distribution")
            #ax.set_xlabel("Mark")
            #ax.set_ylabel("Number of Students")
            #st.pyplot(fig_final)

    try:
        # Create a figure with 1 row and 2 columns
        fig, axes = plt.subplots(1, 2, figsize=(8, 3))  # Small, side-by-side

        # Plot Partial Marks if available
        if 'nota_parcial' in edit_df.columns and not edit_df['nota_parcial'].dropna().empty:
            axes[0].hist(edit_df['nota_parcial'].dropna(), bins=10, edgecolor='black', color="#197100")
            axes[0].set_title("Partial Marks")
            axes[0].set_xlabel("Mark")
            axes[0].set_ylabel("Students")

        # Plot Final Marks if available
        if 'nota_final' in edit_df.columns and not edit_df['nota_final'].dropna().empty:
            axes[1].hist(edit_df['nota_final'].dropna(), bins=10, edgecolor='black', color="#197100")
            axes[1].set_title("Final Marks")
            axes[1].set_xlabel("Mark")
            axes[1].set_ylabel("Students")

        plt.tight_layout()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error generating distribution charts: {e}")
else:
    st.info("Please enter your anonymous Teacher ID to begin.")
# ---------------------- Grade Distribution Histograms ----------------------

