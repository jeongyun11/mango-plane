from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Article, Comment
from .forms import ArticleForm, CommentForm


def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comments = article.comment_set.all()
    comment_form = CommentForm()
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)


@login_required
def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article_pk=article.pk)

    else:
        form = ArticleForm()

    context = {
        'form': form,
    }

    return render(request, 'articles/create.html', context)

@login_required
def update_article(request, pk):
    article = Article.objects.get(pk=pk)

    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'update_article.html', context)

@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        article = Article.objects.get(pk=pk)
        article.delete()

    return redirect('articles:index')

@login_required
def comment_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comment_form = CommentForm(request.POST, request.FILES)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.article = article
        comment.save()

    return redirect('articles:detail', article.pk)


@login_required
def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()

    return redirect('articles:detail', article_pk)

@login_required
def likes(request, article_pk):
    article =  Article.objects.get(pk=article_pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
    return redirect('articles:detail', article_pk)


@login_required
def comment_likes(request, article_pk, comment_pk):
    comment =  Comment.objects.get(pk=comment_pk)
    if request.user in comment.like_users.all():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('articles:detail', article_pk)
