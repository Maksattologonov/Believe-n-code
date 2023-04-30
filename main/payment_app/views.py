from django.views.generic import ListView, TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from payment_app.models import Tariff
from payment_app.serializers import PayboxUrlsSerializer
from payment_app.services import PayboxUrlsService


class DirectionView(ListView):
    model = Tariff
    template_name = 'payment_app/base.html'
    context_object_name = 'directions'


class PaymentView(TemplateView):
    template_name = 'payment_app/payment.html'
    context_object_name = 'payment'


class PayboxUrl(APIView):
    def get(self, *args, **kwargs):
        queryset = PayboxUrlsService.get(type_of=self.request.query_params['type'])
        if queryset is not None:
            serializer = PayboxUrlsSerializer(queryset, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
