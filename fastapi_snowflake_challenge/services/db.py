from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from fastapi_snowflake_challenge.settings import settings


db_url = "snowflake://{user}:{password}@{account}/{database}/{schema}".format(
    user=settings.SF_USER,
    password=settings.SF_PASSWORD,
    account=settings.SF_ACCOUNT,
    database=settings.SF_DATABASE,
    schema=settings.SF_SCHEMA,
)
engine = create_engine(db_url, echo=settings.debug)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    async_session = sessionmaker(engine, class_=Session, expire_on_commit=False)
    with async_session() as session:
        yield session


def get_session_depends() -> Generator[Session, None, None]:
    with get_session() as session:
        yield session
