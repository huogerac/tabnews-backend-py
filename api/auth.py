from flask import url_for, redirect, current_app

from ext.oauth import oauth
from services import auth as auth_services
from services import users as users_services


def login(body):
    return auth_services.authenticate(email=body["email"], password=body["password"])


def github_login():
    redirect_uri = url_for("/.api_auth_github_authorize", _external=True)
    return oauth.github.authorize_redirect(redirect_uri)


def github_authorize():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get("user", token=token)
    profile = resp.json()
    user = users_services.get_or_create_user_by_oauth_login(
        email=profile["email"],
        name=profile.get("name"),
        avatar=profile.get("avatar_url"),
    )

    authentication = auth_services.oauth_authenticate(user["email"])

    redirect_uri = "{}/authorize?token={}&refresh_token={}".format(
        current_app.config["CLIENT_SERVER_URL"],
        authentication["token"],
        authentication["refresh_token"],
    )
    return redirect(redirect_uri, code=302)

    # auth_id, secret_key = auth_services.save_authorization(
    #     email=user.get("email"),
    #     nome=user.get("name"),
    #     avatar=user.get("picture"),
    #     provider=user.get("iss"),
    #     provider_id=user.get("sub"),
    #     oauth_dict=user,
    #     return_key="nonce",
    # )
    # redirect_uri = "{}/#/authorize/{}?secret_key={}".format(
    #     config.CLIENT_SERVER_URL,
    #     auth_id,
    #     secret_key,
    # )
    # return redirect(redirect_uri, code=302)
    # {
    #     avatar_url: "https://avatars.githubusercontent.com/u/962233?v=4",
    #     bio: "Programmer",
    #     blog: "https://huogerac.hashnode.dev",
    #     company: "Billcode",
    #     created_at: "2011-08-05T23:00:51Z",
    #     email: "huogerac@gmail.com",
    #     gravatar_id: "",
    #     html_url: "https://github.com/huogerac",
    #     location: "São José dos Campos",
    #     login: "huogerac",
    #     name: "Roger Camargo",
    #     id: 962233,
    #     node_id: "MDQ6VXNlcjk2MjIzMw==",
    # }
    # return profile
