from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence, Any

class AbstractUnitOfWork(ABC):
    def __init__(self, session_managers: Sequence[Any], authorization: str | None = None):
        self.session_managers: Sequence[Any] = session_managers
        self.authorization: str | None = authorization

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, *_):
        pass

    async def __aenter__(self):
        return self
