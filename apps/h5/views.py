import random
from rest_framework import views
from apps.h5.throttles import SMSCodeRateThrottle
from utils.CCPSDK import CCPRestSDK
from rest_framework.response import Response
from rest_framework import status


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
            if result['statusCode'] == '000000':
                return Response("success")
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
