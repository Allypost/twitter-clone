import json
import random
from collections import defaultdict

from functools import wraps
from json import JSONDecodeError

from app.db import db
from flask import render_template, jsonify, request, redirect
from flask_login import logout_user, current_user, login_user

from app import app
from app.models import User


def json_route(f):
    @wraps(f)
    def inner(**args):
        return jsonify(f(**args))

    return inner


def api_logged_in(f):
    @wraps(f)
    def inner(**args):
        if not current_user.is_authenticated:
            return error_response(["You must be logged in to do this."])
        else:
            return f(**args)

    return inner


def api_anonymous(f):
    @wraps(f)
    def inner(**args):
        if current_user.is_authenticated:
            return error_response(["You're already logged in."])
        else:
            return f(**args)

    return inner


def error_response(reasons: list) -> object:
    return {"success": False, "data": [], "errors": reasons}


def success_response(data) -> object:
    return {"success": True, "data": data, "errors": []}


@app.route("/api/random")
@json_route
def api_random():
    return random.randint(0, 500)


@app.route("/api/auth/register", methods=["POST"])
@json_route
@api_anonymous
def api_register():
    try:
        data = json.loads(request.data)
    except JSONDecodeError:
        return error_response(["Invalid request."])

    required_fields = ["username", "password", "passwordRepeat"]

    has_required = all(field in data for field in required_fields)

    if not has_required:
        return error_response(["Please fill in all required fields."])

    password_too_short = len(data["password"]) < 8

    if password_too_short:
        return error_response(["Your password is too short."])

    passwords_match = data["password"] == data["passwordRepeat"]

    if not passwords_match:
        return error_response(["Passwords must match."])

    username_taken = User.query.filter_by(username=data["username"]).first() is not None

    if username_taken:
        return error_response(["Username is already taken"])

    user = User(username=data["username"]).set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    login_user(user=user)

    return success_response(user.to_dict())


@app.route("/api/auth/login", methods=["POST"])
@json_route
@api_anonymous
def api_login():
    try:
        data = json.loads(
            request.data, object_hook=lambda x: defaultdict(lambda: None, x)
        )
    except JSONDecodeError:
        return error_response(["Invalid request."])

    user = User.query.filter_by(username=data["username"]).first() or User(password="")

    # Password is checked irregardless of whether
    # the user was found to avoid exposing a timing oracle
    valid_credentials = User.check_password(user.password, data["password"])

    if not valid_credentials:
        return error_response(["Invalid credentials."])

    login_user(user=user, remember=data["rememberMe"])

    return success_response(user.to_dict())


@app.route("/api/auth/logout", methods=["POST"])
@json_route
def api_logout():
    logout_user()
    return success_response([])


@app.route("/api/auth/me", methods=["GET"])
@json_route
def api_me():
    if not current_user.is_authenticated:
        return success_response(None)

    user = User.query.get(int(current_user.get_id()))

    return success_response(user.to_dict())


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


# Fall-through routes for frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")
