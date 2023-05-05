from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe


class Spot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_spots')
    title = models.CharField(max_length=80)
    content = models.TextField(null=False)
    image   = models.ImageField(upload_to='tourlist_destinations/', null=True, blank=True)
    category   = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    price_range = models.CharField(max_length=20)
    parking = models.BooleanField(default=False)
    website = models.URLField(max_length=200, null=True, blank=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    
    def calculate_average_rating(self):
        comments = self.comment_set.all()
        if not comments:
            return 0

        total_rating = sum([float(comment.vote) for comment in comments])
        average_rating = total_rating / len(comments)
        return round(average_rating, 1)


class Comment(models.Model):
    VOTE_CHOICES = (
        (5.0, mark_safe('<i class="far fa-laugh-squint EmoticonPicker__Icon EmoticonPicker__Icon--Neutral"></i> 좋았다')),
        (3.0, mark_safe('<i class="far fa-meh EmoticonPicker__Icon EmoticonPicker__Icon--Neutral"></i>괜찮다')),
        (1.0, mark_safe('<i class="far fa-frown EmoticonPicker__Icon EmoticonPicker__Icon--Neutral"></i>나쁘다')),
    )
    vote = models.FloatField(choices=VOTE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    article = models.ForeignKey(Spot, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class CommentImage(models.Model):
    image = models.ImageField(upload_to='tourlist_destinations/')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='images')
    