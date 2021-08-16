import os


def init_app(app):
    config = get_config_from_env()
    app.config.from_object(config)


def get_config_from_env():
    envname = os.getenv("FLASK_ENV", "development").lower()
    if envname == "production":
        return ProductionConfig()
    return DevelopmentConfig()


class ProductionConfig:  # pylint: disable=R0903
    # FLASK
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "Ch@nG3_th1s_IN_PR0D!")

    # DATABASE
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AUTH and JWT
    JWT_ISS = os.getenv("JWT_ISS", "https://tabnews.com.br")
    JWT_AUD = os.getenv("JWT_AUD", "auth.tabnews.com.br")
    JWT_EXPIRE_DAYS = int(os.getenv("JWT_EXPIRE_DAYS", "10"))
    JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "0"))
    JWT_RTOKEN_EXPIRE_DAYS = int(os.getenv("JWT_RTOKEN_EXPIRE_DAYS", "180"))

    # AUTH and OAuth
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


class DevelopmentConfig(ProductionConfig):  # pylint: disable=R0903
    FLASK_ENV = "development"
    DEBUG = True
