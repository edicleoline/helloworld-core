from __future__ import annotations

from typing import Callable

from helloworld.core.data import AbstractDatabaseSessionManager, AbstractRepositoryFactory, AbstractRepository
from helloworld.core.error import exceptions

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import (AgnosticClient, AgnosticDatabase, AgnosticClientSession)

class DatabaseSessionManager(AbstractDatabaseSessionManager):
    def __init__(self):
        self._client: AgnosticClient | None = None
        self._database: AgnosticDatabase | None = None
        self.db_name = None

    def init(self, url: str, db_name: str):
        self.db_name = db_name
        self._client = AsyncIOMotorClient(url)
        self._database = self._client.get_database(db_name)

        return self

    async def create_session(self, authorization: str) -> AgnosticClientSession:
        if self._database is None:
            raise exceptions.DatabaseNotInitializedError

        return await self._client.start_session()

    @classmethod
    async def begin(cls, session: AgnosticClientSession) -> None:
        session.start_transaction()

    @classmethod
    async def commit(cls, session: AgnosticClientSession) -> None:
        await session.commit_transaction()

    @classmethod
    async def rollback(cls, session: AgnosticClientSession) -> None:
        await session.abort_transaction()

    @classmethod
    async def close(cls, session: AgnosticClientSession) -> None:
        await session.end_session()

    @property
    def repository_factory(self):
        class RepositoryFactory(AbstractRepositoryFactory):
            @classmethod
            async def instance(cls, func: Callable, session: AgnosticClientSession) -> AbstractRepository:
                return await func(session, self._database)

        return RepositoryFactory

    async def dispose(self):
        if self._client is None:
            raise exceptions.DatabaseNotInitializedError

        self._client.close()
        self._database = None
        self._client = None