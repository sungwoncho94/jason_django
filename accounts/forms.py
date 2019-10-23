from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model  # 현재 활성화(active)된 user model을 return함


class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        # 우리가 settings.py에 AUTH_usermodel을 커스텀했기때문에, 이제부터 그 모델을 가져올 것
        model = get_user_model()  # accounts.User
        fields = ['email', 'first_name', 'last_name']


# 커스텀한 UserModel을 인식하지 못해서, 직접 커스텀유저폼을 만들어줘야한다.
class CustomUserCreationForm(UserCreationForm):
    # 기존 usercreationform을 모두 상속시킨 후, 원하는 정보만 필드로 추가

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields
        