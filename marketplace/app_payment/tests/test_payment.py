from rest_framework.test import APITestCase, RequestsClient

from django.contrib.auth.models import User
from app_order.models import Order, Delivery, PayMethod
from app_users.models import Profile, Role


class LoadingPresets:
    fixtures = ['default.json', 'goods.json', 'shops.json']

    def setUp(self):
        user = User.objects.create(username="Test")
        role = Role.objects.create(name='User')
        delivery = Delivery.objects.get(id=1)
        pay_method = PayMethod.objects.get(id=1)

        Profile.objects.create(user=user,
                               phone_number="81231231232",
                               balance=10000,
                               role=role,
                               fullname='Test I.I.',
                               published=True,
                               card=12341232)

        Order.objects.create(user=user,
                             delivery=delivery,
                             city='Test_city',
                             address='test_address',
                             pay_method=pay_method,
                             order_comment='test_comment',
                             published=True)


class PaymentTestCase(LoadingPresets, APITestCase):
    def test_payment_even_card(self):
        """Тест оплаты картой с четной цифорй на конце"""
        client = RequestsClient()
        payment_url = 'http://marketplace:8000/api/'
        params = {'order': 1, 'card_num': 12341232, 'payment_amount': 1}
        request = client.post(payment_url, params=params)
        assert request.status_code == 200

    def test_payment_odd_card(self):
        """Тест оплаты картой с нечетной цифорй на конце"""
        client = RequestsClient()
        payment_url = 'http://marketplace:8000/api/'
        params = {'order': 1, 'card_num': 12341231, 'payment_amount': 1}
        request = client.post(payment_url, params=params)
        assert request.status_code == 406

    def test_payment_zero_card(self):
        """Тест оплаты картой с нулем на конце"""
        client = RequestsClient()
        payment_url = 'http://marketplace:8000/api/'
        params = {'order': 1, 'card_num': 12341230, 'payment_amount': 1}
        request = client.post(payment_url, params=params)
        assert request.status_code == 406
