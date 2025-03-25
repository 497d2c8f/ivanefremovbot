import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
import django
django.setup()

from celery import Celery
from celery.schedules import crontab
import datetime
import pytz
import redis
import pickle
from bot.models import *
#from django.db.models import F


NOTIFICATION_INTERVAL = 5 #секунд


app = Celery(
	'tasks',
	broker=f'redis://{os.getenv("REDIS_HOST")}:6379/0',
	backend=f'redis://{os.getenv("REDIS_HOST")}:6379/0',
	broker_connection_retry_on_startup=True,
	timezone = 'America/Adak'
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

	sender.add_periodic_task(NOTIFICATION_INTERVAL, tasks_reached_deadline_handler.s(), name='tasks_reached_deadline_handler')


@app.task
def tasks_reached_deadline_handler():

	tz = pytz.timezone('America/Adak')
	now = datetime.datetime.now(tz)
	timedelta = datetime.timedelta(seconds=NOTIFICATION_INTERVAL)

	tasks_reached_deadline = Task.objects.filter(deadline__lt=now)
	tasks_reached_deadline.update(deadline = now + timedelta)

	r = redis.from_url(f'redis://{os.getenv("REDIS_HOST")}:6379/0')
	r.set(
		'tasks_reached_deadline',
		pickle.dumps([{'telegram_user_id': task.telegram_user_id, 'title': task.title} for task in tasks_reached_deadline])
	)
