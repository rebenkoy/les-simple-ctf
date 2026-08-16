import os, sqlite3
from flask import Flask, request, render_template

FLAG = os.environ.get("FLAG", "")

db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript(
    """
    CREATE TABLE notes (id INTEGER, title TEXT, body TEXT, published INTEGER, secret TEXT);
    INSERT INTO notes VALUES (1, 'Welcome', 'Public bulletin board.', 1, '(kept in the vault)');
    INSERT INTO notes VALUES (2, 'Hours',   'Office is open 9-5.',    1, '(kept in the vault)');
    INSERT INTO notes VALUES (3, 'Draft',   'Not ready yet.',         0, '(kept in the vault)');
    CREATE TABLE vault (id INTEGER, label TEXT, secret TEXT);
    """
)
db.execute("INSERT INTO vault VALUES (1, 'recovery-key', ?)", (FLAG,))
db.commit()

BLOCKED = ["union"]
PRE = "SELECT * FROM "
SUF = " WHERE notes.published = 1"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    rows, cols, error, src = None, None, None, ""
    if request.method == "POST":
        src = request.form.get("src", "")
        if any(b in src.lower() for b in BLOCKED):
            error = "Request rejected: UNION is not allowed."
        else:
            try:
                cur = db.execute(PRE + src + SUF)
                rows = cur.fetchall()
                cols = [d[0] for d in cur.description]
            except Exception as ex:
                error = f"{type(ex).__name__}: {ex}"
    return render_template("index.html", rows=rows, cols=cols, error=error, src=src,
                           pre=PRE, suf=SUF, blocked=BLOCKED)
