from __future__ import annotations

from typing import Any, Type, TypeVar, Dict

T = TypeVar('T')

def validate_kwarg(kwargs: Dict[str, Any], key: str, expected_type: Type[T]) -> bool:
    return key in kwargs and isinstance(kwargs[key], expected_type)

def get_kwarg(kwargs: Dict[str, Any], key: str, expected_type: Type[T]) -> T | None:
    if validate_kwarg(kwargs, key, expected_type):
        return kwargs[key]

    return None