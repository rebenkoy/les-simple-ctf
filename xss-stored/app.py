import time, secrets
from flask import Flask, request, redirect, render_template, jsonify, make_response

app = Flask(__name__)
MESSAGES = []      # {"id", "sid", "text", "seen"}
PLAY = {}          # sid -> my-space text
BOT_LAST = [0.0]   # reviewer heartbeat (epoch)


def sid():
    return request.cookies.get("sid") or secrets.token_hex(8)


def keep(resp, s):
    resp.set_cookie("sid", s, max_age=3600, samesite="Lax")
    return resp


@app.route("/")
def index():
    # landing — two links: submit to the reviewer, or test in your own space first
    return keep(make_response(render_template("index.html")), sid())


@app.route("/report-to/admin", methods=["GET", "POST"])
def report_to_admin():
    s = sid()
    if request.method == "POST":
        text = request.form.get("message", "")
        if text.strip():
            MESSAGES.append({"id": secrets.token_hex(4), "sid": s, "text": text, "seen": False})
            del MESSAGES[:-200]
        return keep(redirect("/report-to/admin"), s)
    mine = [m for m in MESSAGES if m["sid"] == s]
    return keep(make_response(render_template("report.html", messages=mine)), s)


@app.route("/my-space", methods=["GET", "POST"])
def my_space():
    # playground — renders your own input through the same sink, with your own (unprivileged) cookies
    s = sid()
    if request.method == "POST":
        PLAY[s] = request.form.get("message", "")
        return keep(redirect("/my-space"), s)
    return keep(make_response(render_template("my_space.html", message=PLAY.get(s, ""))), s)


@app.route("/admin")
def admin():
    # reviewer view — renders each not-yet-seen message unescaped (the sink)
    return render_template("admin.html", messages=[m for m in MESSAGES if not m["seen"]])


@app.route("/pending")
def pending():
    return jsonify([m["id"] for m in MESSAGES if not m["seen"]])


@app.route("/seen/<mid>")
def seen(mid):
    for m in MESSAGES:
        if m["id"] == mid:
            m["seen"] = True
    return ("", 204)


@app.route("/heartbeat", methods=["GET", "POST"])
def heartbeat():
    BOT_LAST[0] = time.time()
    return ("", 204)


@app.route("/status.json")
def status():
    s = request.cookies.get("sid", "")
    items = [{"id": m["id"], "seen": m["seen"]} for m in MESSAGES if m["sid"] == s]
    return jsonify({"items": items, "last_online": BOT_LAST[0] or None})
