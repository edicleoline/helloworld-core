from __future__ import annotations

import contextlib
import importlib
from datetime import datetime
from typing import AsyncIterator, Callable

from .base_model import BaseModel, Base
from helloworld.core.data import AbstractDatabaseSessionManager, AbstractRepositoryFactory, AbstractRepository
from helloworld.core.error import exceptions

from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine)
from sqlalchemy import event

class DatabaseSessionManager(AbstractDatabaseSessionManager):
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

        self._get_create_use_case = None
        self._db_log_create_use_case = None

        super().__init__()

    def init(self, url: str):
        self._engine = create_async_engine(url)
        self._sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

        return self

    async def create_session(self, authorization: str) -> AsyncSession:
        if self._sessionmaker is None:
            raise exceptions.DatabaseNotInitializedError

        di_module = importlib.import_module("helloworld.log.features.database_log.di")
        self._get_create_use_case = di_module.get_create_use_case
        self._db_log_create_use_case = await self._get_create_use_case(authorization=authorization)

        session = self._sessionmaker()

        session.sync_session.__authorization__ = authorization
        session.sync_session.__changes__ = {}
        session.sync_session.__models__ = {}

        @event.listens_for(Base, "before_insert", propagate=True)
        @event.listens_for(Base, "before_update", propagate=True)
        @event.listens_for(Base, "before_delete", propagate=True)
        def before_persist(mapper, connection, target: BaseModel):
            target.__changed_at__ = str(datetime.now())
            instance_id = f"{(id(getattr(target, "_sa_instance_state")))}"
            session.sync_session.__models__[instance_id] = { k: v for k, v in target.__dict__.items() if k != "_sa_instance_state" }

        @event.listens_for(session.sync_session, "before_commit")
        def before_commit(_session):
            _session.__changes__ = {
                "insert": list(_session.new),
                "update": list(_session.dirty),
                "delete": list(_session.deleted),
            }

        @event.listens_for(session.sync_session, "after_commit")
        def after_commit(_session):
            def trigger_after_commit(changes, models):
                try:
                    entities = []

                    for operation in changes:
                        for model in changes[operation]:
                            instance_id = id(getattr(model, "_sa_instance_state"))
                            __model__ = models.get(str(instance_id))

                            entity = model.to_entity()
                            entity.__dict__.update({ k: v for k, v in __model__.items() if k in entity.__dict__ })

                            entity_dict = dict(entity.__dict__)
                            entity_dict["__type__"] = f"{entity.__class__.__module__}.{entity.__class__.__qualname__}"
                            entity_dict.update({ k: v for k, v in __model__.items() if k not in entity_dict })
                            entity_dict["__operation__"] = operation
                            entity_dict["__committed_at__"] = str(datetime.now())
                            entity_dict["__authorization__"] = authorization

                            entities.append(entity_dict)

                            session.sync_session.__models__.pop(str(instance_id), None)

                    if entities and len(entities) > 0:
                        self.trigger_event("after_commit", enitities=entities)

                except Exception as e:
                    print(f"Error on log_commit_tasks: {e}")

            trigger_after_commit(_session.__changes__, session.sync_session.__models__)
        return session

    async def begin(self, session: AsyncSession) -> None: ...

    @classmethod
    async def commit(cls, session: AsyncSession) -> None:
        await session.commit()

    @classmethod
    async def rollback(cls, session: AsyncSession) -> None:
        await session.rollback()

    @classmethod
    async def close(cls, session: AsyncSession) -> None:
        await session.close()

    @property
    def repository_factory(self):
        class RepositoryFactory(AbstractRepositoryFactory):
            @classmethod
            async def instance(cls, func: Callable, session: AsyncSession) -> AbstractRepository:
                return await func(session)

        return RepositoryFactory

    @contextlib.asynccontextmanager
    async def context_connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise exceptions.DatabaseNotInitializedError

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def context_create_session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise exceptions.DatabaseNotInitializedError

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def dispose(self):
        if self._engine is None:
            raise exceptions.DatabaseNotInitializedError

        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @staticmethod
    async def create_all(connection: AsyncConnection):
        await connection.run_sync(BaseModel.metadata.create_all)

    @staticmethod
    async def drop_all(connection: AsyncConnection):
        await connection.run_sync(BaseModel.metadata.drop_all)