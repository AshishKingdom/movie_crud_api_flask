from flask import request, current_app
from db.models.movie import Movie
from init import db
from schemas.movie import MovieData, movie_data_response
from pydantic import ValidationError

from flask_restx import Namespace, Resource
from flask_login import login_required, current_user

api = Namespace("movie", description="Movie related functions and routes")


@api.route("/")
class MovieCreationAndFetching(Resource):
    """
    Movie related functions and routes
    """

    @login_required
    def post(self):
        """
        Create a new movie entry in the database
        """

        current_app.logger.info("POST /movie request received.")
        # data validation of movie data from request body
        try:
            movie_data = MovieData(**request.get_json())
        except ValidationError as e:
            current_app.logger.error("Validation error: {}".format(e.errors()))
            return {"validation errors": e.errors()}, 400
        except Exception as e:
            current_app.logger.error("Exception: {}".format(str(e)))
            return {"message": str(e)}, 400

        # insert movie data into database
        movie_data.user_id = current_user.id

        new_movie = Movie(
            title=movie_data.title,
            description=movie_data.description,
            release_date=movie_data.release_date,
            director=movie_data.director,
            genre=movie_data.genre,
            avg_rating=movie_data.avg_rating,
            ticket_price=movie_data.ticket_price,
            cast=movie_data.cast,
            user_id=movie_data.user_id,
        )

        db.session.add(new_movie)
        db.session.commit()

        current_app.logger.info(
            "Movie created successfully id: {}".format(new_movie.id)
        )
        return {"message": "Movie created successfully"}, 201

    @api.marshal_with(movie_data_response)
    def get(self):
        """
        Get all movies from the database movies in the requested page sorted by the requested sort_by parameter
        """
        current_app.logger.info("GET /movie request received.")

        page = request.args.get("page", 1, type=int)
        movies_per_page = request.args.get("movies_per_page", 10, type=int)
        sort_by = request.args.get("sort_by", "none", type=str)
        order_by = request.args.get("order_by", "asc", type=str)
        filter_by = request.args.get("filter_by", "none", type=str)
        filter_value = request.args.get("filter_value", "", type=str)

        # sort_by can only be "release_data" or "ticket_price"
        if sort_by not in ["release_date", "ticket_price", "none"]:
            current_app.logger.error("Invalid sort_by parameter")
            return {"message": "Invalid sort_by parameter"}, 400

        # page can only integer greater than 0
        if page < 1:
            current_app.logger.error("Invalid page number")
            return {"message": "Invalid page number"}, 400

        # filter_by can only be "genre", "director" or "release_year"
        if filter_by not in ["genre", "director", "release_year", "none"]:
            current_app.logger.error("Invalid filter_by parameter")
            return {"message": "Invalid filter_by parameter"}, 400

        # get all movies from database
        movies = None
        if sort_by == "none":
            if filter_by == "none":
                # return movie according to the page
                movie_count = Movie.query.count()
                if not movie_count:
                    current_app.logger.error("No movies found")
                    return {"message": "No movies found"}, 400
                else:
                    if page > movie_count // movies_per_page + 1:
                        current_app.logger.error("Invalid page number")
                        return {"message": "Invalid page number"}, 400
                    else:
                        movies = Movie.query.paginate(
                            page=page, per_page=movies_per_page, count=False
                        ).items
            else:
                # return movies according to the filter_by parameter
                movies = (
                    Movie.query.filter(
                        getattr(Movie, filter_by).like("%" + filter_value + "%")
                    )
                    .paginate(page=page, per_page=movies_per_page, count=False)
                    .items
                )
        else:
            if filter_by == "none":
                # return movies according to the sort_by parameter
                if order_by == "asc":
                    movies = (
                        Movie.query.order_by(getattr(Movie, sort_by).asc())
                        .paginate(page=page, per_page=movies_per_page, count=False)
                        .items
                    )
                else:
                    movies = (
                        Movie.query.order_by(getattr(Movie, sort_by).desc())
                        .paginate(page=page, per_page=movies_per_page, count=False)
                        .items
                    )
            else:
                # return movies according to the sort_by and filter_by parameters
                if order_by == "asc":
                    movies = (
                        Movie.query.filter(
                            getattr(Movie, filter_by).like("%" + filter_value + "%")
                        )
                        .order_by(getattr(Movie, sort_by).asc())
                        .paginate(page=page, per_page=movies_per_page, count=False)
                        .items
                    )
                else:
                    movies = (
                        Movie.query.filter(
                            getattr(Movie, filter_by).like("%" + filter_value + "%")
                        )
                        .order_by(getattr(Movie, sort_by).desc())
                        .paginate(page=page, per_page=movies_per_page, count=False)
                        .items
                    )

        if not movies:
            current_app.logger.error("No movies found")
            return {"message": "No movies found"}, 400

        current_app.logger.info("Movies retrieved successfully")
        return movies


