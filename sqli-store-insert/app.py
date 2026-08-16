import os, sqlite3, secrets as rnd
from flask import Flask, request, render_template

FLAG = os.environ.get("FLAG", "")
ADMIN_PW = rnd.token_hex(16)
ME = 2   # you're signed in as alice — login is parameterized now, so no bypass there

db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript(
    """
    CREATE TABLE users (user_id INTEGER, name TEXT, password TEXT);
    INSERT INTO users VALUES (2, 'alice', 'letmein');
    INSERT INTO users VALUES (3, 'bob',   'hunter2');
    CREATE TABLE notes (id INTEGER, user_id INTEGER, name TEXT, note TEXT);
    INSERT INTO notes VALUES (1, 2, 'wifi', 'guest wifi: coffee-house');
    """
)
db.execute("INSERT INTO users VALUES (1, 'admin', ?)", (ADMIN_PW,))
db.execute("INSERT INTO notes VALUES (99, 1, 'flag', ?)", (FLAG,))
db.commit()

# login is now safe (parameterized) — the injectable part is the note writer:
PRE = "INSERT INTO notes (user_id, name, note) VALUES (2, '"
MID = "', '"
SUF = "')"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    error, saved = None, False
    if request.method == "POST":
        name = request.form.get("name", "")
        value = request.form.get("value", "")
        try:
            db.execute(PRE + name + MID + value + SUF)
            db.commit()
            saved = True
        except Exception as ex:
            error = f"{type(ex).__name__}: {ex}"
    notes = db.execute("SELECT name, note FROM notes WHERE user_id = ?", (ME,)).fetchall()
    return render_template("index.html", notes=notes, error=error, saved=saved,
                           me=ME, pre=PRE, mid=MID, suf=SUF)
