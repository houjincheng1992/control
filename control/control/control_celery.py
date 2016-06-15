# coding=utf-8
__author__ = 'houjincheng'

import os
import celery

# from gevent import monkey
# monkey.patch_all()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control.control.settings')

from django.conf import settings

app = celery.Celery('control')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)