from helloworld.core.infra.data.sqlalchemy.db_session_manager import db_session_manager
from helloworld.core.infra.data.sqlalchemy.base_unit_of_work import BaseUnitOfWork
from helloworld.core.data.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork

async def get_db_session_manager():
    return db_session_manager

async def get_unit_of_work(_db_session_manager) -> AbstractUnitOfWork:
    return BaseUnitOfWork(session_factory=_db_session_manager.session)