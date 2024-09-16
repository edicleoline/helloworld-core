from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")

def db_session_manager(type: T):
    def decorator(func):
        func.db_session_manager_type = type
        return func
    return decorator