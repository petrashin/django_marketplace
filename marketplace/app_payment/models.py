from django.db import models
from app_order.models import Order


class Billing(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    card_num = models.SmallIntegerField(verbose_name='card_num', default=0)
    payment_amount = models.FloatField(verbose_name='payment_amount', default=0)
    payment_status = models.BooleanField(verbose_name='payment_status', default=False)
