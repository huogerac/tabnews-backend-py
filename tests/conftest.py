import pytest

import sqlalchemy as sa
from sqlalchemy.orm import Session

from app import create_app
from ext.database import db
from models.users import User


@pytest.fixture(autouse=False)
def app():
    app = create_app()
    with app.app_context():
        db.create_all(app=app)
        yield app
        db.drop_all(app=app)


@pytest.fixture(scope="function", autouse=False)
def db_session(app):
    conn = db.engine.connect()
    trans = conn.begin()

    session = Session(bind=conn)
    session.begin_nested()

    # then each time that SAVEPOINT ends, reopen it
    @sa.event.listens_for(db.session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    yield db.session

    # rollback everything
    trans.rollback()
    conn.close()
    db.session.remove()


@pytest.fixture
def user_mock(db_session):
    new_user = User(name="John Doe", email="john@doe.com")
    db_session.add(new_user)
    db_session.commit()
    return new_user


@pytest.fixture
def valid_token_mock():
    """Decode this token at https://jwt.io"""
    return "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2xvY2FsaG9zdCIsImF1ZCI6ImF1dGgubG9jYWxob3N0IiwiZXhwIjoxNjM3MDkwNDI2LCJleHBpcmVfZGF0ZSI6IjIwMjEtMTEtMTZUMTk6MjA6MjYuNzQ2Mjc1KzAwOjAwIiwic3ViIjoyLCJlbWFpbCI6ImpvaG5AZG9lLmNvbSIsIm5hbWUiOiJKb2huIERvZSIsImF2YXRhciI6bnVsbCwic2NvcGUiOlsidGFibmV3czpjcmVhdGUiXX0.XAXcwMN_elByQ0JrPR2sRS4nQHhBksSBzS_SKocMVuI"


@pytest.fixture
def valid_token_with_no_permissions_mock():
    """Decode this token at https://jwt.io"""
    return "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2xvY2FsaG9zdCIsImF1ZCI6ImF1dGgubG9jYWxob3N0IiwiZXhwIjoxNjM3MDkwNjEzLCJleHBpcmVfZGF0ZSI6IjIwMjEtMTEtMTZUMTk6MjM6MzMuNDY5NzAzKzAwOjAwIiwic3ViIjoyLCJlbWFpbCI6ImpvaG5AZG9lLmNvbSIsIm5hbWUiOiJKb2huIERvZSIsImF2YXRhciI6bnVsbCwic2NvcGUiOltdfQ.PbSwwlRMEizJGMIXe-GpxJUv3-eNupgu68QaMa87_R0"
