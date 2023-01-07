from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    # 일반 사용자 회원가입
    path("join/", join, name = "join"),
    # 약사 및 관리자 회원가입
    path("staff_join/", staff_join, name = "staff_join"),
    # 일반 사용자 로그인
    path("gologin/", gologin, name = "gologin"),
    # 약사 및 관리자 로그인
    path("staff_login/", staff_login, name = "staff_login"),
    # 마이페이지
    path("mypage/", mypage, name = "mypage"),
    # 회원가입 선택 (일반 사용자 or 약사 및 관리자)
    path("select/", select, name = "select"),
    # 회원 탈퇴
    path("account_delete/", account_delete, name = "account_delete"),
]