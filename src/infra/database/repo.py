from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import User
from src.infra.database.mapping import UserInDb


class SqlRepo:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, item: dict[str, Any]):
        try:
            self.session.add(item)
            await self.session.commit()
            await self.session.refresh(item)
        except Exception:
            await self.session.rollback()
            raise


class SalaryScheduleRepo(SqlRepo):
    
    async def get_by_username(self, username: str):
        stmt = (
            select(UserInDb)
            .where(UserInDb.username == username)
            .options(selectinload(UserInDb.salary_schedule))
        )
        res = (await self.session.execute(stmt)).scalars().all()
        if len(res) == 0:
            return None
        return res[0]


class UserRepo(SqlRepo):

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(UserInDb).where(UserInDb.username == username)
        user = (await self.session.execute(stmt)).scalar_one_or_none()
        return user
