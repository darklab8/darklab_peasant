from .discord import DiscordNotificator
import pytest
from peasant import exceptions
from peasant.settings import Settings


def test_discord(settings: Settings) -> None:
    notif = DiscordNotificator(settings=settings)

    notif.debug("debugging msg")
    notif.info("Good news, everyone!")
    with pytest.raises(exceptions.PanicException):
        notif.panic("smth bad happened!")
