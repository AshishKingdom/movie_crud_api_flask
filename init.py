from flask import Flask
from db import db

# from flask_jwt_extended import JWTManager
# from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from core.config import AppConfig


app = Flask(__name__)
app.config.from_object(AppConfig)

login_manager = LoginManager(app)
# login_manager.login_view = "user.login"
db.init_app(app)
# jwt = JWTManager(app)
# ma = Marshmallow(app)
