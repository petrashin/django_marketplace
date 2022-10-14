from django.test import TestCase, Client, RequestFactory

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from cart.models import CartItems
from cart.views import *
from app_goods.models import *
from app_shops.models import *
from django.urls import reverse


class CartViewTestCase(TestCase):
    fixtures = ['goods', 'shops']

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create(username='testuser1', password='test_password123')
        self.session = self.client.session
        self.cart = CartItems()
        self.product_1 = Product.objects.get(pk=1)
        self.shop_1 = Shop.objects.get(pk=1)
        self.prod_slug = self.product_1.slug
        self.shop_slug = self.shop_1.slug

    def test_cart_add_view(self):
        # тестируем добавление товара в корзину из детальной страницы товара
        # количество товара не указано
        resp_incorrect = self.client.post(reverse('cart_add', kwargs={'slug': self.prod_slug}), {'quantity': 0}, follow=True)
        self.assertEqual(resp_incorrect.status_code, 200)
        resp_cart_detail = self.client.get(reverse('cart_detail'))
        self.assertEqual(len(resp_cart_detail.context['cart_items']), 0)

        resp_correct = self.client.post(reverse('cart_add', kwargs={'slug': self.prod_slug}), {'quantity': 2}, follow=True)
        self.assertEqual(resp_correct.status_code, 200)
        resp_cart_detail = self.client.get(reverse('cart_detail'))
        self.assertEqual(len(resp_cart_detail.context['cart_items']), 1)

    def test_cart_shop_add_view(self):
        # тестируем добавление товара с магазином в корзину
        resp_shop_detail = self.client.get(reverse('shop_detail', kwargs={'slug': self.shop_slug}))
        shop = resp_shop_detail.context['object']
        data = {'shop': shop.slug, 'quantity': 1}
        resp = self.client.post(reverse('cart_shop_add', kwargs={'slug': self.prod_slug}), data, follow=True)
        self.assertEqual(resp.status_code, 200)
        resp_cart_detail = self.client.get(reverse('cart_detail'))
        self.assertEqual(len(resp_cart_detail.context['cart_items']), 1)





