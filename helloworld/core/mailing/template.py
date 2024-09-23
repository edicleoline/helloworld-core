from __future__ import annotations

class Template:
    name: str
    content: str
    lang: str

    def __init__(self, name: str, lang: str, content: str):
        self.name = name
        self.content = content
        self.lang = lang