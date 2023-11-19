from init import db, ma
from dataclasses import dataclass

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
    # release date is stored in the format YYYY-MM-DD
    release_date = db.Column(db.Date)
    director = db.Column(db.String)
    genre = db.Column(db.String)
    avg_rating = db.Column(db.Float)
    ticket_price = db.Column(db.Float)
    cast = db.Column(db.String)
    created_by_id = db.Column(db.String)


class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'release_date', 'director', 'genre', 'avg_rating', 'ticket_price', 'cast', 'created_by')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)