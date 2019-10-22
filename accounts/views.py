from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.http import require_GET, require_POST
# login이라는 함수명이 겹치기때문에 다른 이름으로 지어준다


# 회원가입 할 수 있는 form 이 주어져야하는데 동일한 url이 두가지 기능 수행
# get 요청 -> 회원가입할 수 있는 페이지 제공  //  post 요청 -> 회원가입 내용 저장
def signup(request):
    # 로그인 상태에서 또 회원가입창으로 온다면
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        # 유저들이 post요청으로 보낸 데이터를 form에 보낸다
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 회원가입과 동시에 자동로그인
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
        
    else:
        # 회원가입 form 은 장고가 제공. form 에 담아서 context로 보내주기
        form = UserCreationForm
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

# login은 세션을 만드는 것이기 때문에 usercreateform X
def login(request):
    # 로그인 상태에서 또 회원가입창으로 온다면
    if request.user.is_authenticated:
        return redirect('articles:index')

    # post 요청 : login 시켜준다
    if request.method == 'POST':
        # 중요!! Authen-Form에만 첫 번째 인자로 repuest 필요
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # login import 해야함  /  auth_login으로 사용
            # get_user() : 사용자의 정보를 우리한테 주는 함수
            auth_login(request, form.get_user())  # 로그인 성공
            # 로그인할 때, next=? 값이 있다면 그 페이지로 보내주고, 아니면 index로 보내줘
            next_page = request.GET.get('next')
            return redirect(next_page or 'articles:index')
    # get 요청 : login 할 수 있는 페이지 제공
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout(request):
    # 로그아웃 페이지는 필요없고 버튼만 있으면 된다
    auth_logout(request)

    return redirect('articles:index')


@require_POST
def delete(request):
    if request.user.if_authenticated:
        request.user.delete()
    return redirect('articles:index')