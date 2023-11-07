from init import app, db, movie_schema, movies_schema
from flask import request, jsonify
from schemas import UserRegistrationData, UserLoginData, MovieData
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, create_access_token
import bcrypt
from datetime import date
from models import User, Movie





# Movie related functions and routes
@app.route("/movies/create", methods=["POST"])
@jwt_required()
def create_movie()->dict:
    """
    Create a new movie entry in the database
    """
    # data validation of movie data from request body
    try:
        movie_data = MovieData(**request.get_json())
    except ValidationError as e:
        return jsonify({"validation errors":e.errors()}), 400
    
    # check if the rating is between 1 to 10
    if not 1 <= movie_data.avg_rating <= 10:
        return jsonify({"message": "Average rating must be between 1 to 10"}), 400
    
    #check if release date is not in future
    if movie_data.release_date > date.today():
        return jsonify({"message": "Release date must be in the past"}), 400
    
    # insert movie data into database

    new_movie = Movie(title=movie_data.title, 
                      description=movie_data.description,
                      release_date=movie_data.release_date,
                      director=movie_data.director,
                      genre=movie_data.genre, 
                      avg_rating=movie_data.avg_rating, 
                      ticket_price=movie_data.ticket_price,
                      cast=movie_data.cast)
    
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({"message": "Movie created successfully"}), 201


@app.route("/movies/update/<int:movie_id>", methods=["PUT"])
@jwt_required()
def update_movie(movie_id:int)->dict:
    """
    Update a movie entry in the database
    """
    # data validation of movie data from request body
    try:
        movie_data = MovieData(**request.get_json())
    except ValidationError as e:
        return jsonify({"validation errors":e.errors()}), 400
    
    # check if the rating is between 1 to 10
    if not 1 <= movie_data.avg_rating <= 10:
        return jsonify({"message": "Average rating must be between 1 to 10"}), 400
    
    #check if release date is not in future
    if movie_data.release_date > date.today():
        return jsonify({"message": "Release date must be in the past"}), 400
    
    # update movie data in database
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"message": "Movie does not exist"}), 400

    movie.title = movie_data.title
    movie.description = movie_data.description
    movie.release_date = movie_data.release_date
    movie.director = movie_data.director
    movie.genre = movie_data.genre
    movie.avg_rating = movie_data.avg_rating
    movie.ticket_price = movie_data.ticket_price
    movie.cast = movie_data.cast

    db.session.commit()

    return jsonify({"message": "Movie updated successfully"}), 200

@app.route("/movies/delete/<int:movie_id>", methods=["DELETE"])
@jwt_required()
def delete_movie(movie_id:int)->dict:
    """
    Delete a movie entry from the database
    """
    # delete movie from database
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"message": "Movie does not exist"}), 400

    db.session.delete(movie)
    db.session.commit()

    return jsonify({"message": "Movie deleted successfully"}), 200

@app.route("/movies/get/<int:movie_id>", methods=["GET"])
def get_movie_by_id(movie_id:int)->dict:
    """
    Get a movie entry from the database by id
    """
    # get movie from database
    print(movie_id)
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"message": "Movie does not exist"}), 400

    result = movie_schema.dump(movie)
    return jsonify(result), 200


@app.route("/movies/get/all", methods=["GET"])
def get_all_movies()->dict:
    """
    Get all movies from the database movies in the requested page sorted by the requested sort_by parameter
    """
    page = request.args.get("page", 1, type=int)
    sort_by = request.args.get("sort_by", "none", type=str)
    filter_by = request.args.get("filter_by", "none", type=str)
    filter_value = request.args.get("filter_value", "", type=str)

    # sort_by can only be "release_data" or "price"
    if sort_by not in ["release_date", "price", "none"]:
        return jsonify({"message": "Invalid sort_by parameter"}), 400
    
    # page can only integer greater than 0
    if page < 1:
        return jsonify({"message": "Invalid page number"}), 400
    
    # filter_by can only be "genre", "director" or "release_year"
    if filter_by not in ["genre", "director", "release_year", "none"]:
        return jsonify({"message": "Invalid filter_by parameter"}), 400

    # get all movies from database
    movies = Movie.query.all()
    if not movies:
        return jsonify({"message": "No movies found"}), 400
    
    # sort movies by release date or price
    if sort_by == "release_date":
        movies.sort(key=lambda x: x.release_date)
    elif sort_by == "price":
        movies.sort(key=lambda x: x.ticket_price)
    
    # apply filter_by parameter with the help of filter_value parameter
    if filter_by == "genre":
        movies = [movie for movie in movies if filter_value.lower() in movie.genre.lower()]
    elif filter_by == "director":
        movies = [movie for movie in movies if filter_value.lower() in movie.director.lower()]
    elif filter_by == "release_year":
        movies = [movie for movie in movies if filter_value in str(movie.release_date.year)]

    # checking if the page number is consistent with the number of movies 
    # given that there are 10 movies per page
    if page > len(movies) // 10 + 1:
        return jsonify({"message": "Invalid page number"}), 400
    
    # return movies in the requested page
    result = movies_schema.dump(movies[(page-1)*10:page*10])
    return jsonify(result), 200
    

@app.route("/movies/search", methods=["GET"])
def get_search_movie()->dict:
    """
    Get all movies from the database that match the search criteria
    """
    search_param = request.args.get("search_param", "", type=str)
    search_value = request.args.get("search_value", "", type=str)

    # search_param can only be "title", "genre", "description", "director" or "cast"
    if search_param not in ["title", "genre", "description", "director", "cast"]:
        return jsonify({"message": "Invalid search parameter"}), 400
    
    # search value can not be empty
    if not search_value or search_value == "":
        return jsonify({"message": "Invalid search value"}), 400
    
    # search the database for movies that match the search criteria
    movies = Movie.query.all()
    if not movies:
        return jsonify({"message": "No movies found"}), 400
    
    movies = [movie for movie in movies if search_value.lower() in getattr(movie, search_param).lower()]

    result = movies_schema.dump(movies)

    return jsonify(result), 200


# User related functions and routes

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

@app.route("/user/register", methods=["POST"])
def register()->dict:
    """
    Register a new user
    """
    # extract user data
    try:
        user_data = UserRegistrationData(**request.get_json())
    except ValidationError as e:
        return jsonify({"validation errors":e.errors()}), 400
    
    name = user_data.name
    email = user_data.email
    password = user_data.password

    # check if user already exists
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "User already exists"}), 400
    # hash the password
    hashed_password = get_hashed_password(password)
    # create new user
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


@app.route("/user/login", methods=["POST"])
def login()->dict:
    """
    Login a user
    """
    # extract user data from json body
    try:
        user_data = UserLoginData(**request.get_json())
    except ValidationError as e:
        return jsonify({"validation errors":e.errors()}), 400
    email = user_data.email
    password = user_data.password

    # check if user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User does not exist"}), 400
    # check if password is correct
    if not verify_password(password.encode('utf-8'), user.password):
        return jsonify({"message": "Incorrect password"}), 400
    # generate access token
    access_token = create_access_token(identity=email)
    return jsonify({"access_token": access_token}), 200




if __name__ == "__main__":
    app.run(debug=True)