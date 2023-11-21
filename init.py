from flask import Flask
from db import db

from flask_jwt_extended import JWTManager
from core.config import AppConfig


app = Flask(__name__)
app.config.from_object(AppConfig)

db.init_app(app)
jwt = JWTManager(app)
