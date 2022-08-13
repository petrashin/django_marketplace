from django.db import models


# class CartModel(models.Model):
#     user = models.IntegerField(verbose_name='id покупателя',
#                                null=True,
#                                help_text='не null если покупатель авторизован')
#     session_id = models.CharField(max_length='255',
#                                   null=True,
#                                   verbose_name='id сессии',
#                                   help_text='связь корзины с анонимным покупателем'
#                                   )
#     product_id = models.IntegerField(verbose_name='id товара')
#     shop_id = models.IntegerField(verbose_name='id магазина')
