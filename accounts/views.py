from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer

# Create your views here.
@api_view(['POST'])
def signup(request):
    # client에서 보낸 정보 변수로 저장
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
    
    # 패스워드 일치 여부 확인
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # UserSerializer 이용 데이터 직렬화
    serializer = UserSerializer(data=request.data)

    # validation 작업 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        # 비밀번호 해싱
        user.set_password(password)
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)