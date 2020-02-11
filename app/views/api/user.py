import json
from collections import defaultdict
from json import JSONDecodeError

from flask_login import current_user

from app.db import db
from flask import request

from app import app
from app.models import User, follows
from app.views.helpers import (
    json_route,
    error_response,
    success_response,
    api_logged_in,
    paginated_query,
)


@app.route("/api/user/me", methods=["GET"])
@json_route
def api_me():
    if not current_user.is_authenticated:
        return success_response(None)

    user = User.query.get(int(current_user.get_id()))

    return success_response(user.to_dict())


@app.route("/api/user/search", methods=["POST"])
@json_route
def api_user_search():
    try:
        data = json.loads(
            request.data, object_hook=lambda x: defaultdict(lambda: None, x)
        )
    except JSONDecodeError:
        return error_response(["Invalid request."])

    page = data["page"] or 1
    try:
        page = int(page)
    except ValueError:
        page = 1

    query = data["query"] or ""
    query = "%{}%".format(query)

    users = User.query.filter(User.username.ilike(query))

    return paginated_query(query=users, page=page)


@app.route("/api/user/follow", methods=["POST"])
@json_route
@api_logged_in
def api_user_follow():
    try:
        data = json.loads(
            request.data, object_hook=lambda x: defaultdict(lambda: None, x)
        )
    except JSONDecodeError:
        return error_response(["Invalid request."])

    if "id" not in data:
        return error_response(["User ID required"])

    current_id = int(current_user.get_id())
    user_to_follow = User.query.get(int(data["id"]))

    if user_to_follow is None:
        return error_response(["User cannot be found"])

    if user_to_follow.id == current_id:
        return error_response(["You cannot follow yourself"])

    if user_to_follow.followers.filter_by(id=current_id).count() > 0:
        return error_response(["You are already following that user"])

    query = follows.insert().values(
        follower_id=current_id, following_id=user_to_follow.id
    )
    db.session.execute(query)
    db.session.commit()

    user = User.query.get(current_id)

    ids = user.following.with_entities(User.id).all()

    return success_response([item for sublist in ids for item in sublist])


@app.route("/api/user/unfollow", methods=["POST"])
@json_route
@api_logged_in
def api_user_unfollow():
    try:
        data = json.loads(
            request.data, object_hook=lambda x: defaultdict(lambda: None, x)
        )
    except JSONDecodeError:
        return error_response(["Invalid request."])

    if "id" not in data:
        return error_response(["User ID required"])

    current_id = int(current_user.get_id())
    user_to_unfollow = User.query.get(int(data["id"]))

    if user_to_unfollow is None:
        return error_response(["User cannot be found"])

    if user_to_unfollow.followers.filter_by(id=current_id).count() < 1:
        return error_response(["You aren't following that user"])

    query = (
        follows.delete()
        .where(follows.c.follower_id == current_id)
        .where(follows.c.following_id == int(data["id"]))
    )
    db.session.execute(query)
    db.session.commit()

    user = User.query.get(current_id)

    ids = user.following.with_entities(User.id).all()

    return success_response([item for sublist in ids for item in sublist])


@app.route("/api/user/following")
@json_route
@api_logged_in
def api_user_following():
    user = User.query.get(int(current_user.get_id()))

    ids = user.following.with_entities(User.id).all()

    return success_response([item for sublist in ids for item in sublist])


@app.route("/api/user/followers")
@json_route
@api_logged_in
def api_user_followers():
    user = User.query.get(int(current_user.get_id()))

    ids = user.followers.with_entities(User.id).all()

    return success_response([item for sublist in ids for item in sublist])
