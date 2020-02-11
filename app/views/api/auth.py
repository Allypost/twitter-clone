import json
from collections import defaultdict
from json import JSONDecodeError

from flask_login import login_user, logout_user

from app.db import db
from flask import request

from app import app
from app.models import User
from app.views.helpers import (
    json_route,
    api_anonymous,
    error_response,
    success_response,
)


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
