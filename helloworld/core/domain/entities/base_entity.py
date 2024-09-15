from __future__ import annotations

from dataclasses import dataclass, asdict
from ulid import ULID

@dataclass
class BaseEntity:
    id: ULID = ''

    @classmethod
    def from_dict(cls, d = None):
        return cls(**d)

    def to_dict(self):
        return asdict(self)

    def __repr__(self):
        return