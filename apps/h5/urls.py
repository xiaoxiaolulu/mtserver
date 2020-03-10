from django.urls import path
from .views import (
    SmSCodeView,
    LoginView,
    MerchantViewSet,
    MerchantSearchView
)
from rest_framework.routers import DefaultRouter

app_name = 'smscode'

router = DefaultRouter(trailing_slash=False)
router.register('merchant', MerchantViewSet, basename='merchant')


urlpatterns = [
    path('smscode', SmSCodeView.as_view(), name='smscode'),
    path('login', LoginView.as_view(), name='login'),
    path('search', MerchantSearchView.as_view(), name='search')
] + router.urls
