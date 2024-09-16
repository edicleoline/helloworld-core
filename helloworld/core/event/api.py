from __future__ import annotations

from typing import Any, Callable, List, Tuple, Optional

from reactivex.abc import DisposableBase
from reactivex.subject import Subject

_signals: List[Tuple[int, str, Optional[Callable[..., Any]], Subject]] = []

def get_signal(target: Any, identifier: str) -> Subject:
    key = (id(target), identifier)
    for target_id, event_identifier, fn, signal in _signals:
        if target_id == key[0] and event_identifier == identifier:
            return signal

    signal = Subject()
    _signals.append((key[0], identifier, None, signal))
    return signal

def listen(target: Any, identifier: str, fn: Callable[..., Any], *args: Any, **kw: Any) -> DisposableBase:
    signal = get_signal(target, identifier)

    disposable = signal.subscribe(fn, *args, **kw)

    for i, (target_id, event_identifier, _, signal_ref) in enumerate(_signals):
        if target_id == id(target) and event_identifier == identifier:
            _signals[i] = (target_id, event_identifier, fn, signal_ref)
            break

    return disposable

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