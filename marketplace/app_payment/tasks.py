import time
import requests
from marketplace.celery import app
from django.db.models import Max

from .models import Billing
from app_order.models import Order

payment_url = 'http://marketplace:8000/api/'


@app.task
def handle_payment(order_id: int, card_num: int, payment_amount: int):
    time.sleep(2)
    billing = Billing.objects.filter(order=order_id, payment_status=2)
    if not billing.exists():
        params = {'order': order_id, 'card_num': card_num, 'payment_amount': payment_amount}
        res = requests.post(payment_url, params=params)
        if res.status_code == 200:
            _change_status(order_id, True)
            return True
        if res.status_code == 406:
            _change_status(order_id, False)
            return False
        _change_status(order_id, False)
    return False


def _change_status(order_id: int, payment_result: bool):
    billing_max_id = Billing.objects.aggregate(id__max=Max('id'))
    billing = Billing.objects.filter(order__id=order_id, id=billing_max_id['id__max']).only('payment_status')[0]
    order = Order.objects.filter(id=order_id).only('status_pay', 'payment_status')
    order.update(status_pay=payment_result)
    order.update(payment_status=billing.payment_status.get_title_display())
