from celery import Celery
from celery.schedules import crontab
from typing import Any
from .notificator.aggregator import NotificatorAggregator, iNotificator
from typing import NewType
from pydantic import BaseModel, ConfigDict, Field
from celery.signals import beat_init
from peasant.settings import Settings

settings = Settings() # type: ignore[call-arg]

app = Celery("peasant")
app.conf.broker_url = settings.celery_redis_host
app.conf.result_backend = settings.celery_redis_host
app.conf.broker_connection_retry_on_startup = True
app.conf.beat_max_loop_interval = 10

ExpiresInSeconds = NewType("ExpiresInSeconds", int)
PeriodInSeconds = NewType("PeriodInSeconds", float)
default_expires: ExpiresInSeconds = ExpiresInSeconds(60)


class ScheduledOptions(BaseModel):
    expires: ExpiresInSeconds = default_expires


class ScheduledTask(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    task: str
    schedule: PeriodInSeconds | crontab
    args: tuple
    options: ScheduledOptions = Field(default_factory=ScheduledOptions)


scheduled_tasks = (
    ScheduledTask(
        task="peasant.celery.add",
        schedule=PeriodInSeconds(30.0),
        args=(16, 16),
    ),
    ScheduledTask(
        task="peasant.celery.add",
        schedule=crontab(hour=7, minute=30, day_of_week=1),
        args=(32, 32),
    ),
)

app.conf.beat_schedule = dict(
    {repr(task): task.model_dump() for task in scheduled_tasks}
)

from celery.signals import after_task_publish


@beat_init.connect
def auto_purger(sender=None, headers=None, body=None, **kwargs):  # type: ignore
    app.control.purge()
    print("purged tasks")


@app.task
def add(x: int, y: int) -> int:
    result = x + y
    logger: iNotificator = NotificatorAggregator(settings=settings)
    logger.debug(f"{result=}")
    return result
