from rest_framework import serializers

from .models import PayboxUrl


class PayboxUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayboxUrl
        fields = ('url',)