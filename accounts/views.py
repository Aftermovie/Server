from accounts.models import Profile,User
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import ProfileSerializer, UserSerializer

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
        userdata={'name':request.data.get('name')}
        p_serializer = ProfileSerializer(data=userdata)
        if p_serializer.is_valid(raise_exception=True):
            p_serializer.save(user=user)
        return Response(u_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET','PUT'])
def profile(request, user_id):
    pass
    # user= get_object_or_404(User, username=username)
    # if request.method == 'POST':
    #     user = get