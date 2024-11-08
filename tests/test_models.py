import pytest
from datetime import datetime
from fastapi_snowflake_challenge.models.client import Client
from fastapi_snowflake_challenge.schemas.client import ClientSchema


@pytest.fixture
def client_data():
    return ClientSchema(name="Test User", email="test@example.com")


def test_create_client(db_session, client_data):
    client = Client.create(db_session, client_data)
    assert client.id is not None
    assert client.name == client_data.name
    assert client.email == client_data.email
    assert isinstance(client.created_at, datetime)


def test_get_client(db_session, client_data):
    client = Client.create(db_session, client_data)
    fetched_client = Client.get(db_session, client.id)
    assert fetched_client is not None
    assert fetched_client.id == client.id
    assert fetched_client.name == client.name
    assert fetched_client.email == client.email


def test_update_client(db_session, client_data):
    client = Client.create(db_session, client_data)
    updated_data = ClientSchema(name="Updated User", email="updated@example.com")
    updated_client = Client.update(db_session, client.id, updated_data)

    assert updated_client is not None
    assert updated_client.name == "Updated User"
    assert updated_client.email == "updated@example.com"


def test_delete_client(db_session, client_data):
    client = Client.create(db_session, client_data)
    deletion_result = Client.delete(db_session, client.id)

    assert deletion_result is True
    assert Client.get(db_session, client.id) is None


def test_exists(db_session, client_data):
    Client.create(db_session, client_data)
    assert Client.exists(db_session, client_data.email) is True
    assert Client.exists(db_session, "nonexistent@example.com") is False
