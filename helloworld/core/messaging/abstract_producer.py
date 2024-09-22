from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Type

T = TypeVar("T")
M = TypeVar("M")

class AbstractProducer(ABC, Generic[T, M]):
    @abstractmethod
    def init(self, *args, **kwargs) -> AbstractProducer:
        raise NotImplementedError

    @abstractmethod
    async def start(self) -> T:
        raise NotImplementedError

    @abstractmethod
    async def send(self, topic: str, message: M) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def stop(self) -> None:
        raise NotImplementedError