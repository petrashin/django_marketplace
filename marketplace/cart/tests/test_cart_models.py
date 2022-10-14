from django.test import TestCase, RequestFactory

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
        self.cart = CartItems()
        self.product_1 = Product.objects.get(pk=1)
        self.product_2 = Product.objects.get(pk=2)
        self.request = self.factory.get('home')
        self.request.session = self.session
        self.request.user = AnonymousUser()

    def test_cart_add_method(self):
        # тестируем метод добавления товара в корзину неавторизованным пользователем
        self.cart.add(product=self.product_1, request=self.request)
        items = self.cart.get_cart_items(self.request)
        self.assertEqual(items[0].product.name, self.product_1.name)
        self.assertEqual(items[0].user, 0)
        self.assertEqual(items[0].quantity, 1)

    def test_cart_add_different_products(self):
        # тестируем добавление в корзину разных продуктов
        self.cart.add(product=self.product_1, request=self.request)
        self.cart.add(product=self.product_2, request=self.request)
        items = self.cart.get_cart_items(self.request)
        total_cost = self.cart.get_total_cost(self.request)
        cost = sum([(item.price * item.quantity) for item in items])
        self.assertEqual(len(items), 2)
        self.assertEqual(total_cost, cost)

    def test_cart_add_the_same_products(self):
        # тестируем увеличение количества при добавлении в корзину одинаковых продуктов
        self.cart.add(product=self.product_1, request=self.request)
        items = self.cart.get_cart_items(self.request)
        product = items[0].product
        shop = items[0].shop
        self.cart.add(product=product, request=self.request, shop=shop)
        items = self.cart.get_cart_items(self.request)
        total_cost = self.cart.get_total_cost(self.request)
        cost = sum([(item.price * item.quantity) for item in items])
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].quantity, 2)
        self.assertEqual(total_cost, cost)

    def test_cart_add_to_authenticated_user(self):
        # авторизуем пользователя и проверяем присоединение к нему корзины
        self.test_cart_add_different_products()
        items = self.cart.get_cart_items(self.request)
        self.assertEqual(items[0].user, 0)
        self.request.user = self.user
        items = self.cart.get_cart_items(self.request)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].user, self.user.id)

    def test_remove_cart_item(self):
        # тестируем метод удаления товара из корзины
        self.test_cart_add_different_products()
        items = self.cart.get_cart_items(self.request)
        self.assertEqual(len(items), 2)
        self.cart.remove_cart_item(item_id=1)
        items = self.cart.get_cart_items(self.request)
        self.assertEqual(len(items), 1)

    def test_cart_clear(self):
        # тестируем метод очистки корзины
        self.test_cart_add_different_products()
        items = self.cart.get_cart_items(self.request)
        self.assertEqual(len(items), 2)
        self.cart.cart_clear(self.request)
        items = self.cart.get_cart_items(self.request)
        self.assertEqual(len(items), 0)




