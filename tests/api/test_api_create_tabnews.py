import mock


def test_should_return_401_not_authorized(client):

    # Given a request with no authorization
    response = client.post("/api/tabnews")

    # Then
    assert response.status_code == 401
    assert response.json["detail"] == "No authorization token provided"


def test_should_return_401_invalid_token(client):

    # Given a request with an invalid JWT Token
    response = client.post(
        "/api/tabnews",
        headers={"Authorization": "Bearer iNvAliD.TokEn"},
    )

    # Then
    assert response.status_code == 401
    assert response.json["detail"] == "Invalid token: Not enough segments"


def test_should_return_403_not_allowed(valid_token_with_no_permissions_mock, client):

    # Given a request with a valid Token, but no "tabnews:create" scope
    response = client.post(
        "/api/tabnews",
        headers={
            "Authorization": "Bearer {}".format(valid_token_with_no_permissions_mock)
        },
    )

    # Then
    assert response.status_code == 403
    assert response.json["detail"] == "Provided token doesn't have the required scope"


def test_should_return_bad_request(valid_token_mock, client):
    # Given a request with no input data (body)
    response = client.post(
        "/api/tabnews",
        headers={"Authorization": "Bearer {}".format(valid_token_mock)},
    )

    # Then
    assert response.status_code == 400
    assert response.json["detail"] == "None is not of type 'object'"


def test_should_return_no_additional_field_allowed(valid_token_mock, client):
    # Given a request with an addition field in the body request
    response = client.post(
        "/api/tabnews",
        headers={"Authorization": "Bearer {}".format(valid_token_mock)},
        json={"field1": "blá"},
    )

    # Then
    assert response.status_code == 400
    assert (
        response.json["detail"]
        == "Additional properties are not allowed ('field1' was unexpected)"
    )


def test_should_return_title_is_a_required_field(valid_token_mock, client):
    # Given a request with a missing field
    response = client.post(
        "/api/tabnews",
        headers={"Authorization": "Bearer {}".format(valid_token_mock)},
        json={},
    )

    # Then
    assert response.status_code == 400
    assert response.json["detail"] == "'title' is a required property"


def test_should_reject_title_less_than_min_title_length(valid_token_mock, client):
    # Given a request with an invalid title
    response = client.post(
        "/api/tabnews",
        headers={"Authorization": "Bearer {}".format(valid_token_mock)},
        json={"title": "tiny-title"},
    )

    # Then
    assert response.status_code == 400
    assert response.json["detail"] == "'tiny-title' is too short - 'title'"


@mock.patch("services.tabnews.create_tabnews")
def test_should_finally_create_a_tabnews(tabnews_mock, valid_token_mock, client):

    title = "An valid and interesting title"
    description = "A more detailed explanation about the title..."

    create_mock_response = {
        "id": 42,
        "title": title,
        "description": description,
        "created_at": "2021-08-18T19:18:14.602071+00:00",
        "author": {
            "id": 2,
            "name": "John Doe",
            "avatar": None,
        },
    }
    tabnews_mock.return_value = create_mock_response

    # Given a request with an invalid title
    response = client.post(
        "/api/tabnews",
        headers={"Authorization": "Bearer {}".format(valid_token_mock)},
        json={
            "title": title,
            "description": description,
        },
    )

    # Then
    assert response.status_code == 201
    assert response.json == create_mock_response
