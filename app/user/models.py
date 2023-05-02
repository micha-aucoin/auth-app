from typing import Optional

from app.core.models import TimestampModel, UUIDModel
from app.user.examples import ex_user_create, ex_user_patch, ex_user_read
from pydantic import SecretStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(max_length=255, nullable=False, unique=True)
    full_name: str = Field(max_length=255, nullable=False)
    email: str = Field(max_length=255, nullable=False, unique=True)
    disabled: bool = Field(default=False)

    
class User(
    TimestampModel,
    UserBase,
    UUIDModel,
    table=True
):
    __tablename__ = "users"
    hashed_password: str = Field(max_length=255, nullable=False)

class UserRead(UserBase, UUIDModel):
    class Config:
        schema_extra = {"example": ex_user_read}


class UserCreate(UserBase):
    password: str
    
    class Config:
        schema_extra = {"example": ex_user_create}


class UserPatch(UserBase):
    username: Optional[str] = Field(max_length=255)

    class Config:
        schema_extra = {"example": ex_user_patch}


