from rest_framework import serializers

from payment_app.models import PayboxUrl


class PayboxUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayboxUrl
        fields = ('url',)