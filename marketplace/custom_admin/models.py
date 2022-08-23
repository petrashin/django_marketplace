from django.db import models
from app_shops.models import Shop


class File(models.Model):

	file = models.FileField(upload_to='import/', verbose_name="файл импорта")
	created_at = models.DateField(auto_now_add=True, verbose_name="дата импорта")
	shop = models.ForeignKey(Shop, null=True, blank=True, on_delete=models.CASCADE)


class DefaultSettings(models.Model):
	
	delivery_express_coast = models.PositiveIntegerField()
	min_order = models.PositiveIntegerField()
	delivery_min = models.PositiveIntegerField()
	