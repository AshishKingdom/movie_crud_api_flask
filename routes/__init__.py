from flask_restx import Api

from .user import api as user_ns

api = Api(title="Movie API", version="1.0", description="A simple movie API")

api.add_namespace(user_ns, path="/user")
