"""
lets configure proper logger later. (if ever)
"""

from datetime import datetime
import logging

class UnhandledError(Exception):
    pass

def info(msg: str) -> None:
    print(f"{datetime.utcnow()}, INFO, {msg=}")

def error(msg: str) -> None:
    msg = f"{datetime.utcnow()}, ERROR, {msg=}"
    logging.error(msg)
    raise UnhandledError(msg)
