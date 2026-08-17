import os, time, secrets
from flask import Flask, request, redirect, render_template, jsonify, Response, make_response

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")
REPORTS = []       # {"id", "sid", "url", "seen"}
BOT_LAST = [0.0]   # moderator heartbeat (epoch)


def sid():
    return request.cookies.get("sid") or secrets.token_hex(8)


def keep(resp, s):
    resp.set_cookie("sid", s, max_age=3600, samesite="Lax")
    return resp


@app.route("/")
def index():
    # landing — two links: report a link to the moderator, or reflect on yourself first
    return keep(make_response(render_template("index.html")), sid())


@app.route("/search")
def search():
    # reflected sink — what the moderator opens when you report a /search?q= link
    return render_template("search.html", q=request.args.get("q", ""))


@app.route("/my-space")
def my_space():
    # playground — reflects your own query through the same sink, with your own (unprivileged) cookies
    return keep(make_response(render_template("my_space.html", q=request.args.get("q", ""))), sid())


@app.route("/report-to/admin", methods=["GET", "POST"])
def report_to_admin():
    s = sid()
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            REPORTS.append({"id": secrets.token_hex(4), "sid": s, "url": url, "seen": False})
            del REPORTS[:-200]
        return keep(redirect("/report-to/admin"), s)
    mine = [r for r in REPORTS if r["sid"] == s]
    return keep(make_response(render_template("report.html", reports=mine)), s)


@app.route("/pending")
def pending():
    return jsonify([{"id": r["id"], "url": r["url"]} for r in REPORTS if not r["seen"]])


@app.route("/seen/<rid>")
def seen(rid):
    for r in REPORTS:
        if r["id"] == rid:
            r["seen"] = True
    return ("", 204)


@app.route("/heartbeat", methods=["GET", "POST"])
def heartbeat():
    BOT_LAST[0] = time.time()
    return ("", 204)


@app.route("/status.json")
def status():
    s = request.cookies.get("sid", "")
    items = [{"id": r["id"], "seen": r["seen"]} for r in REPORTS if r["sid"] == s]
    return jsonify({"items": items, "last_online": BOT_LAST[0] or None})


@app.route("/moderator")
def moderator():
    if request.cookies.get("role") == "admin":
        return render_template("moderator.html", flag=FLAG)
    return Response("403 — moderators only", status=403)
