from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate
from Blog.models import Post
from accounts.models import Staff, User
from medicine.models import Like, Medicine
from django.contrib.auth import logout

# Create your views here.

# 일반 사용자 회원가입
def join(request):
    if request.method == 'POST':
        # 입력된 비밀번호와 비밀번호 확인이 일치하다면
        if request.POST['password1'] == request.POST['password2']:
            # User 객체 생성
            User.objects.create_user(
                                            email=request.POST['email'],
                                            username=request.POST['email'],
                                            password=request.POST['password1'],
                                            gender=request.POST['gender'],
                                            age=request.POST['age'],)
            # 회원가입 완료 메시지와 함께 로그인 페이지로 로딩
            # message-OK : '회원가입이 완료되었습니다.'
            return render(request, 'login.html', {'message' : 'OK'})
        else:
            # 입력된 비밀번호와 비밀번호 확인이 일치하지 않다면 회원가입 불가
            return render(request, 'register.html', {'PW_error' : '비밀번호가 일치하지 않습니다.'})
    # 일반 사용자 회원가입 페이지 로딩
    return render(request, "register.html")


# 약사 및 관리자 회원가입
def staff_join(request):
    if request.method == 'POST':
        # 입력된 비밀번호와 비밀번호 확인이 일치하다면
        if request.POST['password1'] == request.POST['password2']:
            # DB에 약사 면허 번호와 본명이 일치하는 객체가 있는지 확인 (약사 인증 절차)
            try :
                staff = Staff.objects.get(num=request.POST['staff_num'], name=request.POST['staff_name'])
            # 없다면 staff = None
            except Staff.DoesNotExist:
                staff = None
            # 약사 인증이 완료되었다면
            if staff is not None:
                # 이미 회원가입이 완료된 약사라면
                if staff.user is not None:
                    # 이미 계정이 있으므로 회원 가입 불가, 관리자 로그인 화면으로 전환
                    # already-OK : '해당 약사는 이미 회원가입이 되어 있습니다.'
                    return render(request, "staff_login.html", {'already' : 'OK'})
                # 회원가입은 한 적 없는 약사라면 User 객체 생성
                user = User.objects.create_user(
                                            email=request.POST['email'],
                                            username=request.POST['staff_name'],
                                            password=request.POST['password1'],
                                            is_staff=1,)
                # staff의 user 테이블에 생성된 User 객체 연결
                staff.user = user
                # 저장
                staff.save()
                # 약사 회원가입 완료 후 관리자 로그인 화면 로딩
                # message-OK : '회원가입이 완료되었습니다.'
                return render(request, "staff_login.html", {'message' : 'OK'})
            # 약사 인증 실패
            else:
                return render(request, 'staff_join.html', {'confirm_error' : '약사 정보가 없습니다. \n 회원가입을 다시 진행해주세요.'})
        # 입력된 비밀번호와 비밀번호 확인이 일치하지 않다면 회원가입 불가
        else:
            return render(request, 'staff_join.html', {'PW_error' : '비밀번호가 일치하지 않습니다.'})
    # 약사 및 관리자 회원가입 페이지 로딩
    return render(request, "staff_join.html")


# 일반 사용자 로그인
def gologin(request):
    if request.method == 'POST':
        # 로그인 시 입력된 값 저장
        username = request.POST['email']
        password = request.POST['password']
        # User 인증
        user = authenticate(request, username=username, password=password)
        # 인증 완료시
        if user is not None:
            # 일반 사용자 로그인
            auth.login(request, user)
            # 메인 페이지 로딩
            return redirect('main')
        # 인증 실패시
        else:
            # 아이디 또는 비번 불일치 메시지와 함께 다시 로그인 페이지 로딩
            return render(request, 'login.html', {'error' : '* 아이디 또는 비밀번호가 일치하지 않습니다.'})
    # 일반 사용자 로그인 페이지 로딩
    return render(request, 'login.html')


# 약사 및 관리자 로그인
def staff_login(request):
    if request.method == 'POST':
        # 로그인 시 입력된 값 저장
        username = request.POST['staff_id']
        password = request.POST['password']
        # staff User 인증
        user = authenticate(request, username=username, password=password)
        # 인증 및 user가 staff인지 확인, 완료시
        if user is not None and user.is_staff is True:
            # staff 로그인
            auth.login(request, user)
            # 메인 페이지 로딩
            return redirect('main')
        # 인증 실패시
        else: 
            # 아이디 또는 비번 불일치 메시지와 함께 다시 관리자 로그인 페이지 로딩
            return render(request, 'staff_login.html', {'discord' : '* 아이디 또는 비밀번호가 일치하지 않습니다.'})
    # 약사 및 관리자 로그인 페이지 로딩
    return render(request, 'staff_login.html')


# 마이페이지
def mypage(request):
    # 현재 user가 약사 및 관리자라면
    if User.objects.get(id=request.user.id).is_staff is True:
        # 현재 user가 작성한 medicine 객체 모두 반환
        medicines = Medicine.objects.filter(user_id=request.user.id)
        # 현재 user(약사)가 등록한 약 마이페이지에서 확인 가능
        return render(request, 'mypage.html', {'medicines': medicines})

    # 현재 user가 일반 사용자라면
    if User.objects.get(id=request.user.id).is_staff is False:
        # 현재 user가 스크랩한 약 객체 모두 반환
        likes = Like.objects.filter(user_id=request.user.id)
        # 현재 user가 작성한 post(Q&A 게시글) 객체 모두 반환
        posts = Post.objects.filter(author_id=request.user.id)
        # 현재 user(일반 사용자)가 스크랩한 약과 작성한 게시글 마이페이지에서 확인 가능
        return render(request, 'mypage.html', {'likes': likes, 'posts': posts})
    # 마이페이지 로딩
    return render(request, "mypage.html")


# 회원가입 선택 (일반 사용자 or 약사 및 관리자)
def select(request):
    # 선택 화면 로딩
    return render(request, 'select.html')


# 회원 탈퇴
def account_delete(request):
    # 현재 로그인이 되어있는 상태라면
    if request.user.is_authenticated:
        # 현재 로그인된 user 객체 삭제 (회원 탈퇴)
        request.user.delete()
        # 로그아웃
        logout(request)
        # 메인 페이지 로딩
        return render(request, 'main.html', {'user_delete' : 'OK'})
    return redirect('main')