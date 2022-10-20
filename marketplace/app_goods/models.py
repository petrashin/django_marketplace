import os
from statistics import mean

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Min
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class DiscountType(models.Model):
    DISCOUNT_TYPES = (
        ('1', 'На товар/категорию'),
        ('2', 'На набор'),
        ('3', 'На корзину')
    )

    title = models.CharField(max_length=50, verbose_name='Статусы оплаты', choices=DISCOUNT_TYPES, blank=False,
                             default='Не оплачено')

    def __str__(self):
        return self.get_title_display()

    class Meta:
        verbose_name = 'тип скидки'
        verbose_name_plural = 'типы скидок'


class Discount(models.Model):
    """ Модель Скидка """

    discount_type = models.ForeignKey(DiscountType, on_delete=models.DO_NOTHING, verbose_name=_('discount_type'))
    discount_name = models.CharField(max_length=50,
                                     blank=True,
                                     verbose_name=_('discount_name'),
                                     help_text='название скидки')
    discount_value = models.PositiveSmallIntegerField(null=True,
                                                      default=0,
                                                      blank=True,
                                                      verbose_name=_('discount_value'),
                                                      help_text='скидка в %')
    discount_amount = models.PositiveSmallIntegerField(null=True,
                                                       default=0,
                                                       blank=True,
                                                       verbose_name='Количество необходимое в корзине',
                                                       help_text='Скидка на корзину')
    description = models.TextField(verbose_name=_('description'), blank=True)
    start_date = models.DateTimeField(verbose_name=_('start_date'),
                                      null=True,
                                      blank=True,
                                      help_text=_('discount start date and time'))
    end_date = models.DateTimeField(verbose_name=_('end_date'),
                                    null=True,
                                    blank=True,
                                    help_text=_('discount end date and time'))
    active = models.BooleanField(default=True, verbose_name=_('active'))

    def __str__(self):
        return f'Скидка: {self.discount_name} - тип скидки: {self.discount_type.get_title_display()}'

    class Meta:
        db_table = 'discounts'
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')


class Category(models.Model):
    """ Модель Категория """
    name = models.CharField(max_length=255, verbose_name=_('name'))
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                                        related_name="sub", verbose_name=_('parent category'))
    category_icon = models.FileField(upload_to="icons/categories/", verbose_name=_('category icon'),
                                     default=os.path.abspath(
                                         f'/icons/categories/test_category_icon.jpg'))
    category_image = models.ImageField(upload_to='cat_image/',
                                       blank=True,
                                       null=True,
                                       verbose_name=_('category_image'),
                                       help_text=_('category image'))
    slug = models.SlugField(max_length=255,
                            db_index=True,
                            verbose_name='url',
                            help_text=_('unique url fragment based on the category name')
                            )
    discount = models.ForeignKey(Discount,
                                 null=True,
                                 blank=True,
                                 verbose_name=_('discount'),
                                 on_delete=models.DO_NOTHING,
                                 related_name='category',
                                 help_text=_('relationship with the Discount model')
                                 )
    published = models.BooleanField(default=True, verbose_name=_('published'))

    def get_min_price(self):
        """ Получаем минимальную цену co скидкой на товар категории для index.html """
        products = self.products.all()
        min_price = 0.0
        if products:
            if len(products) > 1:
                min_price = sorted([product.get_discounted_price()
                                    for product in products for product in product.shop_products.all()])[0]
            else:
                min_price = sorted([product.get_discounted_price() for product in products[0].shop_products.all()])[0]

        return min_price

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        ordering = ('name',)
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Product(models.Model):
    """ Модель Товар """
    name = models.CharField(max_length=255, verbose_name=_('name'))
    slug = models.SlugField(max_length=255,
                            db_index=True,
                            verbose_name='url',
                            help_text=_('unique url fragment based on the product name')
                            )
    description = models.TextField(verbose_name=_('description'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))
    category = models.ManyToManyField(Category, verbose_name=_('category'), related_name='products')
    discount = models.ForeignKey(Discount,
                                 null=True,
                                 blank=True,
                                 verbose_name=_('discount'),
                                 on_delete=models.DO_NOTHING,
                                 related_name='products',
                                 help_text=_('relationship with the Discount model')
                                 )
    discount_doublet = models.BooleanField(default=False, verbose_name='Сделать скидку при совпадении?',
                                           help_text='Скидка на набор')
    views_count = models.IntegerField(default=0, verbose_name=_('views_count'))
    sales_count = models.PositiveIntegerField(default=0, verbose_name=_('sales_count'))
    published = models.BooleanField(default=True, verbose_name=_('published'))
    limited_edition = models.BooleanField(default=False, verbose_name=_('limited_edition'))
    technical_specs = models.JSONField(verbose_name='список технических характеристик товара', default=dict)

    def __str__(self):
        return self.name

    def get_avg_price(self):
        """ Получаем среднюю цену товара """
        avg_price = self.shop_products.aggregate(avg_price=Avg('price')).get('avg_price')
        return avg_price

    def get_avg_discounted_price(self):
        """ Получаем среднюю цену товара с учетом скидки """
        shop_products = self.shop_products.all()
        avg_price = 0.0
        if shop_products:
            if len(shop_products) > 1:
                avg_price = round(mean([product.get_discounted_price() for product in shop_products]), 2)
            else:
                avg_price = round(shop_products[0].get_discounted_price(), 2)
        return avg_price

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_review(self):
        return self.reviews_set.all()

    class Meta:
        db_table = 'goods'
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('name',)


class ProductImage(models.Model):
    product = models.OneToOneField(Product,
                                   on_delete=models.CASCADE,
                                   verbose_name=_('product'),
                                   related_name='product_images'
                                   )
    main_image = models.ImageField(upload_to='product_image/',
                                   blank=True,
                                   null=True,
                                   verbose_name=_('main_image'),
                                   help_text=_('main product image')
                                   )
    side_image = models.ImageField(upload_to='product_image/',
                                   blank=True,
                                   null=True,
                                   verbose_name=_('side_image'))
    back_image = models.ImageField(upload_to='product_image/',
                                   blank=True,
                                   null=True,
                                   verbose_name=_('back_image'))

    class Meta:
        db_table = 'product_images'
        verbose_name = _('product_image')
        verbose_name_plural = _('product_images')


class Reviews(models.Model):
    """ Отзывы """
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="email", default=None)
    text = models.TextField(verbose_name=_("text"), max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    product = models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE)
    published = models.BooleanField(default=True, verbose_name=_('published'))

    def __str__(self):
        return f"{self.product} - {self.user.username}"

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')


class ProductTag(models.Model):
    """Тэги для каталога"""
    tag = models.CharField(max_length=10)
    product = models.ManyToManyField(Product, related_name='tags')

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
