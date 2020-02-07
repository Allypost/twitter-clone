import random

from functools import wraps
from flask import render_template, jsonify

from app import app


def json_route(f):
    @wraps(f)
    def inner(**args):
        return jsonify(f(**args))

    return inner


@app.route("/api/random")
@json_route
def api_random():
    return random.randint(0, 500)


# Fall-through routes for frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")
