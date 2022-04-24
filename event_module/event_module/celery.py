from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_module.settings')

app = Celery('event_module',include=['event_module.celery'],broker=settings.CELERY_BROKER_URL,backend=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='Celery')

#Celery Beat Settings
app.conf.beat_schedule = {
    'expired_event_delete_func' : {
        'task':'event_module.task.expired_event_delete_func',
        'schedule':600,
    }
}
    
# }

# Looks up for task modules in Django applications and loads them

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"request:{self.request!r}")
