import random

from flask import render_template

from app import app


@app.route("/api/random")
def api_random():
    return random.randint(0, 500)


# Fall-through routes for frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")
