import time

from decouple import config
from django.db import IntegrityError
from django.db.models import Case, When, Value
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram_app.models import TelegramGroup
from .models import PayboxSuccessPay, Course
from .serializers import TariffSerializer, CourseSerializer, TemporaryAccessSerializer, WebinarSerializer, \
    PromoCodeSerializer
from .services import PayboxService, CourseService, PayboxCallbackService, TemporaryAccessService, WebinarService


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
        queryset = PayboxService.get().order_by(
            Case(
                When(name='Up', then=Value(0)),
                When(name='Pro', then=Value(1)),
                When(name='Ultra', then=Value(2)),
                default=Value(3),
            )
        )
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
        time.sleep(9)
        if self.request.GET.get("pg_payment_id") and self.request.GET.get('pg_order_id') and self.request.GET.get(
                'pg_sig'):
            try:
                payment = PayboxSuccessPay.objects.get(payment_id=int(self.request.GET.get('pg_payment_id')),
                                                       order_id=self.request.GET.get('pg_order_id'))
                if payment:
                    data = Course.objects.get(name=payment.name, pk=payment.order_id)
                    try:
                        telegram_group = TelegramGroup.objects.get(type=data.pk)
                    except TelegramGroup.DoesNotExist:
                        telegram_group = {'group_link': config('TG_GROUP')}
                    response_data = ({'data': data, 'telegram': telegram_group})
                    return render(self.request, template_name='payment_app/success.html', context=response_data)
            except IntegrityError:
                return render(self.request, template_name='payment_app/error.html',
                              context={'error': 'Ошибка уникальности'})
            except PayboxSuccessPay.DoesNotExist:
                return render(self.request, template_name='payment_app/error.html',
                              context={'error': 'Данные введены ошибочно'})
        else:
            return render(self.request, template_name='payment_app/error.html',
                          context={'error': 'Данные введены ошибочно'})


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


class WebinarAPIView(APIView):
    def get(self, *args, **kwargs):
        queryset = WebinarService.get()
        serializer = WebinarSerializer(queryset, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, *args):
        return Response(data=WebinarService.check_promo_code(data=self.request.data),
                        status=status.HTTP_200_OK)
