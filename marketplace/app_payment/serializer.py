from rest_framework import serializers

from .models import Billing


class PostOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Billing
        fields = ('order_id', 'card_num', 'payment_amount')


#
# {
# "order_id": 1,
# "card_num": 113,
# "payment_amount": 12
# }
