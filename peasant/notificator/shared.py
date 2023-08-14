from abc import ABCMeta, abstractmethod


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
