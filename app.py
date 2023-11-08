from init import app, db
import logging
from routes.user import UserRegistrationView, UserLoginView
from routes.movie import MovieView
from routes.search import SearchView

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a')

app.add_url_rule("/user/register", view_func=UserRegistrationView.as_view("user_register"), methods=["POST"])
app.add_url_rule("/user/login", view_func=UserLoginView.as_view("user_login"), methods=["POST"])
app.add_url_rule("/movie", view_func=MovieView.as_view("movie"), methods=["POST", "GET"])
app.add_url_rule("/movie/<int:movie_id>", view_func=MovieView.as_view("movie_id_route"), methods=["GET", "PUT", "DELETE"])
app.add_url_rule("/movie/search", view_func=SearchView.as_view("search"), methods=["GET"])


@app.cli.command("db_create")
def db_create():
    db.create_all()

    print('finished creating database')
    app.logger.info("Database has been created successfully!")

