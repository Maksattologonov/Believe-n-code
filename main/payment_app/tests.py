from django.test import RequestFactory, TestCase
from django.http import HttpResponse

from payment_app.views import ResultCallback


class ResultCallbackTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_with_payment_id(self):
        request = self.factory.get('/callback/?pg_payment_id=12&pg_amount=1&pg_currency=KGS')
        view = ResultCallback.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    # def test_get_without_payment_id(self):
    #     # Создание GET-запроса без параметра pg_payment_id
    #     request = self.factory.get('/callback/')
    #
    #     # Создание экземпляра ResultCallback и вызов метода get()
    #     view = ResultCallback.as_view()
    #     response = view(request)
    #
    #     # Проверка возвращаемого HTTP-ответа
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'payment_app/error.html')
    #
    #     # Дополнительные проверки, если необходимо
