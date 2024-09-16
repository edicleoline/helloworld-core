from __future__ import annotations

from typing import Sequence, Dict

from helloworld.core.data import AbstractDatabaseSessionManager, AbstractUnitOfWork, BaseUnitOfWork

from helloworld.core.infra.data.sqlalchemy import db_session_manager as sqla_db_session_manager
from helloworld.core.infra.data.mongo import db_session_manager as mongo_db_session_manager

def db_session_manager_after_commit(enitities: Sequence[Dict]):
    # print("@@@@@@@@@@@@@@@", enitities)
    pass

def get_sqla_db_session_manager() -> AbstractDatabaseSessionManager:
    db_session_manager = sqla_db_session_manager
    db_session_manager.listen("after_commit", db_session_manager_after_commit)
    return db_session_manager

def get_mongo_db_session_manager() -> AbstractDatabaseSessionManager:
    return mongo_db_session_manager

def get_unit_of_work(authorization: str | None = None) -> AbstractUnitOfWork:
    return BaseUnitOfWork(
        session_managers=[
            get_sqla_db_session_manager(),
            get_mongo_db_session_manager()
        ],
        authorization=authorization
    )
