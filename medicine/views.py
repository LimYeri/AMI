from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth import logout
from accounts.models import User
from medicine.models import Like, Medicine

# 약 검색
def search(request):
    if request.method == 'POST':
        # 검색어 입력값 저장
        searched = request.POST['searched']
        # 검색어 약이 있으면 객체 반환
        medicines = Medicine.objects.filter(name__contains=searched)
        # 검색된 약 리스트 출력
        return render(request, 'medicineList.html', {'medicine_list': medicines, 'searched':searched})
    # 메인 페이지 로딩 (검색창 있음)
    return render(request, 'main.html')


# 약사 및 관리자가 약 제품 등록
def medicinePostCreate(request):
    # 현재 로그인 된 유저가 약사 및 관리자라면
    if request.user.is_staff is True:
        if request.method == 'POST':
            # 약 객체 생성
            medicine = Medicine()
            # 약사가 입력한 값 저장
            medicine.name = request.POST['name']
            medicine.effect = request.POST['effect']
            medicine.takeMedicine = request.POST['takeMedicine']
            medicine.use = request.POST['use']
            medicine.medicineImg = request.FILES['medicineImg']
            medicine.user = request.user
            # 약 등록
            medicine.save()
            # 마이페이지 로딩
            return redirect('mypage')
        else:
            # 약 제품 등록 페이지 로딩
            return render(request, 'medicinePost.html')
    # 현재 로그인 된 유저가 약사 및 관리자가 아니라면
    else:
        # 로그아웃
        logout(request)
        # 에러메시지 출력 후 관리자 로그인 페이지 로딩
        # error-NO : '관리자 계정이 아니므로 약 정보를 등록할 수 없습니다.\n관리자 계정으로 로그인 하세요.'
        return render(request, 'staff_login.html', {'error' : 'NO'})


# 약 제품 상세 페이지 및 스크랩 기능
def medicinePostDetail(request, medicine_id):
    # 현재 로그인된 유저 반환
    user = User.objects.get(id=request.user.id)
    # 해당 medicine_id에 맞는 객체 반환
    MedicinePost = get_object_or_404(Medicine, id=medicine_id)
    context = {"Medicine": MedicinePost}
    # 스크랩 요청
    if request.method == 'POST':
        # 로그인 되어 있지 않다면
        if user is None:
            # 에러메시지 출력 후 로그인 페이지 로딩
            # error-NO : '로그인이 되어있지 않습니다. \n로그인을 먼저 해주세요.'
            return render(request, 'login.html', {'error': 'NO'})
        # 로그인이 되어 있다면
        else:
            # 스크랩 확인
            like = Like.objects.filter(user=user, medicine=MedicinePost)
            
            # 스크랩이 이미 되어 있다면
            if like.exists():
                # 해당 약 스크랩 삭제
                like.delete()
                # 약 제품 상세페이지 로딩
                return render(request, 'medicineDetail.html', context)
            
            # 스크랩이 되어 있지 않다면 스크랩 하기
            Like.objects.create(
                user=user,
                medicine=MedicinePost
            )
            # 약 제품 상세페이지 로딩
            return render(request, 'medicineDetail.html', context)
    # 약 제품 상세페이지 로딩
    else:
        return render(request, 'medicineDetail.html', context)


# 약 리스트
class medicinePostList(ListView):
    model = Medicine
    # 약 제품 게시글 pk값 기준 내림차순 정렬
    ordering = '-pk'
    template_name = 'medicineList.html'


# 약사 및 관리자가 약 제품 수정
def medicinePostEdit(request, medicine_id):
    # 해당 medicine_id에 맞는 객체 반환
    MedicinePost = get_object_or_404(Medicine, id=medicine_id)
    # 현재 user가 약사 및 관리자라면
    if request.user.is_staff is True:
        if request.method == 'POST':
            # 입력 값 저장
            MedicinePost.name = request.POST['name']
            MedicinePost.effect = request.POST['effect']
            MedicinePost.takeMedicine = request.POST['takeMedicine']
            MedicinePost.use = request.POST['use']
            MedicinePost.medicineImg = request.FILES['medicineImg']
            # 약 제품 수정
            MedicinePost.save()
            # 마이페이지 로딩
            return redirect('mypage')
        else:
            # 약 제품 수정 페이지 로딩
            return render(request, 'medicineEdit.html', {'Medicine':MedicinePost})
    # 현재 user가 약사 및 관리자가 아니라면
    else:
        # 로그아웃
        logout(request)
        # 수정 권한이 없으므로 에러메시지 출력 후 관리자 로그인 페이지 로딩
        # editError-NO : '약 제품 수정 및 삭제는 관리자만 수행할 수 있습니다. \n관리자 계정으로 로그인 해주세요.'
        return render(request, 'staff_login.html', {'editError' : 'NO'})


# 약사 및 관리자가 약 제품 삭제
def medicinePostdelete(request, medicine_id):
    # 해당 medicine_id에 맞는 객체 반환
    MedicinePost = get_object_or_404(Medicine, id=medicine_id)
    # 현재 user가 약사 및 관리자라면
    if request.user.is_staff is True:
        # 약 제품 삭제
        MedicinePost.delete()
        # 메인 페이지 로딩
        # return redirect('main')
        return render(request, 'main.html', {'delete':"OK"})
    # 현재 user가 약사 및 관리자가 아니라면
    else:
        # 로그아웃
        logout(request)
        # 수정 권한이 없으므로 에러메시지 출력 후 관리자 로그인 페이지 로딩
        # editError-NO : '약 제품 수정 및 삭제는 관리자만 수행할 수 있습니다. \n관리자 계정으로 로그인 해주세요.'
        return render(request, 'staff_login.html', {'editError' : 'NO'})