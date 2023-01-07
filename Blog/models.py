from django.db import models

from accounts.models import User

# Create your models here.

# Q&A 게시글
class Post(models.Model):
    # 제목
    title = models.CharField(max_length=30)
    # 내용
    content = models.TextField()
    # 작성시간
    created_at = models.DateTimeField(auto_now_add=True)
    # 작성자
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # DB table 이름 = posts
    class Meta:
        db_table = 'posts'
    
    def get_absolute_url(self):
        return f'/Blog/blogPost/{self.pk}'

# 댓글
class Comment(models.Model):
    # 내용
    content = models.TextField()
    # 게시글
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # 작성자
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 작성시간
    created_at = models.DateTimeField(auto_now_add=True)
    
    # DB table 이름 = comments
    class Meta:
        db_table = 'comments'
