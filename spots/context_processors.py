from .models import Spot

def liked_spots(request):
    if request.user.is_authenticated:
        return {'liked_spots': Spot.objects.filter(like_users=request.user)}
    else:
        return {}