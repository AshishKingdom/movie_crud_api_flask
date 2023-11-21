from db import db
from core.config import AppConfig
from flask import current_app, request
from pydantic import ValidationError
from schemas.user import UserRegistrationData, UserLoginData
from db.models.user import User
from core.security import get_hashed_password, verify_password, admin_login_required

from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_current_user, create_access_token

api = Namespace("user", description="User related operations (login, logout, register)")


@api.route("/register")
class UserRegistration(Resource):
    """
    Register a admin user
    """

    def post(self):
        current_app.logger.info("POST user/register request received")

        # verifying the API secret key
        if (
            request.headers.get("x-api-secret-key")
            != current_app.config["API_SECRET_KEY"]
        ):
            current_app.logger.error("Incorrect API secret key")
            return {"message": "Incorrect API secret key"}, 401

        # extract user data
        try:
            user_data = UserRegistrationData(**request.get_json())
        except ValidationError as e:
            current_app.logger.error("Validation error: {}".format(e.errors()))
            return {"validation errors": e.errors()}, 400
        except Exception as e:
            current_app.logger.error("Exception: {}".format(str(e)))
            return {"message": str(e)}, 400

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
        new_user = User(email=email, password=hashed_password, role="admin")

        db.session.add(new_user)
        db.session.commit()

        current_app.logger.info("Admin User created successfully ")
        return {"message": "Admin User created successfully"}, 201


@api.route("/login")
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

        access_token = create_access_token(
            identity={"email": user.email, "role": user.role},
            expires_delta=AppConfig.TOKEN_EXPIRE_TIME,
        )

        current_app.logger.info("Access token granted to the user.")
        return {"access_token": access_token}, 200


@api.route("/test_admin_user")
class TestAdminUser(Resource):
    """
    Test admin login required decorator
    """

    @admin_login_required
    def get(self):
        current_app.logger.info("GET user/test_admin_user request received")
        return {"message": "Admin login required test passed"}, 200
