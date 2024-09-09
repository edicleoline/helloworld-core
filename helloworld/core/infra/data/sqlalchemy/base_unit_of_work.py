from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from helloworld.core.data.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork

class BaseUnitOfWork(AbstractUnitOfWork[AsyncSession]):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        super().__init__(session_factory=session_factory)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    def __await__(self):
        return self.__aenter__().__await__()

    async def __aenter__(self):
        self.session = await self.session_factory()
        return await super().__aenter__()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()