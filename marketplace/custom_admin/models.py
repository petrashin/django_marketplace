from django.db import models
from app_shops.models import Shop
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class File(models.Model):

	file = models.FileField(upload_to='import/', verbose_name="файл импорта")
	created_at = models.DateField(auto_now_add=True, verbose_name="дата импорта")
	shop = models.ForeignKey(Shop, null=True, blank=True, on_delete=models.CASCADE)


class DefaultSettings(models.Model):
	
	delivery_express_coast = models.PositiveIntegerField()
	min_order = models.PositiveIntegerField()
	delivery_min = models.PositiveIntegerField()
	