"""Secret Store — a deliberately plaintext-HTTP web app for a LAN-sniffing challenge.

Users register and stash key -> value secrets. The admin account holds the flag under
the key `challenge-key`. Everything runs over plain HTTP (no TLS) on port 80, so anyone
on the wire can read the admin's login when the admin bot signs in.

Intentionally insecure (plaintext passwords, plaintext transport) — teaching target only.
"""

import os
import sqlite3

from flask import (
    Flask, g, session, request, redirect, url_for, render_template, flash, abort,
)

FLAG = os.environ.get("FLAG", "")
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "")
DB = os.environ.get("DB", "/app/store.db")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "secretstore-dev-key")


def db():
    d = getattr(g, "_db", None)
    if d is None:
        d = g._db = sqlite3.connect(DB)
        d.row_factory = sqlite3.Row
    return d


@app.teardown_appcontext
def _close(_e):
    d = getattr(g, "_db", None)
    if d is not None:
        d.close()


def init_db():
    d = sqlite3.connect(DB)
    d.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS secrets (
            user_id INTEGER NOT NULL,
            k       TEXT NOT NULL,
            v       TEXT NOT NULL,
            PRIMARY KEY (user_id, k)
        );
        """
    )
    row = d.execute("SELECT id FROM users WHERE username = ?", (ADMIN_USER,)).fetchone()
    if row is None:
        d.execute("INSERT INTO users (username, password) VALUES (?, ?)", (ADMIN_USER, ADMIN_PASS))
        uid = d.execute("SELECT id FROM users WHERE username = ?", (ADMIN_USER,)).fetchone()[0]
    else:
        uid = row[0]
        d.execute("UPDATE users SET password = ? WHERE id = ?", (ADMIN_PASS, uid))
    # (re)seed the flag as the admin's secret
    d.execute(
        "INSERT OR REPLACE INTO secrets (user_id, k, v) VALUES (?, 'challenge-key', ?)",
        (uid, FLAG),
    )
    d.commit()
    d.close()


init_db()


def current_user():
    uid = session.get("uid")
    if uid is None:
        return None
    return db().execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()


@app.context_processor
def inject_me():
    return {"me": current_user()}


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form.get("username", "").strip()
        p = request.form.get("password", "")
        if not u or not p:
            flash("Username and password are required.")
            return redirect(url_for("register"))
        try:
            db().execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
            db().commit()
        except sqlite3.IntegrityError:
            flash("That username is taken.")
            return redirect(url_for("register"))
        session["uid"] = db().execute(
            "SELECT id FROM users WHERE username = ?", (u,)
        ).fetchone()[0]
        return redirect(url_for("dashboard"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username", "").strip()
        p = request.form.get("password", "")
        row = db().execute("SELECT * FROM users WHERE username = ?", (u,)).fetchone()
        if row is None or row["password"] != p:
            flash("Invalid credentials.")
            return redirect(url_for("login"))
        session["uid"] = row["id"]
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def dashboard():
    me = current_user()
    if me is None:
        return redirect(url_for("login"))
    keys = db().execute(
        "SELECT k FROM secrets WHERE user_id = ? ORDER BY k", (me["id"],)
    ).fetchall()
    return render_template("dashboard.html", keys=[r["k"] for r in keys])


@app.route("/store", methods=["POST"])
def store():
    me = current_user()
    if me is None:
        return redirect(url_for("login"))
    k = request.form.get("key", "").strip()
    v = request.form.get("value", "")
    if k:
        db().execute(
            "INSERT OR REPLACE INTO secrets (user_id, k, v) VALUES (?, ?, ?)",
            (me["id"], k, v),
        )
        db().commit()
    return redirect(url_for("dashboard"))


@app.route("/reveal/<key>")
def reveal(key):
    me = current_user()
    if me is None:
        return redirect(url_for("login"))
    row = db().execute(
        "SELECT v FROM secrets WHERE user_id = ? AND k = ?", (me["id"], key)
    ).fetchone()
    if row is None:
        abort(404)
    return render_template("reveal.html", key=key, value=row["v"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
