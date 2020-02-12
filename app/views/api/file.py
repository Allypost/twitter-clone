import hashlib
import os
import string
import calendar
import time
import random

from app.db import db
from flask import request, abort, send_file
from flask_login import current_user
from werkzeug.datastructures import FileStorage

from app import app
from app.models import Image
from app.views.helpers import (
    json_route,
    api_logged_in,
    error_response,
    success_response,
)


def hash_file(path):
    m = hashlib.sha256()

    with open(path, "rb") as f:
        BUF_SIZE = 65536  # 64kb
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            m.update(data)

    return m.hexdigest()


@app.route("/api/file/upload", methods=["POST"])
@json_route
@api_logged_in
def api_file_upload():
    if "file" not in request.files:
        return error_response(["File must be provided"])

    file: FileStorage = request.files["file"]

    if not file or file.filename == "":
        return error_response(["File must be provided"])

    if file.mimetype not in {"image/jpeg", "image/gif"}:
        return error_response(
            ["Invalid image format. Must be a .jpg, .jpeg or .gif file."]
        )

    user_id = int(current_user.get_id())

    filename_len = 10
    filename = "".join(
        random.choices(string.ascii_letters + string.digits, k=filename_len)
    )
    ts = calendar.timegm(time.gmtime())

    filename = "%s-%d-%s.jpg" % (user_id, ts, filename)
    fs_path = os.path.join(app.config["UPLOAD_DIR"], filename)

    file.save(fs_path)

    file_hash = hash_file(fs_path)

    image = Image(
        name=filename,
        original_name=file.filename,
        fs_path=fs_path,
        hash=file_hash,
        mime_type=file.mimetype,
        uploader_id=user_id,
    )

    db.session.add(image)
    db.session.commit()

    return success_response(image.to_dict())


@app.route("/api/file/uploads/info/by-name/<name>", methods=["GET"])
@json_route
def api_file_info(name: str):
    file = Image.query.filter_by(name=name).first()

    if file is None:
        return error_response(["File not found"])

    return success_response(file.to_dict())


@app.route("/api/file/uploads/by-name/<name>", methods=["GET"])
def api_file_get(name: str):
    file = Image.query.filter_by(name=name).first()

    if file is None:
        return abort(404)

    return send_file(file.fs_path, mimetype=file.mime_type)
