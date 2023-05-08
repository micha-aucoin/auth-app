from dotenv import load_dotenv

from app.core.config import Settings

load_dotenv("env/.env")

settings = Settings()
