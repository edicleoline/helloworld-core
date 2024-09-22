from __future__ import annotations

from typing import TypeVar, Type, Dict

T = TypeVar("T")

class ServiceManager:
    _instances: Dict[str, Dict[str, T]] = {}

    async def register(self, service_type: str, name: str, cls_name: Type[T]) -> T:
        if service_type not in self._instances:
            self._instances[service_type] = {}

        if name in self._instances[service_type]:
            raise ValueError(f"Instance with name {name} already exists in service type {service_type}.")

        obj = cls_name()
        obj.name = name
        self._instances[service_type][name] = obj

        return obj

    def get(self, service_type: str, name: str) -> T:
        try:
            return self._instances[service_type][name]
        except KeyError:
            raise ValueError(f"No instance found with name {name} in service type {service_type}.")


service_manager = ServiceManager()