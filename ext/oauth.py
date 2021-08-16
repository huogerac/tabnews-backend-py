import os
from authlib.integrations.flask_client import OAuth

oauth = OAuth()


def init_app(app):
    oauth.init_app(app)
    oauth.register(
        name="github",
        client_id=os.getenv("GITHUB_CLIENT_ID"),
        client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
        access_token_url="https://github.com/login/oauth/access_token",
        access_token_params=None,
        authorize_url="https://github.com/login/oauth/authorize",
        authorize_params=None,
        api_base_url="https://api.github.com/",
        client_kwargs={
            "scope": "user:email",
        },
    )
