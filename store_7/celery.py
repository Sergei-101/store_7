# celery.py

from __future__ import absolute_import
import os
from celery import Celery

# Указываем Django настройки для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_7.settings')

app = Celery('store_7')

# Читаем конфигурации Celery из настроек Django, используя префикс 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и загрузка задач из всех приложений Django
app.autodiscover_tasks()
