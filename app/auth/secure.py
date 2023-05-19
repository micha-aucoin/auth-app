from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt

from app import settings
from app.core.security import verify_password
from app.user.crud import UserCRUD
from app.user.models import UserRead


class SecureUser:
    def __init__(self, users: UserCRUD):
        self.users = users

    async def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> UserRead:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        user = await self.users.get(username=username)

        if not user:
            raise credentials_exception

        if not verify_password(password, user.hashed_password):
            raise credentials_exception

        return user

    async def create_access_token(
        self,
        user: UserRead,
    ) -> str:
        if settings.jwt_token_expire_minutes:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.jwt_token_expire_minutes
            )
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode = {
            "username": user.username,
            "exp": expire,
            "iat": datetime.utcnow(),
            "email": user.email,
        }

        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return encoded_jwt
