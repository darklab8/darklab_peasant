from .stdout import StdoutNotificator
import logging
import pytest
from peasant import exceptions
from peasant.settings import Settings


def test_loggus(caplog, settings: Settings) -> None:  # type: ignore
    caplog.set_level(logging.DEBUG)

    notif = StdoutNotificator(settings=settings) # type: ignore[call-arg]

    notif.debug("debugging msg")
    notif.info("Good news, everyone!")
    notif.panic("smth bad happened!")
