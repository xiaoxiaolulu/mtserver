from django.urls import path
from .views import (
    SmSCodeView,
    LoginView
)


app_name = 'smscode'


urlpatterns = [
    path('smscode', SmSCodeView.as_view(), name='smscode'),
    path('login', LoginView.as_view(), name='login'),
]
