from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from sqlalchemy.exc import IntegrityError

from app.core.models import StatusMessage
from app.dependencies import get_password_hash
from app.user.crud import UserCRUD
from app.user.dependencies import get_user_crud
from app.user.models import User, UserCreate, UserPatch, UserRead

router = APIRouter()


@router.post(
    "",
    response_model=UserRead,
    status_code=http_status.HTTP_201_CREATED
)
async def create_user(
        data: UserCreate,
        users: UserCRUD = Depends(get_user_crud)
):
    hashed_password = get_password_hash(data.password)

    # Convert the UserCreate object to a dictionary and add the hashed password
    user_data = data.dict()
    user_data["hashed_password"] = hashed_password

    # Create a new user instance
    new_user = User(**user_data)
    
    try:
        user = await users.create(data=new_user)
    except IntegrityError as e:
        # Raise an HTTPException with a suitable error message
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="The username or email is already in use.",
        ) from e

    return user


@router.get(
    "/{user_id}",
    response_model=UserRead,
    status_code=http_status.HTTP_200_OK
)
async def get_user_by_uuid(
        user_id: str,
        users: UserCRUD = Depends(get_user_crud)
):
    user = await users.get(user_id=user_id, username=None)

    return user


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    status_code=http_status.HTTP_200_OK
)
async def patch_user_by_uuid(
        user_id: str,
        data: UserPatch,
        users: UserCRUD = Depends(get_user_crud)
):
    
    try:
        user = await users.patch(user_id=user_id, data=data)
    except IntegrityError as e:
        # Raise an HTTPException with a suitable error message
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="The username or email is already in use.",
        ) from e

    return user


@router.delete(
    "/{user_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK
)
async def delete_user_by_uuid(
        user_id: str,
        users: UserCRUD = Depends(get_user_crud)
):
    status = await users.delete(user_id=user_id)

    return {"status": status, "message": "The user has been deleted!"}
