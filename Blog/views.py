from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from accounts.models import User
from Blog.models import Post, Comment


# Q&A 게시글 등록
def blogPostCreate(request):
    if request.method == 'POST':
        # 게시글 등록 시 입력된 값 저장
        title = request.POST['title']
        content = request.POST['content']
        author = request.user
        # 유저가 로그인 된 상태라면
        if request.user.is_authenticated:
            Post.objects.create(
                title=title, 
                content=content, 
                author=author)
            return redirect('mypage')
        # 유저가 로그인 되지 않은 상태라면
        else:
            # 에러 메시지 출력 후 로그인 페이지 로딩
            # error-NO : '로그인이 되어있지 않습니다. \n로그인을 먼저 해주세요.'
            return render(request, 'login.html', {'error' : 'NO'})
    else:
        # 게시글 등록 페이지 로딩
        return render(request, 'BlogPost.html')


# Q&A 게시글 상세 페이지
def blogPostDetail(request, post_id):
    # 해당 post_id에 맞는 객체 반환
    BlogPost = get_object_or_404(Post, id=post_id)
    # 해당 게시글 작성자와 현재 user가 같다면 
    if BlogPost.author.id == request.user.id:
        # 게시글 수정 가능 태그 보이게 하기
        message = 'OK'
    else: message = 'NO'
    # 현재 게시글에 등록된 댓글 반환
    comments = Comment.objects.filter(post = post_id)
    # 현재 게시글 정보, 댓글 정보, 유저 정보 반환 후 상세페이지 로딩
    return render(request, 'BlogDetail.html', {"Post": BlogPost, "comments": comments, "message": message})


# Q&A 게시판
class BlogPostList(ListView):
    model = Post
    # 게시글 pk값 기준 내림차순 정렬
    ordering = '-pk'
    template_name = 'BlogList.html'


# Q&A 게시글 댓글 등록
def new_comment(request, post_id):
    # 해당 post_id에 맞는 객체 반환
    BlogPost = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        # 입력된 내용 저장
        content = request.POST['content']
        author = request.user
        # 유저가 로그인 된 상태라면
        if request.user.is_authenticated:
            # 댓글 생성
            Comment.objects.create(
                content=content,
                post=BlogPost,
                author=author
            )
            # 상세페이지 로딩
            return redirect('blogPostDetail', post_id=post_id)
        # 유저가 로그인 되지 않은 상태라면
        else:
            # 에러 메시지 출력 후 로그인 페이지 로딩
            # error-NO : '로그인이 되어있지 않습니다. \n로그인을 먼저 해주세요.'
            return render(request, 'login.html', {'error' : 'NO'})
    # 상세페이지 로딩
    else:
        return redirect('blogPostDetail', post_id=post_id)


# Q&A 게시글 수정
def blogPostEdit(request, post_id):
    # 해당 post_id에 맞는 객체 반환
    BlogPost = get_object_or_404(Post, id=post_id)
    # 작성자와 현재 user가 같다면
    if BlogPost.author.id == request.user.id :
        if request.method == 'POST':
            # 입력 값 저장
            BlogPost.title = request.POST['title']
            BlogPost.content = request.POST['content']
            BlogPost.author = request.user
            # 게시글 수정
            BlogPost.save()
            # 마이페이지 로딩
            return redirect('mypage')
        # 수정 페이지 로딩
        else:
            return render(request, 'update.html', {'Post': BlogPost})
    # 수정 권한이 없으므로 에러 메시지 출력 후 메인 페이지 로딩
    # editError-NO : '회원님에게는 수정 및 삭제 권한이 없습니다.'
    else:
        return render(request, 'main.html', {'editError': 'NO'})


# Q&A 게시글 삭제
def deletePost(request, post_id):
    # 해당 post_id에 맞는 객체 반환
    BlogPost = get_object_or_404(Post, id=post_id)
    # 작성자와 현재 user가 같다면
    if BlogPost.author.id == request.user.id :
        # 게시글 삭제
        BlogPost.delete()
        # 마이페이지 로딩
        return redirect('mypage')
    # 식제 권한이 없으므로 에러 메시지 출력 후 메인 페이지 로딩
    # editError-NO : '회원님에게는 수정 및 삭제 권한이 없습니다.'
    else:
        return render(request, 'main.html', {'editError': 'NO'})