import time

import requests
from marketplace.celery import app

from app_order.models import Order

payment_url = 'http://127.0.0.1:8000/api/'


@app.task
def handle_payment(order_id: int, card_num: int, payment_amount: int):
    print('test')
    order = Order.objects.filter(id=order_id)
    if order.exists:
        params = f"?order_id={order_id}&card_num={card_num}&payment_amount={payment_amount}"
        res = requests.post(payment_url + params)

        if res.status_code == 200:
            order.update(status_pay=True)
            return True
    return False
