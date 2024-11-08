from .db import DatabaseSettings


class Settings(DatabaseSettings):
    project_name: str = "fastapi-snowflake-challenge"
    debug: bool = False
