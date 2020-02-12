import json
from collections import defaultdict
from json import JSONDecodeError

from flask_login import current_user

from app.db import db
from flask import request

from app import app
from app.models import Tweet, follows, Image
from app.views.helpers import (
    json_route,
    error_response,
    success_response,
    api_logged_in,
    paginated_query,
)


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

    image_id = data["imageId"]

    if image_id is not None:
        image_exists = Image.query.filter_by(id=image_id).count() > 0

        if not image_exists:
            return error_response(["Image not found"])

    tweet = Tweet(
        text=data["text"].replace("\r\n", "\n"),
        poster_id=int(current_user.get_id()),
        image_id=image_id,
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

    if tweet.image:
        db.session.delete(tweet.image)

    db.session.commit()

    return success_response(None)


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
