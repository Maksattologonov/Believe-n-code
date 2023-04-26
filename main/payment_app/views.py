from django.views import View
from django.views.generic import ListView,TemplateView
from payment_app.models import Tariff


class DirectionView(ListView):
    model = Tariff
    template_name = 'payment_app/base.html'
    context_object_name = 'directions'


class PaymentView(TemplateView):
    template_name = 'payment_app/payment.html'
    context_object_name = 'payment'
