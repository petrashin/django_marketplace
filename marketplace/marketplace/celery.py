import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
app = Celery('tasks', broker='redis://guest@localhost//')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
