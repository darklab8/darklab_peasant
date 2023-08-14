from .stdout import StdoutNotificator

def test_loggus() -> None:
    
    notif = StdoutNotificator()

    notif.debug("debugging msg")