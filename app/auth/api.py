from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from app.auth.dependencies import get_user_crud
from app.auth.models import Token, TokenData
from app.auth.security import (
    authenticate_user,
    create_access_token,
    get_valid_token_data,
)
from app.core.models import StatusMessage
from app.core.security import oauth2_scheme
from app.users.crud import UserCRUD
from app.users.models import UserCreate, UserRead

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: UserCreate,
    users: Annotated[UserCRUD, Depends(get_user_crud)],
):
    try:
        user = await users.create(data=data)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The username or email is already in use.",
        ) from e

    return user


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    users: Annotated[UserCRUD, Depends(get_user_crud)],
) -> Token:
    user = await authenticate_user(
        username=form_data.username,
        password=form_data.password,
        users=users,
    )

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token = await create_access_token(user=user)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/validate",
    response_model=StatusMessage,
    status_code=status.HTTP_200_OK,
)
async def validate_token(
    users: Annotated[UserCRUD, Depends(get_user_crud)],
    token_data: Annotated[TokenData, Depends(get_valid_token_data)],
):
    status = False
    user = await users.get(username=token_data.username)
    if user:
        status = True

    return {
        "status": status,
        "message": "Valid user credentials",
    }
