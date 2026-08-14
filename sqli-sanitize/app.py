import os, sqlite3
from flask import Flask, request, render_template

FLAG = os.environ.get("FLAG", "")

db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript(
    """
    CREATE TABLE notes (id INTEGER, title TEXT, body TEXT, visibility TEXT);
    INSERT INTO notes VALUES (1, 'Welcome', 'Public bulletin board.', 'public');
    INSERT INTO notes VALUES (2, 'Hours', 'Office is open 9-5.', 'public');
    INSERT INTO notes VALUES (3, 'Parking', 'Visitor spots are out front.', 'public');
    """
)
db.execute("INSERT INTO notes VALUES (99, '[admin] recovery key', ?, 'secret')", (FLAG,))
db.commit()

BLOCKED = ["'", '"', ";", "--", "/*", "union"]
PRE = "SELECT title, body FROM notes WHERE visibility = 'public' AND id = "
SUF = ""

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    rows, error, nid = None, None, ""
    if request.method == "POST":
        nid = request.form.get("id", "")
        if any(b in nid.lower() for b in BLOCKED):
            error = "Request rejected by input firewall."
        else:
            try:
                rows = db.execute(PRE + nid + SUF).fetchall()
            except Exception as ex:
                error = f"{type(ex).__name__}: {ex}"
    return render_template("index.html", rows=rows, error=error, nid=nid,
                           pre=PRE, suf=SUF, blocked=BLOCKED)
