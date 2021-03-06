import os
from datetime import datetime
from typing import Dict, Any, Optional

from flask_sqlalchemy import Model
from sqlalchemy import Table, event
from sqlalchemy.engine import Connection
from sqlalchemy.ext.declarative import declared_attr

from flask_login import UserMixin
from sqlalchemy.orm import Query, Mapper
from werkzeug.security import check_password_hash, generate_password_hash

from app import login
from app.db import db


class BaseModel(Model):
    __table__: Table

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    __hidden__ = set()

    def __repr__(self) -> str:
        return "<%s %r>" % (type(self).__name__, self.id)

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__

    def to_dict(self) -> Dict[str, Any]:
        """Serializes only column data."""
        props = {}
        for prop_name in self.__mapper__.attrs.keys():
            if prop_name in self.__hidden__:
                continue

            prop_value = getattr(self, prop_name)

            if isinstance(prop_value, Query):
                continue

            if isinstance(prop_value, BaseModel):
                prop_value = prop_value.to_dict()

            props[prop_name] = prop_value

        return props


BaseModel = db.make_declarative_base(BaseModel, db.metadata)

follows = db.Table(
    "follows",
    db.Column("follower_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("following_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("created_at", db.DateTime, default=datetime.utcnow, nullable=False),
    db.UniqueConstraint("follower_id", "following_id", name="uq_unique_follow"),
    db.CheckConstraint("follower_id <> following_id", name="ck_no_follow_yourself"),
)


class User(UserMixin, BaseModel):
    __tablename__ = "users"
    __hidden__ = {"password"}

    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(511), nullable=False)

    following = db.relationship(
        "User",
        lambda: follows,
        primaryjoin=lambda: User.id == follows.c.follower_id,
        secondaryjoin=lambda: User.id == follows.c.following_id,
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )

    def set_password(self, password: str) -> "User":
        self.password = generate_password_hash(password)
        return self

    def verify_password(self, password: str) -> bool:
        return self.check_password(self.password, password)

    @staticmethod
    def check_password(pwhash: str, password: str) -> bool:
        return check_password_hash(pwhash, password)


class Image(BaseModel):
    __tablename__ = "images"
    __hidden__ = {"fs_path", "uploader_id"}

    name = db.Column(db.String(255), nullable=False, unique=True)
    original_name = db.Column(db.String(511), default="")
    fs_path = db.Column(db.String(511), nullable=False)
    hash = db.Column(db.String(511), nullable=False)
    mime_type = db.Column(db.String(255))
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    uploader = db.relationship("User")


@event.listens_for(Image, "after_delete")
def image_on_delete_remove_file(mapper: Mapper, connection: Connection, target: Image):
    os.remove(target.fs_path)


class Tweet(BaseModel):
    __tablename__ = "tweets"
    __hidden__ = {"poster_id", "image_id"}

    text = db.Column(db.Text, nullable=False)

    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    poster = db.relationship("User")

    image_id = db.Column(db.Integer, db.ForeignKey("images.id"))
    image = db.relationship("Image")


@login.user_loader
def load_user(id: str) -> Optional[User]:
    return User.query.get(int(id))
