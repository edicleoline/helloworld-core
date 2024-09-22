from __future__ import annotations

import typing

if True:  # zimports removes the tailing comments
    from typing_extensions import (
        Literal as Literal,
    )  # 3.8 but has bugs before 3.10


_LITERAL_TYPES = frozenset([typing.Literal, Literal])