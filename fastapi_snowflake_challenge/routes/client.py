from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi_snowflake_challenge.schemas.client import ClientSchema
from fastapi_snowflake_challenge.models.client import Client
from fastapi_snowflake_challenge.services.db import get_session_depends

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
)


@router.post("/", response_model=ClientSchema)
async def create_client(client: ClientSchema, db_session: Session = Depends(get_session_depends)):
    """
    Creates a new client record in the database.

    Args:
        client (ClientSchema): The client data to create, including name and email.
        db_session (Session): The database session dependency.

    Raises:
        HTTPException: If a client with the same email already exists, returns a 400 status code.

    Returns:
        ClientSchema: The newly created client record with name, email, and other attributes.
    """
    if Client.exists(db_session, client.email):
        raise HTTPException(status_code=400, detail="Client with this email already exists.")

    return Client.create(db_session, client)


@router.get("/", response_model=list[ClientSchema])
async def get_clients(db_session: Session = Depends(get_session_depends)):
    """
    Retrieves all clients from the database.

    Args:
        db_session (Session): The database session dependency.

    Returns:
        list[ClientSchema]: A list of all client records in the database, each with details such as name, email, and created date.
    """
    return db_session.query(Client).all()


@router.get("/{client_id}", response_model=ClientSchema)
async def get_client_details(client_id: int, db_session: Session = Depends(get_session_depends)):
    """
    Retrieve details of a specific client by their ID.

    This endpoint fetches the details of a client from the database based on the provided client ID.

    Parameters:
    - client_id (int): The unique identifier of the client to retrieve.
    - db_session (Session): A database session dependency for database operations.

    Returns:
    - ClientSchema: The client's details if found.

    Raises:
    - HTTPException: If no client with the specified ID exists, returns a 404 status code with an error message.
    """
    client = Client.get(db_session, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail=f"Client not found with id {client_id}")
    return client


@router.put("/{client_id}", response_model=ClientSchema)
async def update_client(client_id: int, client: ClientSchema, db_session: Session = Depends(get_session_depends)):
    """
    Update an existing client in the database with new information.

    This endpoint updates a client's information if:
    - The client with the given ID exists.
    - The new email provided is unique across all clients, or is the same as the existing one for this client.

    Parameters:
    - client_id (int): The unique identifier of the client to update.
    - client (ClientSchema): The new data for the client, provided in the request body.
    - db_session (Session): A database session dependency for database operations.

    Returns:
    - ClientSchema: The updated client data as per the provided schema.

    Raises:
    - HTTPException: If a client with the specified ID does not exist, returns a 404 status code.
    - HTTPException: If an existing client with the specified email already exists (other than the current client),
      returns a 400 status code with an error message.

    """
    existing_client = Client.get(db_session, client_id)
    if not existing_client:
        raise HTTPException(status_code=404, detail=f"Client not found with id {client_id}")

    if existing_client.email != client.email and Client.exists(db_session, client.email, client_id):
        raise HTTPException(status_code=400, detail="Client with this email already exists.")

    return Client.update(db_session, client_id, client)


@router.delete("/{client_id}", status_code=204)
async def delete_client(client_id: int, db_session: Session = Depends(get_session_depends)):
    """
    Delete a client from the database.

    This endpoint removes a client from the database if a client with the specified ID exists.

    Parameters:
    - client_id (int): The unique identifier of the client to delete.
    - db_session (Session): A database session dependency for database operations.

    Returns:
    - HTTP 204 No Content: Indicates successful deletion of the client.

    Raises:
    - HTTPException: If no client with the specified ID exists, returns a 404 status code with an error message.
    """
    deleted = Client.delete(db_session, client_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Client not found with id {client_id}")
