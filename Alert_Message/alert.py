from flask import Flask, render_template_string
import webbrowser
import threading

app = Flask(__name__)

# HTML Template with JavaScript Alert
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alert Page</title>
    <script>
        window.onload = function() {
            alert("Careful! Your grades are dropping in 2 classes. Click for more information.");
        };
    </script>
</head>
<body>
<div style="color: green;">
    <h1>Careful! Your grades are dropping in 2 classes. Click for more information.</h1>
    <img src="{{ url_for('alert', filename='\Users\sonia\OneDrive\Documents\UAB\Segon\2semestre\Neural Network and Deep Learning\alert.png') }}" alt="My Image" width="300">
    <p>Click <a href="https://cv.uab.cat/protected/index.jsp" target="_blank">here</a> to visit the UAB protected site.</p>

</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_template)

def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()  # Open browser automatically
    app.run(debug=False)