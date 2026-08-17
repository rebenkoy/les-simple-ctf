import os
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")
DOMAIN = os.environ.get("DOMAIN", "ctf.test")


@app.route("/")
def index():
    # landing — two links: host on the grader (the attack), or call the API on yourself first
    return render_template("index.html", domain=DOMAIN)


@app.route("/my-space")
def my_space():
    # playground — call /api/account as yourself (no admin session) → guest data, no flag
    return render_template("my_space.html", domain=DOMAIN)


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
