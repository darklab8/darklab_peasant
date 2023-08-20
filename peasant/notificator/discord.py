from .shared import Notificator, NotificationException, format_msg
from peasant import exceptions, types
import requests
from .stdout import StdoutNotificator
from peasant.settings import Settings

class DiscordNotificator(Notificator):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings=settings)
        self.logger = StdoutNotificator(settings=self.settings)

    def debug(self, msg: str) -> None:
        self.send_msg(
            self.settings.discord_channel_health, format_msg(types.LogLev.DEBUG, msg)
        )

    def info(self, msg: str) -> None:
        self.send_msg(self.settings.discord_channel_news, format_msg(types.LogLev.INFO, msg))

    def error(self, msg: str) -> None:
        self.send_msg(self.settings.discord_channel_news, format_msg(types.LogLev.ERROR, msg))

    def panic(
        self,
        msg: str,
        from_exc: Exception | None = None,
        error_cls: types.ExcType = exceptions.PanicException,
    ) -> None:
        self.send_msg(
            self.settings.discord_channel_news, format_msg(types.LogLev.ERROR, msg)
        )
        if from_exc is None:
            raise error_cls(msg)
        raise error_cls(msg) from from_exc
    
    def send_msg(self, webhook: types.DiscordWebhookUrl, msg: str) -> None:
        request_timeout = 10
        if self.settings.debug:
            resp = requests.post(
                url=webhook, json=dict(content=msg), timeout=request_timeout
            )
        else:
            try:
                resp = requests.post(
                    url=webhook, json=dict(content=msg), timeout=request_timeout
                )
            except Exception as err:
                self.logger.error(f"discord.send_msg error, {str(err)=}")

        if resp.status_code != 204:
            self.logger.debug(f"{resp.text=}")
            NotificationException("failed sending msg")
