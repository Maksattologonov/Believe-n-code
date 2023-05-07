import hashlib

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from rest_framework import stat

us
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CoursePrompt
from .serializers import PayboxUrlsSerializer
from .services import PayboxUrlsService
from decouple import config


class DirectionView(ListView):
    model = CoursePrompt
    template_name = 'payment_app/base.html'
    context_object_name = 'directions'


@csrf_exempt
def paybox_callback(request):
    if request.method == 'POST':
        data = request.POST

        print(data)
        # Проверяем подпись запроса
        # sign = data.pop('pg_sig')[0]
        # secret_key = config('PAYBOX_SECRET_KEY')
        # str_to_sign = '&'.join([f'{key}={value}' for key, value in sorted(data.items())])
        # str_to_sign += f'&{secret_key}'
        # if sign != hashlib.md5(str_to_sign.encode()).hexdigest():
        #     return HttpResponse('Ошибка проверки подписи')
        #
        # # Обрабатываем данные запроса
        # status = data['pg_result']
        # order_id = data['pg_order_id']
        # amount = data['pg_amount']
        #
        # # Отправляем ответ PayBox
        return HttpResponse('OK')
    else:
        return HttpResponse(status=405)


class PayboxUrl(APIView):
    def get(self, *args, **kwargs):
        queryset = PayboxUrlsService.get(type_of=self.request.query_params['type'])
        if queryset is not None:
            serializer = PayboxUrlsSerializer(queryset, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
