from db import db


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
    # user_id is a foreign key
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # created_by = db.relationship("User", backref="movies")
