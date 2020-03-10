import random
from rest_framework import views
from django.contrib.auth import get_user_model
from apps.h5.serializers import LoginSerializer
from apps.h5.throttles import SMSCodeRateThrottle
from apps.mtauth.authentications import generate_jwt
from apps.mtauth.serializers import UserSerializer
from utils.CCPSDK import CCPRestSDK
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.utils.timezone import now

User = get_user_model()


class SmSCodeView(views.APIView):
    throttle_classes = [SMSCodeRateThrottle]

    def __init__(self, *args, **kwargs):
        super(SmSCodeView, self).__init__(*args, **kwargs)
        self.number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def generate_sms_code(self):
        return "".join(random.choices(self.number, k=4))

    def get(self, request):
        telephone = request.GET.get('tel')
        if telephone:
            auth_token = 'a2573d4b2d9a4136b23cc54911a999b7'
            auth_sid = '8aaf070870bf34550170bf6075260039'
            app_id = '8aaf070870bf34550170bf607590003f'
            rest = CCPRestSDK.REST(auth_sid, auth_token, app_id)
            code = self.generate_sms_code()
            result = rest.sendTemplateSMS(telephone, [code, 5], "1")
            cache.set(telephone, code, 60 * 5)
            return Response({"code": code})
            # if result['statusCode'] == '000000':
            #     return Response("success")
            # else:
            #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):

    def generate_sms_code(self):
        number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        return "".join(random.choices(number, k=6))

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            telephone = serializer.validated_data.get('telephone')

            try:
                user = User.objects.get(telephone=telephone)
                user.last_login = now()
                user.save()
            except:
                username = "美团用户" + self.generate_sms_code()
                password = ""
                user = User.objects.create(username=username, password=password, telephone=telephone, last_login=now())

            serializer = UserSerializer(user)
            token = generate_jwt(user)
            return Response({"user": serializer.data, "token": token})
        else:
            return Response(data={"message": dict(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
