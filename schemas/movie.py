from pydantic import BaseModel, validator, Field, EmailStr
from datetime import date

class MovieData(BaseModel):
    """Movie data schema"""

    title: str = Field(..., min_length=2, max_length=50)
    description: str = Field(..., min_length=15, max_length=250)
    release_date: date = Field(..., description="Date format: YYYY-MM-DD")
    director: str = Field(..., min_length=2, max_length=50)
    genre:str = Field(..., min_length=2, max_length=50)
    avg_rating: float = Field(..., ge=1, le=10)
    ticket_price: float = Field(..., ge=0)
    cast: str = Field(..., min_length=2, max_length=200)
    created_by_id:EmailStr = None

    @validator("release_date")
    def is_date_past(cls, v):
        if v > date.today():
            raise Exception("Release date must be in the past")
        return v