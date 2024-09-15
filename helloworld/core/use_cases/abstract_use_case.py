from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TRequest = TypeVar('TRequest')
TResponse = TypeVar('TResponse')

class AbstractUseCase(ABC, Generic[TRequest, TResponse]):
    def __init__(self, authorization: str | None = None):
        self.authorization = authorization

    @abstractmethod
    async def execute(self, **kwargs) -> TResponse:
        raise NotImplementedError