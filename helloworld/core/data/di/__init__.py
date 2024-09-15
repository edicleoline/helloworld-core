from __future__ import annotations

from typing import Sequence, Dict

from helloworld.core.infra.data.sqlalchemy.db_session_manager import db_session_manager as sqla_db_session_manager
from helloworld.core.infra.data.mongo.db_session_manager import db_session_manager as mongo_db_session_manager
from helloworld.core.data.database.abstract_db_session_manager import AbstractDatabaseSessionManager
from helloworld.core.data.unit_of_work.abstract_unit_of_work import AbstractUnitOfWork
from helloworld.core.data.unit_of_work.base_unit_of_work import BaseUnitOfWork
from helloworld.core.event.api import listen

def db_session_manager_after_commit(sender, enitities: Sequence[Dict]):
    print("@@@@@@@@@@@@@@@", enitities)

def get_sqla_db_session_manager() -> AbstractDatabaseSessionManager:
    db_session_manager = sqla_db_session_manager
    listen(db_session_manager, "after_commit", db_session_manager_after_commit)
    return db_session_manager

def get_mongo_db_session_manager() -> AbstractDatabaseSessionManager:
    return mongo_db_session_manager

async def get_unit_of_work(authorization: str | None = None) -> AbstractUnitOfWork:
    return BaseUnitOfWork(
        session_managers=[
            get_sqla_db_session_manager(),
            get_mongo_db_session_manager()
        ],
        authorization=authorization
    )