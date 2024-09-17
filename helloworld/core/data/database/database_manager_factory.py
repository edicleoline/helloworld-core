from __future__ import annotations

from typing import TypeVar, Dict

from .abstract_db_session_manager import AbstractDatabaseSessionManager

T = TypeVar("T", bound=AbstractDatabaseSessionManager)

class DatabaseManagerFactory:
    _instances: Dict[str, AbstractDatabaseSessionManager] = {}

    async def instance(self, name: str, session_manager: type[AbstractDatabaseSessionManager]) -> AbstractDatabaseSessionManager:
        if name in self._instances:
            raise ValueError(f"Instance with name {name} already exists.")

        obj = session_manager()
        obj.name = name
        self._instances[name] = obj

        return obj

    async def find(self, name: str):
        return self._instances[name]


database_manager_factory = DatabaseManagerFactory()