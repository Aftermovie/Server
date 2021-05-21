from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import (MovieSerializer, MoviesListSerializer,
                            ReviewSerializer, ReviewsListSerializer,
                            MovieCommentSerializer, MovieCommentsListSerializer,
                            ReviewCommentSerializer, ReviewCommentsListSerializer)
from .models import Movie, Review, MovieComment, ReviewComment

# Create your views here.
@api_view(['GET'])
def movie_list(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        serializer = MoviesListSerializer(movies, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


@api_view(['GET'])
def review_list(request):
    if request.method == 'GET':
        reviews = get_list_or_404(Review)
        serializer = ReviewsListSerializer(reviews, many=True)
        return Response(serializer.data)


@api_view(['GET','POST'])
def movie_reviews(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        reviews = movie.review_set.all()
        serializer = ReviewsListSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie_id=movie)
            return Response(serializer.data)


@api_view(['GET','PUT','DELETE'])
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
def movie_comments(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        comments = movie.comment_set.all()
        serializer = MovieCommentsListSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MovieCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie_id=movie)
            return Response(serializer.data)


@api_view(['PUT','DELETE'])
def movie_comment_edit(request, comment_pk):
    comment = get_object_or_404(MovieComment, pk=comment_pk)
    if request.method == 'PUT':
        serializer = MovieCommentSerializer(comment, data=request.data)
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


