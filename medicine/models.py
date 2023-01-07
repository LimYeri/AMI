from django.db import models

from accounts.models import User

# Create your models here.

# 약
class Medicine(models.Model):
    # 약 이름
    name = models.CharField(max_length=30)
    # 효능·효과
    effect = models.TextField()
    # 복약정보
    takeMedicine = models.TextField(null=True)
    # 용법·용량
    use = models.TextField(null=True)
    # 약 이미지
    medicineImg = models.ImageField(upload_to='images/', null=True, blank=True)
    # 작성자
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # DB table 이름 = medicines
    class Meta:
        db_table = 'medicines'
    
    def get_absolute_url(self):
        return f'/medicine/medicinePost/{self.pk}'

# 스크랩(좋아요)
class Like(models.Model):
    # 유저
    user = models.ForeignKey("accounts.User", related_name='user', on_delete=models.CASCADE)
    # 약
    medicine = models.ForeignKey("Medicine", related_name='medicine', on_delete=models.CASCADE)

    # DB table 이름 = likes
    class Meta:
        db_table = 'likes'
            
    def get_absolute_url(medicine):
        return f'/medicine/medicinePost/{medicine.medicine_id}'
