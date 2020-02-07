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
