from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from typing_extensions import TypeVar, Generic

from helloworld.core.data.repositories.abstract_repository import AbstractRepository
from helloworld.core.event import Events

_T = TypeVar("_T", bound=Any)

class AbstractRepositoryFactory(ABC):
    @classmethod
    async def instance(cls, **kwargs) -> AbstractRepository:
        raise NotImplementedError

class AbstractDatabaseSessionManager(ABC, Events, Generic[_T]):
    def __init__(self):
        super().__init__()
        self.register_event(self, "after_commit")

    @abstractmethod
    def init(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def create_session(self, authorization: str):
        raise NotImplementedError

    @abstractmethod
    async def begin(self, session):
        raise NotImplementedError

    @abstractmethod
    async def commit(self, session):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self, session):
        raise NotImplementedError

    @abstractmethod
    async def close(self, session):
        raise NotImplementedError

    @abstractmethod
    def repository_factory(self):
        raise NotImplementedError

    @abstractmethod
    async def dispose(self):
        raise NotImplementedError

