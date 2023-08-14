from .shared import Notificator
from .stdout import StdoutNotificator
from .telegram import TelegramNotificator
from .discord import DiscordNotificator

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
            notificator.debug(msg)

    def error(self, msg: str) -> None:
        for notificator in self._notificators:
            notificator.debug(msg)
