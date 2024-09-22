from __future__ import annotations

from pydantic import BaseModel, Field, constr
from typing import Optional, Generic, TypeVar, Any

T = TypeVar("T", bound="BaseEntity")

class BaseEntity(BaseModel, Generic[T]):
    id: Optional[str] = Field(None, title="User ID")

    @classmethod
    def from_dict(cls, d = None):
        return cls(**d)

    def to_dict(self):
        return self.to_dict()

    def __repr__(self): ...

    def copy(self: T, **kwargs: Any) -> T:
        data = self.dict()
        data.update(kwargs)
        return self.__class__(**data)