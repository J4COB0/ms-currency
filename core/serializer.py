from .models import Currency
from rest_framework import serializers

class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Currency


class CurrencyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("type_currency", "amount")
        model = Currency