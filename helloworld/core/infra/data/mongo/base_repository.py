from __future__ import annotations

from abc import ABC
from typing import Optional, List, Type, Any

from helloworld.core.data import AbstractRepository, TEntity
from helloworld.core.error import exceptions

from motor.core import (AgnosticClientSession, AgnosticCollection)
from ulid import ULID

class BaseRepository(AbstractRepository[TEntity], ABC):
    def __init__(self, session: AgnosticClientSession, collection: AgnosticCollection, entity_cls: Type[TEntity], authorization: str | None = None):
        self.session = session
        self.collection = collection
        self.entity_cls = entity_cls
        super().__init__(authorization=authorization)

    async def save(self, entity: TEntity) -> TEntity:
        if entity.id:
            document = await self._find_by_id(entity.id)
            if not document: raise exceptions.EntityNotFoundError
            # model.merge_with_entity(entity)
        else:
            entity.id = str(ULID())
            await self.collection.insert_one(entity.__dict__)

        return entity

    async def create(self, entity: TEntity) -> TEntity:
        await self.collection.insert_one(entity.__dict__)
        return entity

    async def _find_by_id(self, entity_id: str) -> Optional[Any]:
        return await self.collection.find_one({"id": entity_id})

    async def find(self, entity_id: str) -> Optional[TEntity]:
        document = await self._find_by_id(entity_id)
        if not document: return None
        document_copy = document.copy()
        document_copy.pop("_id", None)
        return self.entity_cls(**document_copy)

    async def all(self) -> List[TEntity]:
        pass

    async def delete(self, entity_id: str) -> None:
        # await self.__raise_database_if_missing__()
        # model = await self._find_by_id(entity_id)
        # if not model: raise EntityNotFoundError
        # await self.session.delete(model)
        pass