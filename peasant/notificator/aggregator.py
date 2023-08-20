from .shared import Notificator
from .stdout import StdoutNotificator
from .telegram import TelegramNotificator
from .discord import DiscordNotificator
from contextlib import suppress
from peasant import types, exceptions
from peasant.settings import Settings


class NotificatorAggregator(Notificator):
    """
    sending msgs to Stdout/Discord/Telegram :smile:
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._notificators: list[Notificator] = []
        self._notificators.append(StdoutNotificator(settings=settings))
        self._notificators.append(TelegramNotificator(settings=settings))
        self._notificators.append(DiscordNotificator(settings=settings))

    def debug(self, msg: str) -> None:
        for notificator in self._notificators:
            notificator.debug(msg)

    def info(self, msg: str) -> None:
        for notificator in self._notificators:
            notificator.info(msg)

    def panic(
        self,
        msg: str,
        from_exc: Exception | None = None,
        error_cls: types.ExcType = exceptions.PanicException,
    ) -> None:
        for notificator in self._notificators:
            with suppress(error_cls):
                notificator.panic(msg, from_exc=from_exc, error_cls=error_cls)
        if from_exc is None:
            raise error_cls(msg)
        raise error_cls(msg) from from_exc
