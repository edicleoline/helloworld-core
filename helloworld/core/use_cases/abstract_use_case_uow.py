from abc import ABC
from helloworld.core.use_cases.abstract_use_case import AbstractUseCase, TRequest, TResponse
from helloworld.core.data.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork

class AbstractUseCaseUnitOfWork(AbstractUseCase[TRequest, TResponse], ABC):
    def __init__(self, unit_of_work: AbstractUnitOfWork):
        self.unit_of_work = unit_of_work