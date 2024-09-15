from __future__ import annotations

from typing import Any, Callable, List, Tuple
from blinker import Signal

_signals: List[Tuple[int, str, Callable[..., Any] | None, Signal]] = []

def get_signal(target: Any, identifier: str) -> Signal:
    key = (id(target), identifier)
    for target_id, event_identifier, fn, signal in _signals:
        if target_id == key[0] and event_identifier == identifier:
            return signal

    signal = Signal()
    _signals.append((key[0], identifier, None, signal))
    return signal


def listen(target: Any, identifier: str, fn: Callable[..., Any], *args: Any, **kw: Any) -> None:
    signal = get_signal(target, identifier)
    signal.connect(fn, *args, **kw)

    for i, (target_id, event_identifier, _, signal_ref) in enumerate(_signals):
        if target_id == id(target) and event_identifier == identifier:
            _signals[i] = (target_id, event_identifier, fn, signal_ref)
            break


def listens_for(target: Any, identifier: str, *args: Any, **kw: Any) -> Callable[
    [Callable[..., Any]], Callable[..., Any]]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        listen(target, identifier, fn, *args, **kw)
        return fn

    return decorator


def remove(target: Any, identifier: str, fn: Callable[..., Any]) -> None:
    global _signals
    _signals = [
        (target_id, event_identifier, stored_fn, signal)
        for target_id, event_identifier, stored_fn, signal in _signals
        if not (target_id == id(target) and event_identifier == identifier and stored_fn == fn)
    ]


def contains(target: Any, identifier: str, fn: Callable[..., Any]) -> bool:
    return any(
        target_id == id(target) and event_identifier == identifier and stored_fn == fn
        for target_id, event_identifier, stored_fn, signal in _signals
    )