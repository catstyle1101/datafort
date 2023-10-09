from datetime import datetime
from celery import Celery
from celery.schedules import crontab


app = Celery(
    'parser_celery_project',
    broker='redis://redis:6379/0',
    include=['weather_parser'],
)

app.conf.beat_schedule = {
    'parse': {
        'task': 'weather_parser.parse_weather',
        'schedule': crontab(minute=(datetime.now().minute + 1) % 60),
    },
}
