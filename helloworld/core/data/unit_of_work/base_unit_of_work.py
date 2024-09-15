from __future__ import annotations

import inspect
import os
import importlib.metadata
import importlib.util
from collections.abc import Callable
from typing import get_type_hints, TypeVar, Any, Sequence, List, Type

from .abstract_unit_of_work import AbstractUnitOfWork
from helloworld.core.error import exceptions

__DI__ = "di"
__INIT_PY__ = "__init__.py"
__RETURN__ = "return"
__METADATA_NAME__ = "Name"
__HELLO_PACKAGE_NICKNAME__ = "helloworld-"

T = TypeVar("T")

def db_session_manager(type: T):
    def decorator(func):
        func.db_session_manager_type = type
        return func
    return decorator

class BaseUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_managers: Sequence[Any], authorization: str | None = None):
        super().__init__(session_managers, authorization)
        self._sessions_managers: List[(Any, Any)] = []

    def _db_session_manager_by_type(self, type: Type[T]):
        return next((x for x in self.session_managers if isinstance(x, type)), None)

    async def _find_or_create_session(self, db_session_manager_type: Type[T]):
        session = next((x for x in self._sessions_managers if x[0] == db_session_manager_type), None)
        if session: return session[1]

        session_manager = self._db_session_manager_by_type(db_session_manager_type)
        if not session_manager: raise exceptions.NoSessionManagerForTypeError

        session = await session_manager.create_session(authorization=self.authorization)
        await session_manager.begin(session)
        self._sessions_managers.append((db_session_manager_type, session))

        return session

    @property
    def repository_factory(self):
        class RepositoryFactory:
            @classmethod
            async def instance(cls, repository_type: T) -> T:
                func: Any = self.find_di_func_by_type(repository_type)
                if not func: raise exceptions.NoDIFunctionFoundForTypeError

                session = await self._find_or_create_session(func.db_session_manager_type)

                session_manager = self._db_session_manager_by_type(func.db_session_manager_type)
                repository_instance = await session_manager.repository_factory.instance(func, session)
                return repository_instance

        return RepositoryFactory

    #todo: throw if there is more than one found
    #todo: cache it [now!]
    @classmethod
    def find_di_func_by_type(cls, repository_type: T) -> Callable | None:
        packages = [dist.metadata[__METADATA_NAME__] for dist in importlib.metadata.distributions() if
                    dist.metadata[__METADATA_NAME__].startswith(__HELLO_PACKAGE_NICKNAME__)]
        for package_name in packages:
            try:
                module_name = package_name.replace("-", ".")
                package = importlib.import_module(module_name)
                package_path = package.__path__[0]

                for root, dirs, files in os.walk(package_path):
                    if not __DI__ in dirs: continue

                    di_init_path = os.path.join(root, __DI__, __INIT_PY__)
                    if not os.path.exists(di_init_path): continue

                    spec = importlib.util.spec_from_file_location(f"{package_name}.{__DI__}", di_init_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    for name, func in inspect.getmembers(module, inspect.isfunction):
                        type_hints = get_type_hints(func)
                        return_hint = type_hints.get(__RETURN__, None)

                        if return_hint != repository_type: continue

                        return func
            except Exception as e:
                print(f"Error {package_name}: {e}")

        return None

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
            session_manager = self._db_session_manager_by_type(session[0])
            try:
                await getattr(session_manager, action)(session[1])
            except (Exception,): pass