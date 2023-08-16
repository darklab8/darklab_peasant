from .telegram import TelegramNotificator
import pytest
from peasant import exceptions

def test_telegram() -> None:
    notif = TelegramNotificator()

    notif.debug("debugging msg")
    notif.info("Good news, everyone!")
    with pytest.raises(exceptions.PanicException):
        notif.panic("smth bad happened!")
