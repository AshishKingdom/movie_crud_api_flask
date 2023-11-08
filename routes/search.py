from flask import jsonify, request, current_app
from flask.views import MethodView
from models.movie import Movie, movies_schema

class SearchView(MethodView):
    """
    search functionality
    """
    def get(self)->dict:
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
            return jsonify({"message": "Invalid search parameter"}), 400
        
        # search value can not be empty
        if not search_value or search_value == "":
            current_app.logger.error("Invalid search value provided")
            return jsonify({"message": "Invalid search value"}), 400
        
        # search the database for movies that match the search criteria
        movies = Movie.query.filter(
            getattr(Movie, search_param).like("%{}%".format(search_value))).paginate(page=page, per_page=movies_per_page, count=False).items
        
        if not movies:
            current_app.logger.error("No movies found")
            return jsonify({"message": "No movies found"}), 400
        
        result = movies_schema.dump(movies)
        current_app.logger.info("GET /movie/search request successful.")
        return jsonify(result), 200