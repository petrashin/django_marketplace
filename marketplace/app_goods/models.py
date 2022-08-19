import os

from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Discount(models.Model):
    """ Модель Скидка """
    discount_type = models.CharField(max_length=50,
                                     verbose_name='вид скидки',
                                     help_text='вид скидки')
    discount_value = models.PositiveSmallIntegerField(null=True,
                                                      default=0,
                                                      blank=True,
                                                      verbose_name='скидка',
                                                      help_text='скидка в %')
    description = models.TextField(verbose_name='описание скидки', blank=True)
    start_date = models.DateTimeField(verbose_name='начало акции',
                                      null=True,
                                      blank=True,
                                      help_text='дата и время начала действия скидки')
    end_date = models.DateTimeField(verbose_name='конец акции',
                                    null=True,
                                    blank=True,
                                    help_text='дата и время окончания действия скидки')
    active = models.BooleanField(default=True, verbose_name='активна')

    def __str__(self):
        return self.discount_type

    class Meta:
        db_table = 'discounts'
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'


class Category(models.Model):
    """ Модель Категория """
    name = models.CharField(max_length=255, verbose_name='наименование')
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                                        related_name="sub", verbose_name="родительская категория")
    category_icon = models.FileField(upload_to="icons/categories/", verbose_name="иконка категории",
                                     default=os.path.abspath(f'{settings.BASE_DIR}/media/icons/categories/test_category_icon.jpg'))
    slug = models.SlugField(max_length=255,
                            db_index=True,
                            verbose_name='url',
                            help_text='уникальный фрагмент url на основе наименования товара'
                            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    """ Модель Товар """
    name = models.CharField(max_length=255, verbose_name='наименование')
    slug = models.SlugField(max_length=255,
                            db_index=True,
                            verbose_name='url',
                            help_text='уникальный фрагмент url на основе наименования товара'
                            )
    description = models.TextField(verbose_name='описание', blank=True)
    availability = models.BooleanField(default=True, verbose_name='в наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата и время обновления')
    category = models.ManyToManyField(Category, verbose_name='категория', related_name='products')
    discount = models.ForeignKey(Discount,
                                 null=True,
                                 blank=True,
                                 verbose_name='скидка',
                                 on_delete=models.CASCADE,
                                 related_name='products',
                                 help_text='связь с моделью Discount'
                                 )
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')
    sales_count = models.PositiveIntegerField(default=0, verbose_name='количество продаж')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_review(self):
        return self.reviews_set.all()

    class Meta:
        db_table = 'goods'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('name',)


class ProductImage(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='товар',
                                related_name='product_images'
                                )
    main_image = models.ImageField(upload_to='product_image/',
                                   blank=True,
                                   null=True,
                                   verbose_name='изображение товара',
                                   help_text='основное изображение товара'
                                   )
    side_image = models.ImageField(upload_to='product_image/',
                                   blank=True,
                                   null=True,
                                   verbose_name='вид сбоку')
    back_image = models.ImageField(upload_to='product_image/',
                                   blank=True,
                                   null=True,
                                   verbose_name='вид сзади')

    class Meta:
        db_table = 'product_images'
        verbose_name = 'изображение товара'
        verbose_name_plural = 'изображения товаров'


class Reviews(models.Model):
    """ Отзывы """
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="email", default=None)
    text = models.TextField(verbose_name="сообщение", max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    product = models.ForeignKey(Product, verbose_name="товар", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} - {self.user.username}"

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
