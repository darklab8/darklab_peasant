from .shared import Notificator, format_msg
from peasant import settings, types, exceptions
from typing import Any
import requests
from .stdout import StdoutNotificator
from contextlib import suppress

logger = StdoutNotificator()


def send_msg(channel_id: types.TelegramChannelID, bot_message: str) -> Any:
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    params = dict(chat_id=channel_id, parse_mode="Markdown", text=bot_message)
    request_timeout = 10
    if settings.DEBUG:
        response = requests.get(url, params, timeout=request_timeout)
    else:
        with suppress(Exception):
            response = requests.get(url, params, timeout=request_timeout)

    logger.debug(f"{params=}, {response.text=}")


class TelegramNotificator(Notificator):
    def debug(self, msg: str) -> None:
        send_msg(
            settings.TELEGRAM_CHANNEL_HEALTH,
            format_msg(log_level=settings.LogLev.DEBUG, msg=msg),
        )

    def info(self, msg: str) -> None:
        send_msg(
            settings.TELEGRAM_CHANNEL_NEWS,
            format_msg(log_level=settings.LogLev.INFO, msg=msg),
        )

    def error(self, msg: str) -> None:
        send_msg(
            settings.TELEGRAM_CHANNEL_HEALTH,
            format_msg(log_level=settings.LogLev.ERROR, msg=msg),
        )

    def panic(self, msg: str, from_exc: Exception | None = None, error_cls: types.ExcType = exceptions.PanicException) -> None:
        send_msg(
            settings.TELEGRAM_CHANNEL_HEALTH,
            format_msg(log_level=settings.LogLev.PANIC, msg=msg),
        )
        if from_exc is None:
            raise error_cls(msg)
        raise error_cls(msg) from from_exc
