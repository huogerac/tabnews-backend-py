from werkzeug.security import generate_password_hash

from models.users import User
from ext.database import db
from exceptions import ConflictValueException


def list_users():
    users = User.query.all()
    return [user.to_dict() for user in users]


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
