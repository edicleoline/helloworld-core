from abc import ABC
from typing import Optional, List, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from helloworld.core.data.repositories.abstract_repository import AbstractRepository, TEntity, TModel

class BaseRepository(AbstractRepository[TEntity, TModel], ABC):
    def __init__(self, session: AsyncSession, model_cls: Type[TModel]):
        self.session = session
        self.model_cls = model_cls
        super().__init__()

    async def __raise_session_if_missing__(self):
        if not self.session:
            raise ValueError("Session is not provided")

    async def save(self, entity: TEntity) -> TEntity:
        await self.__raise_session_if_missing__()
        if entity.id:
            model = await self._find_by_id(entity.id)
            model.merge_with_entity(entity)
            self.session.add(model)
        else:
            model = self.model_cls().from_entity(entity)
            model.id = str(self.model_cls.new_ulid())

        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return model.to_entity()

    async def _find_by_id(self, entity_id: str) -> Optional[TEntity]:
        await self.__raise_session_if_missing__()
        stmt = select(self.model_cls).where(self.model_cls.id == entity_id)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def find_by_id(self, entity_id: str) -> Optional[TEntity]:
        model = await self._find_by_id(entity_id)
        return model.to_entity() if model else None

    async def all(self) -> List[TEntity]:
        pass

    async def delete_by_id(self, entity_id: str) -> None:
        await self.__raise_session_if_missing__()
        model = await self._find_by_id(entity_id)
        if not model: raise ValueError("Entity not found")
        await self.session.delete(model)
        await self.session.flush()