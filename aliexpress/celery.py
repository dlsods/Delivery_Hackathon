import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aliexpress.settings')

app = Celery('aliexpress')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
