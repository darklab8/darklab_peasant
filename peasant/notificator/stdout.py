import logging
from .shared import Notificator, PanicException
from peasant import settings, types

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

    def error(self, msg: str) -> None:
        logging.error(msg)

    def panic(self, msg: str, from_exc: Exception | None = None, error_cls: types.ExcType = PanicException) -> None:
        logging.error(msg)
        if from_exc is None:
            raise error_cls(msg)
        raise error_cls(msg) from from_exc

