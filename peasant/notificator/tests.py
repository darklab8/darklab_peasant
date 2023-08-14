import pytest
from .discord import DiscordNotificator
from .telegram import TelegramNotificator
from .stdout import StdoutNotificator
from .shared import Notificator
from typing import Type
import logging

@pytest.mark.parametrize(
    "notificator_cls",
    [
        StdoutNotificator,
        DiscordNotificator,
        TelegramNotificator,
    ],
)
def test_notificator(notificator_cls: Type[Notificator], caplog) -> None:
    caplog.set_level(logging.DEBUG)
    msgr = notificator_cls()
    msgr.debug("Health is OK")
