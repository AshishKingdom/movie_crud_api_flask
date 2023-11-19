from db import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    User model with the following attributes:
    - id: primary key
    - name: user name
    - email: user email
    - password: user password
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
