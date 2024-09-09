from abc import ABC, abstractmethod
from typing import Generic, List, Optional
from typing_extensions import TypeVar

TEntity = TypeVar('TEntity')
TModel = TypeVar('TModel', bound=Optional[object], default=None)

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
    async def delete_by_id(self, entity_id: str) -> None:
        raise NotImplementedError