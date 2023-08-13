from celery import Celery

app = Celery('peasant')
app.conf.broker_url = 'redis://localhost:6379/0'

@app.task
def add(x: int, y: int) -> int:
    return x + y
