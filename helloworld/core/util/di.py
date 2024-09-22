from __future__ import annotations

import inspect
import os
import re
import importlib.metadata
import importlib.util
from collections.abc import Callable
from typing import get_type_hints, TypeVar

DI = "di"
METADATA_NAME = "Name"
INIT_PY = "__init__.py"
_RETURN = "return"

T = TypeVar("T")


#todo: throw if there is more than one found
#todo: cache it [now!]
def find_di_func_by_type(repository_type: T, pattern: re.Pattern) -> Callable | None:
    packages = [dist.metadata[METADATA_NAME] for dist in importlib.metadata.distributions()
                if pattern.match(dist.metadata[METADATA_NAME])]
    for package_name in packages:
        try:
            module_name = package_name.replace("-", ".")
            package = importlib.import_module(module_name)
            package_path = package.__path__[0]

            for root, dirs, files in os.walk(package_path):
                if not DI in dirs: continue

                di_init_path = os.path.join(root, DI, INIT_PY)
                if not os.path.exists(di_init_path): continue

                spec = importlib.util.spec_from_file_location(f"{package_name}.{DI}", di_init_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for name, func in inspect.getmembers(module, inspect.isfunction):
                    type_hints = get_type_hints(func)
                    return_hint = type_hints.get(_RETURN, None)

                    if return_hint != repository_type: continue

                    return func
        except Exception as e:
            print(f"Error {package_name}: {e}")

    return None