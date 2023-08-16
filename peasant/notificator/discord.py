from .shared import Notificator, UnhandledError, format_msg
from peasant import settings, exceptions, types
import requests
from .stdout import StdoutNotificator
from contextlib import suppress

logger = StdoutNotificator()


def send_msg(webhook: types.DiscordWebhookUrl, msg: str) -> None:
    request_timeout = 10
    if settings.DEBUG:
        resp = requests.post(
            url=webhook, json=dict(content=msg), timeout=request_timeout
        )
    else:
        with suppress(Exception):
            resp = requests.post(
                url=webhook, json=dict(content=msg), timeout=request_timeout
            )

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
        send_msg(settings.DISCORD_CHANNEL_NEWS, format_msg(settings.LogLev.ERROR, msg))

    def panic(
        self,
        msg: str,
        from_exc: Exception | None = None,
        error_cls: types.ExcType = exceptions.PanicException,
    ) -> None:
        send_msg(
            settings.DISCORD_CHANNEL_HEALTH, format_msg(settings.LogLev.ERROR, msg)
        )
        if from_exc is None:
            raise error_cls(msg)
        raise error_cls(msg) from from_exc
