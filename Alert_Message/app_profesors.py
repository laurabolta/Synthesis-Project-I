import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
import os
import json
from googleapiclient.discovery import build
from datetime import datetime
import base64

# ---------------------- Page config ----------------------
st.set_page_config(page_title="Campus Virtual - Teacher Panel", layout="wide")


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
            background-color: #ffffffcc;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            border-left: 5px solid #00a8cc;
        }
        h2, h3, h4 {
            color: white !important;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.6);
            font-weight: 700;
        }
        .stButton>button {
            background-color: #00a8cc;
            color: white;
            border-radius: 8px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #147d00;
        }
        .stTextInput>div>div>input {
            background-color: #ffffffdd;
            border: 1px solid #00a8cc;
            color: #147d00;
        }
        .stMarkdown, .stAlert, .stTextInput label {
            color: white !important;
        }
        .stAlert {
            color: white !important;
            background-color: #00a8cc33 !important;  /* fons turquesa translúcid */
            border-left: 5px solid #ffffff !important;  /* borde blanc */
        }
    </style>
""", unsafe_allow_html=True)


# ---------------------- Config & Google Sheets ----------------------
#https://drive.google.com/drive/u/0/folders/1yu3K29KFCNh0hPv5vDnnDJNdAJULkvzv

credenciales = "files/credenciales_google.json"
base_csv = "files/base_inicial.csv"
curso_actual = "2024/2025"
csv_central = "files/estudiants_net.csv"
sheet_map_file = "files/sheet_map.json"
FOLDER_ID = "1yu3K29KFCNh0hPv5vDnnDJNdAJULkvzv"  #folder in our drive shared


if os.path.exists(sheet_map_file):
    with open(sheet_map_file, "r") as f:
        sheet_map = json.load(f)
else:
    sheet_map = {}

def cargar_credenciales():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credenciales, scope)
    client = gspread.authorize(creds)
    return client, creds

client, creds = cargar_credenciales()


def get_or_create_sheet(user_id, base_inicial):
    sheet_name = f"Notas_{user_id}"
    try:
        return client.open(sheet_name)
    except gspread.SpreadsheetNotFound:
        # if doesn't exist, create a new sheet 
        return crear_sheet(user_id, base_inicial)

def crear_sheet(user_id, base_inicial):
    sheet_name = f"Notas_{user_id}"
    sheet_file = client.create(sheet_name, folder_id=FOLDER_ID)
    hoja = sheet_file.sheet1
    hoja.update([base_inicial.columns.tolist()] + base_inicial.values.tolist())
    # share with anyone that has the link (you can adjust the acces permissions) 
    sheet_file.share(None, perm_type='anyone', role='writer')
    # save ID for future references 
    sheet_map[user_id] = sheet_file.id
    guardar_map()
    st.success(f"Google Sheet '{sheet_name}' creada desde base_inicial.csv y guardada en el folder.")
    return sheet_file

def guardar_map():
    with open(sheet_map_file, "w") as f:
        json.dump(sheet_map, f)

def is_alert_active(alert_row):
    # Check if alert is for today
    now = datetime.now()
    alert_date = datetime.strptime(alert_row["Date"], "%d/%m/%Y").date()
    if alert_date != now.date():
        return False

    # Check if current time is within class time
    start_time = datetime.strptime(alert_row["AlertTime"], "%H:%M")
    end_time = datetime.strptime(alert_row["EndTime"], "%H:%M")

    return start_time.time() <= now.time() <= end_time.time()



# ---------------------- Processing ----------------------
st.markdown('<div class="titulo-uab"><h1>Campus Virtual - Teacher Panel</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="uab-subtitle">Welcome to Subject X</div>', unsafe_allow_html=True)

user_id = st.text_input("Enter your teacher ID")
if user_id:
    st.markdown(f"Welcome Teacher: **{user_id}**")
    try:
        # Load alerts for this professor
        if os.path.exists("files/co2_alerts_log.csv"):
            all_alerts = pd.read_csv("files/co2_alerts_log.csv")
            user_alerts = all_alerts[all_alerts["ProfessorID"] == user_id]
            active_alerts = user_alerts[user_alerts.apply(is_alert_active, axis=1)]

            if not active_alerts.empty:
                st.subheader("URGENT: CO₂ Alerts for your Classes:")
                st.dataframe(active_alerts)
                st.markdown("""
                    <div style="
                        background-color: rgba(204, 0, 0, 0.8);  /* red with 80 opacity */
                        color: #ffffff;
                        padding: 15px;
                        border-radius: 5px;
                        border: 1px solid rgba(153, 0, 0, 0.9);
                        font-weight: 600;
                        ">
                        <h3>Recommended Actions to reduce CO₂ levels:</h3>
                        <ul>
                            <li><b>Ventilate</b> the classroom (open windows/doors)</li>
                            <li><b>Reduce occupancy</b> if possible</li>
                            <li><b>Continue monitoring</b> air quality with sensors</li>
                            <li>Consider taking short breaks to allow air renewal</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No CO₂ alerts recorded for your sessions.")
        else:
            st.info("No alert log found.")

        base_inicial = pd.read_csv(base_csv, sep=";")
        sheet_file = get_or_create_sheet(user_id, base_inicial)
        sheet = sheet_file.sheet1

        st.info(f"[Open your Google Sheet here]({sheet_file.url})")        
        st.subheader("Fill in the marks:")

        # Read actual data on the paper_sheet 
        data_from_sheet = sheet.get_all_values()
        edit_df = pd.DataFrame(data_from_sheet[1:], columns=data_from_sheet[0])  # exclude header duplicate

        # convert numeric columns
        for col in ["nota_parcial", "nota_final"]:
            if col in edit_df.columns:
                edit_df[col] = edit_df[col].astype(str).str.replace(",", ".").astype(float)

        st.data_editor(edit_df, use_container_width=True, num_rows="dynamic")

        if st.button(" Shared with Admin"):
            try:
                drive_service = build("drive", "v3", credentials=creds)
                file_id = sheet_file.id
                drive_service.files().update(
                    fileId=file_id,
                    addParents=FOLDER_ID,
                    removeParents='root',
                    fields='id, parents'
                ).execute()
                st.success("Hoja movida exitosamente a la carpeta del admin.")
            except Exception as e:
                st.error(f"Error al mover la hoja: {e}")

        if st.button("Save changes to your private Google Sheet"):
            try:
                sheet.update([edit_df.columns.values.tolist()] + edit_df.values.tolist())
                st.success("Changes successfully saved to Google Sheet")
                ruta_central = "files/estudiants_net.csv"
                df_central = pd.read_csv(ruta_central)
                if "nota_parcial" not in df_central.columns:
                    df_central["nota_parcial"] = None

                if "id_anonim" in edit_df.columns and "nota_parcial" in edit_df.columns:
                    df_central["id_anonim"] = df_central["id_anonim"].astype(str)
                    edit_df["id_anonim"] = edit_df["id_anonim"].astype(str)

                    df_actualizado = df_central.merge(edit_df[["id_anonim", "nota_parcial"]], on="id_anonim", how="left")

                    df_actualizado.to_csv(ruta_central, index=False)
                    st.success("Central file 'estudiants_net.csv' updated with new grades.")
                else:
                    st.warning("The column 'nota_parcial' or 'id_anonim' was not found to update the central CSV.")
            except Exception as e:
                st.error(f"Could not save the changes: {e}")

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
                st.markdown(f'<p style="font-size:20px; font-weight:bold; color:white;">{category}:</p>', unsafe_allow_html=True)
                for stat_name, stat_value in values.items():
                    st.markdown(f'<p style="font-size:18px; color:white; margin-left:20px;">- {stat_name}: {stat_value:.2f}</p>', unsafe_allow_html=True)


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


