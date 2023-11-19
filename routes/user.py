from db import db
from flask import current_app, request
from pydantic import ValidationError
from schemas.user import UserRegistrationData, UserLoginData
from db.models.user import User
from core.security import get_hashed_password, verify_password

from flask_restx import Namespace, Resource
from flask_login import login_required, login_user, logout_user
from app import login_manager

api = Namespace("user", description="User related operations (login, logout, register)")


@api.route("/register")
class UserRegistration(Resource):
    """
    Register a new user
    """

    def post(self):
        current_app.logger.info("POST user/register request received")
        # extract user data
        try:
            user_data = UserRegistrationData(**request.get_json())
        except ValidationError as e:
            current_app.logger.error("Validation error: {}".format(e.errors()))
            return {"validation errors": e.errors()}, 400
        except Exception as e:
            current_app.logger.error("Exception: {}".format(str(e)))
            return {"message": str(e)}, 400

        name = user_data.name
        email = user_data.email
        password = user_data.password

        # check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            current_app.logger.error("User already exists")
            return {"message": "User already exists"}, 400
        # hash the password
        hashed_password = get_hashed_password(password)
        # create new user
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info("User created successfully ")
        return {"message": "User created successfully"}, 201


@api.route("/login")
@api.doc(params={"email": "User email", "password": "User password"})
class UserLogin(Resource):
    """
    Login a user
    """

    def post(self):
        current_app.logger.info("POST user/login request received")
        # extract user data from json body
        try:
            user_data = UserLoginData(**request.get_json())
        except ValidationError as e:
            current_app.logger.error("Validation error: {}".format(e.errors()))
            return {"validation errors": e.errors()}, 400
        email = user_data.email
        password = user_data.password

        # check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            current_app.logger.error("User does not exist")
            return {"message": "User does not exist"}, 400
        # check if password is correct
        if not verify_password(password.encode("utf-8"), user.password):
            current_app.logger.error("Incorrect password has been provided")
            return {"message": "Incorrect password"}, 400

        # login using flask_login
        login_user(user)

        current_app.logger.info("User logged in successfully")
        return {"message": "User logged in successfully"}, 200


@api.route("/logout")
@api.doc(security="Bearer Auth")
class UserLogout(Resource):
    """
    Logout a user
    """

    @login_required
    @login_manager.user_loader
    @api.doc(responses={200: "User logged out successfully"})
    def post(self):
        current_app.logger.info("POST user/logout request received")
        logout_user()
        current_app.logger.info("User logged out successfully")
        return {"message": "User logged out successfully"}, 200
