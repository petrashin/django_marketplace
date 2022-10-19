from django.shortcuts import get_object_or_404
from django.test import TestCase, RequestFactory

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from cart.views import *
from app_shops.models import *
from django.urls import reverse


class CartViewTestCase(TestCase):
    fixtures = ['goods', 'shops']

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('cart_detail')
        self.user = get_user_model().objects.create(username='testuser1', password='test_password123')
        self.session = self.client.session
        self.request.session = self.session
        self.request.user = AnonymousUser()
        self.cart = CartItems()
        self.product_1 = Product.objects.get(pk=1)
        self.shop_1 = Shop.objects.get(pk=1)
        self.shop_2 = Shop.objects.get(pk=2)
        self.prod_slug = self.product_1.slug
        self.shop_slug = self.shop_1.slug

    def test_cart_add_view(self):
        # тестируем добавление товара в корзину из детальной страницы товара
        # количество товара не указано
        resp_incorrect = self.client.post(reverse('cart_add', kwargs={'slug': self.prod_slug}), {'quantity': 0},
                                          follow=True)
        self.assertEqual(resp_incorrect.status_code, 200)
        resp_cart_detail = self.client.get(reverse('cart_detail'))
        self.assertEqual(len(resp_cart_detail.context['cart_items']), 0)

        resp_correct = self.client.post(reverse('cart_add', kwargs={'slug': self.prod_slug}), {'quantity': 2},
                                        follow=True)
        self.assertEqual(resp_correct.status_code, 200)
        resp_cart_detail = self.client.get(reverse('cart_detail'))

        self.assertEqual(len(resp_cart_detail.context['cart_items']), 1)
        item_quantity = resp_cart_detail.context['cart_total_quantity']
        self.assertEqual(item_quantity, 2)

    def test_cart_shop_add_view(self):
        # тестируем добавление товара с магазином в корзину
        resp_shop_detail = self.client.get(reverse('shop_detail', kwargs={'slug': self.shop_slug}))
        self.assertEqual(resp_shop_detail.status_code, 200)
        self.assertTemplateUsed(resp_shop_detail, 'app_shops/shop.html')
        shop = resp_shop_detail.context['object']
        resp = self.client.post(reverse('cart_shop_add',
                                        kwargs={'slug1': self.prod_slug, 'slug2': shop.slug}),
                                follow=True
                                )
        self.assertEqual(resp.status_code, 200)
        resp_cart_detail = self.client.get(reverse('cart_detail'))
        self.assertEqual(len(resp_cart_detail.context['cart_items']), 1)
        cart_items = self.cart.get_cart_items(self.request)
        shop = get_object_or_404(Shop, slug=cart_items[0].shop)
        self.assertEqual(shop.id, 1)

    def test_cart_random_shop_add_view(self):
        # тестируем добавление товара с случайным магазином в корзину
        resp1 = self.client.post(reverse('cart_random_shop_add', kwargs={'slug': self.prod_slug}), follow=True)
        self.assertEqual(resp1.status_code, 200)
        resp_cart_detail = self.client.get(reverse('cart_detail'))
        self.assertEqual(len(resp_cart_detail.context['cart_items']), 1)
        resp2 = self.client.post(reverse('cart_random_shop_add', kwargs={'slug': self.prod_slug}), follow=True)
        self.assertEqual(resp2.status_code, 200)
        resp_cart_detail = self.client.get(reverse('cart_detail'))
        if len(resp_cart_detail.context['cart_items']) == 1:
            resp_cart_detail.context['cart_total_quantity'] == 2
        else:
            self.assertEqual(len(resp_cart_detail.context['cart_items']), 2)

    def test_cart_update_quantity_view(self):
        # тестрируем изменение количества товара на странице корзины
        resp = self.client.post(reverse('cart_add', kwargs={'slug': self.prod_slug}), {'quantity': 2}, follow=True)
        self.assertEqual(resp.status_code, 200)
        resp_cart_detail = self.client.get(reverse('cart_detail'))
        self.assertEqual(len(resp_cart_detail.context['cart_items']), 1)
        item_quantity_before = resp_cart_detail.context['cart_total_quantity']
        item_id = resp_cart_detail.context['cart_items'][0].id
        self.assertEqual(item_quantity_before, 2)

        increase_quantity = self.client.post(reverse('cart_update_quantity', kwargs={'pk': item_id}),
                                             {'quantity': 4},
                                             follow=True)
        self.assertEqual(increase_quantity.status_code, 200)
        resp_cart_detail_after = self.client.get(reverse('cart_detail'))
        item_quantity_after = resp_cart_detail_after.context['cart_total_quantity']
        self.assertEqual(item_quantity_after, 4)

        decrease_quantity = self.client.post(reverse('cart_update_quantity', kwargs={'pk': item_id}),
                                             {'quantity': 1},
                                             follow=True)
        self.assertEqual(decrease_quantity.status_code, 200)
        resp_cart_detail_decreased = self.client.get(reverse('cart_detail'))
        item_quantity_decreased = resp_cart_detail_decreased.context['cart_total_quantity']
        self.assertEqual(item_quantity_decreased, 1)

        zero_quantity = self.client.post(reverse('cart_update_quantity', kwargs={'pk': item_id}),
                                         {'quantity': 0},
                                         follow=True)
        self.assertEqual(zero_quantity.status_code, 200)
        resp_cart_detail_zero = self.client.get(reverse('cart_detail'))
        self.assertEqual(len(resp_cart_detail_zero.context['cart_items']), 0)

    def test_cart_update_price_view(self):
        # тестируем изменение цены товара при смене продавца на странице корзины
        resp_add_to_cart = self.client.post(reverse('cart_shop_add',
                                                    kwargs={'slug1': self.prod_slug, 'slug2': self.shop_slug}),
                                            follow=True
                                            )
        self.assertEqual(resp_add_to_cart.status_code, 200)
        resp_cart_detail = self.client.get(reverse('cart_detail'))
        self.assertEqual(len(resp_cart_detail.context['cart_items']), 1)
        item_price_before = resp_cart_detail.context['cart_items'][0].price
        item_shop_before = resp_cart_detail.context['cart_items'][0].shop
        item_id = resp_cart_detail.context['cart_items'][0].id
        resp_update_price = self.client.post(reverse('cart_update_price', kwargs={'pk': item_id}),
                                             {'shop': self.shop_2.id, 'product': self.product_1},
                                             follow=True)
        self.assertEqual(resp_update_price.status_code, 200)
        resp_cart_detail = self.client.get(reverse('cart_detail'))
        item_price_after = resp_cart_detail.context['cart_items'][0].price
        item_shop_after = resp_cart_detail.context['cart_items'][0].shop
        self.assertTrue(item_shop_before != item_shop_after)
        self.assertTrue(item_price_before != item_price_after)

    def test_cart_remove(self):
        # тестируем удаление товара из корзины
        resp_add_product_to_cart = self.client.post(reverse('cart_random_shop_add',
                                                            kwargs={'slug': self.prod_slug}),
                                                    follow=True)
        self.assertEqual(resp_add_product_to_cart.status_code, 200)
        resp_cart_detail = self.client.get(reverse('cart_detail'))
        cart_items = resp_cart_detail.context['cart_items']
        self.assertEqual(len(cart_items), 1)
        item_id = cart_items[0].id
        resp_remove = self.client.get(reverse('cart_remove', kwargs={'pk': item_id}), follow=True)
        self.assertEqual(resp_remove.status_code, 200)
        resp_cart_detail_after_remove = self.client.get(reverse('cart_detail'))
        cart_items = resp_cart_detail_after_remove.context['cart_items']
        self.assertEqual(len(cart_items), 0)
