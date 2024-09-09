from typing import Generic, TypeVar, Type
from ulid import ULID
from sqlalchemy.orm import DeclarativeBase

TEntity = TypeVar('TEntity')

class BaseModel(DeclarativeBase, Generic[TEntity]):
    __entity_cls__: Type[TEntity] = None
    __log__: bool = True

    def to_entity(self) -> TEntity:
        model_attributes = self.__dict__
        model_attributes.pop('_sa_instance_state', None)
        return self.__entity_cls__(**model_attributes)

    def from_entity(self, entity: TEntity):
        self.__dict__.update(entity.__dict__)
        return self

    def __repr__(self) -> str:
        attributes = ', '.join(f'{key}={value}' for key, value in self.__dict__.items())
        return f'{self.__class__.__name__}({attributes})'

    def merge_with_entity(self, entity: TEntity):
        for key, value in entity.__dict__.items():
            if key != "_sa_instance_state" and value is not None:
                setattr(self, key, value)

    @classmethod
    def new_ulid(cls) -> ULID:
        return ULID()
