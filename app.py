from ext import configuration, api, database, oauth
from models.users import *


def create_app(**config):

    app = api.create_api_app()
    configuration.init_app(app, **config)
    database.init_app(app)
    oauth.init_app(app)
    return app
