"""
lets configure proper logger later. (if ever)
"""

from datetime import datetime

def info(msg: str):
    print(f"{datetime.utcnow()}, INFO, {msg=}")
