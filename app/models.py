from datetime import datetime

from flask_sqlalchemy import Model

from app.db import db


class BaseModel(Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<%s %r>" % (type(self).__name__, self.id)


BaseModel = db.make_declarative_base(BaseModel, db.metadata)


class User(BaseModel):
    __tablename__ = "users"

    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(511), nullable=False)


class Image(BaseModel):
    __tablename__ = "images"

    name = db.Column(db.String(255), nullable=False, unique=True)
    fs_path = db.Column(db.String(511), nullable=False)
    hash = db.Column(db.String(511), nullable=False)


class Tweet(BaseModel):
    __tablename__ = "tweets"

    text = db.Column(db.Text, nullable=False)

    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    poster = db.relationship("User", backref=db.backref("users", lazy=True))

    image_id = db.Column(db.Integer, db.ForeignKey("images.id"))
    image = db.relationship("Image", backref=db.backref("tweets", lazy=True))
