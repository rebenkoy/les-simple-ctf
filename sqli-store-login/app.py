import os, sqlite3, secrets as rnd
from flask import Flask, request, render_template

FLAG = os.environ.get("FLAG", "")
ADMIN_PW = rnd.token_hex(16)   # random per boot — not in the source, so you must inject

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

PRE = "SELECT user_id FROM users WHERE name = '"
MID = "' AND password = '"
SUF = "'"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    notes, error, who, username = None, None, None, ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        try:
            row = db.execute(PRE + username + MID + password + SUF).fetchone()
        except Exception as ex:
            row = None
            error = f"{type(ex).__name__}: {ex}"
        if row:
            who = row[0]
            notes = db.execute("SELECT name, note FROM notes WHERE user_id = ?", (who,)).fetchall()
        elif not error:
            error = "Invalid credentials."
    return render_template("index.html", notes=notes, error=error, who=who,
                           username=username, pre=PRE, mid=MID, suf=SUF)
