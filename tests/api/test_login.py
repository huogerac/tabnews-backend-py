import mock
from exceptions import UnauthorizedException


def test_should_get_bad_request_on_missing_password(client):
    response = client.post(
        "/api/auth/login",
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 400
    assert response.json["detail"] == "None is not of type 'object'"


@mock.patch("services.auth.authenticate")
def test_should_return_invalid_password(authenticate_mock, client):
    authenticate_mock.side_effect = UnauthorizedException("Email or password invalid")

    response = client.post(
        "/api/auth/login",
        headers={"content-type": "application/json"},
        json={
            "email": "email@invalid.com",
            "password": "123456789",
        },
    )
    assert response.status_code == 401
    assert response.json["detail"] == "Email or password invalid"


@mock.patch("services.auth.authenticate")
def test_should_return_a_token(authenticate_mock, user_mock, client):
    authenticate_mock.return_value = {
        "user": user_mock.to_dict(),
        "token": "Token.Jwt.Mock",
        "refresh_token": "Refresh.Token.Jwt.Mock",
    }

    response = client.post(
        "/api/auth/login",
        headers={"content-type": "application/json"},
        json={
            "email": "john@doe.com",
            "password": "42",
        },
    )

    assert response.status_code == 200
    assert response.json["user"] is not None
    assert response.json["token"] is not None
    assert response.json["refresh_token"] is not None
