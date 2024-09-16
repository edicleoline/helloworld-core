from __future__ import annotations

from typing import Any
from typing import Optional

from helloworld.core.util import compat

class HasDescriptionCode:
    code: Optional[str] = None

    def __init__(self, *arg: Any, **kw: Any):
        code = kw.pop("code", None)
        if code is not None:
            self.code = code
        super().__init__(*arg, **kw)

    _what_are_we = "error"

    def _code_str(self) -> str:
        if not self.code:
            return ""
        else:
            return (
                f"(Background on this {self._what_are_we} at: "
                f"https://helloworld.me/e/{self.code})"
            )

    def __str__(self) -> str:
        message = super().__str__()
        if self.code:
            message = "%s %s" % (message, self._code_str())
        return message

class HelloWorldError(HasDescriptionCode, Exception):
    def _message(self) -> str:
        text: str

        if len(self.args) == 1:
            arg_text = self.args[0]

            if isinstance(arg_text, bytes):
                text = compat.decode_backslashreplace(arg_text, "utf-8")
            else:
                text = str(arg_text)

            return text
        else:
            return str(self.args)

    def _sql_message(self) -> str:
        message = self._message()

        if self.code:
            message = "%s %s" % (message, self._code_str())

        return message

    def __str__(self) -> str:
        return self._sql_message()

class ArgumentError(HelloWorldError): ...

class EntityNotFoundError(HelloWorldError): ...

class DatabaseNotInitializedError(HelloWorldError): ...

class NoSessionManagerForTypeError(HelloWorldError): ...

class NoDIFunctionFoundForTypeError(HelloWorldError): ...

class InvalidRequestError(HelloWorldError): ...