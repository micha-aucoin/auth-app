from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f".{settings.api_v1_prefix}/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
