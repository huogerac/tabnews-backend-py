from werkzeug.security import generate_password_hash

from models.users import User
from ext.database import db
from exceptions import ConflictValueException


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def create_user(name, email, password):
    password_hash = None
    if password:
        password_hash = generate_password_hash(password)

    if User.query.filter_by(email=email).first():
        raise ConflictValueException(f"Email already in use")

    new_user = User(
        name=name,
        email=email,
        password=password_hash,
    )
    db.session.add(new_user)
    db.session.commit()

    return new_user.to_dict()


def get_or_create_user_by_oauth_login(email, name, avatar):
    # ADD: provider, provider_id, oauth_dict
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email, avatar=avatar)
        db.session.add(user)
        db.session.commit()
    return user.to_dict()
