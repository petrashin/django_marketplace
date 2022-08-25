import time
import requests
from marketplace.celery import app

from .models import Billing
from app_order.models import Order

payment_url = 'http://marketplace:8000/api/'


@app.task
def handle_payment(order_id: int, card_num: int, payment_amount: int):
    time.sleep(2)
    order = Billing.objects.filter(order=order_id, payment_status=2)
    if not order.exists():
        params = {'order': order_id, 'card_num': card_num, 'payment_amount': payment_amount}
        res = requests.post(payment_url, params=params)
        if res.status_code == 200:
            order = Order.objects.filter(id=order_id).only('status_pay')
            order.update(status_pay=True)
            return True
        if res.status_code == 406:
            return True
    return False
