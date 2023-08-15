from .shared import Notificator, UnhandledError, format_msg
from peasant import settings
import requests
from .stdout import StdoutNotificator
from peasant import types

logger = StdoutNotificator()


def send_msg(webhook: types.DiscordWebhookUrl, msg: str) -> None:
    resp = requests.post(url=webhook, json=dict(content=msg))

    if resp.status_code != 204:
        logger.debug(f"{resp.text=}")
        UnhandledError("failed sending msg")


class DiscordNotificator(Notificator):
    def debug(self, msg: str) -> None:
        send_msg(
            settings.DISCORD_CHANNEL_HEALTH, format_msg(settings.LogLev.DEBUG, msg)
        )

    def info(self, msg: str) -> None:
        send_msg(settings.DISCORD_CHANNEL_NEWS, format_msg(settings.LogLev.INFO, msg))

    def error(self, msg: str) -> None:
        send_msg(
            settings.DISCORD_CHANNEL_HEALTH, format_msg(settings.LogLev.ERROR, msg)
        )
