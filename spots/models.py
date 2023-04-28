from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    article = models.ForeignKey(Spot, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    image   = models.ImageField(upload_to='tourlist_destinations/', null=True, blank=True)
    
    
class Emote(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emotion = models.CharField(max_length=10)