@api.route("/<int:movie_id>")
class MovieIDOperations(Resource):
    @login_required
    def put(self, movie_id: int):
        """
        Update a movie entry in the database
        """

        current_app.logger.info("PUT /movie/<movie_id> request received.")
        # data validation of movie data from request body
        try:
            movie_data = MovieData(**request.get_json())
        except ValidationError as e:
            current_app.logger.error("Validation error: {}".format(e.errors()))
            return {"validation errors": e.errors()}, 400
        except Exception as e:
            current_app.logger.error("Exception: {}".format(str(e)))
            return {"message": str(e)}, 400

        user_id = current_user.email
        # update movie data in database
        movie = Movie.query.filter_by(id=movie_id).first()
        if not movie:
            current_app.logger.error("movie with id {} does not exist".format(movie_id))
            return {"message": "Movie does not exist"}, 400

        if movie.created_by.email != user_id:
            current_app.logger.error("You can only update movies created by you")
            return {"message": "You can only update movies created by you"}, 400

        movie.title = movie_data.title
        movie.description = movie_data.description
        movie.release_date = movie_data.release_date
        movie.director = movie_data.director
        movie.genre = movie_data.genre
        movie.avg_rating = movie_data.avg_rating
        movie.ticket_price = movie_data.ticket_price
        movie.cast = movie_data.cast

        db.session.commit()

        current_app.logger.info("Movie updated successfully id: {}".format(movie.id))
        return {"message": "Movie updated successfully"}, 200

    @login_required
    def delete(self, movie_id: int):
        """
        Delete a movie entry from the database
        """

        current_app.logger.info("DELETE /movie/<movie_id> request received.")
        user_id = current_user.email
        # delete movie from database
        movie = Movie.query.filter_by(id=movie_id).first()
        if not movie:
            current_app.logger.error("movie with id {} does not exist".format(movie_id))
            return {"message": "Movie does not exist"}, 400

        if movie.created_by.email != user_id:
            current_app.logger.error("You can only delete movies created by you")
            return {"message": "You can only delete movies created by you"}, 400

        db.session.delete(movie)
        db.session.commit()

        current_app.logger.info("Movie deleted successfully id: {}".format(movie.id))
        return {"message": "Movie deleted successfully"}, 200

    @api.marshal_with(movie_data_response)
    def get(self, movie_id: int):
        """
        Get a movie entry from the database by id
        """

        # get movie from database
        if movie_id is not None:
            current_app.logger.info("GET /movie/<movie_id> request received.")
            movie = Movie.query.filter_by(id=movie_id).first()
            if not movie:
                current_app.logger.error(
                    "movie with id {} does not exist".format(movie_id)
                )
                return {"message": "Movie does not exist"}, 400

            current_app.logger.info(
                "Movie retrieved successfully id: {}".format(movie.id)
            )
            return movie, 200
        else:
            return {"message": "Invalid movie id"}, 400


@api.route("/search")
class MovieSearchAPI(Resource):
    """
    Search functionality
    """

    @api.marshal_with(movie_data_response)
    def get(self):
        """
        Get all movies from the database that match the search criteria
        """
        current_app.logger.info("GET /movie/search request received.")

        search_param = request.args.get("search_param", "", type=str)
        search_value = request.args.get("search_value", "", type=str)
        page = request.args.get("page", 1, type=int)
        movies_per_page = request.args.get("movies_per_page", 10, type=int)

        # search_param can only be "title", "genre", "description", "director" or "cast"
        if search_param not in ["title", "genre", "description", "director", "cast"]:
            current_app.logger.error("Invalid search parameter provided")
            return {"message": "Invalid search parameter"}, 400

        # search value can not be empty
        if not search_value or search_value == "":
            current_app.logger.error("Invalid search value provided")
            return {"message": "Invalid search value"}, 400

        # search the database for movies that match the search criteria
        movies = (
            Movie.query.filter(
                getattr(Movie, search_param).like("%{}%".format(search_value))
            )
            .paginate(page=page, per_page=movies_per_page, count=False)
            .items
        )

        if not movies:
            current_app.logger.error("No movies found")
            return {"message": "No movies found"}, 400

        current_app.logger.info("GET /movie/search request successful.")
        return movies, 200
