from celery import Celery
from celery.schedules import crontab
from celery.app.base import Celery as CeleryApp
from typing import Any
from . import settings

app = Celery('peasant')
app.conf.broker_url = settings.REDIS_HOST
app.conf.broker_connection_retry_on_startup = True

@app.on_after_configure.connect
def setup_periodic_tasks(sender: CeleryApp, **kwargs: dict[str, Any]) -> None:
    sender.add_periodic_task(10.0, add.s(16,16), name='add every 10', expires=10)

    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1), add.s(18,18), name='add every 10', expires=10
    )

@app.task
def add(x: int, y: int) -> int:
    return x + y
