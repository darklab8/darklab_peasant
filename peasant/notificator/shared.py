from abc import ABCMeta, abstractmethod
from datetime import datetime
from peasant import types
from pathlib import Path
import inspect
from peasant import exceptions
from peasant.settings import Settings
from typing import Protocol

def format_msg(log_level: types.LogLevel, msg: str) -> str:
    filenames = list([calling_file.filename for calling_file in inspect.stack()])
    caller_path = "undefined"

    for filename in reversed(filenames):
        if "/peasant/" in filename and "tests" not in filename:
            caller_path = filename
            break

    return f"f={Path(caller_path).name},t={datetime.utcnow()},l={log_level},m={msg}"


class NotificationException(exceptions.PeasantException):
    pass


class iNotificator(Protocol):
    def __init__(self, settings: Settings) -> None: ...

    def debug(self, msg: str) -> None: ...

    def info(self, msg: str) -> None: ...

    def error(self, msg: str) -> None: ...

    def panic(self, msg: str) -> None: ...