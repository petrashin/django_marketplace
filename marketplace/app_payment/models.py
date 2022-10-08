from django.db import models
from django.utils.translation import gettext_lazy as _
from app_order.models import Order


class PayStatus(models.Model):
    PAY_STATUS = (
        ('1', 'Не оплачено'),
        ('2', 'Оплачено'),
        ('3', 'Ошибка оплаты - time_out'),
        ('4', 'Ошибка оплаты - err 35653'),
        ('5', 'Ошибка оплаты - err 999'),
        ('6', 'Ошибка - недостаточное кол-во товара')
    )

    title = models.CharField(max_length=50, verbose_name=_('payment statuses'), choices=PAY_STATUS, blank=False,
                             default='Не оплачено')

    def __str__(self):
        return self.get_title_display()


class Billing(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    time_stamp = models.DateField(auto_now_add=True)
    card_num = models.SmallIntegerField(verbose_name=_('card_num'), default=0)
    payment_amount = models.FloatField(verbose_name=_('payment_amount'), default=0)
    payment_status = models.ForeignKey(PayStatus, blank=True, on_delete=models.DO_NOTHING,
                                       verbose_name=_('payment status'))

    def __str__(self):
        return f'order: {self.order.id} - status: {self.payment_status.get_title_display()}'

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
