import os
import django

from django.test import Client
from django.urls import reverse

from rest_framework.test import APITestCase
from payment_app.models import PayboxSuccessPay, Course


class SuccessCallbackTest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.success_url = reverse('success_callback')
        self.instance = PayboxSuccessPay.objects.create(
            payment_id='123',
            order_id='456',
            name='Test Course',
            type='Test Type'
        )
        self.course = Course.objects.create(
            name='Test Course',
            type='Test Type',
            lms_url='https://google.com'
        )

    def test_success_callback_with_matching_instance(self):
        params = {
            'pg_payment_id': '123',
            'pg_order_id': '456'
        }
        response = self.client.get(self.success_url, params)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment_app/success.html')
        self.assertEqual(response.context['data'], self.course)

    def test_success_callback_with_no_matching_instance(self):
        # Создаем запрос GET с параметрами, которые не совпадают с instance
        params = {
            'pg_payment_id': '789',
            'pg_order_id': '999'
        }
        response = self.client.get(self.success_url, params)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment_app/error.html')

