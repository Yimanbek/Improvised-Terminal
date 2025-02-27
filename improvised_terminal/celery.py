from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'improvised_terminal.settings')

celery_worker = Celery('improvised_terminal')

celery_worker.config_from_object('django.conf:settings', namespace='CELERY')

celery_worker.autodiscover_tasks()



celery_worker.conf.beat_schedule = {
    'Checking-unpaid-orders': {
        'task': 'order.tasks.checking_unpaid_orders',
        'schedule': crontab(hour = 1, minute=0)
    },
}