import os, sqlite3
from flask import Flask, request, render_template

FLAG = os.environ.get("FLAG", "")

db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript(
    """
    CREATE TABLE notes (id INTEGER, title TEXT, body TEXT, published INTEGER);
    INSERT INTO notes VALUES (1, 'Welcome', 'Thanks for using SecureNotes.', 1);
    INSERT INTO notes VALUES (2, 'Groceries', 'milk, eggs, bread', 1);
    INSERT INTO notes VALUES (3, 'Reminder', 'call the dentist', 1);
    """
)
db.execute("INSERT INTO notes VALUES (42, '[admin] recovery key', ?, 0)", (FLAG,))
db.commit()

PRE = "SELECT title, body FROM notes WHERE published = 1 AND id = "
SUF = ""

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    rows, error, nid = None, None, ""
    if request.method == "POST":
        nid = request.form.get("id", "")
        try:
            rows = db.execute(PRE + nid + SUF).fetchall()
        except Exception as ex:
            error = f"{type(ex).__name__}: {ex}"
    return render_template("index.html", rows=rows, error=error, nid=nid,
                           pre=PRE, suf=SUF)
