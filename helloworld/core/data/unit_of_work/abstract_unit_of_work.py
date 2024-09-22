from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

from helloworld.core.data import AbstractRepository

T = TypeVar("T", bound=AbstractRepository)

class RepositoryFactory:
    @classmethod
    async def instance(cls, repository_type: T) -> T:
        raise NotImplementedError

class AbstractUnitOfWork(ABC):
    def __init__(self, authorization: str | None = None):
        self.authorization: str | None = authorization

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, *_): ...

    async def __aenter__(self):
        return self

    @property
    def repository_factory(self) -> RepositoryFactory:
        raise NotImplementedError
