from __future__ import annotations

from abc import ABC
from typing import Optional, List, Type, overload

from helloworld.core.data import AbstractRepository, TEntity, TModel
from helloworld.core.data.repositories.abstract_repository import LogicalOperator
from helloworld.core.error import exceptions

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_

class BaseRepository(AbstractRepository[TEntity, TModel], ABC):
    def __init__(self, session: AsyncSession, model_cls: Type[TModel], authorization: str | None = None):
        self.session = session
        self.model_cls = model_cls
        super().__init__(authorization=authorization)

    async def save(self, entity: TEntity) -> TEntity:
        if entity.id:
            model = await self.__find(id=entity.id)
            if not model: raise exceptions.EntityNotFoundError
            model.merge_with_entity(entity)
        else:
            model = self.model_cls().from_entity(entity)
            model.id = str(self.model_cls.new_id())

        self.session.add(model)
        return model.to_entity()

    async def create(self, entity: TEntity) -> TEntity:
        pass

    async def _find_criteria(self, criteria: LogicalOperator = "and", **kwargs):
        condition = (and_ if criteria == "and" else or_)(*(getattr(self.model_cls, k) == v for k, v in kwargs.items()))
        model = (await self.session.execute(select(self.model_cls).where(condition))).scalar_one_or_none()
        return model.to_entity() if model else None

    async def _find(self, **kwargs) -> Optional[TModel]:
        model = await self.__find(**kwargs)
        return model.to_entity() if model else None

    async def __find(self, **kwargs) -> Optional[TModel]:
        stmt = select(self.model_cls).filter_by(**kwargs)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    @overload
    async def find(self, id: str) -> Optional[TEntity]: ...

    @overload
    async def find(self, criteria: LogicalOperator = "and", **kwargs):
        return await self._find_criteria(criteria, **kwargs)

    async def find(self, *args, **kwargs) -> Optional[TEntity]:
        id = kwargs.get("id") or None
        if id: return (await self.__find(id=id)).to_entity() or None

        raise NotImplementedError

    async def all(self) -> List[TEntity]:
        pass

    async def delete(self, id: str) -> None:
        model = await self.__find(id=id)
        if not model: raise exceptions.EntityNotFoundError
        await self.session.delete(model)