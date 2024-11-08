import pytest
from fastapi.testclient import TestClient

from fastapi_snowflake_challenge.www import app
from fastapi_snowflake_challenge.models.client import Client

from .utils import get_clients_from_fixture


@pytest.fixture
def api_client():
    with TestClient(app) as client:
        yield client


def test_create_client(db_session, api_client):
    """
    Test the creation of a client through the API and handle cases where
    the client with the same email already exists.

    This test covers:
      - Initial attempt to add a client directly via the session to simulate an existing record.
      - Checking that a duplicate client with the same email raises a 400 error.
      - Cleaning up and removing the existing client from the database.
      - Attempting client creation again through the API to ensure successful creation.

    Args:
        db_session (Session): Database session fixture to interact with the database.
        api_client (TestClient): API client fixture for making HTTP requests.

    Asserts:
        - Response status code is 400 when attempting to create a client with an existing email.
        - Response contains the appropriate error message for a duplicate email.
        - Response status code is 200 after removing the duplicate and retrying the client creation.
        - Created client's email and name match the input data.
    """
    user = {"email": "test@example.com", "name": "Test User"}
    # Check if the client already exists
    db_session.add(Client(**user))
    db_session.commit()

    # Create client instance with the same email
    response = api_client.post("/clients/", json={"email": "test@example.com", "name": "Test User"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Client with this email already exists."

    # Clean up the client
    db_session.query(Client).filter_by(email=user["email"]).delete()
    db_session.commit()

    # Set it up again through API
    response = api_client.post("/clients/", json={"email": "test@example.com", "name": "Test User"})
    assert response.status_code == 200

    # Assert the client is created
    data = response.json()
    assert data["email"] == user["email"]
    assert data["name"] == user["name"]

    db_session.query(Client).filter_by(email=user["email"]).delete()
    db_session.commit()


def test_get_clients(api_client):
    response = api_client.get("/clients/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    clients = [client["email"] for client in get_clients_from_fixture()]
    actual_clients = [client["email"] for client in response.json()]
    assert set(clients) == set(actual_clients)


def test_get_client_details(api_client):
    new_client = api_client.post("/clients/", json={"email": "fetch@example.com", "name": "Fetch User"}).json()

    response = api_client.get(f"/clients/{new_client['id']}")
    assert response.status_code == 200
    assert response.json()["email"] == "fetch@example.com"


def test_get_nonexistent_client(api_client):
    response = api_client.get("/clients/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Client not found with id 9999"}


def test_update_client(api_client):
    new_client = api_client.post("/clients/", json={"email": "update@example.com", "name": "Update User"}).json()

    response = api_client.put(
        f"/clients/{new_client['id']}",
        json={"email": "update@example.com", "name": "Updated Name"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


def test_update_nonexistent_client(api_client):
    response = api_client.put(
        "/clients/9999",
        json={"email": "nonexistent@example.com", "name": "Nonexistent User"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Client not found with id 9999"}


def test_delete_client(api_client):
    new_client = api_client.post("/clients/", json={"email": "delete@example.com", "name": "Delete User"}).json()

    response = api_client.delete(f"/clients/{new_client['id']}")
    assert response.status_code == 204

    # Verify deletion by attempting to fetch the deleted client
    get_response = api_client.get(f"/clients/{new_client['id']}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": f"Client not found with id {new_client['id']}"}
