from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_date = models.DateTimeField()
    poster_path = models.CharField(max_length=200)


class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    rank = models.IntegerField()
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)


class MovieComment(models.Model):
    content = models.CharField(max_length=100)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comment')
    rank = models.IntegerField()


class ReviewComment(models.Model):
    content = models.CharField(max_length=100)
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comment')