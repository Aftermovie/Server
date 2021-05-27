from accounts.models import Profile,User
from movies.models import Movie, Review, Genre
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.http.response import JsonResponse
from .serializers import ProfileSerializer, UserSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    # UserSerializer 이용 데이터 직렬화
    u_serializer = UserSerializer(data=request.data)

    # validation 작업 진행
    if u_serializer.is_valid():
        user = u_serializer.save()
        # 비밀번호 해싱
        user.set_password(request.data.get('password'))
        user.save()
        # 해당 user의 profile 만들기
        userdata={'name':request.data.get('name')}
        p_serializer = ProfileSerializer(data=userdata)
        if p_serializer.is_valid():
            p_serializer.save(user=user, prefer_genres=request.data.get('genres'))
        return Response(u_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse({ 'message': '이미 가입된 사용자입니다.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method=='GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method=='POST':
        movie = get_object_or_404(Movie, pk=request.data.get('want_movie_id'))
        if profile.wish_movies.filter(pk=movie.pk).exists():
            profile.wish_movies.remove(movie)
        else:
            profile.wish_movies.add(movie)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)