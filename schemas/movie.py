from pydantic import BaseModel, validator, Field, EmailStr
from datetime import date
import regex as re
from routes import api
from flask_restx import Model, fields


class MovieData(BaseModel):
    """Movie data schema"""

    title: str = Field(..., min_length=2, max_length=50)
    description: str = Field(..., min_length=15, max_length=250)
    release_date: date = Field(..., description="Date format: YYYY-MM-DD")
    director: str = Field(..., min_length=2, max_length=50)
    genre: str = Field(..., min_length=2, max_length=50)
    avg_rating: float = Field(..., ge=1, le=10)
    ticket_price: float = Field(..., ge=0)
    cast: str = Field(..., min_length=2, max_length=200)
    user_id: EmailStr = None

    @validator("release_date")
    def is_valid_date(cls, v):
        re_exp = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not re_exp.match(str(v)):
            raise Exception("Invalid date format")
        if v > date.today():
            raise Exception("Release date must be in the past")
        return v

    @validator("title", "description", "director", "genre", "cast")
    def is_valid_content_string(cls, v):
        reg_exp = re.compile(r"^[a-zA-Z0-9_\.!, -]*$")
        if not reg_exp.match(v):
            raise Exception("Invalid characters in {}".format(v))
        return v


movie_data_response = Model(
    "MovieDataResponse",
    {
        "id": fields.Integer,
        "title": fields.String,
        "description": fields.String,
        "release_date": fields.Date,
        "director": fields.String,
        "genre": fields.String,
        "avg_rating": fields.Float,
        "ticket_price": fields.Float,
        "cast": fields.String,
        "created_by_id": fields.String,
    },
)
