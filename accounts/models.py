from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from movies.models import Movie, Genre


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=10)
    wish_movies = models.ManyToManyField(Movie, related_name='wish_user')
    watch_movies = models.ManyToManyField(Movie, related_name='watch_user')
    prefer_genres = models.ManyToManyField(Genre, related_name='prefer_user')