from django.http.response import JsonResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from movies.serializers.common import (MovieSerializer, CommentsListSerializer,
                            ReviewSerializer, ReviewsListSerializer,
                            CommentSerializer,)
from movies.serializers.nested import MoviesListSerializer
from .models import Movie, Review, Comment, Genre
from accounts.models import User
from server.settings import TMDB_API_KEY

import requests
from tmdb import URLMaker

# Create your views here.
@api_view(['GET','POST'])
@authentication_classes([])
@permission_classes([])
def movie_list(request):
    if request.method=='GET':
        movies = Movie.objects.all().order_by('-tmdb_score')[:40]
        serializer = MoviesListSerializer(movies, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        movies = Movie.objects.filter(title__icontains=request.data.get('target'))
        if movies:
            serializer = MoviesListSerializer(movies, many=True)
            return Response(serializer.data)
    # 에러 보내는 용도
    return Http404()

# 영화 상세 정보 조회
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['GET','POST'])
def movie_reviews(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # 영화 리뷰 조회
    if request.method == 'GET':
        reviews = movie.reviews.all()
        serializer = ReviewsListSerializer(reviews, many=True)
        return Response(serializer.data)
    # 영화 리뷰 생성
    elif request.method == 'POST':
        if request.user.is_authenticated:
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                if request.user.profile.watch_movies.filter(pk=movie_pk).exists():
                    return JsonResponse( {'message': '리뷰는 하나만 작성 가능합니다.'}, status=status.HTTP_400_BAD_REQUEST)
                request.user.profile.watch_movies.add(movie)
                serializer.save(movie=movie, create_user=request.user)
                return Response(serializer.data)
        else:
            return JsonResponse( {'message': '로그인이 필요합니다.'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET','PUT','DELETE'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    # 리뷰 세부사항 조회
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    # 리뷰 수정
    elif request.method == 'PUT':
        # 일부 수정의 경우를 위해 partial=True parameter 추가
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    # 리뷰 삭제
    elif request.method == 'DELETE':
        review.delete()
        context = {
            'success': True,
            'message': f'{review_pk}번 리뷰 삭제'
        }
        return Response(context, status=204)


@api_view(['GET','POST'])
def review_comments(request, review_pk):
    review = get_object_or_404(Movie, pk=review_pk)
    if request.method == 'GET':
        comments = review.comments.all()
        serializer = CommentsListSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(review=review, create_user=request.user)
            return Response(serializer.data)


@api_view(['PUT','DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_comment_edit(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.create_user:
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
            return JsonResponse(context, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def review_comments(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        comments = review.comments.all()
        serializer = CommentsListSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(review=review, create_user=request.user)
            return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_edit(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.create_user:
        comment.delete()
        context = {
            'success': True,
            'message': f'{comment_pk}번 댓글 삭제'
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({ 'message': '본인의 댓글만 삭제할 수 있습니다.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def genre_sort(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    movies = genre.movies.all()
    serializer = MoviesListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        # 싫어요를 이미 누른 경우 싫어요 목록에서 삭제, 좋아요 목록에 추가
        if review.dislike_users.filter(id=request.user.pk).exists():
            review.dislike_users.remove(request.user)
            review.like_users.add(request.user)
        if review.like_users.filter(id=request.user.pk).exists():
            review.like_users.remove(request.user)
        else:
            review.like_users.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)
    return JsonResponse({ 'message' : '로그인이 필요합니다.'}, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_dislike(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        # 싫어요를 이미 누른 경우 싫어요 목록에서 삭제, 좋아요 목록에 추가
        if review.like_users.filter(id=request.user.pk).exists():
            review.like_users.remove(request.user)
            review.dislike_users.add(request.user)
        if review.dislike_users.filter(id=request.user.pk).exists():
            review.dislike_users.remove(request.user)
        else:
            review.dislike_users.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)
    return JsonResponse({ 'message' : '로그인이 필요합니다.'}, status=status.HTTP_403_FORBIDDEN)

def get_data(request):
    my_url = URLMaker(TMDB_API_KEY)
    try:
        db_movie = get_list_or_404(Movie)
    except:
        pass
    for i in range(1,1000):
        target = my_url.get_url(page=i, language='ko-KR')
        res = requests.get(target)
        movies = res.json().get('results')
        if movies:
            for movie in movies:
                # if db_movie.filter(movie_id=movie.get('id')).exists():
                #     continue
                if movie.get('vote_average') >= 7.5 and movie.get('vote_count') >= 1500 and movie.get('overview') and movie.get('backdrop_path'):
                    data={
                        'movie_id' : movie.get('id'),
                        'title' : movie.get('title'),
                        'tmdb_score': movie.get('vote_average'),
                        'popularity': movie.get('popularity'),
                        'overview' : movie.get('overview'),
                        'release_date' : movie.get('release_date'),
                        'poster_path' : 'https://www.themoviedb.org/t/p/original'+movie.get('poster_path'),
                        'image' : 'http://image.tmdb.org/t/p/w1280'+movie.get('backdrop_path'),
                    }
                    serializer = MovieSerializer(data=data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        try:
                            new_movie = get_object_or_404(Movie, movie_id=movie.get('id'))
                            for genre_id in movie.get('genre_ids'):
                                target_genre = get_object_or_404(Genre, number=genre_id)
                                new_movie.genre.add(target_genre)
                        except:
                            print(movie.get('title'))
        else:
            break

    return JsonResponse({'success': True})
