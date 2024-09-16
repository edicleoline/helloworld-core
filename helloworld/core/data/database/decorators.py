from __future__ import annotations

def db_session_manager(name: str):
    def decorator(func):
        func.db_session_manager_name = name
        return func
    return decorator