from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from .models import ResultData
from .tasks import send_data_to_fastapi, store_input_data_in_redis
from celery.result import AsyncResult
import time
from collections import namedtuple


def index(request):
    return render(request, 'index.html')

@csrf_exempt
def process_request(request):
    if request.method == 'POST':
        input_data = json.loads(request.body.decode('utf-8'))["input_data"]
        input_data = [str(x) for x in input_data.split(",")]
        # 데이터 확인
        print(f"Input data (Django): {input_data}")
        store_input_data_in_redis(input_data)
        if input_data:       
            task = send_data_to_fastapi.delay(input_data)
            print(f"Result from task1: {task}")
            print(f"Result from task2: {task.id}")
            
            return JsonResponse({"task_id": str(task.id)})
        else:
            return JsonResponse({"task_id": "No input_data provided"})
    else:
        return JsonResponse({"error": "Only POST requests are allowed"})

@csrf_exempt
def get_result(request, task_id):
    if request.method == 'GET':
        task = AsyncResult(task_id)
        time.sleep(2)
        try:
            result = task.result   # 작업의 결과값을 가져옵니다.
        except Exception as e:
            result = None   # 예외가 발생하면 결과값을 None으로 설정합니다.

        result_payload = {
            "task_id": task_id,
            'ready': task.ready(),
            'result': result,
        }

        data = result_payload['result']
        Song = namedtuple("Song", ["title", "artist", "ky", "tj"])
        results = [Song(x['title'], x['artist'], x['ky_song_num_id'], x['tj_song_num_id']) for x in data['result']]
        print(results)

        return JsonResponse(result_payload) #,{"result":results}
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'})

