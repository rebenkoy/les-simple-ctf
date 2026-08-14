import os, sqlite3
from flask import Flask, request, render_template

FLAG = os.environ.get("FLAG", "")

db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript(
    """
    CREATE TABLE notes (id INTEGER, title TEXT, body TEXT);
    INSERT INTO notes VALUES (1, 'Roadmap', 'Q3 planning notes.');
    INSERT INTO notes VALUES (2, 'Lunch', 'Team lunch on Friday.');
    INSERT INTO notes VALUES (3, 'Onboarding', 'Welcome checklist for new hires.');
    CREATE TABLE shares (note_id INTEGER, user TEXT);
    INSERT INTO shares VALUES (1, 'alice'), (2, 'alice'), (3, 'bob');
    CREATE TABLE secrets (flag TEXT);
    """
)
db.execute("INSERT INTO secrets VALUES (?)", (FLAG,))
db.commit()

PRE = "SELECT title, body FROM notes WHERE id IN (SELECT note_id FROM shares WHERE user = '"
SUF = "')"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    rows, error, u = None, None, ""
    if request.method == "POST":
        u = request.form.get("user", "")
        try:
            rows = db.execute(PRE + u + SUF).fetchall()
        except Exception as ex:
            error = f"{type(ex).__name__}: {ex}"
    return render_template("index.html", rows=rows, error=error, u=u,
                           pre=PRE, suf=SUF)
