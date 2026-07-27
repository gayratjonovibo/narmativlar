import os
from celery import Celery

# Django settings faylini standart deb belgilaymiz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Celery konfiguratsiyasini settings.py faylidan CELERY_ prefiksi bilan o'qiydi
app.config_from_object('django.conf:settings', namespace='CELERY')

# Barcha registratsiya qilingan app'lardan tasks.py fayllarini avtomatik qidirib topadi
app.autodiscover_tasks()