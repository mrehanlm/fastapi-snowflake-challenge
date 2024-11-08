from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    SF_USER: str
    SF_PASSWORD: str
    SF_ACCOUNT: str
    SF_DATABASE: str
    SF_SCHEMA: str
