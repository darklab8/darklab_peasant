from .shared import Notificator, format_msg
from peasant import types, exceptions
from typing import Any
import requests
from .stdout import StdoutNotificator
from peasant.settings import Settings

class TelegramNotificator(Notificator):

    def __init__(self, settings: Settings) -> None:
        super().__init__(settings=settings)
        self.logger = StdoutNotificator(settings=self.settings)

    def debug(self, msg: str) -> None:
        self.send_msg(
            self.settings.telegram_channel_health,
            format_msg(log_level=types.LogLev.DEBUG, msg=msg),
        )

    def info(self, msg: str) -> None:
        self.send_msg(
            self.settings.telegram_channel_news,
            format_msg(log_level=types.LogLev.INFO, msg=msg),
        )

    def error(self, msg: str) -> None:
        self.send_msg(
            self.settings.telegram_channel_health,
            format_msg(log_level=types.LogLev.ERROR, msg=msg),
        )

    def panic(
        self,
        msg: str,
        from_exc: Exception | None = None,
        error_cls: types.ExcType = exceptions.PanicException,
    ) -> None:
        self.send_msg(
            self.settings.telegram_channel_health,
            format_msg(log_level=types.LogLev.PANIC, msg=msg),
        )
        if from_exc is None:
            raise error_cls(msg)
        raise error_cls(msg) from from_exc
    
    def send_msg(self, channel_id: types.TelegramChannelID, bot_message: str) -> Any:
        url = f"https://api.telegram.org/bot{self.settings.telegram_bot_token}/sendMessage"
        params = dict(chat_id=channel_id, parse_mode="Markdown", text=bot_message)
        request_timeout = 10
        if self.settings.debug:
            response = requests.get(url, params, timeout=request_timeout)
        else:
            try:
                response = requests.get(url, params, timeout=request_timeout)
            except Exception as err:
                self.logger.error(f"telegram.send_msg error, {str(err)=}")

        self.logger.debug(f"{params=}, {response.text=}")
