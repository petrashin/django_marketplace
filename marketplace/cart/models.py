import random

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from app_goods.models import Product
from app_shops.models import Shop, ShopProduct


class CartItems(models.Model):
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

    def _session_id(self, request):
        """
          Получение id корзины из cookies для пользователя,
          или установка новых cookies если не существуют
          _модификатор для видимости в пределах модуля
          """
        self.session = request.session
        session_id = self.session.get(settings.CART_SESSION_ID)
        return session_id

    def get_user_or_session_id(self, request):
        """ Получаем user_id и session_id из request """
        user = request.user
        if user.is_anonymous:
            user = 0
            session_id = self._session_id(request)

        else:
            user = user.id
            session_id = self._session_id(request)
        return [user, session_id]

    def get_cart_items(self, request):
        """ Получаем товары для текущей корзины """
        user = self.get_user_or_session_id(request)[0]
        session_id = self.get_user_or_session_id(request)[1]
        # return CartItems.objects.filter(user=user, session_id=session_id)
        return CartItems.objects.filter(session_id=session_id)

    def get_single_cart_item(self, request, item_id):
        """ Получаем отдельный товар из корзины """
        session_id = self.get_user_or_session_id(request)[1]
        return get_object_or_404(CartItems,
                                 # session_id=session_id,
                                 id=item_id)

    def get_shops_for_cart_item(self, product):
        return list(ShopProduct.objects.filter(product=product).prefetch_related('shop'))

    def get_price_for_cart_item(self, product, shop=None):
        """ Получаем цену на товар в корзине в зависимости от магазина """
        shop = shop
        if shop is not None:
            # если выбран продавец, получаем актуальную цену на выбранный товар
            price = get_object_or_404(ShopProduct, product=product, shop=shop).get_discounted_price()
        else:
            # если продавец не выбран получаем рандомного продавца и цену на его товар
            shops = self.get_shops_for_cart_item(product=product)
            shop = random.choice(shops)
            price = shop.get_discounted_price()
        return [price, shop.shop.name]

    def create_new_cart_item(self, request, product, quantity=1):
        data = {'user': self.get_user_or_session_id(request)[0],
                'session_id': self.get_user_or_session_id(request)[1],
                'product': product,
                'shop': self.get_price_for_cart_item(product)[1],
                'price': self.get_price_for_cart_item(product)[0],
                'quantity': quantity
                }
        CartItems.objects.create(**data)

    def add(self, product, request, quantity=1):
        """
        Добавить продукт в корзину если его там нет или увеличить его количество.
        """
        cart_items = self.get_cart_items(request)
        product_in_cart = False
        for item in cart_items:
            if item.product == product:
                item.quantity += int(quantity)
                item.save()
                product_in_cart = True
        if not product_in_cart:
            self.create_new_cart_item(request, product, quantity)

    def update_cart_quantity(self, request, item_id):
        """Обновляет количество отдельного товара"""
        postdata = request.POST.copy()
        quantity = postdata.get('quantity')
        # item_id = int(postdata.get('item_id'))
        if quantity:
            cart_item = self.get_single_cart_item(request, item_id)
            if cart_item:
                if quantity.isdigit() and int(quantity) > 0:
                    cart_item.quantity = int(quantity)
                    cart_item.save()
                else:
                    cart_item.delete()

    def update_cart_price(self, request, item_id):
        """ Обновляет цену товара при смене продавца"""
        postdata = request.POST.copy()
        shop = postdata.get('shop')
        price = ShopProduct.objects.get(shop=shop).get_discounted_price()
        cart_item = self.get_single_cart_item(request, item_id)
        if cart_item:
            cart_item.price = price
            cart_item.save()

    def get_item_total_price(self):
        return self.price * self.quantity

    def get_total_quantity(self, request):
        cart_items = self.get_cart_items(request)
        return cart_items.aggregate(total_quantity=Sum(self.quantity))

    def get_total_cost(self, request):
        cart_items = self.get_cart_items(request)
        return cart_items.aggregate(total_cost=Sum(self.price))

    def remove_cart_item(self, request, item_id):
        cart_item = self.get_single_cart_item(request, item_id)
        if cart_item:
            cart_item.delete()

    class Meta:
        db_table = 'cart_model'
        ordering = ('added_at',)
        verbose_name = 'товар в корзине'
        verbose_name_plural = 'товары в корзине'
