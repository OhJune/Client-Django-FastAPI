from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
import redis
from django.conf import settings
import datetime 
from fastconnect.celery import app as celery_app
import logging


@shared_task(bind=True)
def store_input_data_in_redis(self, input_data):
    redis_conn = redis.Redis(host='35.216.91.72', port=6379, db=4, password= 'AlsongDlsong')
    print(redis_conn)
    # redis_conn = celery_app.backend.client
    date = datetime.datetime.now()
    redis_key = f"input_data:{date}"
    redis_conn.set(redis_key, ",".join(input_data))
    
@shared_task
def send_data_to_fastapi(data):
    url = "http://localhost:8001/process"  # FastAPI 엔드포인트 주소
    response = requests.post(url, json={"input_data": data})
    return response.json()

