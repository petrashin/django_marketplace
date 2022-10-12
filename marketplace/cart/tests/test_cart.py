from django.test import TestCase, Client, RequestFactory

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
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
        request.user = AnonymousUser()
        request.session = self.session
        product_1 = Product.objects.get(pk=1)
        product_2 = Product.objects.get(pk=2)
        cart_item = CartItems()

        # тестируем метод добавления товара в корзину неавторизованным пользователем
        cart_item.add(product=product_1, request=request)
        items = cart_item.get_cart_items(request)
        self.assertEqual(items[0].product.name, product_1.name)
        self.assertEqual(items[0].user, 0)
        self.assertEqual(items[0].quantity, 1)

        # добавляем в корзину другой продукт
        cart_item.add(product=product_2, request=request)
        items = cart_item.get_cart_items(request)
        self.assertEqual(len(items), 2)

        # тестируем увеличение количества при добавлении в корзину такого-же продукта
        product = items[0].product
        shop = items[0].shop
        cart_item.add(product=product, request=request, shop=shop)
        items = cart_item.get_cart_items(request)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].quantity, 2)

        # авторизуем пользователя и проверяем присоединение к нему корзины
        request.user = self.user
        items = cart_item.get_cart_items(request)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].user, self.user.id)
        self.assertEqual(items[0].quantity, 2)

    def test_cart_item_remove(self):
        pass



