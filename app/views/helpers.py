from functools import wraps
from typing import Callable

from flask import jsonify, request
from flask_login import current_user
from sqlalchemy.orm import Query


def json_route(f: Callable):
    @wraps(f)
    def inner(**args):
        return jsonify(f(**args))

    return inner


def api_logged_in(f: Callable):
    @wraps(f)
    def inner(**args):
        if not current_user.is_authenticated:
            return error_response(["You must be logged in to do this."])
        else:
            return f(**args)

    return inner


def api_anonymous(f: Callable):
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


def paginated_query(*, page: int, query: Query) -> dict:
    page = max(1, page)
    per_page = 20

    entity = query.column_descriptions[0]["entity"]

    q = {"before": request.args.get("before"), "after": request.args.get("after")}

    if q["after"]:
        query = query.filter(entity.created_at >= q["after"])

    if q["before"]:
        query = query.filter(entity.created_at <= q["before"])

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
