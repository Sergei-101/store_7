from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Указываем Django настройки для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_7.settings')

app = Celery('store_7')

# Задаем настройки, указывая Redis как брокера
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://localhost:6379/0'

# Автоматическое обнаружение тасков в приложениях Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
