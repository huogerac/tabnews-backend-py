from models.news import Tabnews
from ext.database import db

from services.users import get_user_by_email


def list_tabnews():
    tabnews = Tabnews.query.order_by(Tabnews.id.desc()).all()
    return [t.to_dict() for t in tabnews]


def create_tabnews(title, description, author_email):
    user = get_user_by_email(author_email)
    tabnews = Tabnews(
        title=title,
        description=description,
        author_id=user.id,
    )
    db.session.add(tabnews)
    db.session.commit()
    return tabnews.to_dict()
