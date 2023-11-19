from init import app, db, login_manager
import logging
from db.models.user import User

# from routes.user import UserRegistrationView, UserLoginView
# from routes.movie import MovieView
# from routes.search import SearchView
from routes.base import api

api.init_app(app)

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="a")

# app.add_url_rule("/user/register", view_func=UserRegistrationView.as_view("user_register"), methods=["POST"])
# app.add_url_rule("/user/login", view_func=UserLoginView.as_view("user_login"), methods=["POST"])
# app.add_url_rule("/movie", view_func=MovieView.as_view("movie"), methods=["POST", "GET"])
# app.add_url_rule("/movie/<int:movie_id>", view_func=MovieView.as_view("movie_id_route"), methods=["GET", "PUT", "DELETE"])
# app.add_url_rule("/movie/search", view_func=SearchView.as_view("search"), methods=["GET"])


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.cli.command("db_create")
def db_create():
    db.create_all()

    app.logger.info("Database has been created successfully!")
