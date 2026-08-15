import os
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/account")
def account():
    origin = request.headers.get("Origin", "*")
    if request.cookies.get("session") == "admin":
        body = {"user": "reviewer", "email": "reviewer@store.ctf.test", "secret_note": FLAG}
    else:
        body = {"user": "guest", "email": None, "secret_note": None}
    resp = jsonify(body)
    resp.headers["Access-Control-Allow-Origin"] = origin
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    return resp
