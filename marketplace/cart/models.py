import random

from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404
from decimal import Decimal

from app_goods.models import Product
from app_shops.models import Shop, ShopProduct


class CartItems(models.Model):
    published = models.BooleanField(default=True, verbose_name='видимость/не оплачено')
    user = models.IntegerField(verbose_name='id покупателя',
                               null=True,
                               help_text='не null если покупатель авторизован')
    session_id = models.CharField(max_length=55,
                                  null=True,
                                  verbose_name='id сессии',
                                  help_text='связь корзины с анонимным покупателем'
                                  )
    product = models.ForeignKey(Product,
                                null=True,
                                on_delete=models.CASCADE,
                                verbose_name='id товара')
    shop = models.CharField(max_length=255,
                            null=True,
                            blank=True,
                            verbose_name='магазин',
                            help_text='название выбранного магазина'
                            )
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                null=True,
                                verbose_name='цена товара')
    quantity = models.PositiveSmallIntegerField(default=1,
                                                verbose_name='количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления товара')

    def get_session_id(self, request):
        """ Получение id корзины из cookies для пользователя """
        self.session = request.session
        self.session[settings.CART_SESSION_ID] = self.session.session_key
        return self.session.get(settings.CART_SESSION_ID)

    def get_user_or_session_id(self, request):
        """ Получаем user_id и session_id из request, связываем корзины
        неавторизованного пользователя и пользователя после авторизации"""
        user = request.user
        session_id = self.get_session_id(request)
        user_id = user.id
        if user.is_anonymous:
            user_id = 0
            session_id = session_id
        else:
            if CartItems:
                # получаем корзину неавторизованного пользователя и присваиваем user_id
                cart_items = CartItems.objects.filter(user=0).select_related(self.product)
                if cart_items:
                    if len(cart_items) > 1:
                        for item in cart_items:
                            item.user = user_id
                            item.save()
                    else:
                        cart_items[0].user = user_id
                        cart_items[0].save()

            else:
                user_id = user_id
                session_id = None
        return [user_id, session_id]

    def get_cart_items(self, request):
        """ Получаем товары для текущей корзины """
        user = self.get_user_or_session_id(request)[0]
        session_id = self.get_user_or_session_id(request)[1]
        if request.user.is_authenticated:
            return CartItems.objects.filter(user=user).select_related(self.product)
        else:
            return CartItems.objects.filter(session_id=session_id).select_related(self.product)

    def get_single_cart_item(self, item_id):
        """ Получаем отдельный товар из корзины """
        return get_object_or_404(CartItems,
                                 id=item_id)

    def get_shops_for_cart_item(self, product):
        """ Получаем магазины для товара из корзины """
        return list(ShopProduct.objects.filter(product=product).
                    select_related('product', 'shop').
                    prefetch_related('shop'))

    def get_random_shop_price_for_cart_item(self, product):
        """ Получаем случайный магазин если он не выбран покупателем и
        цену на товар для этого магазина"""
        shops = self.get_shops_for_cart_item(product=product)
        shop = random.choice(shops)
        price = shop.get_discounted_price()
        return [price, shop.shop.name]

    def create_new_cart_item(self, request, product, shop, quantity=1):
        if shop is not None:
            price = get_object_or_404(ShopProduct, product=product, shop__name=shop).get_discounted_price()
        else:
            shop = self.get_random_shop_price_for_cart_item(product)[1]
            price = self.get_random_shop_price_for_cart_item(product)[0]
        data = {'user': self.get_user_or_session_id(request)[0],
                'session_id': self.get_user_or_session_id(request)[1],
                'product': product,
                'shop': shop,
                'price': price,
                'quantity': quantity
                }

        CartItems.objects.create(**data)

    def add(self, request, product, shop, quantity=1):
        """
        Добавить продукт в корзину если его там нет или увеличить его количество.
        """
        cart_items = self.get_cart_items(request)
        product_in_cart = False
        if shop is None:
            shop = self.get_random_shop_price_for_cart_item(product)[1]
        for item in cart_items:
            if item.product == product and item.shop == shop:
                item.quantity += int(quantity)
                item.save()
                product_in_cart = True
                break
        if not product_in_cart:
            self.create_new_cart_item(request, product, shop, quantity)

    def update_cart_quantity(self, request, item_id):
        """Обновляет количество отдельного товара"""
        postdata = request.POST.copy()
        quantity = postdata.get('quantity')
        if quantity:
            cart_item = self.get_single_cart_item(item_id)
            if cart_item:
                if quantity.isdigit() and int(quantity) > 0:
                    cart_item.quantity = int(quantity)
                    cart_item.save()
                else:
                    cart_item.delete()

    def update_cart_price(self, request, item_id):
        """ Обновляет цену товара при смене продавца"""
        postdata = request.POST.copy()
        shop = int(postdata.get('shop'))
        product = postdata.get('product')
        shop_object = ShopProduct.objects.get(shop=shop, product__name=product)
        price = shop_object.get_discounted_price()
        shop = shop_object.shop.name
        cart_item = self.get_single_cart_item(item_id)
        if cart_item:
            cart_item.price = price
            cart_item.shop = shop
            cart_item.save()

    def get_item_total_price(self):
        return self.price * self.quantity

    def get_total_quantity(self, request):
        return self.get_cart_items(request).count()

    def get_total_cost(self, request):
        cart_items = self.get_cart_items(request)
        cart_total_cost = Decimal('0.00')
        if cart_items:
            if len(cart_items) > 1:
                for item in cart_items:
                    cart_total_cost += item.get_item_total_price()
            elif len(cart_items) == 1:
                cart_total_cost = cart_items[0].get_item_total_price()
        return cart_total_cost

    def remove_cart_item(self, item_id):
        cart_item = self.get_single_cart_item(item_id)
        if cart_item:
            cart_item.delete()

    def cart_clear(self, request):
        """ Очищаем корзину покупателя """
        cart_items = self.get_cart_items(request)
        cart_items.delete()

    class Meta:
        db_table = 'cart_model'
        ordering = ('added_at',)
        verbose_name = 'товар в корзине'
        verbose_name_plural = 'товары в корзине'
