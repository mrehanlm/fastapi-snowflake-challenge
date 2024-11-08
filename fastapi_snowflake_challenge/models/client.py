from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Sequence

from .base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, Sequence("id_seq"), primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, db_session, data):
        """
        Creates a new client record in the database.
        """
        new_client = cls(name=data.name, email=data.email)
        db_session.add(new_client)
        db_session.commit()
        db_session.refresh(new_client)
        return new_client

    @classmethod
    def update(cls, db_session, client_id, data):
        """
        Updates an existing client record in the database.
        """
        client = db_session.query(cls).filter(cls.id == client_id).first()
        if client is None:
            return None

        if data.name is not None:
            client.name = data.name
        if data.email is not None:
            client.email = data.email

        db_session.commit()
        db_session.refresh(client)
        return client

    @classmethod
    def get(cls, db_session, client_id):
        """
        Retrieves a client record by ID.
        """
        return db_session.query(cls).filter(cls.id == client_id).first()

    @classmethod
    def delete(cls, db_session, client_id):
        """
        Deletes a client record by ID.
        """
        client = db_session.query(cls).filter(cls.id == client_id).first()
        if client is None:
            return False

        db_session.delete(client)
        db_session.commit()
        return True

    @classmethod
    def exists(cls, db_session, email):
        return bool(db_session.query(cls).filter_by(email=email).all())
