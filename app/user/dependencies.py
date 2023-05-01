from app.core.db import get_async_session
from app.user.crud import UserCRUD
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_crud(
        session: AsyncSession = Depends(get_async_session)
) -> UserCRUD:
    return UserCRUD(session=session)