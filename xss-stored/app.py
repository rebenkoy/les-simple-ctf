import time, secrets
from flask import Flask, request, redirect, render_template, jsonify, make_response

app = Flask(__name__)
MESSAGES = []      # {"id", "sid", "text", "seen"}
PLAY = {}          # sid -> playground text
BOT_LAST = [0.0]   # reviewer heartbeat (epoch)


def sid():
    return request.cookies.get("sid") or secrets.token_hex(8)


def keep(resp, s):
    resp.set_cookie("sid", s, max_age=3600, samesite="Lax")
    return resp


@app.route("/", methods=["GET", "POST"])
def index():
    s = sid()
    if request.method == "POST":
        text = request.form.get("message", "")
        if text.strip():
            MESSAGES.append({"id": secrets.token_hex(4), "sid": s, "text": text, "seen": False})
            del MESSAGES[:-200]
        return keep(redirect("/"), s)
    mine = [m for m in MESSAGES if m["sid"] == s]
    return keep(make_response(render_template("index.html", messages=mine)), s)


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


@app.route("/playground-submit", methods=["POST"])
def playground_submit():
    s = sid()
    PLAY[s] = request.form.get("message", "")
    return keep(redirect("/playground-view"), s)


@app.route("/playground-view")
def playground_view():
    s = sid()
    return keep(make_response(render_template("playground.html", message=PLAY.get(s, ""))), s)
