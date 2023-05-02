from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Spot, Comment
from .forms import SpotForm, CommentForm
from django.contrib.auth import get_user_model
from django.db.models import Count


def index(request):
    spots = Spot.objects.order_by('-pk')
    context = {
        'spots': spots,
    }
    return render(request, 'spots/index.html', context)


# EMOTIONS = [
#     {'label': '좋았다', 'value': 1},
#     {'label': '괜찮다', 'value': 2},
#     {'label': '별로', 'value': 3},
# ]
@login_required
def detail(request, spot_pk):
    spot = Spot.objects.get(pk=spot_pk)
    comments = spot.comment_set.all()
    comment_count = comments.count()

    like_count = spot.comment_set.filter(vote='like').count()
    dislike_count = spot.comment_set.filter(vote='dislike').count()
    soso_count = spot.comment_set.filter(vote='soso').count()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES, spot=spot)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.spot = spot
            comment.save()
            return redirect('spots:detail', spot_pk=spot.pk)
    else:
        comment_form = CommentForm(spot=spot)
    context = {
        'spot': spot,
        'comments': comments,
        'comment_form': comment_form,
        'comment_count': comment_count,
        'like_count': like_count,
        'dislike_count': dislike_count,
        'soso_count': soso_count,
    }
    return render(request, 'spots/detail.html', context)




@login_required
def create(request):
    if request.method == "POST":
        form = SpotForm(request.POST, request.FILES)
        if form.is_valid():
            spot = form.save(commit=False)
            spot.user = request.user
            spot.save()
            return redirect('spots:detail', spot_pk=spot.pk)

    else:
        form = SpotForm()

    context = {
        'form': form,
    }

    return render(request, 'spots/create.html', context)

@login_required
def update_spot(request, pk):
    spot = Spot.objects.get(pk=pk)

    if request.user == spot.user:
        if request.method == 'POST':
            form = SpotForm(request.POST, request.FILES, instance=spot)
            if form.is_valid():
                form.save()
                return redirect('spots:detail', spot.pk)
        else:
            form = SpotForm(instance=spot)
    else:
        return redirect('spots:index')
    context = {
        'form': form,
        'spot': spot,
    }
    return render(request, 'update_spot.html', context)

@login_required
def delete(request, pk):
    spot = Spot.objects.get(pk=pk)
    if request.user == spot.user:
        spot = spot.objects.get(pk=pk)
        spot.delete()

    return redirect('spots:index')

@login_required
def comment_create(request, spot_pk):
    spot = Spot.objects.get(pk=spot_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, spot=spot)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = spot
            comment.user = request.user
            comment.save()
            return redirect('spots:detail', spot_pk=spot.pk)
    else:
        form = CommentForm(spot=spot)
    return render(request, 'spots/comment_create.html', {'form': form, 'spot': spot,})


@login_required
def comment_delete(request, spot_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()

    return redirect('spots:detail', spot_pk)

@login_required
def likes(request, spot_pk):
    spot =  Spot.objects.get(pk=spot_pk)
    if request.user in spot.like_users.all():
        spot.like_users.remove(request.user)
    else:
        spot.like_users.add(request.user)
    return redirect('spots:detail', spot_pk)


@login_required
def comment_likes(request, spot_pk, comment_pk):
    comment =  Comment.objects.get(pk=comment_pk)
    if request.user in comment.like_users.all():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('spots:detail', spot_pk)

def search(request):
    keyword = request.GET.get('keyword')
    spots = Spot.objects.filter(title__contains = keyword) # SELECT ... FROM ... LIKE '%<keyword>%'
    context = {
        'spots': spots,
        'keyword': keyword,
    }
    return render(request, 'spots/search.html', context)