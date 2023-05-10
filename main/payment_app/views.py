from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram_app.models import TelegramGroup
from .serializers import TariffSerializer, CourseSerializer
from .services import PayboxService, CourseService, PayboxCallbackService


class CourseView(APIView):
    def get(self, *args, **kwargs):
        if self.request.query_params:
            queryset = CourseService.get(type__name=self.request.query_params['type'])
        else:
            queryset = CourseService.get()
        serializer = CourseSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PayboxUrl(APIView):
    def get(self, *args, **kwargs):
        queryset = PayboxService.get()
        if queryset is not None:
            serializer = TariffSerializer(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class ResultCallback(View):

    def get(self, *args, **kwargs):
        PayboxCallbackService.save(payment_id=self.request.GET.get('pg_payment_id'),
                                   amount=self.request.GET.get('pg_amount'),
                                   currency=self.request.GET.get('pg_currency'),
                                   description=self.request.GET.get('pg_description'),
                                   user_phone=self.request.GET.get('pg_user_phone'),
                                   email=self.request.GET.get('pg_user_contact_email'),
                                   signature=self.request.GET.get('pg_sig'))
        return HttpResponse("OK", status=status.HTTP_200_OK)


class SuccessCallback(View):
    def get(self, *args, **kwargs):
        try:
            obj = PayboxCallbackService.get(payment_id=self.request.GET.get("pg_payment_id"))
            data = TelegramGroup.objects.get()

            response_data = ({'status': 'success'})
            return render(self.request, template_name='payment_app/success.html', context=response_data)
        except Exception as ex:
            return render(self.request, template_name='payment_app/error.html', context={"error": str(ex)})
