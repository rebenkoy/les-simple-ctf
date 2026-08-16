import os, sqlite3, secrets as rnd
from flask import Flask, request, redirect, render_template, session

FLAG = os.environ.get("FLAG", "")
# v1 leaves /login injectable; v2 sets SAFE_LOGIN=1 so /login uses bound params
SAFE_LOGIN = os.environ.get("SAFE_LOGIN", "") == "1"
ADMIN_PW = rnd.token_hex(16)   # random per boot — not in the source

db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript(
    """
    CREATE TABLE users (user_id INTEGER, name TEXT, password TEXT);
    INSERT INTO users VALUES (2, 'alice', 'letmein');
    INSERT INTO users VALUES (3, 'bob',   'hunter2');
    CREATE TABLE notes (id INTEGER, user_id INTEGER, name TEXT, note TEXT);
    INSERT INTO notes VALUES (1, 2, 'wifi', 'guest wifi: coffee-house');
    INSERT INTO notes VALUES (2, 3, 'todo', 'remember to buy milk');
    """
)
db.execute("INSERT INTO users VALUES (1, 'admin', ?)", (ADMIN_PW,))
db.execute("INSERT INTO notes VALUES (99, 1, 'flag', ?)", (FLAG,))
db.commit()

LOGIN_PRE = "SELECT user_id FROM users WHERE name = '"
LOGIN_MID = "' AND password = '"
LOGIN_SUF = "'"

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", rnd.token_hex(16))


@app.route("/")
def home():
    return redirect("/notes" if session.get("uid") is not None else "/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")
        try:
            if SAFE_LOGIN:
                row = db.execute("SELECT user_id FROM users WHERE name = ? AND password = ?",
                                 (u, p)).fetchone()
            else:
                row = db.execute(LOGIN_PRE + u + LOGIN_MID + p + LOGIN_SUF).fetchone()
        except Exception as ex:
            row, error = None, f"{type(ex).__name__}: {ex}"
        if row:
            session["uid"] = row[0]
            return redirect("/notes")
        elif not error:
            error = "Invalid credentials."
    return render_template("login.html", error=error, safe=SAFE_LOGIN,
                           pre=LOGIN_PRE, mid=LOGIN_MID, suf=LOGIN_SUF)


@app.route("/notes")
def notes():
    uid = session.get("uid")
    if uid is None:
        return redirect("/login")
    rows = db.execute("SELECT name, note FROM notes WHERE user_id = ?", (uid,)).fetchall()
    who = db.execute("SELECT name FROM users WHERE user_id = ?", (uid,)).fetchone()
    return render_template("notes.html", notes=rows, who=(who[0] if who else uid), uid=uid)


@app.route("/add-note", methods=["GET", "POST"])
def add_note():
    uid = session.get("uid")
    if uid is None:
        return redirect("/login")
    error = None
    pre = f"INSERT INTO notes (user_id, name, note) VALUES ({uid}, '"
    if request.method == "POST":
        name = request.form.get("name", "")
        value = request.form.get("value", "")
        try:
            db.execute(pre + name + "', '" + value + "')")
            db.commit()
            return redirect("/notes")
        except Exception as ex:
            error = f"{type(ex).__name__}: {ex}"
    return render_template("add_note.html", error=error, uid=uid,
                           pre=pre, mid="', '", suf="')")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
