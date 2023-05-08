from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from fastapi.security import OAuth2PasswordRequestForm

from app import settings
from app.auth.dependencies import authenticate_user, create_access_token, get_user_crud
from app.auth.models import Token
from app.user.crud import UserCRUD

router = APIRouter()


@router.post(
    "/token",
    response_model=Token,
    status_code=http_status.HTTP_200_OK,
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    users: UserCRUD = Depends(get_user_crud),
):
    user = await authenticate_user(
        username=form_data.username,
        password=form_data.password,
        users=users,
    )
    if not user:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.jwt_token_expire_minutes,
    )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
