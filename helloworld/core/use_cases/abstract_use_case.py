from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TRequest = TypeVar('TRequest')
TResponse = TypeVar('TResponse')

class AbstractUseCase(ABC, Generic[TRequest, TResponse]):
    @abstractmethod
    async def execute(self, request: TRequest) -> TResponse:
        raise NotImplementedError