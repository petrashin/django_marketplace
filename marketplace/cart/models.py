from django.db import models
from app_goods.models import Product


class CartModel(models.Model):
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
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                null=True,
                                verbose_name='цена товара')
    quantity = models.PositiveSmallIntegerField(default=1,
                                                verbose_name='количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления товара')

    class Meta:
        db_table = 'cart_model'
        ordering = ('added_at',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
