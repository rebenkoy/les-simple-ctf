import os, sqlite3
from flask import Flask, request, render_template

FLAG = os.environ.get("FLAG", "")

db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript(
    """
    CREATE TABLE notes (id INTEGER, title TEXT, body TEXT, author TEXT);
    INSERT INTO notes VALUES (1, 'Welcome', 'Preview any field of the latest note.', 'system');
    CREATE TABLE secrets (flag TEXT);
    """
)
db.execute("INSERT INTO secrets VALUES (?)", (FLAG,))
db.commit()

BLOCKED = ["union"]
PRE = "SELECT "
SUF = " FROM notes LIMIT 1"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    value, error, field = None, None, ""
    if request.method == "POST":
        field = request.form.get("field", "")
        if any(b in field.lower() for b in BLOCKED):
            error = "Request rejected: UNION is not allowed."
        else:
            try:
                row = db.execute(PRE + field + SUF).fetchone()
                value = row[0] if row else None
            except Exception as ex:
                error = f"{type(ex).__name__}: {ex}"
    return render_template("index.html", value=value, error=error, field=field,
                           pre=PRE, suf=SUF, blocked=BLOCKED)
