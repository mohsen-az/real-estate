from __future__ import absolute_import

import os
from celery import Celery

from config.settings import basic

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('config')

app.config_from_object('config.settings.development', namespace='CELERY')

app.autodiscover_tasks(lambda: basic.INSTALLED_APPS)
