import os, time, secrets
from flask import Flask, request, redirect, render_template, jsonify, Response, make_response

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")
STATE = {"published": False}
PAGES = []         # {"id", "sid", "html", "seen"} — hosted for the admin to open
PLAY = {}          # sid -> my-space html (private preview, not queued for the bot)
BOT_LAST = [0.0]   # admin heartbeat (epoch)


def sid():
    return request.cookies.get("sid") or secrets.token_hex(8)


def keep(resp, s):
    resp.set_cookie("sid", s, max_age=3600, samesite="Lax")
    return resp


@app.route("/")
def index():
    # landing — two links: host a page for the admin, or preview it on yourself first
    return keep(make_response(render_template("index.html")), sid())


@app.route("/report-to/admin", methods=["GET", "POST"])
def report_to_admin():
    s = sid()
    if request.method == "POST":
        html = request.form.get("html", "")
        if html.strip():
            PAGES.append({"id": secrets.token_hex(4), "sid": s, "html": html, "seen": False})
            del PAGES[:-200]
        return keep(redirect("/report-to/admin"), s)
    mine = [p for p in PAGES if p["sid"] == s]
    return keep(make_response(render_template("report.html", pages=mine)), s)


@app.route("/hosted/<pid>")
def hosted(pid):
    # serve a player's raw page — this is the "attacker page" the admin opens
    for p in PAGES:
        if p["id"] == pid:
            return Response(p["html"], mimetype="text/html")
    return Response("not found", status=404)


@app.route("/my-space", methods=["GET", "POST"])
def my_space():
    # playground — preview your page in an iframe as yourself (no admin cookie), watching /publish 403
    s = sid()
    if request.method == "POST":
        PLAY[s] = request.form.get("html", "")
        return keep(redirect("/my-space"), s)
    return keep(make_response(render_template("my_space.html", has_page=bool(PLAY.get(s)))), s)


@app.route("/my-space/page")
def my_space_page():
    return Response(PLAY.get(sid(), ""), mimetype="text/html")


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
