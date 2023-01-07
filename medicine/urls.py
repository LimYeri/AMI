from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # 약 검색
    path("search/", search, name = "search"),
    # 약사 및 관리자가 약 제품 등록
    path("medicinePostCreate/", medicinePostCreate, name = "medicinePostCreate"),
    # 약 제품 상세 페이지
    path("medicinePost/<int:medicine_id>", medicinePostDetail, name="medicinePostDetail"),
    # 약 리스트
    path("medicineList/", medicinePostList.as_view(), name="medicinePostList"),
    # 약사 및 관리자가 약 제품 수정
    path("medicinePost/<int:medicine_id>/medicineEdit", medicinePostEdit, name="medicinePostEdit"),
    # 약사 및 관리자가 약 제품 삭제
    path("medicinePost/<int:medicine_id>/delete", medicinePostdelete, name="medicinePostdelete"),
]