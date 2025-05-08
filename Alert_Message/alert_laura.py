from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("alertas_academicas.csv")

@app.route("/")
def index():
    ids = df["id_anonim"].unique()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Selecciona un estudiant</title>
        <style>
            body {
                font-family: 'Helvetica Neue', sans-serif;
                background-color: #f7f7f9;
                text-align: center;
                padding: 50px;
            }
            h2 {
                color: #333;
                margin-bottom: 30px;
            }
            .student-link {
                display: inline-block;
                background-color: #ffffff;
                color: #1a73e8;
                border: 1px solid #ddd;
                padding: 12px 18px;
                margin: 8px;
                border-radius: 6px;
                text-decoration: none;
                font-size: 15px;
                transition: 0.2s;
            }
            .student-link:hover {
                background-color: #f0f0f0;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <h2>Selecciona un estudiant:</h2>
    """

    for id in ids:
        html += f'<a class="student-link" href="/alerta/{id}">{id}</a>'

    html += "</body></html>"
    return html


@app.route("/alerta/<student_id>")
def alerta(student_id):
    dfi = df[df["id_anonim"] == student_id]
    dfi["diferencia"] = dfi["nota_assignatura"] - dfi["predicted_nota_assignatura"]
    alertes = dfi[dfi["diferencia"] < -2]


    if alertes.empty:
        return f"<h3>No hi ha alertes per a l'estudiant <b>{student_id}</b>.</h3>"

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Alertes</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                padding: 30px;
            }
            .alert-box {
                display: flex;
                align-items: center;
                background-color: #fef3f2;
                border-left: 6px solid #d93025;
                padding: 15px;
                border-radius: 6px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .alert-icon {
                font-size: 24px;
                margin-right: 15px;
                color: #d93025;
            }
            .alert-text {
                color: #333;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <h2>Alertes per a {student_id}:</h2>
    """

    for _, row in alertes.iterrows():
        html += f"""
        <div class="alert-box">
            <div class="alert-icon">⚠️</div>
            <div class="alert-text">
                <strong>{row['assignatura']}</strong><br>
                Nota real: {row['nota_assignatura']:.2f} | Predicció: {row['predicted_nota_assignatura']:.2f} <br>
                Desviació: {row['diferencia']:.2f} punts <br>
                <em>{row['alerta']}</em>
            </div>
        </div>
        """

    html += "</body></html>"

    return render_template_string(html)

if __name__ == "__main__":
    app.run(debug=True)
