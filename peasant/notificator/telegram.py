from .shared import Notificator, format_msg, PanicException
from peasant import settings, types
from typing import Any
import requests
from .stdout import StdoutNotificator

logger = StdoutNotificator()


def send_msg(channel_id: types.TelegramChannelID, bot_message: str) -> Any:
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    params = dict(chat_id=channel_id, parse_mode="Markdown", text=bot_message)
    response = requests.get(url, params)

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

    def panic(self, msg: str) -> None:
        send_msg(
            settings.TELEGRAM_CHANNEL_HEALTH,
            format_msg(log_level=settings.LogLev.ERROR, msg=msg),
        )
        raise PanicException(msg)
