from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Spot, Comment
from .forms import SpotForm, CommentForm, CommentImageFormSet, CommentImage
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.http import JsonResponse
from utils.map import get_latlng_from_address
import os

def index(request):
    spots = Spot.objects.order_by('-pk')
    spots_with_ratings = []
    for spot in spots:
        average_rating = spot.calculate_average_rating()
        spots_with_ratings.append((spot, average_rating))
    context = {
        'spots': spots,
        'spots_with_ratings': spots_with_ratings,
    }
    return render(request, 'spots/index.html', context)

def detail(request, spot_pk):
    spot = Spot.objects.get(pk=spot_pk)
    comments = spot.comment_set.all()
    comment_count = comments.count()
    kakao_script_key = os.getenv('kakao_script_key')
    like_count = spot.comment_set.filter(vote=5.0).count()
    soso_count = spot.comment_set.filter(vote=3.0).count()
    dislike_count = spot.comment_set.filter(vote=1.0).count()
    address = spot.address
    latitude, longitude = get_latlng_from_address(address)
    average_rating = spot.calculate_average_rating()

    image_exists = any(comment.images.exists() for comment in comments)

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
        'average_rating': average_rating,
        'image_exists': image_exists,
        'kakao_script_key': kakao_script_key,
        'latitude': latitude,
        'longitude': longitude,
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
    return render(request, 'spots/update_spot.html', context)
# requsert -> spot으로 나중에 

@login_required
def delete(request, pk):
    spot = Spot.objects.get(pk=pk)
    if request.user == request.user:
        spot = spot.objects.get(pk=pk)
        spot.delete()

    return redirect('spots:index')

@login_required
def comment_create(request, spot_pk):
    spot = Spot.objects.get(pk=spot_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, spot=spot, request=request)
        formset = CommentImageFormSet(request.POST, request.FILES, prefix='commentimage_set')

        if form.is_valid() and formset.is_valid():
            comment = form.save(commit=False)
            comment.article = spot
            comment.user = request.user
            comment.save()

            for image_form in formset:
                if 'commentimage_set-0-image' in request.FILES:
                    for img in request.FILES.getlist('commentimage_set-0-image'):
                        image = CommentImage(comment=comment, image=img)
                        image.save()
                    break

            return redirect('spots:detail', spot_pk=spot.pk)
    else:
        form = CommentForm(spot=spot, request=request)
        formset = CommentImageFormSet(prefix='commentimage_set')

    context = {
        'form': form,
        'formset': formset,
        'spot': spot,
    }
    return render(request, 'spots/comment_create.html', context)

@login_required
def comment_delete(request, spot_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()

    return redirect('spots:detail', spot_pk)


@login_required
def likes(request, spot_pk):
    spot = Spot.objects.get(pk=spot_pk)
    if request.user in spot.like_users.all():
        spot.like_users.remove(request.user)
        liked = False
    else:
        spot.like_users.add(request.user)
        liked = True
    data = {
        'liked': liked,
    }
    return JsonResponse(data)

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
    spots_with_ratings = []
    len_element = 8
    paginator = Paginator(spots, len_element)
    page_number = request.GET.get('page')
    if page_number == None :
        page_number = 1
    page_obj = paginator.get_page(page_number)
    for spot in page_obj:
        average_rating = spot.calculate_average_rating()
        spots_with_ratings.append((spot, average_rating))
    len_page = (len(spots) + 1) // len_element
    pages = range(1, len_page + 1)
    context = {
        'spots': page_obj,
        'keyword': keyword,
        'pages': pages,
        'page_number': int(page_number),
        'spots_with_ratings': spots_with_ratings,
    }
    return render(request, 'spots/search.html', context)

@require_POST
def delete_recently_viewed_spots(request):
    request.session['viewed_spots_pks'] = []
    return JsonResponse({}, status=200)

def city(request):
    tag = request.GET.get('city')
    spots = Spot.objects.filter(address__contains=tag)
    spots_with_ratings = []
    for spot in spots:
        average_rating = spot.calculate_average_rating()
        spots_with_ratings.append((spot, average_rating))
    comments = Comment.objects.filter(article__in=spots)
    context = {
        'spots': spots,
        'spots_with_ratings': spots_with_ratings,
        'comments': comments
    }
    return render(request, 'spots/city.html', context)



    # spots = Spot.objects.order_by('-pk')
    # spots_with_ratings = []
    # for spot in spots:
    #     average_rating = spot.calculate_average_rating()
    #     spots_with_ratings.append((spot, average_rating))
    # context = {
    #     'spots': spots,
    #     'spots_with_ratings': spots_with_ratings,
    # }