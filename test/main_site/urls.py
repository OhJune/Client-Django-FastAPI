from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index), # 127.0.0.1로 접속하면 알아서 main_site url로 이동하여서 이까지 왔고 이제 views.py의 index함수로 가!
    path('page1/',views.page1), # 127.0.0.1/page1/로 접속하면 알아서 views.py의 page1함수로 가!
    path('page2/',views.page2), # 127.0.0.1/page2/로 접속하면 알아서 views.py의 page2함수로 가!
    path('page3/',views.page3), # 127.0.0.1/page2/로 접속하면 알아서 views.py의 page2함수로 가!
    path('page4/',views.page4), # 127.0.0.1/page2/로 접속하면 알아서 views.py의 page2함수로 가!
    path('about/',views.about), # 127.0.0.1/page2/로 접속하면 알아서 views.py의 page2함수로 가!
    path('contact/',views.contact), # 127.0.0.1/page2/로 접속하면 알아서 views.py의 page2함수로 가!
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)