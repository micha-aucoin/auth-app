from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_password_hash
from app.users.models import User, UserCreate, UserPatch


class UserCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        data: UserCreate,
    ) -> User:
        user = User(
            **data.dict(),
            hashed_password=get_password_hash(data.password),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get(self, username: str) -> User:
        statement = select(User).where(User.username == username)
        results = await self.session.execute(statement=statement)
        user = results.scalar_one_or_none()  # type: User | None

        if not user:
            return False

        return user

    async def patch(self, username: str, data: UserPatch) -> User:
        user = await self.get(username=username)
        values = data.dict(exclude_unset=True)

        for k, v in values.items():
            setattr(user, k, v)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def delete(self, username: str) -> bool:
        statement = delete(User).where(User.username == username)

        await self.session.execute(statement=statement)
        await self.session.commit()

        return True
