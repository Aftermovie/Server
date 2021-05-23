from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),
    path('create_data/', views.get_data),
    path('<int:movie_pk>/', views.movie_detail),
    path('<int:movie_pk>/reviews/', views.movie_reviews),
    path('reviews/<int:review_pk>/', views.review_detail),
    path('reviews/<int:review_pk>/comments/', views.review_comments),
    path('comments/<int:comment_pk>/', views.comment_edit),
]
