from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.timezone import now
from apps.mtauth.authentications import generate_jwt
from apps.mtauth.serializers import UserSerializer
from rest_framework.response import Response


class LoginView(APIView):

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.last_login = now()
            user.save()
            token = generate_jwt(user)
            user_serializer = UserSerializer(user)
            return Response({"token": token, "user": user_serializer.data})
        else:
            return Response({"message": "用户名或密码错误！"}, status=status.HTTP_400_BAD_REQUEST)
