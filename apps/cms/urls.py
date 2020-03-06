from django.urls import path
from .views import LoginView, MerchantViewSet
from rest_framework.routers import DefaultRouter


app_name = 'cms'

router = DefaultRouter()
router.register('merchant', MerchantViewSet, basename='merchant')

urlpatterns = [
    path('login', LoginView.as_view(), name='login')
] + router.urls
