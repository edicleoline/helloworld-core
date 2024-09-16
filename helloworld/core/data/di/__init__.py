from __future__ import annotations

from helloworld.core.data import AbstractUnitOfWork, BaseUnitOfWork

def get_unit_of_work(authorization: str | None = None) -> AbstractUnitOfWork:
    return BaseUnitOfWork(authorization=authorization)
