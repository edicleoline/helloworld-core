from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, overload, Literal

from typing_extensions import TypeVar

TEntity = TypeVar('TEntity')
TModel = TypeVar('TModel', bound=Optional[object], default=None)

LogicalOperator = Literal["and", "or"]

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
    async def find(self, id: int) -> TEntity | None:
        raise NotImplementedError

    @overload
    async def find(self, criteria: LogicalOperator = "and", **kwargs) -> TEntity | None: ...

    async def find(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def all(self) -> List[TEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError