from __future__ import annotations

from abc import ABC, abstractmethod

class AbstractSender(ABC):
    @abstractmethod
    def init(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def send(self, to: str, subject: str, body: str, **kwargs) -> None:
        raise NotImplementedError