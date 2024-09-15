from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, overload
from typing_extensions import TypeVar

TEntity = TypeVar('TEntity')
TModel = TypeVar('TModel', bound=Optional[object], default=None)

class AbstractRepository(ABC, Generic[TEntity, TModel]):
    def __init__(self, authorization: str | None = None):
        self.authorization = authorization

    @abstractmethod
    async def save(self, entity: TEntity) -> TEntity:
        raise NotImplementedError

    @abstractmethod
    async def create(self, entity: TEntity) -> TEntity:
        raise NotImplementedError

    @overload
    async def find(self, id: str) -> Optional[TEntity]:
        raise NotImplementedError

    async def find(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def all(self) -> List[TEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: str) -> None:
        raise NotImplementedError