from datetime import datetime
from typing import Dict, Any, Optional

from flask_sqlalchemy import Model
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declared_attr
from app.db import db


class BaseModel(Model):
    __table__: Table

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    __hidden = set()

    def __repr__(self) -> str:
        return "<%s %r>" % (type(self).__name__, self.id)

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__

    def to_dict(self) -> Dict[str, Any]:
        """Serializes only column data."""
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in self.__hidden
        }


BaseModel = db.make_declarative_base(BaseModel, db.metadata)


class User(BaseModel):
    __tablename__ = "users"
    __hidden = {"password"}

    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(511), nullable=False)


class Image(BaseModel):
    __tablename__ = "images"
    __hidden = {"fs_path"}

    name = db.Column(db.String(255), nullable=False, unique=True)
    fs_path = db.Column(db.String(511), nullable=False)
    hash = db.Column(db.String(511), nullable=False)


class Tweet(BaseModel):
    __tablename__ = "tweets"
    __hidden = {"poster_id", "image_id"}

    text = db.Column(db.Text, nullable=False)

    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    poster = db.relationship("User", backref=db.backref("users", lazy=True))

    image_id = db.Column(db.Integer, db.ForeignKey("images.id"))
    image = db.relationship("Image", backref=db.backref("images", lazy=True))
