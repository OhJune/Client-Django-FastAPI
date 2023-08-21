# django_project/app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process_request', views.process_request, name='process_request'),
    path("get_result/<str:task_id>", views.get_result, name="get_result"),
    
]