from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    # Q&A 게시글 등록
    path("blogPostCreate/", blogPostCreate, name = "blogPostCreate"),
    # Q&A 게시글 상세 페이지
    path("blogPost/<int:post_id>", blogPostDetail, name = "blogPostDetail"),
    # Q&A 게시판
    path("blogList/", BlogPostList.as_view(), name = "BlogPostList"),
    # Q&A 게시글 댓글 등록
    path("blogPost/<int:post_id>/new_comment", new_comment, name = "new_comment"),
    # Q&A 게시글 수정
    path("blogPost/<int:post_id>/blogPostEdit", blogPostEdit, name = "blogPostEdit"),
    # Q&A 게시글 삭제
    path("blogPost/<int:post_id>/deletePost", deletePost, name = "deletePost"),
]