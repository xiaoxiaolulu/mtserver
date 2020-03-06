from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.timezone import now
from apps.meituan.models import Merchant
from apps.meituan.serializers import MerchantSerializer
from apps.mtauth.authentications import generate_jwt, JWTAuthentication
from apps.mtauth.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination


class MerchantPagination(PageNumberPagination):

    page_size = 12
    page_query_param = 'page'


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


class MerchantViewSet(viewsets.ModelViewSet):

    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    pagination_class = MerchantPagination
