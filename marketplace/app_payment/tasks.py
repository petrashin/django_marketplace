import time

from marketplace.celery import app


@app.task
def handle_payment(data):
    time.sleep(5)
    if len(str(data['card_num'])) == 16:
        return True
    else:
        return False
