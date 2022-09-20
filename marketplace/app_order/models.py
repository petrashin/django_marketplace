from django.db import models
from app_shops.models import ShopProduct, Shop
from django.contrib.auth.models import User


class Delivery(models.Model):
    DELIVERY_TYPES = (
        ('1', 'Доставка'),
        ('2', 'Экспресс-Доставка'),
    )
    title = models.CharField(max_length=30, verbose_name='вариант доставки', choices=DELIVERY_TYPES, blank=False,
                             default='Доставка')

    def __str__(self):
        return self.title


class PayMethod(models.Model):
    PAY_TYPES = (
        ('1', 'Онлайн картой'),
        ('2', 'Онлайн со случайного чужого счёта'),
    )

    title = models.CharField(max_length=50, verbose_name='вариант оплаты', choices=PAY_TYPES, blank=False,
                             default='Онлайн картой')

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_order = models.DateField(auto_now_add=True)
    order_goods = models.JSONField(verbose_name="список товаров заказа", blank=False, default=dict)
    status_pay = models.BooleanField(default=False)
    delivery = models.ForeignKey(Delivery, on_delete=models.DO_NOTHING, verbose_name='вариант доставки')
    city = models.CharField(max_length=30, verbose_name='город')
    address = models.CharField(max_length=100, verbose_name='адрес')
    pay_method = models.ForeignKey(PayMethod, on_delete=models.DO_NOTHING, verbose_name='вариант оплаты', blank=True, null=True)
    order_comment = models.CharField(max_length=150, null=True, blank=True, verbose_name='комментарий к заказу')
    published = models.BooleanField(default=True, verbose_name='опубликовать')
    payment_status = models.CharField(max_length=256, default=None, verbose_name='статус оплаты', blank=True, null=True)

    class Meta:
        db_table = 'app_order_order'
        verbose_name = 'заказы'
        verbose_name_plural = 'заказы'

    def get_total_cost(self):
        """Функция получения стоимости заказа без скидок"""
        total_cost = 0
        for shop in self.order_goods:
            for key, value in self.order_goods[shop].items():
                shop_id = Shop.objects.get(name=shop).id
                product = ShopProduct.objects.get(product_id=key, shop=shop_id)
                total_cost += product.price * value
        return float(total_cost)

    def get_total_cost_with_discount(self):
        """Функция получения стоимости заказа с учетом скидок"""
        total_cost = 0
        for shop in self.order_goods:
            for key, value in self.order_goods[shop].items():
                shop_id = Shop.objects.get(name=shop).id
                product = ShopProduct.objects.get(product_id=key, shop=shop_id)
                total_cost += product.get_discounted_price() * value
        return float(total_cost)
