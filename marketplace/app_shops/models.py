from django.db import models
from django.urls import reverse


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