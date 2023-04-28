from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Spot, Comment
from .forms import SpotForm, CommentForm


def index(request):
    spots = Spot.objects.order_by('-pk')
    context = {
        'spots': spots,
    }
    return render(request, 'spots/index.html', context)


def detail(request, spot_pk):
    spot = Spot.objects.get(pk=spot_pk)
    comments = spot.comment_set.all()
    comment_form = CommentForm()
    context = {
        'spot': spot,
        'comments': comments,
        'comment_form': comment_form,
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
    comment_form = CommentForm(request.POST, request.FILES)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.article_id = spot_pk
        comment.save()

    return redirect('spots:detail', spot.pk)


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
