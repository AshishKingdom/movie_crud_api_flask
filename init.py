from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from core.config import AppConfig


app = Flask(__name__)
app.config.from_object(AppConfig)

db = SQLAlchemy(app)
jwt = JWTManager(app)
ma = Marshmallow(app)