"""The Hidden Vault — an admin secret store whose only "security" is its obscure domain.

There is no authentication. The page asks "are you an admin?"; click Yes and it hands over
the flag. The whole point: the domain was supposed to be secret, but the TLS SNI leaked it.
Obscurity is not security.
"""

import os
from flask import Flask, render_template

FLAG = os.environ.get("FLAG", "")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/reveal", methods=["POST"])
def reveal():
    # no auth — clicking the button is the whole "check"
    return render_template("reveal.html", flag=FLAG)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
