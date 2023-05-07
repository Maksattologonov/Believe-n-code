import hashlib

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from rest_framework import status
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
        pg_order_id = data.get('pg_order_id')
        pg_payment_id = data.get('pg_payment_id')
        pg_amount = data.get('pg_amount')
        pg_currency = data.get('pg_currency')
        return HttpResponse(pg_order_id, pg_payment_id, pg_amount, pg_currency)
    else:
        data = 'CLEAR'
        return HttpResponse('OK' + " " + data)


class PayboxUrl(APIView):
    def get(self, *args, **kwargs):
        queryset = PayboxUrlsService.get(type_of=self.request.query_params['type'])
        if queryset is not None:
            serializer = PayboxUrlsSerializer(queryset, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
