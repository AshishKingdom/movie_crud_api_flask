from pydantic import BaseModel
from datetime import date

class UserRegistrationData(BaseModel):
    """User registration data schema"""
    name: str
    email: str
    password: str

class UserLoginData(BaseModel):
    """User login data schema"""
    email: str
    password: str

class MovieData(BaseModel):
    """Movie data schema"""
    title: str
    description: str
    release_date: date
    director: str
    genre:str
    avg_rating: float
    ticket_price: float
    cast: str