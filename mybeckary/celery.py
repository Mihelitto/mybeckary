import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybeckary.settings')

app = Celery('mybeckary')

app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()