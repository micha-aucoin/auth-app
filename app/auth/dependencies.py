from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.secure import SecureUser
from app.core.db import get_async_session
from app.users.crud import UserCRUD


async def get_user_crud(
    session: AsyncSession = Depends(get_async_session),
) -> UserCRUD:
    return UserCRUD(session=session)


async def get_secure_user(
    users: UserCRUD = Depends(get_user_crud),
) -> SecureUser:
    return SecureUser(users=users)
