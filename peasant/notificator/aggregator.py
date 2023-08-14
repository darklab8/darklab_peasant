from .shared import Notificator
from .stdout import StdoutNotificator

class NotificatorAggregator(Notificator):
    """
    sending msgs to Stdout/Discord/Telegram :smile:
    """

    def __init__(self) -> None:
        self.notificators: list[Notificator] = []

        self.notificators.append(
            StdoutNotificator()
        )
    
    def debug(self, msg: str) -> None:
        for notificator in self.notificators:
            notificator.debug(msg)

    def info(self, msg: str) -> None:
        for notificator in self.notificators:
            notificator.debug(msg)

    def error(self, msg: str) -> None:
        for notificator in self.notificators:
            notificator.debug(msg)
