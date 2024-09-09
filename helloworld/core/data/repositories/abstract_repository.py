from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

TEntity = TypeVar('TEntity')
TModel = TypeVar('TModel')

class AbstractRepository(ABC, Generic[TEntity, TModel]):
    @abstractmethod
    async def save(self, entity: TEntity) -> TEntity:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, entity_id: str) -> Optional[TEntity]:
        raise NotImplementedError

    @abstractmethod
    async def all(self) -> List[TEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: str) -> None:
        raise NotImplementedError