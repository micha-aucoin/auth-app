from os import getenv

from app.core.config import Settings

settings = Settings(
    api_v1_prefix=getenv("API_V1_PREFIX"),
    debug=getenv("DEBUG"),
    project_name=getenv("PROJECT_NAME"),
    version=getenv("VERSION"),
    description=getenv("DESCRIPTION"),
    db_async_connection_str=f"{getenv('PG_DRIVER')}://{getenv('PG_USERNAME')}:{getenv('PG_PASSWORD')}@{getenv('PG_HOST')}:{getenv('PG_PORT')}/{getenv('PG_DATABASE')}",
    jwt_secret=getenv("JWT_SECRET"),
)
