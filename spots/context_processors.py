from .models import Spot
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .views import search
def liked_spots(request):
    if request.user.is_authenticated:
        return {'liked_spots': Spot.objects.filter(like_users=request.user)}
    else:
        return {}
    
def recently_viewed(request):
    recently_viewed_spots = []
    viewed_spots_pks = request.session.get('viewed_spots_pks', [])

    for spot_pk in viewed_spots_pks:
        spot = get_object_or_404(Spot, pk=spot_pk)
        recently_viewed_spots.append(spot)

    if request.resolver_match.view_name == 'spots:detail':
        spot_pk = request.resolver_match.kwargs.get('spot_pk')
        if spot_pk not in viewed_spots_pks:
            viewed_spots_pks.append(spot_pk)
            request.session['viewed_spots_pks'] = viewed_spots_pks

    return {'recently_viewed_spots': recently_viewed_spots, 'viewed_spots_pks': viewed_spots_pks}

def clear_recently_viewed(request):
    request.session.pop('viewed_spots_pks', None)


def spot_search(request):
    return {'search': search}