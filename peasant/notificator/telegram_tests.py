from .telegram import TelegramNotificator
import pytest
from peasant import exceptions
from peasant.settings import Settings


def test_telegram(settings: Settings) -> None:
    notif = TelegramNotificator(settings=settings) # type: ignore[call-arg]

    notif.debug("debugging msg")
    notif.info("Good news, everyone!")
    notif.panic('f=lambda_function.py,t=2023-08-20 04:52:53.158158,l=PANIC,m=')

    
