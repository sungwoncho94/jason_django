from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
# UserCreationForm을 통해 user에 대한 정보 가지고옴
# UserChangeForm : 유저 정보를 수정하기 위한 form
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
# Authentication에 대한 행위를 할 수 있음 import login으로 로그인할 수 있음.
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required


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
    return render(request, 'accounts/form.html', context)

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
    return render(request, 'accounts/form.html', context)


def logout(request):
    # 로그아웃 페이지는 필요없고 버튼만 있으면 된다
    auth_logout(request)

    return redirect('articles:index')


@require_POST
def delete(request):
    if request.user.if_authenticated:
        request.user.delete()
    return redirect('articles:index')

@login_required
def update(request):
    # 수정해주세요~ 요청이 들어올 때 실제로 바꾸는 기능 수행
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:form')
    # 수정할 수 있는 페이지 주세요~ 라는 요청이 들어올 때 회원정보 바꿀 수 있는 form 보여준다
    else:
        # 현재 나의 정보를 채운 채로 form에 보낸다.
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)


@login_required
def password(request):
    if request.method == 'POST':
        # 첫 번째 인자 = user정보 / 두번째 = data
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 비밀번호 바꾼 후, 자동으로 로그인상태 유지
            update_session_auth_hash(request, user)
            #return redirect('accounts:update')
            # 비밀번호 변경 후 index페이지로 보내주기
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
        context = {
            'form': form,
        }
        return render(request, 'accounts/form.html', context)
