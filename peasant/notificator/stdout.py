import logging
from .shared import format_msg
from peasant import types
from peasant.settings import Settings

class StdoutNotificator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def debug(self, msg: str) -> None:
        print(format_msg(log_level=types.LogLev.DEBUG, msg=msg))

    def info(self, msg: str) -> None:
        print(format_msg(log_level=types.LogLev.INFO, msg=msg))

    def error(self, msg: str) -> None:
        print(format_msg(log_level=types.LogLev.ERROR, msg=msg))

    def panic(
        self,
        msg: str,
    ) -> None:
        print(format_msg(log_level=types.LogLev.PANIC, msg=msg))
