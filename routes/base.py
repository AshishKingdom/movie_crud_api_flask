from routes import api 

from routes.api.user import api as user_ns
from routes.api.movie import api as movie_ns

api.add_namespace(user_ns, path="/user")
api.add_namespace(movie_ns)