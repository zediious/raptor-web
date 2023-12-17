import os
from logging import getLogger

from celery import Celery

LOGGER = getLogger('config.celery')

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('raptor', broker='pyamqp://guest@rabbitmq//')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    LOGGER.debug(f'Request: {self.request!r}')