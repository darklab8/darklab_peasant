from abc import ABCMeta, abstractmethod
from datetime import datetime
from peasant import types
from pathlib import Path
import inspect
from typing import Optional
from peasant import exceptions


def format_msg(log_level: types.LogLevel, msg: str) -> str:
    filenames = list([calling_file.filename for calling_file in inspect.stack()])
    caller_path = "undefined"

    for filename in reversed(filenames):
        if "/peasant/" in filename and "tests" not in filename:
            caller_path = filename
            break

    return f"f={Path(caller_path).name},t={datetime.utcnow()},l={log_level},m={msg}"


class UnhandledError(Exception):
    pass

class Notificator(metaclass=ABCMeta):
    @abstractmethod
    def debug(self, msg: str) -> None:
        """
        Pinging and etc msgs
        """
        pass

    @abstractmethod
    def info(self, msg: str) -> None:
        """
        Important msg users wish to see
        """

    @abstractmethod
    def panic(self, msg: str, from_exc: Optional[Exception] = None, error_cls: types.ExcType = exceptions.PanicException) -> None:
        """
        Critical problems.
        """
