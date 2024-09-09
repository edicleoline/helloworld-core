from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable

TSession = TypeVar('TSession')

class AbstractUnitOfWork(ABC, Generic[TSession]):
    def __init__(self, session_factory: Callable[[], TSession] = None):
        self.session_factory = session_factory

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    def __await__(self):
        return self.__aenter__().__await__()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError