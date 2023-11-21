from init import app, db
import logging
from db.models.user import User
from routes.base import api

api.init_app(app)

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="a")


@app.cli.command("db_create")
def db_create():
    db.create_all()

    app.logger.info("Database has been created successfully!")
