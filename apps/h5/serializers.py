from rest_framework import serializers
from django.core.cache import cache


class LoginSerializer(serializers.Serializer):

    telephone = serializers.CharField(max_length=11, min_length=11)
    smscode = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        telephone = attrs.get("telephone")
        smscode = attrs.get("smscode")
        cached_code = cache.get(telephone)
        if cached_code != smscode:
            raise serializers.ValidationError('短信验证码错误！')
        return attrs
