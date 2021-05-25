from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),
    path('create_data/', views.get_data),
    path('<int:movie_pk>/', views.movie_detail),
    path('<str:movie_name>/', views.movie_search),
    path('<int:movie_pk>/reviews/', views.movie_reviews),
    path('reviews/<int:review_pk>/', views.review_detail),
    path('reviews/<int:review_pk>/like', views.review_like),
    path('reviews/<int:review_pk>/dislike', views.review_dislike),
    path('reviews/<int:review_pk>/comments/', views.review_comments),
    path('comments/<int:comment_pk>/', views.comment_edit),
    path('genre/<int:genre_pk>/', views.genre_sort),
]
