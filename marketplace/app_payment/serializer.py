from rest_framework import serializers

from .models import Billing


class GetBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = ('order',)


class PostBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = ('order', 'card_num', 'payment_amount')
