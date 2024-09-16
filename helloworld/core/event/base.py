from __future__ import annotations

from typing import List, Any, Tuple, Callable
import asyncio

from reactivex.subject import Subject
from reactivex import operators as ops

class AsyncEvents:
    _signals: List[Tuple[str, Subject]]

    def __init__(self):
        self._signals = []

    async def register_event(self, event_name: str) -> None:
        if not any(event for event, _ in self._signals if event == event_name):
            signal = Subject()
            self._signals.append((event_name, signal))

    async def trigger_event(self, event_name: str, **kwargs: Any) -> None:
        for event, signal in self._signals:
            if event == event_name:
                await asyncio.sleep(0)
                signal.on_next(kwargs)
                return
        print(f"Event '{event_name}' not registered.")

    async def listen(self, event_name: str, observer: Callable[..., Any]) -> None:
        for event, signal in self._signals:
            if event == event_name:
                async def async_observer(data):
                    await asyncio.sleep(0)
                    observer(data)

                signal.pipe(ops.map(lambda x: asyncio.create_task(async_observer(x)))).subscribe()
                return
        print(f"Event '{event_name}' not registered, cannot listen.")


class Events:
    _signals: List[Tuple[str, Subject]]

    def __init__(self):
        self._signals = []

    def register_event(self, event_name: str) -> None:
        if not any(event for event, _ in self._signals if event == event_name):
            signal = Subject()
            self._signals.append((event_name, signal))

    def trigger_event(self, event_name: str, **kwargs: Any) -> None:
        for event, signal in self._signals:
            if event == event_name:
                signal.on_next(kwargs)
                return

        print(f"Event '{event_name}' not registered.")

    def listen(self, event_name: str, observer: Callable[..., Any]) -> None:
        for event, signal in self._signals:
            if event == event_name:
                signal.subscribe(observer)
                return

        print(f"Event '{event_name}' not registered, cannot listen.")