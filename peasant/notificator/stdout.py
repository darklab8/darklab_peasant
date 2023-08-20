import logging
from .shared import Notificator
from peasant import types, exceptions
from peasant.settings import Settings

class StdoutNotificator(Notificator):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings=settings)
        logging.basicConfig(
            format="f=%(pathname)s,t=%(asctime)s,l=%(levelname)s,m=%(message)s",
            encoding="utf-8",
            level={
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "ERROR": logging.ERROR,
            }[self.settings.log_level],
)


    def debug(self, msg: str) -> None:
        logging.debug(msg)

    def info(self, msg: str) -> None:
        logging.info(msg)

    def error(self, msg: str) -> None:
        logging.error(msg)

    def panic(
        self,
        msg: str,
        from_exc: Exception | None = None,
        error_cls: types.ExcType = exceptions.PanicException,
    ) -> None:
        logging.error(msg)
        if from_exc is None:
            raise error_cls(msg)
        raise error_cls(msg) from from_exc
