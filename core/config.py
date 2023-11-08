from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

class AppConfig:
    """
    Application configuration
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = int(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    TOKEN_EXPIRE_TIME = timedelta(seconds=int(os.getenv('TOKEN_EXPIRE_TIME')))