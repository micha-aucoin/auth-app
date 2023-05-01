from os import getenv

from app.core.config import Settings
from dotenv import load_dotenv

load_dotenv(getenv("ENV_FILE"))

settings = Settings()