from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.auth.models import TokenData
from app.core.db import get_async_session
from app.core.security import oauth2_scheme
from app.users.crud import UserCRUD


async def get_user_crud(
    session: AsyncSession = Depends(get_async_session),
) -> UserCRUD:
    return UserCRUD(session=session)


async def get_valid_token_data(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )

        username: str = payload.get("username")
        email: str = payload.get("email")

        if username is None or email is None:
            raise credentials_exception

        token_data = TokenData(
            username=username,
            email=email,
        )

    except JWTError:
        raise credentials_exception

    return token_data
