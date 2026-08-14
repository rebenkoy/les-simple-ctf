import os, sqlite3
from flask import Flask, request, render_template

FLAG = os.environ.get("FLAG", "")

db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript(
    """
    CREATE TABLE users (username TEXT);
    INSERT INTO users VALUES ('alice'), ('bob'), ('carol'), ('dave');
    CREATE TABLE secrets (flag TEXT);
    """
)
db.execute("INSERT INTO secrets VALUES (?)", (FLAG,))
db.commit()

PRE = "SELECT 1 FROM users WHERE username = '"
SUF = "'"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    msg, error, u = None, None, ""
    if request.method == "POST":
        u = request.form.get("username", "")
        try:
            hit = db.execute(PRE + u + SUF).fetchone()
            msg = "That username is taken." if hit else "Username available!"
        except Exception as ex:
            error = f"{type(ex).__name__}: {ex}"
    return render_template("index.html", msg=msg, error=error, u=u,
                           pre=PRE, suf=SUF)
