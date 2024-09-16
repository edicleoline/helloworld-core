from __future__ import annotations

from abc import ABC

from helloworld.core import AbstractUseCase, TRequest, TResponse
from helloworld.core.data import AbstractUnitOfWork

class BaseUseCaseUnitOfWork(AbstractUseCase[TRequest, TResponse], ABC):
    def __init__(self, unit_of_work: AbstractUnitOfWork, authorization: str | None = None):
        self.unit_of_work = unit_of_work
        super().__init__(authorization=authorization)