from __future__ import absolute_import
# coding=utf-8
VERSION = "1.0.0"

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .control_celery import app as celery_app