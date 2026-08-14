from flask import Flask, request, redirect, render_template

app = Flask(__name__)
MESSAGES = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        MESSAGES.append(request.form.get("message", ""))
        del MESSAGES[:-50]
        return redirect("/")
    return render_template("index.html", messages=MESSAGES)


@app.route("/admin")
def admin():
    return render_template("admin.html", messages=MESSAGES)
