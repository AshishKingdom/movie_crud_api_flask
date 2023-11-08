from init import db
from flask import current_app, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from pydantic import ValidationError
from schemas.user import UserRegistrationData, UserLoginData
from models.user import User
from core.security import get_hashed_password, verify_password
from core.config import AppConfig

class UserRegistrationView(MethodView):
    """
    Register a new user
    """
    def post(self)->dict:
        current_app.logger.info("POST user/register request received")
        # extract user data
        try:
            user_data = UserRegistrationData(**request.get_json())
        except ValidationError as e:
            current_app.logger.error("Validation error: {}".format(e.errors()))
            return jsonify({"validation errors":e.errors()}), 400
        except Exception as e:
            current_app.logger.error("Exception: {}".format(str(e)))
            return jsonify({"message": str(e)}), 400
        
        name = user_data.name
        email = user_data.email
        password = user_data.password

        # check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            current_app.logger.error("User already exists")
            return jsonify({"message": "User already exists"}), 400
        # hash the password
        hashed_password = get_hashed_password(password)
        # create new user
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info("User created successfully id: {}".format(new_user.id))
        return jsonify({"message": "User created successfully"}), 201


class UserLoginView(MethodView):
    """
    Login a user
    """
    def post(self)->dict:
        current_app.logger.info("POST user/login request received")
        # extract user data from json body
        try:
            user_data = UserLoginData(**request.get_json())
        except ValidationError as e:
            current_app.logger.error("Validation error: {}".format(e.errors()))
            return jsonify({"validation errors":e.errors()}), 400
        email = user_data.email
        password = user_data.password

        # check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            current_app.logger.error("User does not exist")
            return jsonify({"message": "User does not exist"}), 400
        # check if password is correct
        if not verify_password(password.encode('utf-8'), user.password):
            current_app.logger.error("Incorrect password has been provided")
            return jsonify({"message": "Incorrect password"}), 400
        # generate access token
        access_token = create_access_token(identity=email, expires_delta=AppConfig.TOKEN_EXPIRE_TIME)
        current_app.logger.info("User logged in successfully")
        return jsonify({"access_token": access_token}), 200