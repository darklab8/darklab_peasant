import logging
from .shared import UnhandledError, Notificator, PanicException
from peasant import settings

logging.basicConfig(
    format="f=%(pathname)s,t=%(asctime)s,l=%(levelname)s,m=%(message)s",
    encoding="utf-8",
    level={
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "ERROR": logging.ERROR,
    }[settings.LOG_LEVEL],
)


class StdoutNotificator(Notificator):
    def debug(self, msg: str) -> None:
        logging.debug(msg)

    def info(self, msg: str) -> None:
        logging.info(msg)

    def panic(self, msg: str, exc: Exception | None = None) -> None:
        logging.error(msg)
        if exc is None:
            raise PanicException(msg)
        raise PanicException(msg) from exc

