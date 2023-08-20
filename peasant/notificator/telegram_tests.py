from .telegram import TelegramNotificator
import pytest
from peasant import exceptions
from peasant.settings import Settings


def test_telegram(settings: Settings) -> None:
    notif = TelegramNotificator(settings=settings) # type: ignore[call-arg]

    notif.debug("debugging msg")
    notif.info("Good news, everyone!")
    with pytest.raises(exceptions.PanicException):
        notif.panic("smth bad happened!")
