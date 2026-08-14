import subprocess, sys
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    expr, output = "", None
    if request.method == "POST":
        expr = request.form.get("expr", "")
        r = subprocess.run(
            [sys.executable, "calc.py"], input=expr,
            capture_output=True, text=True, timeout=5,
        )
        output = r.stdout + r.stderr
    return render_template("index.html", expr=expr, output=output)
