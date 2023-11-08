import bcrypt

def get_hashed_password(password:str)->bytes:
    """
    Hash a password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password:bytes, hashed_password:bytes)->bool:
    """
    Verify a password
    """
    return bcrypt.checkpw(password, hashed_password)
