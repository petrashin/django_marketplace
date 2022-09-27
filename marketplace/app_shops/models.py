from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from app_goods.models import Product


class Shop(models.Model):
    """ Модель Магазин """
    name = models.CharField(max_length=255, verbose_name=_('name'))
    slug = models.SlugField(max_length=255,
                            db_index=True,
                            verbose_name='url',
                            help_text=_('unique url fragment based on the shop name')
                            )
    about = models.TextField(verbose_name=_('about shop'), blank=True)
    phone_1 = models.CharField(max_length=12, verbose_name=_('phone_1'), blank=True)
    phone_2 = models.CharField(max_length=12, verbose_name=_('phone_2'), blank=True)
    e_mail_1 = models.EmailField(verbose_name='e_mail_1', blank=True)
    e_mail_2 = models.EmailField(verbose_name='e_mail_2', blank=True)
    post_index = models.CharField(max_length=15, verbose_name=_('post_index'), blank=True)
    country = models.CharField(max_length=50, verbose_name=_('country'), blank=True)
    city = models.CharField(max_length=255, verbose_name=_('city'), blank=True)
    street = models.CharField(max_length=255, verbose_name=_('street'), blank=True)
    house_number = models.CharField(max_length=10, verbose_name=_('house_number'), blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop_detail', kwargs={'slug': self.slug})

    class Meta:
        db_table = 'shops'
        verbose_name = _('shop')
        verbose_name_plural = _('shops')


class ShopImage(models.Model):
    shop = models.OneToOneField(Shop,
                                on_delete=models.CASCADE,
                                verbose_name=_('shop'),
                                related_name='shop_images'
                                )
    image = models.ImageField(upload_to='shop_image/',
                              blank=True,
                              null=True,
                              verbose_name=_('image'),
                              help_text=_('shop image')
                              )

    class Meta:
        db_table = 'shop_images'
        verbose_name = _('shop image')
        verbose_name_plural = _('shop images')


class ShopProduct(models.Model):
    """ Модель Товар в магазине """
    shop = models.ForeignKey(Shop,
                             null=True,
                             verbose_name=_('shop'),
                             on_delete=models.CASCADE,
                             related_name='shop_products',
                             help_text=_('relationship with the Shop model')
                             )
    product = models.ForeignKey(Product,
                                null=True,
                                verbose_name=_('product'),
                                on_delete=models.CASCADE,
                                related_name='shop_products',
                                help_text=_('relationship with the Product model')
                                )

    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                null=True,
                                verbose_name=_('base price'),
                                help_text=_('price without discount')
                                )
    quantity = models.PositiveSmallIntegerField(verbose_name=_('quantity'),
                                                null=True,
                                                help_text=_('quantity of goods in the store')
                                                )
    is_available = models.BooleanField(default=True, verbose_name=_('is_available'))

    def get_discount(self):
        category_discount = self.product.category.all()[0].discount
        product_discount = self.product.discount

        discount = 0
        if product_discount and product_discount.discount_type.id == 1:
            product_discount_value = product_discount.discount_value
        else:
            product_discount_value = 0

        if category_discount and category_discount.discount_type.id == 1:
            category_discount_value = category_discount.discount_value
        else:
            category_discount_value = 0
        if product_discount_value > 0 or category_discount_value > 0:
            if product_discount_value > category_discount_value:
                discount = product_discount_value
            else:
                discount = category_discount_value

        return discount

    def get_discounted_price(self):
        """ Получаем цену со скидкой на товар/категорию"""

        discount = self.get_discount()
        if discount > 0:
            discounted_price = self.price - (self.price * discount / 100)
            if discounted_price >= 1:
                return Decimal(discounted_price)
            else:
                return Decimal(1)
        else:
            return self.price
        return self.price

    def get_shops_for_product(self, product):
        """ Получаем магазины для продукта"""
        return ShopProduct.objects.filter(product=product). \
            select_related('shop', 'product', 'product__discount'). \
            prefetch_related('shop', 'product__category', 'product__product_images')

    def __str__(self):
        return f'{self.shop.name}:{self.product.name}'

    class Meta:
        unique_together = ('shop', 'product')
        db_table = 'shop_products'
        verbose_name = _('product in the store')
        verbose_name_plural = _('products in the stores')
