from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # sign up
    path('signup/', views.signup, name='signup'),
    # login
    path('login/', views.login, name='login'),
    # logout
    path('logout/', views.logout, name='logout'),
    # 회원탈퇴
    path('delete/', views.delete, name='delete'),
    # 회원정보 수정
    path('update/', views.update, name='update'),
    # 비밀번호 바꾸는건 따로 설정해줘야함
    path('password/', views.password, name='password'),
]
