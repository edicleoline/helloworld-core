from __future__ import annotations

from abc import ABC
from typing import Optional, List, Type, overload

from helloworld.core.data import AbstractRepository, TEntity, TModel
from helloworld.core.error import exceptions

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class BaseRepository(AbstractRepository[TEntity, TModel], ABC):
    def __init__(self, session: AsyncSession, model_cls: Type[TModel], authorization: str | None = None):
        self.session = session
        self.model_cls = model_cls
        super().__init__(authorization=authorization)

    async def save(self, entity: TEntity) -> TEntity:
        if entity.id:
            model = await self._find(id=entity.id)
            if not model: raise exceptions.EntityNotFoundError
            model.merge_with_entity(entity)
        else:
            model = self.model_cls().from_entity(entity)
            model.id = str(self.model_cls.new_id())

        self.session.add(model)
        return model.to_entity()

    async def create(self, entity: TEntity) -> TEntity:
        pass

    async def _find(self, **kwargs) -> Optional[TModel]:
        stmt = select(self.model_cls).filter_by(**kwargs)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    @overload
    async def find(self, id: str) -> Optional[TEntity]: ...

    async def find(self, *args, **kwargs) -> Optional[TEntity]:
        id = kwargs.get("id") or None
        if id: return (await self._find(id=id)).to_entity() or None

        raise NotImplementedError

    async def all(self) -> List[TEntity]:
        pass

    async def delete(self, id: str) -> None:
        model = await self._find(id=id)
        if not model: raise exceptions.EntityNotFoundError
        await self.session.delete(model)