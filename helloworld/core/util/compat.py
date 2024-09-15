from __future__ import annotations

def decode_backslashreplace(text: bytes, encoding: str) -> str:
    return text.decode(encoding, errors="backslashreplace")