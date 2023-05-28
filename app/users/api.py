from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.auth.models import TokenData
from app.core.models import StatusMessage
from app.users.crud import UserCRUD
from app.users.dependencies import get_user_crud, get_valid_token_data
from app.users.models import UserCreate, UserPatch, UserRead

router = APIRouter()


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
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


@router.get(
    "",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    users: Annotated[UserCRUD, Depends(get_user_crud)],
    token_data: Annotated[TokenData, Depends(get_valid_token_data)],
):
    user = await users.get(username=token_data.username)

    return user


@router.patch(
    "",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def patch_user(
    data: UserPatch,
    users: Annotated[UserCRUD, Depends(get_user_crud)],
    token_data: Annotated[TokenData, Depends(get_valid_token_data)],
):
    try:
        user = await users.patch(username=token_data.username, data=data)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The username or email is already in use.",
        ) from e

    return user


@router.delete(
    "",
    response_model=StatusMessage,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    users: Annotated[UserCRUD, Depends(get_user_crud)],
    token_data: Annotated[TokenData, Depends(get_valid_token_data)],
):
    status = await users.delete(username=token_data.username)

    return {
        "status": status,
        "message": f"The user, {token_data.username} has been deleted!",
    }
