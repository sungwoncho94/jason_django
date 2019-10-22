from django.db import models
from django.conf import settings  
# 통상 user model(장고가 제공하는)가져올때 get_user_model 함수로 쓰는데 models.py에서만 정의할때는 settings에서 직접 들고온다. : 
# models.py에서는 user model 쓸 때, settings로부터 직접 가지고온다 -> get_user_model()사용하지 않음

# article.user로 유저 정보를 꺼내볼 수 있다.
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 한명의 유저가 여러개 article생성하는데, 회원탈퇴하면 article을 삭제할 것이다 -> on_delete=models.CASCADE
    
    class Meta:
        ordering = ('-pk', )


class Comment(models.Model):
    # 1:N 관계 표시
    # article.comment_set.all()  ==  article.comments.all()  (related 이름 설정하면 이렇게 받을 수 있음)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    # user.comments  /  comments.user로 접근할 수 있다.
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk', )
