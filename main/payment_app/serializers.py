from rest_framework import serializers

from common.services import build_paybox_signature
from .models import Course, Tariff, TemporaryAccess, Webinar, PromoCode

from decouple import config


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        params = {
            'pg_order_id': obj.id,
            'pg_merchant_id': int(config('PAYBOX_MERCHANT_ID')),
            'pg_amount': obj.type.new_price,
            'pg_currency': 'USD',
            'pg_description': obj.type.description,
            'pg_salt': f'Оплата за {obj.name}, по тарифу {obj.type}',
            # 'pg_result_url': str(config('PAYBOX_RESULT_URL')),
            'pg_testing_mode': int(config('PAYBOX_TESTING_MODE')),
            'pg_param1': obj.name,
            'pg_param2': obj.type.name
        }
        secret_key = str(config('PAYBOX_SECRET_KEY'))
        return build_paybox_signature(params, secret_key)

    class Meta:
        model = Course
        fields = ('id', 'name', 'url', 'temporary_lms_url')


class TemporaryAccessSerializer(serializers.Serializer):
    name = serializers.CharField()
    # email = serializers.CharField()
    telegram_number = serializers.CharField()
    tariff = serializers.CharField()
    course = serializers.CharField()


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ('name',)


class WebinarSerializer(serializers.ModelSerializer):
    promo_code = serializers.CharField(source='promo_code.name', read_only=True)

    class Meta:
        model = Webinar
        fields = ('id', 'title', 'date_time', 'promo_code', 'text')
