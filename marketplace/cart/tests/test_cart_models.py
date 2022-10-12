from django.test import TestCase, Client, RequestFactory

from django.contrib.auth import get_user_model
from cart.models import CartItems
from app_goods.models import *
from app_shops.models import *


class CartModelTestCase(TestCase):
    fixtures = ['goods', 'shops']

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create(username='testuser1', password='test_password123')
        self.session = self.client.session

    def test_cart_add(self):
        request = self.factory.get('home')
        request.user = self.user
        request.session = self.session
        product = Product.objects.get(pk=2)
        cart_item = CartItems()
        cart_item.add(product=product, request=request)
        item = CartItems.objects.get(pk=1)
        self.assertEqual(item.product.name, product.name)
        cart_item.add(product=product, request=request)
        item = CartItems.objects.get(pk=1)
        self.assertEqual(item.quantity, 2)

