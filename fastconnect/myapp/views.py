from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def process(request):
    input_data = json.loads(request.body.decode('utf-8'))["input_data"]

    # 데이터를 문자열로 변환합니다. 
    input_data = [str(x) for x in input_data.split(",")]
    
    # 데이터 확인
    print(f"Input data (Django): {input_data}")

    fastapi_service_url = 'http://localhost:8001/process'
    response = requests.post(fastapi_service_url, json={"input_data": input_data})
    result = response.json()['result']

    return JsonResponse({'result': result})
