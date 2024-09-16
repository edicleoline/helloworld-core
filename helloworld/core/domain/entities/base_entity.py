from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional

from ulid import ULID

class BaseEntity(BaseModel):
    id: Optional[ULID] = Field(None, title="User ID")

    @classmethod
    def from_dict(cls, d = None):
        return cls(**d)

    def to_dict(self):
        return self.to_dict()

    def __repr__(self): ...