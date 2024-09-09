from abc import ABC
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from helloworld.core.data.repositories.abstract_repository import AbstractRepository, TEntity, TModel

class BaseRepository(AbstractRepository[TEntity, TModel], ABC):
    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__()

        types = self.__orig_bases__[0].__args__
        self.__model_cls__ = types[1]

    async def save(self, entity: TEntity) -> TEntity:
        print("model", self.__model_cls__)
        return None

    async def find_by_id(self, entity_id: str) -> Optional[TEntity]:
        pass

    async def all(self) -> List[TEntity]:
        pass

    async def delete(self, entity_id: str) -> None:
        pass