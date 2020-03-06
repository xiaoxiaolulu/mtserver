from rest_framework.serializers import ModelSerializer
from .models import MTUser


class UserSerializer(ModelSerializer):

    class Meta:
        model = MTUser
        exclude = ['password']
