from werkzeug.security import check_password_hash

from models.users import User
from services import token as token_services
from exceptions import UnauthorizedException


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    INVALID_LOGIN_MSG = "Email or password invalid"
    if not user:
        raise UnauthorizedException(INVALID_LOGIN_MSG)

    valid_password = check_password_hash(user.password, password)
    if not valid_password:
        raise UnauthorizedException(INVALID_LOGIN_MSG)

    token = token_services.generate_token(user)
    refresh_token = token_services.generate_refresh_token(user)

    return {
        "user": user.to_dict(),
        "token": token,
        "refresh_token": refresh_token,
    }
