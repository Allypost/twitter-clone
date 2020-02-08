import os

from flask import Flask
from flask_login import LoginManager

app = Flask(__name__, template_folder="../frontend/dist")

app.config.from_object(os.environ["APP_SETTINGS"])

login = LoginManager(app)

from app import db, views
