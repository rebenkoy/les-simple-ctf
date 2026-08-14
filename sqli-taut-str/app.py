import os, sqlite3
from flask import Flask, request, render_template

FLAG = os.environ.get("FLAG", "")

db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript(
    """
    CREATE TABLE users (username TEXT, password TEXT, role TEXT);
    INSERT INTO users VALUES ('alice', 'sunshine22', 'user');
    INSERT INTO users VALUES ('bob', 'hunter2', 'user');
    INSERT INTO users VALUES ('carol', 'p@ssw0rd!', 'user');
    """
)
db.execute("INSERT INTO users VALUES ('admin', ?, 'admin')", (FLAG,))
db.commit()

PRE = "SELECT username, password FROM users WHERE role = 'user' AND username = '"
SUF = "'"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    rows, error, u = None, None, ""
    if request.method == "POST":
        u = request.form.get("username", "")
        try:
            rows = db.execute(PRE + u + SUF).fetchall()
        except Exception as ex:
            error = f"{type(ex).__name__}: {ex}"
    return render_template("index.html", rows=rows, error=error, u=u,
                           pre=PRE, suf=SUF)
