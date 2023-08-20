"""
Lambda handler
"""
from .settings import Settings
from .seleniumer import Loginner
from typing import Any
from peasant.notificator.aggregator import NotificatorAggregator


def handler(event: dict[str, Any], context: Any) -> str:
    settings = Settings(**event)

    logger = NotificatorAggregator(settings=settings)
    if settings.test_mode:
        msg_test_success = "Test is made succesfully"
        logger.debug(msg_test_success)
        return msg_test_success

    Loginner(settings=settings).login()

    msg_lambda_success = 'Lambda is executed succesfully'
    logger.debug(msg_lambda_success)
    return msg_lambda_success
