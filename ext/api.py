import os
import connexion
from flask_cors import CORS

from exceptions import UnauthorizedException


def create_api_app(version="/"):
    connexion_app = connexion.FlaskApp(
        __name__,
        specification_dir="../api/",
        options={
            "swagger_url": "api",
        },
    )
    connexion_app.add_api("openapi.yaml", validate_responses=True, base_path=version)

    cors_origin = os.getenv("CORS_ALLOW_ORIGIN")
    if cors_origin:
        api_cors = {
            "origins": [cors_origin],
        }
        CORS(connexion_app.app, resources={"/*": api_cors})

    app = connexion_app.app

    @app.errorhandler(UnauthorizedException)
    def unauthorized_handler(error):  # pylint: disable=W0612
        return {
            "detail": str(error),
            "status": 401,
            "title": "Unauthorized Request",
        }, 401

    return app
