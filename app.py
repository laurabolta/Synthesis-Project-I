from flask import Flask, render_template
import webbrowser
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sonia")
def sonia():
    return render_template("sonia.html")

def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()  # Open browser automatically
    app.run(debug=True)