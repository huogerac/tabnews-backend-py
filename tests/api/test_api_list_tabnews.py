import mock


@mock.patch("services.tabnews.list_tabnews")
def test_should_return_an_empty_user_list(tabnews_mock, client):
    tabnews_mock.return_value = []

    response = client.get("/api/tabnews")

    assert response.status_code == 200
    assert response.json == []


@mock.patch("services.tabnews.list_tabnews")
def test_should_list_all_tabnews(tabnews_mock, client):
    list_mock = [
        {
            "id": 1,
            "title": "Tabnews 1",
            "description": "The first tabnews row",
            "created_at": "2021-07-29T20:28:42.429307+00:00",
            "author": {
                "id": 1,
                "name": "John",
                "avatar": "https://my-avatar.png",
                "email": "j@abc.com",
                "created_at": "2021-07-29T20:28:42.429307+00:00",
            },
        }
    ]
    tabnews_mock.return_value = list_mock

    response = client.get("/api/tabnews")

    assert response.json == list_mock
