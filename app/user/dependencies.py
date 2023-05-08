from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.core.db import get_async_session
from app.core.models import TokenData
from app.user.crud import UserCRUD
from app.user.models import UserRead


async def get_user_crud(
    session: AsyncSession = Depends(get_async_session),
) -> UserCRUD:
    return UserCRUD(session=session)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f".{settings.api_v1_prefix}/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    users: UserCRUD = Depends(get_user_crud),
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
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = await users.get(username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[UserRead, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
