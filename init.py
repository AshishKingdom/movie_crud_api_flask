from flask import Flask
from sqlalchemy import Integer, String, Column, Date, Float
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "testkey1234567890"

db = SQLAlchemy(app)
jwt = JWTManager(app)
ma = Marshmallow(app)

class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'release_date', 'director', 'genre', 'avg_rating', 'ticket_price', 'cast')


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("Database Created Successfully!")
