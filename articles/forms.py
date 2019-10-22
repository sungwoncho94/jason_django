from django import forms
from .models import Article, Comment



class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'content',] # -> 유저정보도 넘겨주겠다고했는데, 유저정보는 받는다고 안함

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content', ]
        # exclude = ['article', ]
