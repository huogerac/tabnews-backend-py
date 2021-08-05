import pytest

import sqlalchemy as sa
from sqlalchemy.orm import Session

from app import create_app
from ext.database import db


@pytest.fixture(scope="session")
def app():
    app = create_app()
    with app.app_context():
        db.create_all(app=app)
        yield app
        db.drop_all(app=app)


@pytest.fixture(scope="function", autouse=True)
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
