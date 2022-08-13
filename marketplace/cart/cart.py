from decimal import Decimal
import random

from django.conf import settings
from app_goods.models import Product
from app_shops.models import ShopProduct
from .models import CartModel


class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.user = request.user
        if self.user.is_anonymous:
            self.user = 0
            self.session_id = self.session.session_key
        else:
            self.session_id = 'null'
            self.user = self.user.id

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_slug = product.slug
        shops = list(ShopProduct.objects.filter(product=product.id).values('shop__name', 'shop', 'current_price'))
        for s in shops:
            s['current_price'] = str(s['current_price'])
        shop = random.choice(shops)
        shop_name = shop['shop__name']
        price = shop['current_price']
        if product_slug not in self.cart:
            self.cart[product_slug] = {'quantity': 0,
                                       'shop': shop_name,
                                       'shops': shops,
                                       'price': price}
            CartModel.objects.create(user=self.user,
                                     session_id=self.session_id,
                                     product=product,
                                     price=price,
                                     quantity=quantity)
        if update_quantity:
            self.cart[product_slug]['quantity'] = quantity
        else:
            self.cart[product_slug]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_slug = product.slug
        if product_slug in self.cart:
            del self.cart[product_slug]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_slugs = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(slug__in=product_slugs)
        for product in products:
            self.cart[str(product.slug)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
