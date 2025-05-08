from flask import Flask, render_template_string
import webbrowser
import threading

app = Flask(__name__)


html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Alert Page</title>
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
        .alert-text a {
            color: #1a73e8;
            text-decoration: underline;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="alert-box">
        <div class="alert-icon">⚠️</div>
        <div class="alert-text">
            You are failing Unit 2. <a href="https://cv.uab.cat/protected/index.jsp" target="_blank">Here</a> are some exercises to help you revise for your next exam.
        </div>
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
    app.run(debug=True)