import pytest
from .discord import DiscordNotificator
from .telegram import TelegramNotificator
from .stdout import StdoutNotificator
from .shared import Notificator
from typing import Type
import logging
from _pytest.logging import LogCaptureFixture
from peasant.settings import Settings


@pytest.mark.parametrize(
    "notificator_cls",
    [
        StdoutNotificator,
        DiscordNotificator,
        TelegramNotificator,
    ],
)
def test_notificator(
    notificator_cls: Type[Notificator], caplog: LogCaptureFixture, settings: Settings
) -> None:
    caplog.set_level(logging.DEBUG)
    msgr = notificator_cls(settings=settings)  # type: ignore[call-arg]
    msgr.debug("Health is OK")
