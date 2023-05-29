from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app import settings
from app.auth.models import TokenData
from app.core.security import oauth2_scheme, verify_password
from app.users.crud import UserCRUD
from app.users.models import UserRead


async def authenticate_user(
    username: str,
    password: str,
    users: UserCRUD,
) -> UserRead:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = await users.get(username=username)

    if not user:
        raise credentials_exception

    if not verify_password(password, user.hashed_password):
        raise credentials_exception

    return user


async def create_access_token(
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


async def get_valid_token_data(
    token: str = Depends(oauth2_scheme),
) -> TokenData:
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
