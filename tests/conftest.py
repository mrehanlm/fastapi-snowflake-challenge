import pytest

from fastapi_snowflake_challenge.models.client import Client
from fastapi_snowflake_challenge.services.db import get_session

from .utils import get_clients_from_fixture


def cleanup_session(session):
    # Iterate through all instances added to the session
    for instance in session.new:
        session.delete(instance)
    # Flush to apply the deletions
    session.flush()
    session.commit()


@pytest.fixture
def db_session():
    with get_session() as session:
        yield session
        cleanup_session(session)


@pytest.hookimpl()
def pytest_sessionstart(session):
    with get_session() as db_session:
        db_session.query(Client).delete()
        db_session.commit()
        for client_data in get_clients_from_fixture():
            db_session.add(Client(**client_data))
        db_session.commit()


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    with get_session() as db_session:
        db_session.query(Client).delete()
        db_session.commit()
