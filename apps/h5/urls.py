from django.urls import path
from .views import (
    SmSCodeView
)


app_name = 'smscode'


urlpatterns = [
    path('smscode', SmSCodeView.as_view(), name='smscode'),
]
