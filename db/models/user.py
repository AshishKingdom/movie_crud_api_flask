from db import db


class User(db.Model):
    """
    User model with the following attributes:
    - email: user email
    - password: user password
    - role: user role (default: student)
    """

    __tablename__ = "users"

    email = db.Column(db.String, index=True, primary_key=True)
    password = db.Column(db.String)
    role = db.Column(db.String, default="student")
