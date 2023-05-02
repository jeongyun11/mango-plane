from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe


class Spot(models.Model):
    CATEGORY_CHOICES = (
        ('산', '산'),
        ('바다', '바다'),
        ('계곡', '계곡'),
        ('섬', '섬'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_spots')
    title = models.CharField(max_length=80)
    content = models.TextField(null=False)
    image   = models.ImageField(upload_to='tourlist_destinations/', null=True, blank=True)
    category   = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    price_range = models.CharField(max_length=20)
    parking = models.BooleanField(default=False)
    business_hours = models.CharField(max_length=50)
    holiday =  models.DateField()
    website = models.URLField(max_length=200, null=True, blank=True)


class Comment(models.Model):
    VOTE_CHOICES = (
        ('like', mark_safe('<i class="far fa-laugh-squint EmoticonPicker__Icon EmoticonPicker__Icon--Neutral"></i> 좋았다')),
        ('soso', mark_safe('<i class="far fa-meh EmoticonPicker__Icon EmoticonPicker__Icon--Neutral"></i>괜찮다')),
        ('dislike', mark_safe('<i class="far fa-frown EmoticonPicker__Icon EmoticonPicker__Icon--Neutral"></i>나쁘다')),
    )
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    article = models.ForeignKey(Spot, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    image   = models.ImageField(upload_to='tourlist_destinations/', null=True, blank=True)
    vote = models.CharField(max_length=7, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    