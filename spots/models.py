from django.db import models
from django.conf import settings


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


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    article = models.ForeignKey(Spot, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    image   = models.ImageField(upload_to='tourlist_destinations/', null=True, blank=True)