from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import (MovieSerializer, MoviesListSerializer,
                            ReviewSerializer, ReviewsListSerializer,
                            CommentSerializer, CommentsListSerializer,)
from .models import Movie, Review, Comment, Genre
from accounts.models import User

import requests
from tmdb import URLMaker

# Create your views here.
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def movie_list(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        serializer = MoviesListSerializer(movies, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


@api_view(['GET','POST'])
@authentication_classes([])
@permission_classes([])
def movie_reviews(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        reviews = movie.reviews.all()
        serializer = ReviewsListSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # user_pk = request.data.get('user_id'), 추후 수정
        user = get_object_or_404(User, pk=1)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, create_user=user)
            return Response(serializer.data)


@api_view(['GET','PUT','DELETE'])
@authentication_classes([])
@permission_classes([])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # 일부 수정의 경우를 위해 partial=True parameter 추가
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        review.delete()
        context = {
            'success': True,
            'message': f'{review_pk}번 리뷰 삭제'
        }
        return Response(context, status=204)


@api_view(['GET','POST'])
@authentication_classes([])
@permission_classes([])
def review_comments(request, review_pk):
    review = get_object_or_404(Movie, pk=review_pk)
    if request.method == 'GET':
        comments = review.comments.all()
        serializer = CommentsListSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(review=review, )
            return Response(serializer.data)


@api_view(['PUT','DELETE'])
@authentication_classes([])
@permission_classes([])
def movie_comment_edit(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        comment.delete()
        context = {
            'success': True,
            'message': f'{comment_pk}번 댓글 삭제'
        }
        return Response(context, status=204)


@api_view(['GET','POST'])
@authentication_classes([])
@permission_classes([])
def review_comments(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        comments = review.comments.all()
        serializer = CommentsListSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # user_pk = request.data.get('user_id'), 추후 수정
        user = get_object_or_404(User, pk=1)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(review_id=review, create_user=user)
            return Response(serializer.data)


@api_view(['PUT','DELETE'])
@authentication_classes([])
@permission_classes([])
def comment_edit(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        comment.delete()
        context = {
            'success': True,
            'message': f'{comment_pk}번 댓글 삭제'
        }
        return Response(context, status=204)


def get_data(request):
    TMDB_API_KEY = 'fd99d2b1c23f6f04fe6697ee24cbabc9'
    my_url = URLMaker(TMDB_API_KEY)
    for i in range(1,1000):
        target = my_url.get_url(page=i, language='ko-KR')
        res = requests.get(target)
        movies = res.json().get('results')
        for movie in movies:
            if movie.get('vote_average') >= 8 and movie.get('vote_count') >= 100 and movie.get('overview') and movie.get('backdrop_path'):
                data={
                    'title' : movie.get('title'),
                    'overview' : movie.get('overview'),
                    'release_date' : movie.get('release_date'),
                    'poster_path' : 'https://www.themoviedb.org/t/p/original'+movie.get('poster_path'),
                    'image' : 'https://www.themoviedb.org/t/p/original'+movie.get('backdrop_path'),
                }
                genres = movie.get('genre_ids')
                serializer = MovieSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    # for genre_id in genres:
                    #     genre = get_object_or_404(Genre, pk=genre_id)
                    #     serializer.genre.add(genre)
                    serializer.save()
    return Response(data)
