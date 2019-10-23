from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Article, Comment
from django.http import HttpResponse
from .forms import ArticleForm, CommentForm
from IPython import embed


@require_GET
def index(request):
    # embed()  # 요청이 들어오자마자 request에 뭐가 있는지 보자!
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)


@require_GET
def detail(request, article_pk):
    # 사용자가 url 에 적어보낸 article_pk 를 통해 디테일 페이지를 보여준다.
    article = get_object_or_404(Article, pk=article_pk)
    comment_form = CommentForm()
    # comments = Comment.objects.all()  -> 모든 댓글 다 가져옴
    # comments = article.comment_set.all()  # comment_set -> comments
    comments = article.comments.all()  # article에 맞는 댓글만 가지고오기
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)

# @login_required는 get요청을 사용하는 함수에서만 사용할 수 있따

# 로그인 되어있는 상태에서만 create를 시행할 수 있도록!
# 로그인 하지 않을 상태에서 /create로 들어가면 바로 로그인 페이지로 보낸다
@login_required  # 로그인 하지 않은 상태에서는 /accounts/login(설정한 로그인 경로)으로 보내줌
# @login_required(login_url='/users/login/')  -> 로그인 페이지를 설정할 수도 있다 // default 값 = /accounts/login/
def create(request):
    if request.method == 'POST':
        # Article 을 생성해달라고 하는 요청
        form = ArticleForm(request.POST)  # title, content + user정보도 넣어야한다
        if form.is_valid():
            # form.save() 에서 밑에처럼 바꾼다
            article = form.save(commit=False)
            article.user = request.user  # 누가 만든 article인지 얘기해주기
            article.save()
            return redirect('articles:detail', article.pk) # article_pk로 하면 오류남  왜??
    else: # GET
        # Article 을 생성하기 위한 페이지를 달라고 하는 요청
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/create.html', context)


@login_required  # 로그인이 안돼있는 상태에서는 수정할 수 없음
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if article.user == request.user:

        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article_pk)
        else: # GET method
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {'form': form}
    return render(request, 'articles/update.html', context)


@login_required  # 로그인이 되어있는지 확인한 후, 로그인 후 다시 여기로 올 수 있도록 해줌
@require_POST  # POST요청이 맞는지 확인한 후, delete함수를 실행한다
def delete(request, article_pk):
    if request.user.is_authenticated:
        # article_pk 에 맞는 article 을 꺼낸다. 삭제한다.
        article = get_object_or_404(Article, pk=article_pk)
        # 삭제를 요청하는 user와 article을 작성한 user가 같은 경우에만 삭제
        if article.user == request.user:
            article.delete()
            return redirect('articles:index')
        else:
            return redirect('articles:detail', article_pk)
    else:
        return redirect('articles:index')


# 댓글을 생성하는 요청을 받는다.
@require_POST
def comments_create(request, article_pk):
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # DB에 바로 저장하지 않고 대기시킴
            comment.article_id = article_pk
            # commet의 user정보를 request.user로 넣겠다
            comment.user = request.user
            comment.save()
    return redirect('articles:detail', article_pk)


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
            return redirect('articles:detail', article_pk)
        else:
            return render(request, 'articles/datail', article_pk)
    return HttpResponse('You are Unauthorized', status=401)


def like(request, article_pk):
    user = request.user
    article = get_object_or_404(Article, pk=article_pk)

    # if user in article.liked_users.all():
    if article.liked_users.filter(pk=user.pk).exists():
        # 이미 좋아요 한 유저가 다시 한번 누르면 좋아요 취소
        user.liked_articles.remove(article)
    else:
        # user가 좋아요를 누른 article에 현재 article을 추가할 것
        user.liked_articles.add(article)
    
    # 좋아요누른 후 다시 detail page 보여주기
    return redirect('articles:detail', article_pk)


def follow(request, article_pk, user_pk):
    # 로그인한 유저가 게시글 유저를 팔로우/언팔하는 기능
    # user_pk = 게시글 유저의 pk를 받아서 팔/언팔 하는 것
    user = request.user
    person = get_object_or_404(get_user_model(), pk=user_pk) # 게시글 작성자 = 404(getusermodel을 통해서 모델 넘겨받고, )

    # 내가 선택한 user가 followers명단에 있다면 -> 언팔할 것
    if user in person.followers.all():
        person.followers.remove(user)
    else:
        person.followers.add(user)

    return redirect('articles:detail', article_pk)


