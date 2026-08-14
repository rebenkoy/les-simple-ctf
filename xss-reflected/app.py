import os
from flask import Flask, request, redirect, render_template, jsonify, Response

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")
REPORTS = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    return render_template("search.html", q=request.args.get("q", ""))


@app.route("/report", methods=["POST"])
def report():
    url = request.form.get("url", "").strip()
    if url:
        REPORTS.append(url)
        del REPORTS[:-20]
    return redirect("/")


@app.route("/reports.json")
def reports():
    return jsonify(REPORTS)


@app.route("/moderator")
def moderator():
    if request.cookies.get("role") == "admin":
        return render_template("moderator.html", flag=FLAG)
    return Response("403 — moderators only", status=403)
