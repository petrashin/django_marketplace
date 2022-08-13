from django.contrib import admin

from .models import Delivery, PayMethod, Order


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
	fields = ['title']


@admin.register(PayMethod)
class PayMethodAdmin(admin.ModelAdmin):
	fields = ['title']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	pass
