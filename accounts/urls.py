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
    path('delete/', views.delete, name='delete')
]
