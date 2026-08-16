import os, time, secrets
from flask import Flask, request, redirect, render_template, jsonify, Response, make_response

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")
STATE = {"published": False}
PAGES = []         # {"id", "sid", "html", "seen"}
BOT_LAST = [0.0]   # admin heartbeat (epoch)


def sid():
    return request.cookies.get("sid") or secrets.token_hex(8)


def keep(resp, s):
    resp.set_cookie("sid", s, max_age=3600, samesite="Lax")
    return resp


@app.route("/")
def index():
    s = sid()
    mine = [p for p in PAGES if p["sid"] == s]
    return keep(make_response(render_template("index.html", pages=mine)), s)


@app.route("/host", methods=["POST"])
def host():
    s = sid()
    html = request.form.get("html", "")
    pid = ""
    if html.strip():
        pid = secrets.token_hex(4)
        PAGES.append({"id": pid, "sid": s, "html": html, "seen": False})
        del PAGES[:-200]
    return keep(redirect("/?id=" + pid if pid else "/"), s)


@app.route("/hosted/<pid>")
def hosted(pid):
    # serve a player's raw page — this is the "attacker page" the admin opens
    for p in PAGES:
        if p["id"] == pid:
            return Response(p["html"], mimetype="text/html")
    return Response("not found", status=404)


@app.route("/publish")
def publish():
    if request.cookies.get("role") == "admin":
        STATE["published"] = True
        return Response("recovery note published", status=200)
    return Response("403 — admin only", status=403)


@app.route("/public")
def public():
    return render_template("public.html", published=STATE["published"], flag=FLAG)


@app.route("/pending")
def pending():
    return jsonify([p["id"] for p in PAGES if not p["seen"]])


@app.route("/seen/<pid>")
def seen(pid):
    for p in PAGES:
        if p["id"] == pid:
            p["seen"] = True
    return ("", 204)


@app.route("/heartbeat", methods=["GET", "POST"])
def heartbeat():
    BOT_LAST[0] = time.time()
    return ("", 204)


@app.route("/status.json")
def status():
    s = request.cookies.get("sid", "")
    items = [{"id": p["id"], "seen": p["seen"]} for p in PAGES if p["sid"] == s]
    return jsonify({"items": items, "last_online": BOT_LAST[0] or None})
