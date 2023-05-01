from app.core.models import StatusMessage
from app.dependencies import get_password_hash
from app.user.crud import UserCRUD
from app.user.dependencies import get_user_crud
from app.user.models import User, UserCreate, UserPatch, UserRead
from fastapi import APIRouter, Depends
from fastapi import status as http_status

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
    user = await users.create(data=new_user)

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
    user = await users.patch(user_id=user_id, data=data)

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
