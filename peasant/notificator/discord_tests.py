from .discord import DiscordNotificator
import pytest
from peasant import exceptions


def test_discord() -> None:
    notif = DiscordNotificator()

    notif.debug("debugging msg")
    notif.info("Good news, everyone!")
    with pytest.raises(exceptions.PanicException):
        notif.panic("smth bad happened!")
