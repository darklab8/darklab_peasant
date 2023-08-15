from .shared import Notificator, PanicException
from .stdout import StdoutNotificator
from .telegram import TelegramNotificator
from .discord import DiscordNotificator
from contextlib import suppress
from peasant import types

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

    def panic(self, msg: str, from_exc: Exception | None = None, error_cls: types.ExcType = PanicException) -> None:
        
        for notificator in self._notificators:
            with suppress(PanicException):
                notificator.panic(msg)
        if from_exc is None:
            raise error_cls(msg)
        raise error_cls(msg) from from_exc

        

