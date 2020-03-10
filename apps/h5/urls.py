from django.urls import path
from .views import (
    SmSCodeView,
    LoginView,
    MerchantViewSet
)
from rest_framework.routers import DefaultRouter

app_name = 'smscode'

router = DefaultRouter(trailing_slash=False)
router.register('merchant', MerchantViewSet, basename='merchant')


urlpatterns = [
    path('smscode', SmSCodeView.as_view(), name='smscode'),
    path('login', LoginView.as_view(), name='login'),
] + router.urls
