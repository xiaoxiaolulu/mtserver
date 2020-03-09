from django.urls import path
from .views import (
    LoginView,
    MerchantViewSet,
    PictureUploadView,
    CategoryViewSet,
    GoodsViewSet
)
from rest_framework.routers import DefaultRouter


app_name = 'cms'

router = DefaultRouter(trailing_slash=False)
router.register('merchant', MerchantViewSet, basename='merchant')
router.register('category', CategoryViewSet, basename='category')
router.register('goods', GoodsViewSet, basename='goods')

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('upload', PictureUploadView.as_view(), name='upload')
] + router.urls
