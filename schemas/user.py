from pydantic import BaseModel, EmailStr, Field, validator


class UserRegistrationData(BaseModel):
    """User registration data schema"""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)

    @validator("password")
    def is_good_password(cls, value):
        """Validate password"""
        if not any(char.isdigit() for char in value):
            raise Exception("password must contain at least one digit")
        if not any(char.isupper() for char in value):
            raise Exception("password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise Exception("password must contain at least one lowercase letter")
        return value


class UserLoginData(BaseModel):
    """User login data schema"""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)
