import time
import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from jwt.exceptions import ExpiredSignatureError


def generate_jwt(user):
    expire_time = int(time.time() + 60 * 60 * 24 * 7)
    return jwt.encode({"userid": user.pk, "exp": expire_time}, key=settings.SECRET_KEY).decode('utf-8')


class JWTAuthentication(BaseAuthentication):
    """
        Simple JWT based authentication.
        The client should authenticate by passing the JWT key in the authorization.
        HTTP header, beginning with the string "JWT".Such as:

        Authorization: jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOjEsImV4cCI6MTU4NDAzMTQzNn0.
        7XAEAB3gnYw0f83WBUxXiIbSa5j08F_0dNec9sKO4UY
    """

    keyword = 'JWT'
    user = get_user_model()

    @property
    def get_model(self):
        return self.user

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Unavailable JWT request header.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Unavailable JWT request header!There should be no Spaces in JWT Token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            jwt_token = auth[1]
            jwt_info = jwt.decode(jwt_token, settings.SECRET_KEY)
            user_id = jwt_info.get('userid')
            try:
                user = self.get_model.objects.get(pk=user_id)
                return user, jwt_token
            except Exception as error:
                msg = error
            raise exceptions.AuthenticationFailed(msg)
        except ExpiredSignatureError:
            msg = 'JWT Token has expired.'
            raise exceptions.AuthenticationFailed(msg)
