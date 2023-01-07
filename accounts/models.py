from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# 사용자 models (장고에서 제공하는 AbstractUser 사용, 추가로 받을 필드 정보와 없앨 필드 정보 입력)
class User(AbstractUser):
    # 이메일
    email = models.EmailField(unique=True) 
    # 성별
    gender = models.CharField(max_length=30, null=True)
    # 나이대
    age = models.CharField(max_length=30, null=True)
    # first_name, last_name, last_login 테이블 삭제
    first_name = None
    last_name = None
    last_login = None
    
    # DB table 이름 = users
    class Meta:
        db_table = 'users'

# 약사 및 관리자 models (약사를 staff로 설정)
class Staff(models.Model):
    # 약사 면허 번호
    num = models.CharField(max_length=30, unique=True)
    # 약사 본명
    name = models.CharField(max_length=30)
    # 연동된 AMI 계정
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # DB table 이름 = staffs
    class Meta:
        db_table = 'staffs'