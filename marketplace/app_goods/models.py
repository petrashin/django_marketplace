from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from app_shops.models import Shop


class Category(models.Model):
    """ Модель Категория """
    name = models.CharField(max_length=255, verbose_name='наименование')
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


class PriceType(models.Model):
    """ Модель Тип цены """
    name = models.CharField(max_length=200,
                            verbose_name='наименование',
                            help_text='наименование типа цены')
    discount = models.PositiveSmallIntegerField(null=True,
                                                default=0,
                                                blank=True,
                                                verbose_name='скидка',
                                                help_text='скидка в %')
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
        return self.name

    class Meta:
        db_table = 'price_types'
        verbose_name = 'тип цены'
        verbose_name_plural = 'типы цен'


class Price(models.Model):
    """ Модель Цена """
    price_type = models.ForeignKey(PriceType,
                                   on_delete=models.CASCADE,
                                   verbose_name='тип цены',
                                   related_name='prices',
                                   help_text='связь с моделью PriceType'
                                   )

    base_price = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     verbose_name='цена товара',
                                     help_text='базовая цена товара'
                                     )
    discounted_price = models.DecimalField(max_digits=10,
                                           decimal_places=2,
                                           default=0,
                                           verbose_name='цена товара со скидкой')

    def __str__(self):
        return f'{self.price_type.name}: {self.base_price}'

    def get_discounted_price(self):
        """ Получаем цену со скидкой """
        discount = self.price_type.discount
        if discount > 0:
            return Decimal(self.base_price - (self.base_price * discount / 100))
        return self.base_price

    def save(self, *args, **kwargs):
        """ Сохраняем цену со скидкой в поле discounted_price """
        self.discounted_price = self.get_discounted_price()
        super(Price, self).save(*args, **kwargs)

    class Meta:
        db_table = 'prices'
        verbose_name = 'цена'
        verbose_name_plural = 'цены'


class Product(models.Model):
    """ Модель Товар """
    name = models.CharField(max_length=255, verbose_name='наименование')
    slug = models.SlugField(max_length=255,
                            db_index=True,
                            verbose_name='url',
                            help_text='уникальный фрагмент url на основе наименования товара'
                            )
    description = models.TextField(verbose_name='описание', blank=True)
    quantity = models.PositiveSmallIntegerField(null=True, verbose_name='количество товара')
    availability = models.BooleanField(default=True, verbose_name='в наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата и время обновления')
    shop = models.ManyToManyField(Shop, verbose_name='магазин', related_name='products')
    category = models.ManyToManyField(Category, verbose_name='категория', related_name='products')
    price = models.ForeignKey(Price,
                              null=True,
                              on_delete=models.CASCADE,
                              verbose_name='цена',
                              related_name='products',
                              help_text='связь с моделью Price'
                              )

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
