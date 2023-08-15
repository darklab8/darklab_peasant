from .shared import Notificator, PanicException
from .stdout import StdoutNotificator
from .telegram import TelegramNotificator
from .discord import DiscordNotificator
from contextlib import suppress

class NotificatorAggregator(Notificator):
    """
    sending msgs to Stdout/Discord/Telegram :smile:
    """

    def __init__(self) -> None:
        self._notificators: list[Notificator] = []
        self._notificators.append(StdoutNotificator())
        self._notificators.append(TelegramNotificator())
        self._notificators.append(DiscordNotificator())

    def debug(self, msg: str) -> None:
        for notificator in self._notificators:
            notificator.debug(msg)

    def info(self, msg: str) -> None:
        for notificator in self._notificators:
            notificator.info(msg)

    def panic(self, msg: str, exc: Exception | None = None) -> None:
        
        for notificator in self._notificators:
            with suppress(PanicException):
                notificator.panic(msg)
        if exc is None:
            raise PanicException(msg)
        raise PanicException(msg) from exc

        

