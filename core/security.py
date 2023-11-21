import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity


def get_hashed_password(password: str) -> bytes:
    """
    Hash a password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: bytes, hashed_password: bytes) -> bool:
    """
    Verify a password
    """
    return bcrypt.checkpw(password, hashed_password)


def admin_login_required(f):
    """
    Validate if the user is logged in as an admin
    """

    @jwt_required()
    def wrapper(*args, **kwargs):
        # get the identity of the current user
        identity = get_jwt_identity()
        # check if the user is logged in as an admin
        if identity.get("role") != "admin":
            return {"message": "Admin login required"}, 401
        return f(*args, **kwargs)

    return wrapper
