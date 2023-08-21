from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# 기본 장고파일 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastconnect.settings')
app = Celery('fastconnect')
app.config_from_object('django.conf:settings', namespace='CELERY')

#등록된 장고 앱 설정에서 task 불러오기
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# app.autodiscover_tasks()

