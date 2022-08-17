from django import forms

from .models import CartItems


class CartShopsForm(forms.Form):
    def __init__(self, product, *args, **kwargs):
        self.product = product

        super(CartShopsForm, self).__init__(*args, **kwargs)
        shops = CartItems().get_shops_for_cart_item(self.product)
        shop_tuple = tuple((shop.shop, shop.shop.name) for shop in shops)
        self.shop = forms.ChoiceField(choices=shop_tuple)
        self.item_id = forms.IntegerField(required=False, widget=forms.HiddenInput)





# TODO удалить после тестирования модели Cart_items

# from decimal import Decimal
# import random
#
# from django.conf import settings
# from django.db.models import F
# from django.shortcuts import get_object_or_404
#
# from app_goods.models import Product
# from app_shops.models import ShopProduct
# from .models import CartItems

#
# class Cart(object):
#
#     def __init__(self, request):
#         """
#         Инициализируем корзину
#         """
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#         if not cart:
#             # save an empty cart in the session
#             cart = self.session[settings.CART_SESSION_ID] = {}
#         self.cart = cart
#         self.user = request.user
#
#         if self.user.is_anonymous:
#             self.user = 0
#             self.session_id = self.session.session_key
#         else:
#             self.session_id = 'null'
#             self.user = self.user.id
#
#     def get_cart_items(self):
#         """ Получаем товары для текущей корзины """
#         return CartItems.objects.filter(user=self.user, session_id=self.session_id)
#
#     def get_single_cart_item(self, product):
#         """ Получаем отдельный товар из корзины """
#         return get_object_or_404(CartItems, user=self.user, session_id=self.session_id, product=product)

    # def get_shops_for_cart_item(self, product):
    #     return list(ShopProduct.objects.filter(product=product).prefetch_related('shop'))

    # def add(self, product, quantity=1, update_quantity=False):
    #     """
    #     Добавить продукт в корзину если его там нет или увеличить его количество.
    #     """
    #     product_slug = product.slug
    #     shop = None
    #     if shop is not None:
    #         # если выбран продавец, получаем актуальную цену на выбранный товар
    #         price = get_object_or_404(ShopProduct, product=product, shop=shop).get_discounted_price()
    #     else:
    #         # если продавец не выбран получаем рандомного продавца и цену на его товар
    #         shops = self.get_shops_for_cart_item(product=product)
    #         shop = random.choice(shops)
    #         price = shop.get_discounted_price()
    #
    #     if product_slug not in self.cart:
    #         self.cart[product_slug] = {'quantity': 0,
    #                                    'shop': shop,
    #                                    'price': str(price)}
    #         CartItems.objects.create(user=self.user,
    #                                  session_id=self.session_id,
    #                                  product=product,
    #                                  shop=shop,
    #                                  price=price,
    #                                  quantity=quantity)
    #
    #     else:
    #         self.cart[product_slug]['quantity'] += quantity
    #         cart_item = self.get_single_cart_item(product=product)
    #         cart_item.quantity += int(quantity)
    #         cart_item.save()
    #
    #     save = self.save()

    # def update_cart_quantity(self, product, request):
    #     """Обновляет количество отдельного товара"""
    #     postdata = request.POST.copy()
    #     quantity = postdata.get('quantity')
    #     if quantity:
    #         cart_item = self.get_single_cart_item(product=product)
    #         if cart_item:
    #             if quantity.isdigit() and int(quantity) > 0:
    #                 cart_item.quantity = int(quantity)
    #                 cart_item.save()
    #             else:
    #                 cart_item.delete()
    #
    # def update_cart_shop(self, product, request):
    #     """ Обновляет магазин и цену товара """
    #     postdata = request.POST.copy()
    #     shop = postdata['shop']
    #     price = ShopProduct.objects.get(shop__name=shop).get_discounted_price()
    #     cart_item = self.get_single_cart_item(product=product)
    #     if cart_item:
    #         cart_item.shop = shop
    #         cart_item.price = price
    #         cart_item.save()
    #
    # def save(self):
    #     # Обновление сессии cart
    #     self.session[settings.CART_SESSION_ID] = self.cart
    #     # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
    #     self.session.modified = True
    #
    # def remove(self, product):
    #     """
    #     Удаление товара из корзины.
    #     """
    #     product_slug = product.slug
    #     cart_item = CartItems.objects.get(user=self.user, product=product, session_id=self.session_id)
    #     if product_slug in self.cart:
    #         del self.cart[product_slug]
    #         cart_item.delete()
    #         self.save()
    #
    # def __iter__(self):
    #     """
    #     Перебор элементов в корзине и получение продуктов из базы данных.
    #     """
    #     product_slugs = self.cart.keys()
    #     # получение объектов product и добавление их в корзину
    #     products = Product.objects.filter(slug__in=product_slugs)
    #     for product in products:
    #         self.cart[str(product.slug)]['product'] = product
    #
    #     for item in self.cart.values():
    #         item['price'] = Decimal(item['price'])
    #         item['total_price'] = item['price'] * item['quantity']
    #         yield item
    #
    # def __len__(self):
    #     """
    #     Подсчет всех товаров в корзине.
    #     """
    #     return sum(item['quantity'] for item in self.cart.values())
    #
    # def get_total_price(self):
    #     """
    #     Подсчет стоимости товаров в корзине.
    #     """
    #     return sum(Decimal(item['price']) * item['quantity'] for item in
    #                self.cart.values())
    #
    # def clear(self):
    #     # удаление корзины из сессии и из БД
    #     del self.session[settings.CART_SESSION_ID]
    #     self.session.modified = True
    #     user_cart = self.get_cart_items()
    #     user_cart.delete()


# shops = ShopProduct.objects.filter(product=1).prefetch_related('shop')
# print(shops)
# shop = random.choice(shops)
# print(shop.shop.name)
# print(shop.get_discounted_price())



