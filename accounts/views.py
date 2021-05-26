from accounts.models import Profile,User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
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
    if u_serializer.is_valid(raise_exception=True):
        user = u_serializer.save()
        # 비밀번호 해싱
        user.set_password(request.data.get('password'))
        user.save()
        # 해당 user의 profile 만들기
        userdata={'name':request.data.get('name')}
        p_serializer = ProfileSerializer(data=userdata)
        if p_serializer.is_valid(raise_exception=True):
            p_serializer.save(user=user)
        return Response(u_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET','PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request,user_pk):
    if request.method=='POST':
        user=get_object_or_404(User,pk=user_pk)
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)