import os, sqlite3
from flask import Flask, request, render_template

FLAG = os.environ.get("FLAG", "")

db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript(
    """
    CREATE TABLE notes (title TEXT, body TEXT);
    INSERT INTO notes VALUES ('Welcome', 'Search the public knowledge base below.');
    INSERT INTO notes VALUES ('Wifi', 'The guest wifi password is on the whiteboard.');
    INSERT INTO notes VALUES ('Coffee', 'Refills are in the third-floor kitchen.');
    CREATE TABLE secrets (flag TEXT);
    """
)
db.execute("INSERT INTO secrets VALUES (?)", (FLAG,))
db.commit()

PRE = "SELECT title, body FROM notes WHERE title LIKE '%"
SUF = "%'"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    rows, error, q = None, None, ""
    if request.method == "POST":
        q = request.form.get("q", "")
        try:
            rows = db.execute(PRE + q + SUF).fetchall()
        except Exception as ex:
            error = f"{type(ex).__name__}: {ex}"
    return render_template("index.html", rows=rows, error=error, q=q,
                           pre=PRE, suf=SUF)
