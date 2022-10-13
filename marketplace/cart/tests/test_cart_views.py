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
        self.product_2 = Product.objects.get(pk=2)

    # def test_cart_add_view(self):
    #     slug = self.product_1.slug
    #     request = self.factory.get('cart_detail')
    #     request.user = AnonymousUser()
    #     request.session = self.session
    #     resp_cart_detail = self.client.get(reverse('cart_detail'))
    #     self.assertEqual(resp_cart_detail.status_code, 200)
    #     self.assertTemplateUsed(resp_cart_detail, 'cart.html')
    #     resp_product_detail = self.client.get(reverse('product_detail', kwargs={'slug': slug}))
    #     self.assertEqual(resp_product_detail.status_code, 200)
    #     self.assertTemplateUsed(resp_product_detail, 'app_goods/product.html')
    #     resp = self.client.post(f'/cart/add/{slug}/', follow=True)
    #     print(resp.context)
    #     self.assertEqual(resp.status_code, 200)
        # resp_cart_detail = self.client.get(reverse('cart_detail'))
        # print(resp_cart_detail.context)




