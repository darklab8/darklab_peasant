from .stdout import StdoutNotificator
import logging

def test_loggus(caplog) -> None: # type: ignore
    caplog.set_level(logging.DEBUG)
    
    notif = StdoutNotificator()

    notif.debug("debugging msg")
    notif.info("Good news, everyone!")
    notif.error("smth bad happened!")
