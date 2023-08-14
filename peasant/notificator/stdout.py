from datetime import datetime
import logging
from .shared import UnhandledError, Notificator

class StdoutNotificator(Notificator):

    def debug(self, msg: str) -> None:
        print(f"{datetime.utcnow()}, DEBUG, {msg=}")

    def info(self, msg: str) -> None:
        print(f"{datetime.utcnow()}, INFO, {msg=}")

    def error(self, msg: str) -> None:
        msg = f"{datetime.utcnow()}, ERROR, {msg=}"
        logging.error(msg)
        raise UnhandledError(msg)
