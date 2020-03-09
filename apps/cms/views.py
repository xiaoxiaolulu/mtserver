from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.timezone import now
from apps.meituan.models import Merchant, GoodsCategory, Goods
from apps.meituan.serializers import MerchantSerializer, GoodsCategorySerializer, GoodsSerializer
from apps.mtauth.authentications import generate_jwt, JWTAuthentication
from apps.mtauth.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework.decorators import action
from os import path
import shortuuid
from django.conf import settings


class MerchantPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class CmsBaseView(object):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


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


class MerchantViewSet(CmsBaseView, viewsets.ModelViewSet):
    queryset = Merchant.objects.order_by('-create_time').all()
    serializer_class = MerchantSerializer
    # authentication_classes = [JWTAuthentication]
    pagination_class = MerchantPagination


class CategoryViewSet(
    CmsBaseView,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategorySerializer

    @action(['GET'], detail=False, url_path="merchant/(?P<merchant_id>\d+)")
    def merchant_category(self, request, merchant_id=None):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        categories = queryset.filter(merchant=merchant_id)
        serializer = serializer_class(categories, many=True)
        return Response(serializer.data)


class GoodsViewSet(
    CmsBaseView,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer


class PictureUploadView(CmsBaseView, APIView):

    def save_file(self, file):
        filename = shortuuid.uuid() + path.splitext(file.name)[-1]
        filepath = path.join(settings.MEDIA_ROOT, filename)
        with open(filepath, 'wb') as fp:
            for chunk in file.chunks():
                fp.write(chunk)
        return self.request.build_absolute_uri(settings.MEDIA_URL + filename)

    def post(self, request):
        file = request.data.get('file')
        file_url = self.save_file(file)
        return Response({"picture": file_url})
