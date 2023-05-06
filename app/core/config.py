from pydantic import BaseSettings


class Settings(BaseSettings):
    # Base
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str

    # Database
    db_async_connection_str: str

    # JWT
    jwt_secret: str
    jwt_algorithm: str
    jwt_token_expire_minutes: int
