import os

from celery import Celery ,schedules
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

from datetime import timedelta

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'check_subs': {
        'task': 'subscription.tasks.check_subs',
        'schedule':  crontab(hour=0, minute=30),
        
    },
    # 'delete_closed_room':{
    #     'task':'chat.tasks.delete_closed_room',
    #     'schedule':crontab(hour=0, minute=30),
    # },
    # 'delete_unverified_image':{
    #     'task':'chat.tasks.delete_unverified_image',
    #     'schedule':crontab(hour=0, minute=30),
    # }
    # ,
    # 'delete_signature':{
    #     'task':'chat.tasks.delete_signature',
    #     'schedule':timedelta(minute=30),
    # }
    # ,
    'otp_expire':{
        'task':'account.tasks.otp_expire',
        'schedule':timedelta(minute=1),
    }
    
}