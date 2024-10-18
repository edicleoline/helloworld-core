from __future__ import annotations

from typing import Generic, TypeVar, Type

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from helloworld.core.util.snow_flake import snow_flake

__SA_INSTANCE_STATE__ = '_sa_instance_state'

TEntity = TypeVar('TEntity')

Base = declarative_base()

class BaseModel(Base, Generic[TEntity]):
    __abstract__ = True
    __allow_unmapped__ = True

    __entity_cls__: Type[TEntity] = None
    __log__: bool = True

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    def to_entity(self) -> TEntity:
        model_attributes = { k: v for k, v in self.__dict__.copy().items() if not k.startswith("__") }
        model_attributes.pop(__SA_INSTANCE_STATE__, None)
        return self.__entity_cls__(**model_attributes)

    def from_entity(self, entity: TEntity):
        self.__dict__.update(entity.__dict__)
        return self

    def __repr__(self) -> str:
        attributes = ', '.join(f'{key}={value}' for key, value in self.__dict__.items())
        return f'{self.__class__.__name__}({attributes})'

    def merge_with_entity(self, entity: TEntity):
        for key, value in entity.__dict__.items():
            if key == __SA_INSTANCE_STATE__ or value is None:
                continue
            setattr(self, key, value)

    @classmethod
    def new_id(cls) -> int:
        return snow_flake.generate()
