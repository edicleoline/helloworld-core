from __future__ import annotations

def service_manager(service_type: str, name: str):
    def decorator(func):
        func.__service_type__ = service_type
        func.__service_name__ = name
        return func
    return decorator