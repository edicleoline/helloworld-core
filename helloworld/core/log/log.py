from __future__ import annotations

import logging
import sys
from typing import Any
from typing import Optional
from typing import overload
from typing import Set
from typing import Type
from typing import TypeVar
from typing import Union

from helloworld.core.util._typing import Literal

STACKLEVEL = True
STACKLEVEL_OFFSET = 1

_IT = TypeVar("_IT", bound="Identified")

_EchoFlagType = Union[None, bool, Literal["debug"]]

rootlogger = logging.getLogger("helloworld")
if rootlogger.level == logging.NOTSET:
    rootlogger.setLevel(logging.WARN)


def _add_default_handler(logger: logging.Logger) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )
    logger.addHandler(handler)


_logged_classes: Set[Type[Identified]] = set()


def _qual_logger_name_for_cls(cls: Type[Identified]) -> str:
    return (
        getattr(cls, "_sqla_logger_namespace", None)
        or cls.__module__ + "." + cls.__name__
    )


def class_logger(cls: Type[_IT]) -> Type[_IT]:
    logger = logging.getLogger(_qual_logger_name_for_cls(cls))
    cls._should_log_debug = lambda self: logger.isEnabledFor(  # type: ignore[method-assign]  # noqa: E501
        logging.DEBUG
    )
    cls._should_log_info = lambda self: logger.isEnabledFor(  # type: ignore[method-assign]  # noqa: E501
        logging.INFO
    )
    cls.logger = logger
    _logged_classes.add(cls)
    return cls


_IdentifiedLoggerType = Union[logging.Logger, "InstanceLogger"]


class Identified:
    __slots__ = ()

    logging_name: Optional[str] = None

    logger: _IdentifiedLoggerType

    _echo: _EchoFlagType

    def _should_log_debug(self) -> bool:
        return self.logger.isEnabledFor(logging.DEBUG)

    def _should_log_info(self) -> bool:
        return self.logger.isEnabledFor(logging.INFO)


class InstanceLogger:
    _echo_map = {
        None: logging.NOTSET,
        False: logging.NOTSET,
        True: logging.INFO,
        "debug": logging.DEBUG,
    }

    _echo: _EchoFlagType

    __slots__ = ("echo", "logger")

    def __init__(self, echo: _EchoFlagType, name: str):
        self.echo = echo
        self.logger = logging.getLogger(name)

        if self._echo_map[echo] <= logging.INFO and not self.logger.handlers:
            _add_default_handler(self.logger)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.log(logging.WARNING, msg, *args, **kwargs)

    warn = warning

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.log(logging.ERROR, msg, *args, **kwargs)

    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        kwargs["exc_info"] = 1
        self.log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self.log(logging.CRITICAL, msg, *args, **kwargs)

    def log(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        if self.logger.manager.disable >= level:
            return

        selected_level = self._echo_map[self.echo]
        if selected_level == logging.NOTSET:
            selected_level = self.logger.getEffectiveLevel()

        if level >= selected_level:
            if STACKLEVEL:
                kwargs["stacklevel"] = (
                    kwargs.get("stacklevel", 1) + STACKLEVEL_OFFSET
                )

            self.logger._log(level, msg, args, **kwargs)

    def isEnabledFor(self, level: int) -> bool:
        if self.logger.manager.disable >= level:
            return False
        return level >= self.getEffectiveLevel()

    def getEffectiveLevel(self) -> int:
        level = self._echo_map[self.echo]
        if level == logging.NOTSET:
            level = self.logger.getEffectiveLevel()
        return level


def instance_logger(
    instance: Identified, echoflag: _EchoFlagType = None
) -> None:
    if instance.logging_name:
        name = "%s.%s" % (
            _qual_logger_name_for_cls(instance.__class__),
            instance.logging_name,
        )
    else:
        name = _qual_logger_name_for_cls(instance.__class__)

    instance._echo = echoflag  # type: ignore

    logger: Union[logging.Logger, InstanceLogger]

    if echoflag in (False, None):
        logger = logging.getLogger(name)
    else:
        logger = InstanceLogger(echoflag, name)

    instance.logger = logger  # type: ignore


class echo_property:
    @overload
    def __get__(
        self, instance: Literal[None], owner: Type[Identified]
    ) -> echo_property: ...

    @overload
    def __get__(
        self, instance: Identified, owner: Type[Identified]
    ) -> _EchoFlagType: ...

    def __get__(
        self, instance: Optional[Identified], owner: Type[Identified]
    ) -> Union[echo_property, _EchoFlagType]:
        if instance is None:
            return self
        else:
            return instance._echo

    def __set__(self, instance: Identified, value: _EchoFlagType) -> None:
        instance_logger(instance, echoflag=value)