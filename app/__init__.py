import os

from flask import Flask

app = Flask(__name__, template_folder="../frontend/dist")

app.config.from_object(os.environ["APP_SETTINGS"])

from app import db, views
