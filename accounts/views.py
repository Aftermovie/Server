from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer

# Create your views here.
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    # UserSerializer 이용 데이터 직렬화
    serializer = UserSerializer(data=request.data)

    # validation 작업 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        # 비밀번호 해싱
        user.set_password(request.data.get('password'))
        user.save()
        response_data = {
            'name' : request.data.get('name'),
            'username': request.data.get('username'),
        }
        return Response(response_data, status=status.HTTP_201_CREATED)