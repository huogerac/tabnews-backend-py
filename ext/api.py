import connexion


def create_api_app(version="/"):
    connexion_app = connexion.FlaskApp(
        __name__,
        specification_dir="../api/",
        options={
            "swagger_url": "api",
        },
    )
    connexion_app.add_api("openapi.yaml", validate_responses=True, base_path=version)

    app = connexion_app.app

    return app
