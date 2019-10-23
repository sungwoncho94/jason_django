from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# ManytoManyField -> 특정 모델 필드에 쓴다.

# class User(): 가 있다면
#    models.ManyToManyField를 쓸 수 있는데, User필드가 없으니까 장고가 제공해주는걸 썼다.

class User(AbstractUser):
    # 모든 유저는 나를 팔로우하는 사람들 필드인 followers를 가지고 있다
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')

''' ex
jason -> 공정배
공정배.followers = jason
jason.followings = 공정배
'''
