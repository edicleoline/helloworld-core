from __future__ import annotations

import re
from typing import TypeVar, Any, List

from .abstract_unit_of_work import AbstractUnitOfWork
from helloworld.core.error import exceptions
from helloworld.core.services.service_manager import service_manager
from ..database.abstract_db_session_manager import AbstractDatabaseSessionManager
from helloworld.core.util.di import find_di_func_by_type

__HELLO_PACKAGE_NICKNAME__ = "helloworld-"
di_packages_pattern = re.compile(rf"^{re.escape(__HELLO_PACKAGE_NICKNAME__)}")

T = TypeVar("T")

class BaseUnitOfWork(AbstractUnitOfWork):
    def __init__(self, authorization: str | None = None):
        super().__init__(authorization)
        self._sessions_managers: List[(str, str, Any)] = []

    async def _find_or_create_session(self, service_type: str, service_name: str):
        session = next((x for x in self._sessions_managers if x[0] == service_name), None)
        if session: return session[1]

        session_manager: AbstractDatabaseSessionManager = service_manager.get(service_type, service_name)
        if not session_manager: raise exceptions.NoSessionManagerForTypeError

        session = await session_manager.create_session(authorization=self.authorization)
        await session_manager.begin(session)
        self._sessions_managers.append((service_type, service_name, session))

        return session

    @property
    def repository_factory(self):
        class RepositoryFactory:
            @classmethod
            async def instance(cls, repository_type: T) -> T:
                func: Any = find_di_func_by_type(repository_type, di_packages_pattern)
                if not func: raise exceptions.NoDIFunctionFoundForTypeError(repository_type)

                session = await self._find_or_create_session(func.__service_type__, func.__service_name__)
                session_manager = service_manager.get(func.__service_type__, func.__service_name__)

                repository_instance = await session_manager.repository_factory.instance(func, session)
                return repository_instance

        return RepositoryFactory

    async def __aexit__(self, exc_type, *_) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.close()

    async def commit(self):
        await self._execute_for_all_sessions("commit")

    async def rollback(self):
        await self._execute_for_all_sessions("rollback")

    async def close(self):
        await self._execute_for_all_sessions("close")

    async def _execute_for_all_sessions(self, action: str):
        for session in self._sessions_managers:
            session_manager = service_manager.get(session[0], session[1])
            try:
                await getattr(session_manager, action)(session[2])
            except Exception as e:
                print(e)