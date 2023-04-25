from django.views.generic import ListView
from tariff.models import Tariff


class PayboxView(ListView):
    model = Tariff
    template_name = 'tariff/base.html'
    context_object_name = 'tariffs'


# def payment_view(request):
#     payment = BasePayment.objects.create(
#         variant='default',
#         currency='KZT',
#         total=1000.00,
#         description='Оплата заказа #123',
#         email='user@example.com',
#         extra_data={
#             'order_id': '123',
#         },
#     )
#     return render(request, 'payment.html', {
#         'payment': payment,
#         'paybox_form_url': reverse('process_payment', kwargs={'pk': payment.pk}),
#     })
