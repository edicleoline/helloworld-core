from __future__ import annotations

import typing

if True:  # zimports removes the tailing comments
    from typing_extensions import (
        Literal as Literal,
    )  # 3.8 but has bugs before 3.10


_LITERAL_TYPES = frozenset([typing.Literal, Literal])


def cast_value(value: str):
    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    lower_value = value.lower()
    if lower_value in {"true", "false"}:
        return lower_value == "true"

    return value