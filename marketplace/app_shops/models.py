from decimal import Decimal

from django.db import models
from django.urls import reverse

from app_goods.models import Product, PriceType


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
    price_type = models.ForeignKey(PriceType,
                                   null=True,
                                   verbose_name='тип цены',
                                   on_delete=models.CASCADE,
                                   related_name='shop_products',
                                   help_text='связь с моделью PriceType'
                                   )
    old_price = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    null=True,
                                    verbose_name='базовая цена',
                                    help_text='цена без скидки'
                                    )
    current_price = models.DecimalField(max_digits=10,
                                        decimal_places=2,
                                        null=True,
                                        blank=True,
                                        verbose_name='действующая цена',
                                        help_text='цена со скидкой'
                                        )
    quantity = models.PositiveSmallIntegerField(verbose_name='количество',
                                                null=True,
                                                help_text='количество товара в магазине'
                                                )
    is_available = models.BooleanField(default=True, verbose_name='в наличии')

    def get_current_price(self):
        """ Получаем цену со скидкой """
        discount = self.price_type.discount
        if discount > 0:
            current_price = self.old_price - (self.old_price * discount / 100)
            if current_price >= 1:
                return Decimal(current_price)
            else:
                return Decimal(1)
        return self.old_price

    def save(self, *args, **kwargs):
        """ Сохраняем цену со скидкой в поле current_price """
        self.current_price = self.get_current_price()
        super(ShopProduct, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.shop.name}:{self.product.name}'

    class Meta:
        db_table = 'shop_products'
        verbose_name = 'товар в магазине'
        verbose_name_plural = 'товары в магазинах'
