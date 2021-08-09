from unittest.mock import ANY
from models.news import Tabnews
from services import tabnews


def test_should_list_tabnews(db_session, user_mock):

    # Given a Tabnews
    new_tabnews = Tabnews(
        title="First tabnews",
        description="This is the first tabnews",
        author_id=user_mock.id,
    )
    db_session.add(new_tabnews)
    db_session.commit()

    # When we list tabnews
    my_news = tabnews.list_tabnews()

    # Then
    assert my_news == [
        {
            "author": {
                "avatar": user_mock.avatar,
                "created_at": ANY,
                "email": user_mock.email,
                "id": user_mock.id,
                "name": user_mock.name,
            },
            "created_at": ANY,
            "description": "This is the first tabnews",
            "id": ANY,
            "title": "First tabnews",
        },
    ]
