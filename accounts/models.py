from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users', blank=True, null=True)
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    