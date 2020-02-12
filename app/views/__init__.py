from flask import render_template, redirect

from app.views.api.auth import *
from app.views.api.tweet import *
from app.views.api.user import *
from app.views.api.file import *


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


# Fall-through routes for frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")
