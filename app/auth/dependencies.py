from datetime import datetime, timedelta

from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.core.db import get_async_session
from app.user.crud import UserCRUD


async def get_user_crud(
    session: AsyncSession = Depends(get_async_session),
) -> UserCRUD:
    return UserCRUD(session=session)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(
    username: str,
    password: str,
    users: UserCRUD,
):
    user = await users.get(username=username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    return encoded_jwt
