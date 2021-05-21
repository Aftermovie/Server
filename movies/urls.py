from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movie_list),
    path('movies/<int:movie_pk>/', views.movie_detail),
    path('reviews/', views.review_list),
    path('movies/<int:movie_pk>/reviews/', views.movie_reviews),
    path('reviews/<int:review_pk>/', views.review_detail),
    path('reviews/<int:review_pk>/comments/', views.review_comments),
    path('reviews/comments/<int:comment_pk>/', views.review_comment_edit),
    path('movies/<int:movie_pk>/comments/', views.movie_comments),
    path('movies/comments/<int:comment_pk>/', views.movie_comment_edit),
    path('create_movies/', views.get_data),
]
