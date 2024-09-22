from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from helloworld.core.services.service_manager import service_manager

TRequest = TypeVar('TRequest')
TResponse = TypeVar('TResponse')

T = TypeVar("T")

class AbstractUseCase(ABC, Generic[TRequest, TResponse]):
    def __init__(self, authorization: str | None = None):
        self.authorization = authorization

    @abstractmethod
    async def execute(self, **kwargs) -> TResponse:
        raise NotImplementedError

    @property
    def services(self):
        class ServiceFactory:
            @classmethod
            async def get(cls, service_type: str, name: str) -> T:
                return service_manager.get(service_type, name)

        return ServiceFactory