import os

from flask import Flask
from flask_login import LoginManager

app = Flask(__name__, template_folder="../frontend/dist")

app.config.from_object(os.getenv("APP_SETTINGS", "config.ProductionConfig"))

login = LoginManager(app)

from app import db, views
