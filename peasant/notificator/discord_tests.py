from .discord import DiscordNotificator
from .shared import iNotificator
import pytest
from peasant import exceptions
from peasant.settings import Settings


def test_discord(settings: Settings) -> None:
    notif: iNotificator = DiscordNotificator(settings=settings)

    notif.debug("debugging msg")
    notif.info("Good news, everyone!")
    notif.panic("smth bad happened!")
