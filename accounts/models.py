from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie, Genre


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=10)
    wish_movies = models.ManyToManyField(Movie, on_delete=models.CASCADE, related_name='wish_user')
    watch_movies = models.ManyToManyField(Movie, on_delete=models.CASCADE, related_name='watch_user')
    prefer_genres = models.ManyToManyField(Genre, on_delete=models.CASCADE, related_name='prefer_user')
    # 활동점수 기록, 생성될 때 0
    # score = models.IntegerField(default=0)


# class Message(models.Model):
#     content = models.CharField(max_length=300)
#     send_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     recieve_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)