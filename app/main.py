from datetime import timedelta
from typing import Annotated

import uvicorn
from app import settings
from app.core.models import HealthCheck, Token
from app.dependencies import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from app.router.api_v1.endpoints import api_router
from app.user.crud import UserCRUD
from app.user.dependencies import get_user_crud
from app.user.models import UserRead
from fastapi import Depends, FastAPI, HTTPException
from fastapi import status as http_status
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    debug=settings.debug
)


@app.get("/", response_model=HealthCheck, tags=["status"])
async def health_check():
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description
    }


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    users: UserCRUD = Depends(get_user_crud),
):
    
    user = await authenticate_user(username=form_data.username, password=form_data.password, users=users)
    
    if not user:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserRead, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]


app.include_router(api_router, prefix=settings.api_v1_prefix)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)
