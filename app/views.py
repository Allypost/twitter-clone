import json
import random
from collections import defaultdict

from functools import wraps
from json import JSONDecodeError

from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import Query
from sqlalchemy.sql import Insert

from app.db import db
from flask import render_template, jsonify, request, redirect
from flask_login import logout_user, current_user, login_user

from app import app
from app.models import User, Tweet, follows


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


def error_response(reasons: list) -> dict:
    return {"success": False, "data": [], "errors": reasons}


def success_response(data) -> dict:
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


@app.route("/api/tweet", methods=["POST"])
@json_route
@api_logged_in
def api_tweet():
    try:
        data = json.loads(
            request.data, object_hook=lambda x: defaultdict(lambda: None, x)
        )
    except JSONDecodeError:
        return error_response(["Invalid request."])

    tweet_len = len(data["text"] or "")

    if tweet_len < 1:
        return error_response(["Your tweet must be at least one character."])

    if tweet_len > 120:
        return error_response(["Your tweet must be at most 120 characters."])

    tweet = Tweet(
        text=data["text"].replace("\r\n", "\n"), poster_id=int(current_user.get_id())
    )

    db.session.add(tweet)
    db.session.commit()

    return success_response(tweet.to_dict())


@app.route("/api/tweet/<int:tweet_id>", methods=["DELETE"])
@json_route
@api_logged_in
def api_delete_tweet(tweet_id: int):
    tweet = Tweet.query.get(tweet_id)

    if not tweet or tweet.poster_id != int(current_user.get_id()):
        return error_response(["You don't have permission to do that."])

    db.session.delete(tweet)
    db.session.commit()

    return success_response(None)


def paginated_query(*, page: int, query: Query) -> dict:
    page = max(1, page)
    per_page = 20

    entity = query.column_descriptions[0]["entity"]

    paginated_items = query.order_by(entity.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    items_list = paginated_items.items or []

    return success_response(
        {
            "page": paginated_items.page,
            "perPage": per_page,
            "total": paginated_items.pages,
            "next": paginated_items.has_next and paginated_items.next_num,
            "prev": paginated_items.has_prev and paginated_items.prev_num,
            "items": [item.to_dict() for item in items_list],
        }
    )


@app.route("/api/tweet/timeline/public", defaults={"page": 1}, methods=["GET"])
@app.route("/api/tweet/timeline/public/<int:page>", methods=["GET"])
@json_route
def api_tweet_public_list(page: int):
    return paginated_query(page=page, query=Tweet.query)


@app.route("/api/tweet/timeline/my", defaults={"page": 1}, methods=["GET"])
@app.route("/api/tweet/timeline/my/<int:page>", methods=["GET"])
@json_route
@api_logged_in
def api_tweet_my_list(page: int):
    query = Tweet.query.filter_by(poster_id=int(current_user.get_id()))

    return paginated_query(page=page, query=query)


@app.route("/api/tweet/timeline/private", defaults={"page": 1}, methods=["GET"])
@app.route("/api/tweet/timeline/private/<int:page>", methods=["GET"])
@json_route
@api_logged_in
def api_tweet_private_list(page: int):
    following_query = db.session.query(follows.c.following_id).filter(
        follows.c.follower_id == int(current_user.get_id())
    )
    query = Tweet.query.filter(Tweet.poster_id.in_(following_query))

    return paginated_query(page=page, query=query)


@app.route("/api/user/me", methods=["GET"])
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
