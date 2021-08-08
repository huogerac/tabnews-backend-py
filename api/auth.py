from services import auth as auth_services


def login(body):
    return auth_services.authenticate(email=body["email"], password=body["password"])
