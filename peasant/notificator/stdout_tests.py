from .stdout import StdoutNotificator
import logging
import pytest
from .shared import PanicException

def test_loggus(caplog) -> None:  # type: ignore
    caplog.set_level(logging.DEBUG)

    notif = StdoutNotificator()

    notif.debug("debugging msg")
    notif.info("Good news, everyone!")
    with pytest.raises(PanicException):
        notif.panic("smth bad happened!")
