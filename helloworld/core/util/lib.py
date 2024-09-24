from __future__ import annotations

import importlib
from typing import Type, Any


def load_class_from_string(class_path: str) -> Type[Any]:
    module_path, class_name = class_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)