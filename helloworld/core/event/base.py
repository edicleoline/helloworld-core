from __future__ import annotations

from typing import List, Any, Tuple, Callable

from reactivex.subject import Subject

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

        raise ValueError(f"Event '{event_name}' not registered.")

    def listen(self, event_name: str, observer: Callable[..., Any]) -> None:
        for event, signal in self._signals:
            if event == event_name:
                signal.subscribe(observer)
                return

        raise ValueError(f"Event '{event_name}' not registered, cannot listen.")