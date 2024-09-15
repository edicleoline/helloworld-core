from __future__ import annotations

from typing import List

from .api import get_signal, Signal

class Events:
    _signals: List[(str, Signal)]

    def __init__(self):
        self._signals = []

    def register_event(self, target, event_name: str) -> None:
        if not any(event for event, _ in self._signals if event == event_name):
            signal = get_signal(target, event_name)
            self._signals.append((event_name, signal))

    def trigger_event(self, target, event_name: str, **kwargs) -> None:
        for event, signal in self._signals:
            if event == event_name:
                signal.send(target, **kwargs)
                return

        print(f"Event '{event_name}' not registered.")