from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependencies import get_secure_user
from app.auth.models import Token, TokenData
from app.auth.secure import SecureUser

router = APIRouter()


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    security: Annotated[SecureUser, Depends(get_secure_user)],
):
    user = await security.authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token = await security.create_access_token(user=user)

    return {"access_token": access_token, "token_type": "bearer"}


# @router.post(
#     "/validate",
#     response_model=TokenData,
#     status_code=status.HTTP_200_OK,
# )
# async def validate(
