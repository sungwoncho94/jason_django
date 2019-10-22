from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
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
    comments = Comment.objects.all()
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
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else: # GET
        # Article 을 생성하기 위한 페이지를 달라고 하는 요청
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/create.html', context)


@login_required  # 로그인이 안돼있는 상태에서는 수정할 수 없음
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article_pk)
    else: # GET method
        form = ArticleForm(instance=article)
    context = {'form': form}
    return render(request, 'articles/update.html', context)


@login_required  # 로그인이 되어있는지 확인한 후, 로그인 후 다시 여기로 올 수 있도록 해줌
@require_POST  # POST요청이 맞는지 확인한 후, delete함수를 실행한다
def delete(request, article_pk):
    if request.user.is_authenticated:
        # article_pk 에 맞는 article 을 꺼낸다. 삭제한다.
        article = get_object_or_404(Article, pk=article_pk)
        article.delete()
        return redirect('articles:index')
    else:
        return redirect('articles:index')


# 댓글을 생성하는 요청을 받는다.
@require_POST
def comments_create(request, article_pk):
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article_id = article_pk
            comment.save()
    return redirect('articles:detail', article_pk)


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return redirect('articles:detail', article_pk)
    return HttpResponse('You are Unauthorized', status=401)