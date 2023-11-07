from init import db
from dataclasses import dataclass

@dataclass
class User(db.Model):
    """
    User model with the following attributes:
    - id: primary key
    - name: user name
    - email: user email
    - password: user password
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)


@dataclass
class Movie(db.Model):
    """
    Movie model with the following attributes:
    - id: primary key
    - title: movie title
    - description: movie description
    - release_date: movie release date
    - director: movie director
    - genre: movie genre
    - avg_rating: movie average rating
    - ticket_price: movie ticket price
    - cast: movie cast
    """
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    release_date = db.Column(db.Date)
    director = db.Column(db.String)
    genre = db.Column(db.String)
    avg_rating = db.Column(db.Float)
    ticket_price = db.Column(db.Float)
    cast = db.Column(db.String)