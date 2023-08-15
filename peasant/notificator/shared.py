from abc import ABCMeta, abstractmethod
from datetime import datetime
from peasant import settings, types
from pathlib import Path

def format_msg(log_level: types.LogLevel, msg: str) -> str:
    return f"f={Path(__file__).name},t={datetime.utcnow()},l={log_level},m={msg}"

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
    def error(self, msg: str) -> None:
        """
        Critical problems.
        """
