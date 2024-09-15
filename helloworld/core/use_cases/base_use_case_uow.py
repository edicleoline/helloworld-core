from __future__ import annotations

from abc import ABC

from helloworld.core.use_cases.abstract_use_case import AbstractUseCase, TRequest, TResponse
from helloworld.core.data.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork

class BaseUseCaseUnitOfWork(AbstractUseCase[TRequest, TResponse], ABC):
    def __init__(self, unit_of_work: AbstractUnitOfWork, authorization: str | None = None):
        self.unit_of_work = unit_of_work
        super().__init__(authorization=authorization)