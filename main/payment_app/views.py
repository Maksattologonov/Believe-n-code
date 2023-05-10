import hashlib
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram_app.models import TelegramGroup
from .models import Course
from .serializers import TariffSerializer, CourseSerializer
from .services import PayboxUrlsService, CourseService
from decouple import config


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
        queryset = PayboxUrlsService.get()
        if queryset is not None:
            serializer = TariffSerializer(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class CheckCallback(APIView, View):
    template_name = 'payment_app/index.html'
    # @csrf_exempt
    # def get(self, *args, **kwargs):
    #     pg_salt = self.request.query_params['pg_salt']
    #     pg_payment_id = self.request.query_params['pg_payment_id']
    #     pg_sig = self.request.query_params['pg_sig']
    #
    #     return HttpResponse("GET-> " + pg_salt + " " + pg_payment_id + " " + pg_sig)


class SuccessCallback(View):
    template_name = 'payment_app/success.html'

    def get(self, *args, **kwargs):
        data = kwargs.get('pg_description')
        param = self.request.GET.get("pg_description")
        response_data = {}
        if param == 'test':
            response_data = {'group_id': TelegramGroup.objects.values('group_link').get(id=1)['group_link']}
        print('params:', param)
        print("data: ", data)
        response_data.update({'status': 'success'})
        return render(self.request, template_name='payment_app/success.html', context=response_data)

