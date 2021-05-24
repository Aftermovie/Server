from django.db import models
from django.db.models.fields.related import ManyToManyField
from accounts.models import User, Profile


class Genre(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=20)


class Movie(models.Model):
    movie_id = models.IntegerField()
    tmdb_score = models.FloatField()
    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_date = models.DateField()
    poster_path = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    genre = models.ManyToManyField(Genre, related_name='movies')


class Review(models.Model):
    content = models.TextField()
    rank = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    like_users = models.ManyToManyField(User, related_name='likes')
    dislike_users = models.ManyToManyField(User, related_name='dislikes')


class Comment(models.Model):
    content = models.CharField(max_length=100)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)