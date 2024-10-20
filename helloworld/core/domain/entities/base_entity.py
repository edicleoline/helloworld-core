from __future__ import annotations

from pydantic import BaseModel, Field, constr, field_serializer
from typing import Optional, Generic, TypeVar, Any

from helloworld.core.util.snow_flake import snow_flake

T = TypeVar("T", bound="BaseEntity")

class BaseEntity(BaseModel, Generic[T]):
    id: Optional[int] = Field(None, title="Entity id")

    @field_serializer("id")
    def serialize_message(self, id: str | int, _info):
        return str(id)

    def copy(self: T, **kwargs: Any) -> T:
        data = self.dict()
        data.update(kwargs)
        return self.__class__(**data)

    @classmethod
    def new_id(cls) -> int:
        return snow_flake.generate()