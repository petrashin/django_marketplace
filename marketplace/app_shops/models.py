from django.db import models
from django.urls import reverse

from app_goods.models import Product, Price


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
    price = models.ForeignKey(Price,
                              null=True,
                              on_delete=models.CASCADE,
                              verbose_name='цена',
                              related_name='shop_products',
                              help_text='связь с моделью Price'
                              )
    quantity = models.SmallIntegerField(verbose_name='количество')

