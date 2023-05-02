from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.user.models import User, UserCreate, UserPatch


class UserCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: User) -> User:
        values = data.dict()

        user = User(**values)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get(self, user_id: Optional[str | UUID], username: str | None) -> User:
        if username:
            statement = select(
                User
            ).where(
                User.username == username
            )
        else:
            statement = select(
                User
            ).where(
                User.uuid == user_id
            )
        results = await self.session.execute(statement=statement)
        user = results.scalar_one_or_none()  # type: User | None

        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!"
            )

        return user

    async def patch(self, user_id: str | UUID, data: UserPatch) -> User:
        user = await self.get(user_id=user_id, username=None)
        values = data.dict(exclude_unset=True)

        for k, v in values.items():
            setattr(user, k, v)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def delete(self, user_id: str | UUID) -> bool:
        statement = delete(
            User
        ).where(
            User.uuid == user_id
        )

        await self.session.execute(statement=statement)
        await self.session.commit()

        return True
