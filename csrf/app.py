import os
from flask import Flask, request, redirect, render_template, jsonify, Response

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")
STATE = {"published": False}
REPORTS = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/publish")
def publish():
    if request.cookies.get("role") == "admin":
        STATE["published"] = True
        return Response("recovery note published", status=200)
    return Response("403 — admin only", status=403)


@app.route("/public")
def public():
    return render_template("public.html", published=STATE["published"], flag=FLAG)


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
