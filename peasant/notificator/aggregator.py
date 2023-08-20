from .shared import iNotificator
from .stdout import StdoutNotificator
from .telegram import TelegramNotificator
from .discord import DiscordNotificator
from peasant.settings import Settings


class NotificatorAggregator:
    """
    sending msgs to Stdout/Discord/Telegram :smile:
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._notificators: list[iNotificator] = []
        self.logger = StdoutNotificator(settings=settings)
        self._notificators.append(self.logger)
        self._notificators.append(TelegramNotificator(settings=settings))
        self._notificators.append(DiscordNotificator(settings=settings))

    def debug(self, msg: str) -> None:
        for notificator in self._notificators:
            notificator.debug(msg)

    def info(self, msg: str) -> None:
        for notificator in self._notificators:
            notificator.info(msg)

    def error(self, msg: str) -> None:
        for notificator in self._notificators:
            notificator.info(msg)

    def panic(self, msg: str) -> None:
        for notificator in self._notificators:
            notificator.panic(msg)
