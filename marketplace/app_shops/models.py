from decimal import Decimal

from django.db import models
from django.urls import reverse

from app_goods.models import Product


class Shop(models.Model):
    """ Модель Магазин """
    name = models.CharField(max_length=255, verbose_name='наименование')
    slug = models.SlugField(max_length=255,
                            db_index=True,
                            verbose_name='url',
                            help_text='уникальный фрагмент url на основе наименования магазина'
                            )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop_detail', kwargs={'slug': self.slug})

    class Meta:
        db_table = 'shops'
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'


class ShopProduct(models.Model):
    """ Модель Товар в магазине """
    shop = models.ForeignKey(Shop,
                             null=True,
                             verbose_name='магазин',
                             on_delete=models.CASCADE,
                             related_name='shop_products',
                             help_text='связь с моделью Shop'
                             )
    product = models.ForeignKey(Product,
                                null=True,
                                verbose_name='товар',
                                on_delete=models.CASCADE,
                                related_name='shop_products',
                                help_text='связь с моделью Product'
                                )

    price = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    null=True,
                                    verbose_name='базовая цена',
                                    help_text='цена без скидки'
                                    )
    quantity = models.PositiveSmallIntegerField(verbose_name='количество',
                                                null=True,
                                                help_text='количество товара в магазине'
                                                )
    is_available = models.BooleanField(default=True, verbose_name='в наличии')

    def get_discounted_price(self):
        """ Получаем цену со скидкой """
        if self.product.discount.discount_value > 0:
            discount = self.product.discount.discount_value
            discounted_price = self.price - (self.price * discount / 100)
            if discounted_price >= 1:
                return Decimal(discounted_price)
            else:
                return Decimal(1)
        return self.price

    def __str__(self):
        return f'{self.shop.name}:{self.product.name}'

    class Meta:
        db_table = 'shop_products'
        verbose_name = 'товар в магазине'
        verbose_name_plural = 'товары в магазинах'
