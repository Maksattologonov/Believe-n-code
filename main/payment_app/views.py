from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PayboxSuccessPay, Course, Tariff
from .serializers import TariffSerializer, CourseSerializer, TemporaryAccessSerializer
from .services import PayboxService, CourseService, PayboxCallbackService, TemporaryAccessService


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
        if self.request.GET.get('pg_payment_id'):

            PayboxCallbackService.save(order_id=self.request.GET.get('pg_order_id'),
                                       payment_id=self.request.GET.get('pg_payment_id'),
                                       amount=self.request.GET.get('pg_amount'),
                                       currency=self.request.GET.get('pg_currency'),
                                       description=self.request.GET.get('pg_description'),
                                       user_phone=self.request.GET.get('pg_user_phone'),
                                       email=self.request.GET.get('pg_user_contact_email'),
                                       signature=self.request.GET.get('pg_sig'))
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return render(request=self.request, template_name="payment_app/error.html", context={'error': 'ERROR'})


class SuccessCallback(View):
    def get(self, *args, **kwargs):

        if self.request.GET.get("pg_payment_id"):
            instance = Tariff.objects.get(pk=self.request.GET.get('pg_order_id'))
            if instance:
                data = Course.objects.get(name=instance.name, type__name=instance.type)
                response_data = ({'data': data})
                return render(self.request, template_name='payment_app/success.html', context=response_data)
        else:
            return render(self.request, template_name='payment_app/error.html')


class TemporaryAccessAPIView(APIView):
    def post(self, *args, **kwargs):
        serializer = TemporaryAccessSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        url = TemporaryAccessService.create_access(name=serializer.validated_data.get('name'),
                                                   # email=serializer.validated_data.get('email'),
                                                   telegram_number=serializer.validated_data.get('telegram_number'),
                                                   tariff=serializer.validated_data.get('tariff'),
                                                   course=serializer.validated_data.get('course'))
        if url:
            return Response(data=url, status=status.HTTP_201_CREATED)

