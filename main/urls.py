from django.urls import path
from main.views import *

urlpatterns = [
    # 메인 페이지
    path("", main, name = "main"),
]